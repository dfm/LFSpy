import numpy as np
from FES import FES
from evaluation import evaluation
from classification import classification
import scipy.io
mat = scipy.io.loadmat('matlab_Data')

def LFS(Train, TrainLables, Test, TestLables, Para):

    gamma = Para["gamma"]
    tau = Para["tau"]
    alpha = Para["alpha"]
    sigma = Para["sigma"]
    NBeta = Para["NBeta"]
    NRRP = Para["NRRP"]
    knn = 1

    N = np.shape(Train)[1]
    M = np.shape(Train)[0]
    
    fstar = np.zeros((M, N)) #(M,N)
    fstarLin = np.zeros((M, N))
    
    tmp = []
    
    for j in range(0,tau):
        b, a, EpsilonMax[:,1] = FES(alpha, M, N, Train, TrainLables, fstar, sigma)
        TBTemp, TRTemp, Bratio, feasib, tmp = evaluation(alpha, NBeta, N, EpsilonMax, b, a, Train, TrainLables, gamma, NRRP, knn)
        
        W1 = 0
        feasib = 0
        Bratio[W1] = -1 * np.inf
        tmp, I1 = np.max(Bratio, [], 2)
        for i in range(0, N):
            fstar[:, i] = TBTemp[:, i, I1(i)]
            fstarLin[:, i] = TRTemp[:, i, I1(i)]
            
    [sClass1, sClass2] = classification(Train, TrainLables, N, Test, fstar, gamma, knn)
        
    return [fstar, fstarLin, ErCls1, ErCls2, ErClassification]

LFS(mat['Train'], mat['TrainLables'], mat['Test'], mat['TestLables'],{
    'gamma': 0.2,
    'tau': 2,
    'sigma': 1,
    'alpha': 1,
    'NBeta': 20,
    'NRRP': 2000

})