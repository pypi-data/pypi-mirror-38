from pelix.ipopo.decorators import (ComponentFactory, Property, Requires,
                                    BindField, UnbindField, Provides, Validate, 
                                    Invalidate, Instantiate)

import ast
import configparser
import xacc
import xaccvqe
import time
import os
from xacc import Algorithm

@ComponentFactory("VQE_energy_algorithm_factory")
@Provides("xacc_algorithm_service")
@Property("_algorithm", "algorithm", "vqe-energy")
@Property("_name", "name", "vqe-energy")
@Requires("_molecule_generator", "molecule_generator_service", aggregate=True)
@Requires("_ansatz_generator", "ansatz_generator_service", aggregate=True)
@Instantiate("VQE_energy_algorithm_instance")
class VQEEnergy(Algorithm):

    def __init__(self):
        
        self.molecule_generators = {}
        self.ansatz_generators = {}
        self.vqe_options_dict = {}
        self.n_qubits = 0
        self.op = None

    @Validate
    def validate(self, context):
        print("VQEEnergy Algorithm Validated")

    @BindField('_ansatz_generator')
    @BindField('_molecule_generator')
    def bind_dicts(self, field, service, svc_ref):
        if svc_ref.get_property('molecule_generator'):
            generator = svc_ref.get_property('molecule_generator')
            self.molecule_generators[generator] = service
        elif svc_ref.get_property('ansatz_generator'):
            generator = svc_ref.get_property('ansatz_generator')
            self.ansatz_generators[generator] = service

    @UnbindField('_ansatz_generator')
    @UnbindField('_molecule_generator')
    def unbind_dicts(self, field, service, svc_ref):
        
        if svc_ref.get_property('molecule_generator'):
            generator = svc_ref.get_property('molecule_generator')
            del self.molecule_generators[generator]
        elif svc_ref.get_property('ansatz_generator'):
            generator = svc_ref.get_property('ansatz_generator')
            del self.ansatz_generators[generator]

    @Invalidate
    def invalidate(self, context):
        print("VQEEnergy Algorithm Invalidated")

    def execute(self, inputParams):
        qpu = xacc.getAccelerator(inputParams['accelerator'])
        xaccOp = self.molecule_generators[inputParams['molecule-generator']].generate(
            inputParams)
        ansatz = self.ansatz_generators[inputParams['name']].generate(
            inputParams, xaccOp.nQubits())

        if 'qubit-map' in inputParams:
            qubit_map = ast.literal_eval(inputParams['qubit-map'])
            xaccOp, ansatz, n_qubits = xaccvqe.mapToPhysicalQubits(
                xaccOp, ansatz, qubit_map)
        else:
            n_qubits = xaccOp.nQubits()
        vqe_opts = {'task': 'compute-energy', 'ansatz': ansatz, 'accelerator': qpu}
        
        self.op = xaccOp
        self.n_qubits = n_qubits
        
        if 'initial-parameters' in inputParams:
            vqe_opts['vqe-params'] = ','.join([str(x) for x in ast.literal_eval(inputParams['initial-parameters'])])
            
        if 'n-execs' in inputParams:
            xacc.setOption('sampler-n-execs', inputParams['n-execs'])
            qpu = xacc.getAcceleratorDecorator('improved-sampling', qpu)
            vqe_opts['accelerator'] = qpu

        if 'readout-error' in inputParams and inputParams['readout-error']:
            qpu = xacc.getAcceleratorDecorator('ro-error',qpu)
            vqe_opts['accelerator'] = qpu
               
        xacc.setOptions(inputParams)

        self.vqe_options_dict = vqe_opts

        buffer = qpu.createBuffer('q', n_qubits)
        results = xaccvqe.execute(xaccOp, buffer, **vqe_opts)
        return buffer

    def analyze(self, buffer, inputParams):
        ps = buffer.getAllUnique('parameters')
        timestr = time.strftime("%Y%m%d-%H%M%S")
        csv_name = "%s_%s_%s_%s" % (os.path.splitext(buffer.getInformation('file-name'))[0],
                                        buffer.getInformation('accelerator'),
                                        'vqeenergy', timestr)
        f = open(csv_name+".csv", 'w')
        for p in ps:
            f.write(str(p).replace('[', '').replace(']', ''))
            energy = 0.0
            for c in buffer.getChildren('parameters', p):
                exp = c.getInformation('exp-val-z')
                energy += exp * c.getInformation('coefficient')
                f.write(','+str(c.getInformation('exp-val-z')))
            f.write(','+str(energy)+'\n')
        f.close()
       
        if 'richardson-extrapolation' in inputParams and inputParams['richardson-extrapolation']:
            angles = buffer.getInformation('vqe-angles')
            qpu = self.vqe_options_dict['accelerator']
            self.vqe_options_dict['accelerator'] = xacc.getAcceleratorDecorator('rich-extrap',qpu)
            self.vqe_options_dict['task'] = 'compute-energy'
            xaccOp = self.op
            self.vqe_options_dict['vqe-params'] = ','.join([str(x) for x in angles])

            print(xaccOp, self.vqe_options_dict['ansatz'].toString('q'))
         
            for r in [1,3,5,7]:
                csv_name = "%s_%s_%s_%s" % (os.path.splitext(buffer.getInformation('file-name'))[0],
                            buffer.getInformation('accelerator'),
                            'rich_extrap_'+str(r), timestr)
                f = open(csv_name+".csv", 'w')
                xacc.setOption('rich-extrap-r',r)

                for i in range(1 if not 'rich-extrap-iter' in inputParams else int(inputParams['rich-extrap-iter'])):
                    richardson_buffer = qpu.createBuffer('q', self.n_qubits)
                    results = xaccvqe.execute(xaccOp, richardson_buffer, **self.vqe_options_dict)
                
                    ps = richardson_buffer.getAllUnique('parameters')
                    for p in ps:
                        f.write(str(p).replace('[', '').replace(']', ''))
                        energy = 0.0
                        for c in richardson_buffer.getChildren('parameters', p):
                            exp = c.getInformation('ro-fixed-exp-val-z') if c.hasExtraInfoKey('ro-fixed-exp-val-z') else c.getInformation('exp-val-z')
                            energy += exp * c.getInformation('coefficient')
                            f.write(','+str(exp))
                        f.write(','+str(energy)+'\n')
                f.close()

        if 'hf-energy' in inputParams:
            hf_energy = ast.literal_eval(inputParams['hf-energy'])
            energy = buffer.getInformation('vqe-energy')
            correlation_energy = energy - hf_energy
            buffer.addExtraInfo('correlation-energy', correlation_energy)        