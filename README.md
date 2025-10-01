# Semantic-clusters-of-words
Semantics clusters of words

The pipeline of getting semantics distance between words based on words definitions from dictionary and, as a result, semantics clusters. Code without using special Python-libraries, just pandas, numpy and re. Can work with (almost) any language.
Consist of several functions:

 - define_dict - split the original text in form of ‘word \t definition’ into dictionary

 - clean_often_words – remove often used words like conjunctions and particles (needs the list of often used words for your language)

 - find_freq – count frequency of each word in definition for getting the list of rare words
 
 - remove_rare_words – remove rare used words based on found frequencies
 
 - fill_base – compound all definitions words into matrix-like base based on Bag of words approach (like vectorization)
 
 - edit_distance – self-made classical edit_distance metric based on vectors of Bag of words
 
 - get_matrix – the function for getting the matrix of distances of all words in provided dictionary based on edit-distance similarity of their definitions
