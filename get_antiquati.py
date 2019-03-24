import webbrowser
import os.path
import shutil

DATA_DIR = '//SASHA-PC/Users/Public/Documents/Progetto iMAGECLEF/ImageCLEF13/data/WEBUPV/'

INPUT_FILE_KEYWORDS = 'data/feats_textual/old/webupv13_train_textual.keywords'   #keywords
INPUT_FILE_SCOFEAT = './data/feats_textual/webupv13_train_textual_preprocessato.scofeat'      #immagine con lista word estratte     // 

INPUT_FILE_IMGSRC = './data/webupv13_train_lists/train_rimgsrc.txt'        #misto ID_immagine ID_page e url immagine
INPUT_FILE_RURLS = './data/webupv13_train_lists/train_rurls.txt'          #ID_immagine con pagina web
INPUT_FILE_IURLS = './data/webupv13_train_lists/train_iurls.txt'         #ID_immagine con posizione
INPUT_FILE_IIDS = './data/webupv13_train_lists/train_iids.txt'          #solo ID_immagine 

#Visualizza info per ID_immagine      
def showInfoForIid(iid,verbose):
   print "\nIID: "+iid
   print "-"*21
   print "\nImage source url(s): "+str(getUrlsForIid(INPUT_FILE_IURLS,iid))
   webbrowser.open("file://"+getImageFilename(iid))
   if verbose:
      print "\nSource page(s): "
      for rid in getRidsForIid(INPUT_FILE_IMGSRC,iid):
         print "RID "+": "+rid
         print "   SRCS "+": "+str(getSrcsForRidIid(INPUT_FILE_IMGSRC,rid,iid))
      print "\nSource page(s) urls: "+str(getUrlsForIid(INPUT_FILE_RURLS,iid))
      print "\nSearch keywords:"+str(getKwsForIid(INPUT_FILE_IIDS,INPUT_FILE_KEYWORDS,iid))
      scofeats = getScofeatsForIid(INPUT_FILE_SCOFEAT,iid)  # iid -> scfs
      print "\nNear words and scores: "+str(scofeats)
      print "\nFilename dell'immagine: "+getImageFilename(iid)

#ritorna ID_immagine in base all'ID_page    INPUT_FILE_IMGSRC,rid
def getIidsForRid(inputFile,srid):
   # print "Reading "+inputFile+"..."
   f = open(inputFile, 'rU')
   iids = []
   for line in f:
      data = line.strip().split()
      # print data
      iid = data[0]
      rid = data[1]
      if srid == rid:
         iids.append(iid)
   f.close()
   return iids
   
#ritorna ID_page in base all' ID_immagine   INPUT_FILE_IMGSRC , iid
def getRidsForIid(inputFile,siid):
   # print "Reading "+inputFile+"..."
   f = open(inputFile, 'rU')
   rids = []
   for line in f:
      data = line.strip().split()
      # print data
      iid = data[0]
      rid = data[1]
      if siid == iid:
         rids.append(rid)
   f.close()
   return rids

#Posizione immagine nelle sottocartelle,    INPUT_FILE_IMGSRC . rid, iid
def getSrcsForRidIid(inputFile,srid,siid):
   # print "Reading "+inputFile+"..."
   f = open(inputFile, 'rU')
   srcs = [] 
   for line in f:
      data = line.strip().split()
      # print data
      iid = data[0]
      rid = data[1]
      if siid == iid and srid == rid:
         for x in range (2,len(data)):
            src = data[x]
            srcs.append(src)
         break
   f.close()
   return srcs

#Ritorna ARRAY di url principale in base all'ID_immagine   INPUT_FILE_IURLS/INPUT_FILE_RURLS
def getUrlsForIid(inputFile,siid):
   # print "Reading "+inputFile+"..."
   f = open(inputFile, 'rU')
   urls = [] 
   for line in f:
      data = line.strip().split()
      # print data
      iid = data[0]
      if siid == iid:
         for x in range (1,len(data)):
            rurl = data[x]
            urls.append(rurl)
         break
   f.close()
   return urls

#Ritorna le keywords associate all' ID_immagine
def getKwsForIid(iidFile, kwFile,siid):
   # print "Reading "+kwFile+"..."
   fId = open(iidFile, 'rU')
   fKw = open(kwFile, 'rU')
   kws = []

   for line in fId:
      iid = line.strip()
      kwData = fKw.readline().strip().split()
      if siid == iid:
         for x in range (0,len(kwData),3):
            kw = kwData[x]
            pos = kwData[x+1]
            mor = kwData[x+2]
            kws.append(( kw, pos, mor ))
         break
   fId.close()
   fKw.close()
   return kws
   
#Ritorna le Parole della pagina relativa all' ID_immagine
def getScofeatsForIid(scofile,siid):
   # print "Reading "+scfFile+"..."
   fSc = open(scofile, 'rU')                             
   scofeats = []
   for line in fSc:
      scofeat = line.strip().split()
      iid = scofeat[0]
      if siid == iid:
         for x in range (2,len(scofeat),2):
            word = scofeat[x]
            score = int(scofeat[x+1])
            scofeats.append((word,score))
         break
   fSc.close()
   return scofeats
   
#Visualizza info per ID_page
def showInfoForRid(rid):
   print "\nRID: "+rid
   print "-"*21
   #webbrowser.open("file://"+getPageFilename(rid))
   #print "nome pagina: "+getPageFilename(rid)
   print "\nAssociated images(s): "
   for iid in getIidsForRid(INPUT_FILE_IMGSRC,rid):
      print "IID "+": "+iid
      print "   SRCS "+": "+str(getSrcsForRidIid(INPUT_FILE_IMGSRC,rid,iid))
    
def getPageFilename(rid):
   i=0;
   filename = ""
   while not os.path.isfile(filename):
      filename = DATA_DIR+"pages/"+(rid[:2].upper())+"/"+rid+"."+str(i)+".xml"
      i = i+1
   return filename
   
#copia immagini in una directory   
def copyScofeats(scofeats,cList,verbose):
   sword ='-'.join(cList)
   destDir = DATA_DIR+"_"+sword
   if verbose:
      print "Copying "+str(len(scofeats))+" images to "+sword+" ...",
   if os.path.exists(destDir):
      shutil.rmtree(destDir)
   os.makedirs(destDir)
   for scofeat in scofeats:
      iid = scofeat
      shutil.copy(getImageFilename(iid),destDir)  #mod copy in copyfile
   if verbose:
      print "Done!"


#Ritorna il nome del file immagine    
def getImageFilename(iid):
   return DATA_DIR+"images/"+iid[:2]+"/"+iid+".jpg"
   
