# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 23:59:23 2018

"""
from time import time
from ppsing import sin_ant
import numpy as np
from sklearn.metrics.pairwise import pairwise_kernels
import pickle
import scipy.spatial.distance as sp


def T_syn_ant(vocab):
    """ Funcion que calcula las matrices de antonimos y sinonimos.
    
    Entradas:    
        vocab : Vocabulario del wordmebedding implementado
    
    Salidas     
        T_syn: matriz de sinonimos, T_syn (ij)= 1 si wi y wj son sinonimos, 0 otro caso
        T_ant: matriz de antonimos, T_ant (ij)= -1 si wi y wj son antonimos, 0 otro caso
    """
    n=len(vocab)
    # inicializa arrays con 0
    T_syn = np.array([[0.0]*n]*n)
    T_ant = np.array([[0.0]*n]*n)
    
    for i in range(n):        
        #obtener sinonimos y antonimos
        syn,ant = sin_ant(vocab[i])
        for j in syn:
            try: T_syn[i][vocab.index(j)]= 1.0
            except: continue 
        for j in ant:
            try: T_ant[i][vocab.index(j)]= -1.0
            except: continue
  
    return T_syn,T_ant


#funcion de metricas

KERNELS={
    'gaus':'rbf',
    'cosine':'cosine',
    'mah': sp.mahalanobis }




def W(X,kernel='gaus',**kwds ): 

    """
    hay varias formas para implementar el calculode W.
    uno es con cosine similarity.
    otro es distance mahalanobis, revizar
    """
    try:
        kernel_func=KERNELS[kernel]
    except:
        print('metrica no correspondiente')
        return 1

    matrix=pairwise_kernels(X,metric=kernel_func,filter_params=True,n_jobs=-1,**kwds)                 
    return matrix


                
def W_af(W,T_ant,T_syn,gama,b_ant,b_syn):

    W_final = gama*W + b_ant*T_ant*W + b_syn*T_syn*W
    return W_final




def cont_neg_pos(W):
    """ 
    Esta funcion cuenta enlaces negativos y positivos de la matriz W
    """
    cont_neg=0
    cont_pos=0
    for i in range(len(W)):
        for j in range(i+1,len(W)):
            if(W[i][j]<0.0):
                cont_neg +=1
            elif (W[i][j]):
                cont_pos +=1
    return cont_neg, cont_pos
