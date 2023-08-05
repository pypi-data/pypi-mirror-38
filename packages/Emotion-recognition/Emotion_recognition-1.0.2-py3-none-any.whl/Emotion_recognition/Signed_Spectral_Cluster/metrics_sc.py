import numpy as np


def metric(T_ant,T_sin,labels):
    """ Calcula el costo asociado al modelo 

        cuenta la cantidad de antonimos en un mismo cluster
        y la cantidad de sinonimos fuera del cluster
    """

    n=len(T_ant)
    cost=0
    for i in range(n):
        for j in range(i+1,n): 
            if(T_ant[i,j]<0.0):
                if (labels[i]==labels[j]):
                    cost+=1
            if (T_sin[i,j]>0.0):
                if (labels[i]!=labels[j]):
                    cost+=1

    return cost


def show_cluster (vocab,labels,word):
    """ entrega el cluster(palabras) donde se encuentra
        la palbra word.
    """   
    try:
        label=labels[vocab.index(word)]
    except:
        print('no existe esa frase en el vocabulario')
        return 1

    cluster=list()
    for i in range(len(labels)):
        if (label==labels[i]):
            cluster.append(vocab[i])
    return cluster


def links_clusters (affinity,labels,senti_labels=None):
    """
        Genera una estructura de datos que guarda los links positivos,
        links negativos y el volumen de los clusters de interes (sentimentales)
        
        entradas:
            affinity : np.array, matriz de afinidad del grafo.
            labels: list(), lista de etiquetas al aplicar el clustering al grafo.
            senti_labels: set(), conjunto de etiquetas de interes.

        Salida:
            links: dict(), diccionario donde la primera llave es el cluster de interes,
            y entrega diccionario donde las llave son:
                 
                 'vol'(volumen del cluster)
                 'neg'(links-)
                 'pos'(links+) 

        ejemplo: links[1]['vol']--> volumen del cluster 1
        La complejidad es n
    """    


    if (senti_labels==None):
        senti_labels=set(labels)

    links=dict()
    for i in range(len(labels)):

        etiqueta=labels[i]
        if etiqueta in senti_labels:
            
            if etiqueta not in links.keys():
                links[etiqueta]=dict()
                X=np.absolute(affinity[:,i])
                X_neg=0.5*(X-affinity[:,i])
                X_pos=0.5*(X+affinity[:,i])
                links[etiqueta]['c_pos']=np.sign(X_pos)
                links[etiqueta]['c_neg']=np.sign(X_neg)
                links[etiqueta]['neg']=X_neg
                links[etiqueta]['pos']=X_pos

            else:
                        
                X=np.absolute(affinity[:,i])
                X_neg=0.5*(X-affinity[:,i])
                X_pos=0.5*(X+affinity[:,i])
                links[etiqueta]['c_pos']+=np.sign(X_pos)
                links[etiqueta]['c_neg']+=np.sign(X_neg)
                links[etiqueta]['neg']+=X_neg
                links[etiqueta]['pos']+=X_pos
    
    return links



def simCluster (vocab,sentences,links):
    """
    Calcula un diccionario, que guarda los siguientes funcionales:
        S+(A,Ci)=links+(A,Ci)/vol(Ci)+links-(A,Ci^c)/vol(Ci^c)
        S-(A,Ci)=links-(A,Ci)/vol(Ci)+links+(A,Ci^c)/vol(Ci^c)
        Entradas:
            affinity: matriz de afinidad del grafo.
            vocab: vocabulario del modelo.
            sentences: lista de palabras.
            links: diccionario otorgado por links_clusters
        Salidas:
            functional: diccionario, con labels como llave y que guarda una lista con los funcionales.

        Ejemplo: functional[C_i]=[S+(A,C_i),S-(A,C_i)]
    """
    functional = dict()
    output = dict()
    for i in links.keys():
        output[i]=0.0
    #vol_A=0

    cant_a=0
    X=np.array([[0,0]]*len(links.keys()))
    # obtiene indices de las palabras y volumen de la frase A
    for frase in sentences:
        try:
            i=vocab.index(frase)         
            


            for label_1 in links:

                if (label_1 not in functional.keys()):
                    #lista de enlaces l_mas, l_menos, l_mas_c,l_menos_c
                    functional[label_1]=([0,0],[0,0],[0,0],[0,0])
                
                for label_2 in links:
                    if (label_1==label_2): 
                        # suma de pesos totales de la palabra i, con todas las del cluster
                        functional[label_1][0][0]+=links[label_1]['pos'][i]
                        functional[label_1][1][0]+=links[label_1]['neg'][i]
                        # suma cantitades de enlaces positivos y negativos de oracion
                        functional[label_1][0][1]+=links[label_1]['c_pos'][i]
                        functional[label_1][1][1]+=links[label_1]['c_neg'][i]

                    else:
                        functional[label_1][2][0]+=links[label_2]['pos'][i]
                        functional[label_1][3][0]+=links[label_2]['neg'][i]
                        #sumar cantidades de enlaces positivos y negativos de la oracion
                        functional[label_1][2][1]+=links[label_2]['c_pos'][i]
                        functional[label_1][3][1]+=links[label_2]['c_neg'][i]
        except:
            continue
            #print(frase)

    for label in functional:
        cant_0_1 = 1
        cant_1_1 = 1
        cant_2_1 = 1
        cant_3_1 = 1
        
        if (functional[label][0][1]!=0):
            cant_0_1 = functional[label][0][1]
        if (functional[label][1][1]!=0):
            cant_1_1 = functional[label][1][1]
        if (functional[label][2][1]!=0):
            cant_2_1 = functional[label][2][1]
        if (functional[label][3][1]!=0):
            cant_3_1 = functional[label][3][1]

        output[label]=(functional[label][0][0]/cant_0_1)+(functional[label][3][0]/cant_3_1)
        output[label]-=((functional[label][1][0]/cant_1_1)+(functional[label][2][0]/cant_2_1))   
    return output


def distribution(clusters):
    """Entrega un array con la cantidad de elementos en cada cluster
    """
    n =np.max(clusters)
    cant_k=[0]*n
    for i in clusters:
        cant_k[i-1] += 1
    return cant_k 

  
def position(functional):
    lista=list()
    for label,valor in functional.items():
        lista.append((valor,label))
    lista.sort()
    return lista[-1][1]

def dict_cluster(vocab, clusters):
    """Crea dicionario con keys = cluster 
        y value = lista de palabras del cluster.
    """
    dic = {}
    for i in range(len(clusters)):
        try:
            dic[clusters[i]].append(vocab[i])
        except:
            dic[clusters[i]]=[vocab[i]]

    return dic

def cluster_of_word(vocab,clusters,word):
    """Dice a que cluster pertenece a la palabra word.
    """
    indice = vocab.index(word)
    return clusters[indice]

def cluster_of_list(vocab,clusters,words):
    """word: lista de palabras
        Recibe una lista de palabras y entrega una lista 
        con los clusters a los que pertenecen dichas palabras.
    """
    n = len(words)
    out = [0]*n
    for i in range(n):
        out[i] = cluster_of_word(vocab,clusters,words[i])

    return out 

def classification_clusters(dic_clusters):

    """dic_cluster: diccionario con las palabras por cluster generado por dic_cluster
        dic_out = diccionario con los clusters clasificados
        Recibe un diccionario de clusters generado con dict_cluster,
        entrega un diccionario con los clusters clasificados.
    """
    dic_out = {'positivo':[],'negativo':[],'neutro':[]}

    print('p = positivo, n = negativo y a = no emocional')
    pregunta = input('¿Listo para clasificar los clusters en esas categorias? y/n: ')
    if (pregunta !='y'):
        return
    for i in list(dic_clusters.keys()):
        print(dic_clusters[i])
        tipo = input('¿Es del tipo p/n/a?: ')
        if (tipo=='p'):
            dic_out['positivo'].append(i)
        elif (tipo=='n'):
            dic_out['negativo'].append(i)
        elif (tipo=='a'):
            dic_out['neutro'].append(i)        
        else:
            print(f'Error, cluster {str(i)} no clasificado')

    return dic_out
            


def map_sentiment(func,sentiments):
    out=dict()
    for sentiment in sentiments:
        cant=0
        suma=0
        for i in sentiments[sentiment]:
            cant+=1
            suma+=func[i]
        out[sentiment]=suma/cant
    return out



