# CRI, a Competent Reader Imitator

This repository contains all the code that has been used for the *CRI, a Competent Reader Imitator* paper.
It is arranged as follows:
+   the folder **analyses** contains some curves and the data used to generate these curves
+   the folder **Corpus** contains four folders, one for each volume that has been anotated,
    each of these folders contains the articles of the volume anotated.
+   the folder **Corpus_corrected** contains the articles for an earlier version of the Corpus when we
    the data we where working with had not been processed the same way, loosing all punctuation
+   the folder **Expected_results** contains the oracles for the anotated volumes. It consists of one
    python file for each volume that contains a dictionary named expected with keys 
    being the starting page of the articles and values being the list of all binomial names in the article
+   the folder **Expected_results_binoms_corrected** contains the oracles for the earlier version of the corpus
    that is stored in **Corpus_corrected**
+   the folder **Expected_results_position** contains the oracle for the corpus but with the positions of the binoms
    added. It is this oracle that is used in our evaluation procedure
+   the folder **Processed_corpus**  contains the articles for each volume in the corpus after being preprocessed
    using the script **pretraitement.py**. These are the versions of the articles we use in our evaluation procedure 
+   the folder **results** contains some experiment results
+   the folder **scores** also contains some experiment results
+   the script **accents.py** was used to retrieve the matches that contains accents in the list of matches over the
    archive.
+   the script **classifier.py** is the main script, it has a command line interface that documents it.
+   the script **compute_stopwords.py** is used to set the rare-frequent threshold and puts the regex to filter
    the most frequent words in **stopwords.txt**
+   the script **concatenate__concatenante_pages.py** was used to create the articles in **Corpus**
    by calling **concatenate_pages** with the starting and ending page number of each article retrieved from the oracle
+   the script **concatenante_pages.py** was used to create the articles in **Corpus**
+   the script **convert_truth.py** is used to convert the oracles with just the binomial names into the oracles
    with the positions.
+   the script **decision_bound_procedure.py** is used to see the variations in the different metrics in function
    of the rare-frequent threshold.
+   the file **experience_functions.py** contains the main functions and definition used in the other scripts
+   the script **get_context.py** is used to retrieve the context in which a match was found.
+   the script **get_random_lines.py** is used to get a sample of all the matches that were found in the archive
    to manually evaluate the quality of our classifier.
+   the script **intersect.py** was used to get an idea of the number of words in common between 
    two independant volumes of LA NATURE
+   the script **pretraitement.py** is used to preprocess a file (remove double spaces, end of line `-` etc.)
+   the script **score_article.py** is used to get the results of our classifer compared with the oracle for any
    specific article in the corpus
+   the script **score_corpus.py** is the main evaluation script, it allow to process all of the corpus and get the
    results with regards to the oracles.
+   the script **tri_classification.py** is used to sort the output of the classifier in different ways.
+   the script **validate.py** was used to ensure that the oracles in **Expected_results_binoms_corrected** were
    all defined.
+   the file **verite.py** contains an early version of the oracles for **Corpus_corrected**
+   the files **words.txt** and **words_uncorected.txt** contain the list of all unique words in two different
    versions of the archive sorted by frequency in increasing order. **words_uncorected.txt** is the one used in 
    **compute_stopwords.py**


most of the scripts have a command line interface (except for the smaller ones)
