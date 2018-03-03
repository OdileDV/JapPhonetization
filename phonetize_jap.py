import urllib.request,gzip,shutil
import xml.etree.ElementTree as ET
import sys,csv,re

if len(sys.argv) == 1:
	print("Please enter a file name")
	exit()	
 
# fetch and unzip the kanji file

url = "http://www.edrdg.org/kanjidic/kanjidic2.xml.gz"

urllib.request.urlretrieve(url,'kanjidic2.xml.gz')

with gzip.open('kanjidic2.xml.gz', 'rb') as f_in:
    with open('kanjidic2.xml', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


# parse the kanji file

root = ET.parse('kanjidic2.xml').getroot()

kanjiExtract = open('kanji_extract.txt','w',encoding='utf8')

for character in root.findall('character'):
    literal = character.find('literal').text
    kanjiExtract.write(literal)
    for reading in character.findall('reading_meaning/rmgroup/reading'):
        kana = reading.get('r_type')
        if (kana == "ja_on"):
            kanjiExtract.write('\tJO\t'+reading.text)
        if (kana == "ja_kun"):
            kanjiExtract.write('\tJK\t'+reading.text)
    kanjiExtract.write('\n')           

kanjiExtract.close()


# phonetize the words

def phonetizeJap(file,newline='',encoding="utf8"):
    
    # si le mot matche avec un kana de la table de kanas, renvoie la phonétisation correspondante
    def phonetizeKana(kanaTable,unit):
        phonetizedKana = ''
        for kana in kanaTable:
            if (unit == kana[0]):
                phonetizedKana = kana[1] 
                break  
        return(phonetizedKana)    
    
    inputFile = open(file, newline=newline, encoding=encoding)
    outputFile = open(file+'_out.txt','w',encoding=encoding)
  
    inputLines = []
    with inputFile:
        for row in csv.reader(inputFile, delimiter='\t'):
            inputLines.append(row)
    #print(inputLines) 
    
    phonetizedWords = []
        
    # for this program: we stock the katakanas and hiraganas in a single list
    kanaTable = []
    with open("katakana_table.csv", newline='',encoding="utf8") as katakanaFile :
        for row in csv.reader(katakanaFile, delimiter='\t'):
            kanaTable.append(row)
    with open("hiragana_table.csv", newline='',encoding="utf8") as hiraganaFile :
        for row in csv.reader(hiraganaFile, delimiter='\t'):
            kanaTable.append(row)
    #print(kanaTable)           

    kanjiTable = []
    with open("kanji_extract.txt", newline='',encoding="utf8") as kanjiExtract :
        for row in csv.reader(kanjiExtract, delimiter='\t'):
            kanjiTable.append(row)
    #print(kanjiTable)                 
                    
    for token in inputLines:
        if (token[1] == "word"):

            tokenPhones = []

            if (re.search("^[a-zA-Z]+$",token[0])):
                tokenPhones.append(token[0])
                tokenPhones.append('!!ROMAJI!!')
                #print(tokenPhones)
                outputFile.write(token[0]+'\t!!ROMAJI!!\n')
                continue
            
            splittedToken = list(token[0])
            #print("splitted token = ",splittedToken)
            for unit in splittedToken:
                #look for katakanas and hiraganas
                phonetizedKana = phonetizeKana(kanaTable,unit)
                #print('\tphon = ',phonetizedKana)
                if not(phonetizedKana):
                    #look for kanjis
                    for kanji in kanjiTable:
                        #print(kanji)
                        if (unit == kanji[0]):
                            #print('\tkana =',kanji[2])
                            splittedTokenNew = list(kanji[2])
                            for unitNew in splittedTokenNew:
                                phonetizedKana += phonetizeKana(kanaTable,unitNew) # += car on peut avoir plusieurs kanas par kanji
                                #print('\tphon =',phonetizedKana)
                if not(phonetizedKana):
                    phonetizedKana = '#'
                tokenPhones.append(phonetizedKana)
                #print(tokenPhones)
               
            phonetization = ''.join(tokenPhones)
            wordPhonpair = [token[0],phonetization]
            #print(wordPhonpair)
            outputFile.write(token[0]+'\t'+phonetization+'\n')
                    
    outputFile.close()

phonetizeJap(sys.argv[1])
