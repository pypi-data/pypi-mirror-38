from pyqpanda.Algorithm.QuantumGradient.quantum_gradient import *
from pyqpanda.Algorithm.vqe import flatten

Hp_19=PauliOperator({'Z0 Z5':0.18,'Z0 Z6':0.49,'Z1 Z6':0.59,'Z1 Z7':0.44,'Z2 Z7':0.56,'Z2 Z8':0.63,'Z5 Z10':0.23,
                 'Z6 Z11':0.64,'Z7 Z12':0.60,'Z8 Z13':0.36,'Z9 Z14':0.52,'Z10 Z15':0.40,'Z10 Z16':0.41,'Z11 Z16':0.57,
                 'Z11 Z17':0.50,'Z12 Z17':0.71,'Z12 Z18':0.40,'Z13 Z18':0.72,'Z13 Z3':0.81,'Z14 Z3':0.29})
Hd_19=PauliOperator({'X0':1,'X1':1,'X2':1,'X3':1,'X4':1,'X5':1,'X6':1,
                    'X7':1,'X8':1,'X9':1,'X10':1,'X11':1,'X12':1,'X13':1,
                    'X14':1,'X15':1,'X16':1,'X17':1,'X18':1})
Hp_7=PauliOperator({'Z0 Z4':0.73,'Z0 Z5':0.33,'Z0 Z6':0.5,'Z1 Z4':0.69,'Z1 Z5':0.36,'Z2 Z5':0.88,'Z2 Z6':0.58,
                 'Z3 Z5':0.67,'Z3 Z6':0.43})
Hd_7=PauliOperator({'X0':1,'X1':1,'X2':1,'X3':1,'X4':1,'X5':1,'X6':1})

Hp_13=PauliOperator({'Z0 Z7':0.33,'Z0 Z8':0.61,'Z0 Z9':0.55,'Z1 Z7':0.46,'Z1 Z8':0.40,'Z1 Z11':0.94,
                 'Z2 Z8':0.42,'Z2 Z9':0.43,'Z3 Z9':0.81,'Z3 Z10':0.45,'Z3 Z12':0.90,'Z4 Z10':0.67,
                 'Z4 Z11':0.77,'Z5 Z10':0.84,'Z5 Z11':0.76,'Z5 Z12':0.83,'Z6 Z7':0.50,'Z6 Z11':0.49,'Z6 Z12':0.69})
Hd_13=PauliOperator({'X0':1,'X1':1,'X2':1,'X3':1,'X4':1,'X5':1,'X6':1,
                    'X7':1,'X8':1,'X9':1,'X10':1,'X11':1,'X12':1})



def quantum_gradient_qaoa_test(Hp,Hd,step,gamma,beta,times_=100,optimizer=('Momentum',0.02,0.9),method=1,delta=1e-7,is_test=True):

    
    qubit_number=Hp.get_qubit_count()
    print('qq',qubit_number)


    init()
    qubit_list_=qAlloc_many(qubit_number)
    qaoa_obj=qaoa(qubit_number,step,gamma,beta,Hp,Hd)
    initial_cost_value=qaoa_obj.get_cost_value(qubit_list_)
    print('initial cost',initial_cost_value)
    if optimizer[0]=='Momentum':
        qaoa_obj.momentum_optimizer(qubit_list=qubit_list_,
        times=times_,
        learning_rate=optimizer[1],
        momentum=optimizer[2],
        method=method,
        delta=delta,
        is_test=is_test)
    elif optimizer[0]=='GradientDescent':
        qaoa_obj.momentum_optimizer(qubit_list=qubit_list_,
        times=times_,
        learning_rate=optimizer[1],
        method=method,
        delta=delta,
        is_test=is_test)
    else:
        print("undefined")

    final_cost_value=qaoa_obj.get_cost_value(qubit_list_)
    print('final_cost_value',final_cost_value)
    return final_cost_value


def quantum_gradient_qaoa_test_factorize(number=77,step=5):
    '''
    number:target number,assume it is a pseudoprime,such as 35,77
    '''
    #target_bin=bin(number)[2:]
    h1=PauliOperator({'Z2':-0.2,"Z1":-1,'Z0':-0.5,'':3.5})
    h2=PauliOperator({'Z6':-4,'Z5':-2,"Z4":-1,"Z3":-0.5,'':7.5})
    h3=PauliOperator({'':77})
    hp=h1*h2-h3
    hp=hp*hp*(1/77/77)
    hx=PauliOperator({'X0':1,"X1":1,'X2':1,"X3":1,'X4':1,'X5':1,"X6":1})
    hp=flatten(hp)
    gamma=(1-2*np.random.random_sample(step))*2
    beta=(1-2*np.random.random_sample(step))*pi/4
    cost_value=quantum_gradient_qaoa_test(Hp=hp,Hd=hx,step=step,gamma=gamma,beta=beta,times_=100,optimizer=('Momentum',0.02,0.9),method=1,delta=1e-7,is_test=True)
    return cost_value






# def quantum_gradient_qaoa_test():

#     step=2
#     gamma=(1-2*np.random.random_sample(step))*2
#     beta=(1-2*np.random.random_sample(step))*pi/4

#     qubit_number=7
#     Hp=Hp_7*0.5
#     Hp=flatten(Hp)
#     init()
#     qlist=qAlloc_many(qubit_number)
#     qqat=qaoa(qubit_number,step,gamma,beta,Hp,Hd_7)
#     cost_value=qqat.get_cost_value(qlist)
#     print('cost',cost_value)

#     #qqat.optimize(qlist,20,0.01)
#     qqat.momentum_optimize(qlist,50,0.02,0.9,method=1,delta=1e-6)
#     print(qqat.beta,qqat.gamma)
#     exp2=qqat.get_cost(qlist)
#     print('exp2',exp2)
#     finalize()


