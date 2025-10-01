import pandas
import numpy
import re

class definition:
	def __init__(self, word, defined):
		self.word = word
		self.defined = defined

class frequency:
	def __init__(self, word, freq):
		self.word = word
		self.freq = freq

def define_dict (dictionary): #Split on words and definitions
	new_dictionary = []
	for i in range (0, len (dictionary), 2):
		new_dictionary.append (definition (dictionary [i].lower(), dictionary [i+1].lower()))
	return new_dictionary

def clean_often_words (dictionary, path_to_often_used_words): #Remove often used words
	with open(path_to_often_used_words, "r", encoding='utf-8') as file:
		often_words = file.read().replace ("\n", "\t").split("\t")

	for i in range (0, len (dictionary)):
		definition = re.sub(r'[^\w\s]', '', dictionary [i].defined)
		definition = list (definition)
		dictionary [i].defined = " ".join([word for word in definition if word not in often_words])

	return dictionary

def find_freq (dictionary): #Get all words frequencies from definitions
	freqs = []
	for i in range (0, len (dictionary)):
		definition = (dictionary [i].defined).split (" ")
		for j in range (0, len (definition)):
			no_coincidence = False
			if len (freqs)!=0:
				for f in range (0, len (freqs)):
					if definition [j] == freqs [f].word:
						freqs [f].freq = freqs [f].freq+1
						no_coincidence = False
						break
					else:
						no_coincidence = True
			else:
				no_coincidence = True
			if no_coincidence:
				freqs.append (frequency (definition [j], 1))

	stopper = 0
	all_words = []
	while stopper != len (freqs):
		all_words.append (freqs [stopper].word)
		if freqs [stopper].freq<2:
			freqs.pop (stopper)
		else:
			stopper += 1

	return freqs, all_words

def remove_rare_words (freqs, dictionary): #Remove rare used words
	for i in range (0, len (dictionary)):
		definition = (dictionary [i].defined).split (" ")
		dictionary [i].defined = " ".join([def_word for def_word in definition if def_word not in list(map(lambda x: x.word, freqs))])
	return dictionary

def fill_base (dictionary, all_words): #Get the base as Bag of words
	all_words.insert(0, 'word')
	columns = all_words
	base = pandas.DataFrame(columns=columns)

	for i in range (0, len (dictionary)):
		definition = dictionary [i].defined.split (" ")
		if len (definition) == 0:
			continue
		base.loc[-1] = 0
		base.reset_index(drop=True, inplace=True)
		base.at [i, 'word'] = dictionary [i].word
		for j in range (0, len (definition)):
			for c in range (1, len (columns)):
				if definition [j] == columns [c]:
					base.at [i, columns [c]] = 1
					break
	return base

def edit_distance (first, second): #Self-made edit distance metric
	dist_matr = numpy.zeros((len (first)+2, len (first)+2))
	for i in range (0, dist_matr.shape [0]):
		if (i+2) < dist_matr.shape [0]:
			dist_matr [0, i+2] = first [i]
			dist_matr [i+2, 0] = second [i]
		if (i+1) >= dist_matr.shape [0]:
			break
		dist_matr [1, i+1] = i
		dist_matr [i+1, 1] = i
	for i in range (2, dist_matr.shape [0]):
		for j in range (2, dist_matr.shape [0]):
			if dist_matr [i, 0] != dist_matr [0, j]:
				dist_matr [i, j] = min ((dist_matr [i-1, j-1]+2), (dist_matr [i-1, j]+1), (dist_matr [i, j-1]+1))
			else:
				dist_matr [i, j] = dist_matr [i-1, j-1]
	return dist_matr [dist_matr.shape [0]-1, dist_matr.shape [0]-1]

def get_matrix (base): #Get the matrix of distances for all words
	list_cols = ['word']
	cols = list(base.columns.values)
	cols.pop(0)
	cols.pop(0)
	for i in range (0, base.shape [0]):
		list_cols.append (base.at [i, 'word'])

	matr = pandas.DataFrame(columns = list_cols)
	for i in range (0, base.shape [0]):
		first_combination = []
		for element in cols:
			first_combination.append (str(base.at [i, element]))
		matr.loc[len (matr.index)] = 0
		matr.at [i, 'word'] = base.at [i, 'word']
		for j in range (0, base.shape [0]):
			second_combination = []
			for element in cols:
				second_combination.append (str(base.at [j, element]))
			matr.at [i, (base.at [j, 'word'])] = edit_distance (first_combination, second_combination)
	matr.reset_index (drop=True, inplace=True)
	return matr

path_to_text = "corpus/text.txt"
path_to_often_used_words = "corpus/often_used_words.txt"
#to get the definitions
with open(path_to_text, "r", encoding='utf-8') as file:
	dictionary = file.read().replace ("\n", "\t").split("\t")
dictionary = define_dict (dictionary)

#to clean often words
dictionary = clean_often_words (dictionary, path_to_often_used_words)

#to find frequencies
frequencies, all_words = find_freq (dictionary)

#to remove rare words
dictionary = remove_rare_words (frequencies, dictionary)

#to make the base
base = fill_base (dictionary, all_words)

#to get a matrix
matrix = get_matrix (base)