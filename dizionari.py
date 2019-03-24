"""
Modulo Gestione concetti
"""

import nltk
import numpy as np
import matplotlib.pyplot as plt

from nltk.corpus import wordnet as wn
"""
Prende in ingresso un INPUT FILE SCOFEAT
Conta le frequenze e disegna un grafico.
"""
def funzione_fro(inputfile):
   Arratemp = range (1001)
   for x in range(0,len(Arratemp)):
      Arratemp[x] = 0;
   fSc = open(inputfile, 'rU')

   for line in fSc:
      scofeat = line.strip().split()
      for x in range (2,len(scofeat),2):
         score = int(scofeat[x+1]) 
         score = int(score/100)
         Arratemp[score] = Arratemp[score] +1;
   fSc.close()
   
   x = len(Arratemp) 
   t = np.arange(x)
   
   width = 1.0     # gives histogram aspect to the bar diagram  
  
   ax = plt.axes()  
   ax.set_xticks(t + (width / 2))  
   ax.set_xticklabels(np.arange(100,100000,100))  
  
   plt.bar(t, Arratemp, width, color='r')  
   plt.ylabel("Totali")
   plt.xlabel("Frequenze")
   plt.show() 

  
"""
inputFile: file con il dizionario
Legge un dizionario da file
Ritorna: dizionario { ( ,), ... ,}
"""
def lettura_dizionario_file(inputFile):
   fIn = open(inputFile,'rU')
   dizionario = {}
   c =1;
   for line in fIn:
      riga = line.strip().split()
      #concetto = riga[0]
      for x in range (0,len(riga)):
         word = riga[x]
         dizionario[word] = c
      c = c+1
   fIn.close()
   return dizionario

"""
inputFile: nome file dizionario da scrivere
diz: struttura dati da scrivere 
conf: struttura dati di concetti
Scrive un dizionario su file, c parte da 1 , la prima riga del file concetti
da saltare.
"""    
def scrittura_dizionario_file(inputFile,diz,conf):
   fOut = open(inputFile,'w');
   oggetti = diz.items()
   c = 1
   for cList in conf:
      for j in oggetti:
         if j[1] == c:
            fOut.write( str(j[0])+" ")
      fOut.write("\n")
      c = c+1
   fOut.close()
  

"""
"  -true se la parola e' buona (quindi non contiene caratteri - e _ , 
"  -false altrimenti
"""
def filtro_parole_composte(parola):
   ris = True;
   for car in parola:
      if (car == '_') or (car == '-'):
         ris = False
         break;
   return ris;
   
"""
cotti: struttura dati di concetti
dastem: true, se si vuole un file di concetti stemmati
        false, altrimenti
Estrae i lemmi da parole, elimina parole composte fa lo stemming su quelle estratte
Ritorna la struttura dati dizionario
"""
def estrai_lemmi(cotti,dastem):
   porter = nltk.PorterStemmer()
   dizionario = {}
   cont =1 ;
   for outer in cotti:
      for a in outer:
         for asd in wn.synset(a).lemmas:
            if filtro_parole_composte(asd.name):

               if dastem:
                  dizionario[porter.stem( asd.name.lower() )] = cont
               else:
                  dizionario[  asd.name.lower()  ] = cont
			   
      cont = cont +1
   return dizionario
