# -*- coding: utf-8 -*- 
import time
import nltk
from nltk.corpus import stopwords
import string
from dizionari import *
from valuta_termini import * 
from get_antiquati import *
from nltk.corpus import wordnet as wn

INPUT_FILE_SCOFEAT = './data/feats_textual/webupv13_train_textual_preprocessato.scofeat'      #immagine con lista word estratte     // webupv13_train_textual_preprocessato.scofeat
INPUT2_FILE_SCOFEAT = './data/feats_textual/webupv13_train_textual_preprocessato_ns.scofeat'   # non stemmati 
INPUT_FILE_CONCEPTS = './data/webupv13_devel_lists/devel_concepts.txt'           #concetti 
LEMMI_NS = 'lemmi_ns.txt'
LEMMI ='lemmi.txt'
OUTPUT_FILE_DATI_FINALI = 'stat_500_095.txt'
PREUSCITA = 'Preuscita_1000_095.txt'

"""
concFile: file di concetti in input
Legge il file dei cooncetti 
Ritorna array di concetti
"""
def getConcepts(concFile):
   fConc = open(concFile, 'rU')
   concepts = []
   fConc.readline()
   for line in fConc:
      concept = []
      data = line.strip().split()
      word = data[0]
      pos = data[1][:1]
      nums = data[2].split(',')
      for num in nums:
         if '/' in word:   # composite concept
            concept.append(word.split('/')[0]+"."+pos+"."+num.split('/')[0])
            concept.append(word.split('/')[1]+"."+pos+"."+num.split('/')[1])
            break
         conc = word+"."+pos+"."+num
         concept.append(conc)
         # print conc
         # print wn.synset(conc)
      concepts.append(concept)
   fConc.close()
   return concepts   

"""
fileOutbase: file di uscita con totali
inputfile:  Prefile  
Crea un file con totali per concetto
"""
def statConcetti(fileOutBase,inputfile):
   fOut = open (fileOutBase, 'w')
   for cList in concetti:
      baseline = searchScofeats(inputfile,cList)
      #copyScofeats(baseline,cList,True)
      #print cList," ",len(baseline); 
      fOut.write(str(cList) +" "+ str(len(baseline)) +"\n")
   fOut.close() 
   
"""   
fileinput: prefile
lista: lista di numeri corrispondenti alle right dei concetti
crea cartelle con immagini
"""
def copiaSelettiva(fileinput,lista):
   indice = 2;
   for cList in concetti:
      if indice in lista:
         baseline = searchScofeats(fileinput,cList)
         copyScofeats(baseline,cList,True)   
      indice = indice +1  
   
"""
Funzione che esegue il preprocessing su uno scofeat
"""   
def CreazioneSmallScofeat(inputFile,outputFile):
   fSc = open(inputFile, 'rU')
   fOut = open(outputFile, 'w')
   for line in fSc:
      scofeats = []
      score = 0
      scofeat = line.strip().split()
      iid = scofeat[0]
      for x in range (2,len(scofeat),2):
         word = scofeat[x]
         score = int(scofeat[x+1])
         scofeats.append((word,score))
      new_scofeats = Preprocessing(scofeats)
      fOut.write(iid+" "+str(len(new_scofeats))+" ")
      for a in new_scofeats:
         fOut.write( str(a[0]) +" "+ str(a[1]) +" ")     
      fOut.write('\n')  
   fOut.close()
   fSc.close()

def checkNumero(numero):
   try:
      int( numero )
      return True;
   except ValueError:
      return False;

   
"""
"  Da passare alla funzione dopo un lemmatize
"  Controllo se una parola e' inglese , True in caso affermativo
""" 
def checkInglese(parola):
   result = False;
   if not wn.synsets(parola):
      result = False;                # non e' una parola inglese
   else:
      result = True;                 # e' una parola inglese
   return result


"""
"  rimuovo stopwords(inglese) ,numeri ,faccio un primo stemming , filtro per inglese 
"  lista = { (parola, peso) , ... , (,) }
"""
def Preprocessing(lista):
   wnl = nltk.WordNetLemmatizer();
   new_scofeat = []
   
   for t in lista:
      if not t[0] in stopwords.words('english'):
         #Se il carattere e' un numero lo scarto
         if not checkNumero(t[0]):
            parola = wnl.lemmatize(t[0])
               
            #Se la parola e' inglese la aggiungo
            if checkInglese(parola):
               new_scofeat.append(( parola ,t[1] ))    #porter.stem( )
              
   return new_scofeat
   
"""
fa solo stemming su uno scofeat preprocessato
"""   
def stemming_avanzato(inputFile,outputFile):
   fIn = open(inputFile,'rU')
   porter = nltk.PorterStemmer()
   fOut = open(outputFile,'w')
   
   for line in fIn:
      rigaUscita = []
      riga = line.strip().split()
      iid = riga[0]
      for x in range (2,len(riga),2):
         rigaUscita.append( (porter.stem(riga[x]),int(riga[x+1]) ) );
         
      fOut.write( str(iid)+" "+str(len(rigaUscita))+" ")
      for a in rigaUscita:
         fOut.write( str(a[0]) +" "+ str(a[1]) +" ")    
      fOut.write("\n")
      
   fOut.close()
   fIn.close()
   
"""
scofile:  scofile stemmato in input
soglia:  soglia usata dentro la funzione ValutazioneTerminiImmagine [0.05 - 0.95]
diz:    dizionario di concetti
fileUscita:   crea un file preuscita      [id { concetti... }]
Funzione Principale di ricerca 
"""
def ricerca_avanzata(scofile,frequenza,soglia,diz,fileUscita):
   fSc = open(scofile, 'rU')
   fOut = open(fileUscita, "w")
   ftwo = open(INPUT2_FILE_SCOFEAT, 'rU')

   # per ogni linea del file scofeat stemmato
   for line in fSc:
      entrato = False;
      scofeat = line.strip().split()
      iid = scofeat[0]
      fOut.write( str(iid) +" ")
      listaT = []
      
      # controllo ogni parola con il file dei concetti, se trovo le parole nella parte alta ,
      # li scrivo su un fileUscita , altrimenti approfondisco nella parte bassa.
      for x in range (2,len(scofeat),2):
         
         word = scofeat[x]
         if int(scofeat[x+1]) >= frequenza:
            if word in diz :    
               fOut.write( str( concetti[ diz[word]-1 ][0] ) +" ")
               entrato = True;
               
         else:
            if not entrato:
               if word in diz :    
                  fOut.write( str( concetti[ diz[word]-1 ][0] ) +" ")
                  entrato = True;
            else:
               break;  
      # se nessuna delle due parti dello scofeat non ha dato risultati allora ricerco tramite 
      # la funzione ValutazioneTerminiImmagine      
      if not entrato:
         for linea in ftwo:
            scofeatTWO = linea.strip().split()
            iidTWO = scofeatTWO[0]
            if iidTWO == iid:
               for x in range (2,len(scofeatTWO),2):
                  if int(scofeatTWO[x+1]) >= frequenza:
                     listaT.append(scofeatTWO[x]);
               break;                  
               
         concetti_uscenti = ValutazioneTerminiImmagine( listaT, soglia , concetti)
         for par in concetti_uscenti:
            fOut.write( str(par) +" " )    
         
      fOut.write("\n") 
	  
   fSc.close()
   ftwo.close()
   fOut.close()

         
if __name__ == "__main__": 
   """
   " inizializzazioni varie
   """
   concetti = getConcepts (INPUT_FILE_CONCEPTS)
   start = time.clock()
   # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  

   #stemming_avanzato(INPUT_FILE_SCOFEAT,'WEBUPV_TOTALE_STEM.txt')
   
   #asd = estrai_lemmi(concetti,False);
   #scrittura_dizionario_file(LEMMI_NS,asd,concetti)
   dizionario = lettura_dizionario_file(LEMMI)
   #copiaSelettiva(PREUSCITA,[15])   #82,15,93,3
   
   #funzione_fro(INPUT_FILE_SCOFEAT)
   #ricerca_avanzata(INPUT_FILE_SCOFEAT,500, 0.95,dizionario,PREUSCITA)
   #showInfoForIid('-GZYyCQqPvuUb-x4',False)         

   # ++++++++++++++++++++++++++++++++++++++++++++++++++

   #CreazioneSmallScofeat(INPUT_FILE_SCOFEAT,INPUT2_FILE_SCOFEAT)        #usata una sola volta
   #statConcetti(OUTPUT_FILE_DATI_FINALI,PREUSCITA)
   
   stop = time.clock()
   print "tempo",stop - start 



