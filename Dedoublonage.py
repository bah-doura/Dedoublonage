# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 02:24:14 2019

@author: BAH
"""

from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import re
import docx
import nltk
import os
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
import numpy as np

path = 'C:\\Users\\BAH\Work Space\\M2_MIAGE\\PRM2\\TP2\\test_folder'


#Lecture et conversion d'un fichier PDF en .txt
def convertPdfFile(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    str = re.sub(r'[^a-zA-Z0-9èéêîï ]',r' ', text)
    return str.lower() 


#Lecture et conversion d'un fichier .docx en .txt
    
def convertDocxFile(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        txt = para.text.encode('ascii', 'ignore')
        fullText.append(txt)
    text =  b''.join(fullText) 
    str = re.sub(r'[^a-zA-Z0-9èéêîï ]',r' ', text.decode("utf-8"))
    return str.lower() 

#Lecture du et conversion en tableau du fichier des vocabulaires
def  readVocabulary(path):
    f = open(path)
    li = []
    for ln in f:
        li.append(ln.split())
    #return re.sub(r'[^a-zA-Z0-9èéêîï ]',r' ', text)
    return li

#Fonction pour compter le nombre d'occurance
def countOccurences(str, word):
    count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word), str))
    return count

#Suppression de stop word dans les fichiers
def stopWordFilter(str):
    stop_words = set(stopwords.words('french')) 
    word_tokens = word_tokenize(str) 
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    filtered_sentence = [] 
    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w)
    text =  ' '.join(filtered_sentence)
    return text 

#Lecture des noms de fichiers
def radFilesNames(path):
    i=0
    listFilesNames =[]
    for filename in os.listdir(path):
        listFilesNames.insert(i,filename)
        i = i+1
    return listFilesNames

#Permet de créer un vecteur
def createVector(vocabulary, str):
    #Suppression de mots inutiles
    text = stopWordFilter(str)
    #initialisation du vecteur
    a = range(len(vocabulary[0]))
    a = [i*0 for i in a]
    vector = np.array(a)
    i=0;
    for item in vocabulary[0]:
        word = vocabulary[0][i]
        #print(word)
        vector[i] = countOccurences(text.lower(), word)
        i=i+1
    return vector

#Permet de lire tous les fichiers PDF d'un dans un dossier et créer les les vecteurs 
# avant de trouver les nombre d'occurance
def createMapOccurence(path, vocabulary):
    filesVectors = dict()
    duplicateFilesMap = dict()
    filesName = radFilesNames(path)
    for filename in filesName:
        extension =  os.path.splitext(filename)[1]
        if extension == '.pdf':
            #print(filesVectors+"\n")
            text = convertPdfFile(path+'\\'+filename)
            vector = createVector(vocabulary, text)
            #print(vector)
            filesVectors[filename]=vector
        elif extension == '.docx':
           # print(filename+"\n")
            text = convertDocxFile((path+'\\'+filename))
            vector = createVector(vocabulary, text)
            #print(vector)
            filesVectors[filename]=vector
    for file in filesVectors.keys():
        duplicateFilesMap[file] = 0
        currentVecotr = filesVectors.get(file)
        i = -1
        for key in filesVectors.keys():
            vector = filesVectors.get(key)
            distance =np.linalg.norm(vector-currentVecotr)
            if distance == 0.0:
                newPair = {file: i+1}
                i=i+1
                duplicateFilesMap.update(newPair)
    return duplicateFilesMap
   
#Permet de trouver d'afficher la map
    
def printNomberOccurenceFile(mapData):
    for k, v in mapData.items():
        print ("{} : {}".format(k, v))
        
        
#Test 
vocabulary = readVocabulary("C:\\Users\\BAH\Work Space\\M2_MIAGE\\PRM2\\TP2\\vocabulaire.txt")
mapVecotr = createMapOccurence(path, vocabulary)
printNomberOccurenceFile(mapVecotr)