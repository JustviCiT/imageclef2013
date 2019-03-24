"""
"   FIle Contenente valutazione termini,concetto ricerca prefile
"""
from nltk.corpus import wordnet as wn

  
"""
*  listaT:lista di termini dell'immagine
*  soglia: soglia relativa al path
*  conf: struttura dati dei concetti
"  Valuta uno scofeat di una immagine
"""
def ValutazioneTerminiImmagine( listaT, soglia , conf):
   uscenti = []
   massimo_totale = 0.0
   misura = 0.0
   concetto_totale = ''
   
   for outer in conf:
      for x in outer :
         L_concetto = wn.synset( x )   
         massimo = valutaConcetto(L_concetto,listaT)
         #print " il massimo e' ",massimo," con il concetto ",L_concetto;
         
         if massimo >= soglia:
            uscenti.append( x )
            #print " il massimo e' ",massimo," con il concetto ",L_concetto;
         
         if massimo >= massimo_totale:
            massimo_totale = massimo
            concetto_totale = x
       
   if len(uscenti) == 0 :
      uscenti.append( concetto_totale )
   #print "Concetto:",concetto_totale,"parola:",parola_totale,"max_totale: ",massimo_totale   
   return uscenti


"""
"  Non usata
"""   
def filtraggioFrequenza(listaT,frequenza):
   parole = []
   entrato = False;
   for a in listaT:
      if a[1] >= frequenza:
         parole.append( a[0] )
         entrato = True;
      else:
         break;
         
   if not entrato:
      for a in listaT:
         parole.append( a[0] )
   return parole

"""
"  Non usata
"""    
def disambiguateTerms(terms,verbose):
   sensi = []
   for t_i in terms:    # t_i is target term
      selSense = None
      selScore = 0.0
      for s_ti in wn.synsets(t_i):
         score_i = 0.0
         for t_j in terms:    # t_j term in t_i's context window
            if (t_i==t_j):
               continue
            bestScore = 0.0
            for s_tj in wn.synsets(t_j, wn.NOUN):      #   , wn.NOUN   tolto 
               tempScore = s_ti.wup_similarity(s_tj)
               if (tempScore>bestScore):
                  bestScore=tempScore
            score_i = score_i + bestScore
         if (score_i>selScore):
            selScore = score_i
            selSense = s_ti
      if verbose:
         if (selSense is not None):
            print t_i,": ",selSense,", ",selSense.definition
            print "Score: ",selScore
         else:
            print t_i,": --"
      if (selSense is not None):
         sensi.append(selSense)
   return sensi

"""
scofile: file Preuscita con id  (lista concetti)
sconceptList: lista di concetti da ricercare
Ricerca usata per il file Preuscita
""" 
def searchScofeats(scofile,sconceptList):
   swords = {}
   for sconcept in sconceptList:
      swords[sconcept] = 1
   fSc = open(scofile, 'rU')
   scofeatsBaseline = []
   for line in fSc:
      scofeat = line.strip().split()
      iid = scofeat[0]
      for x in range (1,len(scofeat)):
         word = scofeat[x]
         if word in swords: 
            scofeatsBaseline.append(iid)          
   fSc.close()

   return scofeatsBaseline

"""
*  Pconcetto: concetto in ingresso
*  lista_parole: lista di parole da valutare
"  Prende un concetto in ingresso e le keywords ed estrae per ogni 
*  tutti i synset con il numero dato da valori  
"""   
def valutaConcetto(Pconcetto,lista_parole):
   massimo = 0.0
   valori = [1]

   for a in lista_parole:
      for k in wn.synsets( a ,pos=['n'] ):    
         if int( str(k)[-4:-2] ) in valori:
            misura = Pconcetto.wup_similarity ( k )  
                  
            if misura > massimo:
               massimo = misura
             
   return massimo