from nltk import word_tokenize
import unicodedata 
from nltk.corpus import wordnet as wn 
from pattern.es import lemma, singularize, parse 
from utils.utils import stopWords, abc




#funcion que elmina todos los signos que no son palabras, puntos o espacios
def elimina_sign(text):
    text_out=''
    for i in text:
        if i not in abc:
             text_out+=' '
        else :
            text_out +=i
    return text_out




def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))


# lemmatiza verbos y singulariza sustantivos y adjetivos
def pword(text):
    ind=parse(text).split('/')[1][0] 
    
    # verbo
    if ind=='V':
        word=lemma(text)

    # sustantivo o adjetivo    
    else:
        word=singularize(text)
    return word


# Encontrar Sinonimos y Antonimos
# entrega un conjunto de sinonimos y antonimos
def sin_ant(text):
    lema=wn.lemmas(text,lang='spa')
    antonimos=list()
    sinonimos=list()
    for i in lema:
        sinonimos.extend(i.synset().lemma_names(lang='spa'))
        for j in i.synset().lemmas():
            for k in j.antonyms():
                antonimos.extend(k.synset().lemma_names(lang='spa'))


    sinonimos=set(sinonimos)
    antonimos=set(antonimos)
    return sinonimos,antonimos


## procesa el texto, retorna una lista con palabras procesadas

def ptext(text):
    output=list()        
    
    #quita el enlace
    text=text.split('https')[0]

    #pasa todo a minusculas
    text = text.lower()

    #elmina signos de puntuacion
    #text=elimina_tildes(text)

    #elimina caracteres
    text=elimina_sign(text)

    #separa el texto por frases u oraciones
    frases=text.split('.');

    #separa por las palabras
    for fr in frases:
        if len(fr)!=0: 
            words_sw = word_tokenize(fr)
            words=[]
            for i in words_sw:
                
                word=pword(i)
                words.append(word)

            if len(words)!=0:            
                output.append(words)

    return output
