# JapPhonetization

1) Python program: "phonetize_jap.py"
to be launched with the file to phonetize as an argument
ex : 	python phonetize_jap.py test1.txt

libraries needed:
urllib.request
gzip
shutil
xml.etree.ElementTree
sys
csv
re

2) Data files
2 data files are called by the program and have to be in the same folder:
hiragana_table.csv
katakana_table.csv

3) Data file to collect
The program fetches, unzips and parses a kanji dictionary.
Fetched file:	kanjidic2.xml.gz
Unziped file:	kanjidic2.xml
Final file:		kanji_extract.txt

4) Test file "test1.txt"
Contains input tokens

日本	word
すごい	word
食べる	word
パソコン	word
Sony	word
العربية	word
食べعる	word
32802	numeral
3,209	numeral
一〇〇	numeral
四百六十九	numeral

The output of the program is "test1.txt_out.txt":
日本	nitihona
すごい	sugoøi
食べる	sikuberu
パソコン	pasokona
Sony	!!ROMAJI!!
العربية	#######
食べعる	sikube#ru

The numerals do not appear in the output, as I have not treated them in the program.
If a word consists of latin characters, the output is:	!!ROMAJI!!
If a word contains unknown characters, each unknown character is represented by a #.
