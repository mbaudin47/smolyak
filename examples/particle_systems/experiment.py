import numpy as np
from smolyak.indices import MixedDifferences, MultiIndex
from smolyak.applications.particle_systems.optimal_control import iteration
from smolyak.approximator import Decomposition, Approximator
from smolyak import experiments
import os
import pickle      
from smolyak.aux import plots
import matplotlib2tikz
from sympy.physics.quantum.circuitplot import matplotlib
from matplotlib.pyplot import savefig
class Experiment(object):
    def __init__(self,**opts):
        self.opts=opts
        np.seterr(all='raise')
        #c_iter=500
        #alpha=1
        #rho=-0.1
        power_reject=opts['power']
        power_attract=opts['power']
        def potential(p1,p2,power):
            return (p2 - p1) * np.absolute(p2 - p1)**(power-1)
        def d_potential(p1,p2,power,k):
            return (-1)**k*power*np.absolute(p2-p1)**(power-1)
        def total_potential(p1,p2):
            return -potential(p1,p2,power_reject)#+potential(p1,p2,power_attract)
        def total_d_potential(p1,p2,k):
            return -d_potential(p1,p2,power_reject,k)#+d_potential(p1,p2,power_attract,k)
        def func(c_particles,c_steps,c_iter,control):
            #print(c_particles,c_steps)
            return iteration(2*c_particles,2*c_steps,c_iter,self.opts['alpha'],self.opts['d'],self.opts['rho'],total_potential,total_d_potential,control,random=self.opts['random'])
        def extrapolation(c_particles,c_steps,c_iter,control):
            return 2*func(2*c_particles,c_steps,c_iter,control)-func(c_particles,c_steps,c_iter,control)
        self.func=func
        
    def __call__(self,test):
        return self.run_test(test)
    def run_test(self,test):   
        control=np.array([0.1]+self.opts['d']*[1.])
        decomposition = Decomposition(func=MixedDifferences(f=lambda x,y:self.func(x,y,100,control)[0], zipped=False,c_var=2,reparametrization=True), n=2,is_md=True)
        SA = Approximator(decomposition=decomposition)
        SA.expand_adaptive(T_max=test['T_max'])
        #SA.expand_nonadaptive(L=test['L'])
        return SA
    
    def run_nonadaptive(self,test):
        control=np.array([1.,0.1])
        decomposition = Decomposition(n=2,
                                      is_md=True,
                                      work_factor=[2,1],
                                      contribution_factor=[1,1])
        SA = Approximator(decomposition=decomposition)
        SA.expand_nonadaptive(L=test['L'])
        return SA
    
    def global_opt(self,test):
        return self.func(71,50,1,np.array(test))
    
    def analyze_global_opt(self,results,info):
        X,Y=info['user_data']
        nx,ny=len(X),len(Y)
        X,Y = np.meshgrid(X,Y)
        X,Y=X.T,Y.T
        Z=np.reshape(np.array([result[1] for result in results]),(nx,ny))
        plots.plot3D(X, Y, Z)
    
def analyze(results,info):
    ind=[i for i in range(len(info['status'])) if info['status'][i]=='finished']
    info['runtime']=[info['runtime'][i] for i in ind]
    results=[results[i] for i in ind]
    order = plots.plot_convergence(info['runtime'], [np.array(A.get_approximation()) for A in results],expect_order=-1)
    print('Convergence order ({}): {}'.format(info['name'],order))
    plots.save('convergence')
    results[-1].plot_indices(weighted='contribution/runtime',percentiles=5)
    plots.save('indices')
        
if __name__ == '__main__':
    #X=np.linspace(-1,1,5)
    #Y=np.linspace(0.1,2,20)
    #rsa=ResponseSurfaceApproximation([X,Y])
    #tests=[(i,j) for i in X for j in Y]
    #path=experiments.conduct(tests=tests,func=rsa.global_opt,overwrite=True,user_data=[X,Y])
    #path='2017/7/31/global_opt'
    #info,results=experiments.load(path=path)
    #os.chdir(path)
    #rsa.analyze_global_opt(results,info)
    opts={
        'alpha':1,
        'rho':-0.05,
        'power':1,
        'd':2,
        'random':True
    }
    rsa=Experiment(**opts)
    tests=[
        {'T_max':2**l} for l in range(5)
    ]
    name='rand_opt_alpha{}_rho{}_power{}_d{}'.format(opts['alpha'],opts['rho'],opts['power'],opts['d'])
    path=experiments.conduct(tests=tests, func=rsa, supp_data=opts,runtime_profile=False,memory_profile=True,analyze=rsa.analyze)
    #path='experiments/2017/8/9/'+name
    info,results=experiments.load(path=path)
    os.chdir(path)
    rsa.analyze(results,info)
