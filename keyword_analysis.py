import operator
import os

import matplotlib

import nltk
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize

import PyPDF2

# In some cases you may run into some weirdness in installed 
# python versions, matplotlib and a "not installed as a framework" error.
# If so, the command below resolves the backend.
# Note that it MUST be run before any further imports.
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Point to where the PDFs you're reading from live
KW_FILES_DIR = 'files/'

# You can define additional stopwords if needed.
additional_stopwords = []

def get_keyword_frequency():
    for kw_file in os.listdir(KW_FILES_DIR):
        try:
            suffix = kw_file.rsplit('.', 1)[1].lower()
        except IndexError:
            print("No suffix on the file. We don't know what to do.")
            return
        print("Opening %s" % kw_file)
        kw_file_path = KW_FILES_DIR + kw_file
        if suffix == 'pdf':
            # Open and read the file into pyPDF2
            kw_data = PyPDF2.PdfFileReader(kw_file_path)
            #Iterate through PDF pages and extract
            kw_text = ''
            for page in kw_data.pages:
                kw_text += page.extractText()
        elif suffix == "txt":
            kw_data= open(kw_file_path,'r')
            kw_text = kw_data.read()
        else:
            print("Unknown file type. Please use PDF or TXT files")
            return

        if kw_text == '':
            print(
                """
                Failed to extract text from %s. 
                Can you cut and paste into a txt file and use that instead?
                """ % kw_file
            )
            continue

        # Strip newlines cause we just don't care about them for
        # word counts, and cast to lowercase for consistency
        kw_text = kw_text.replace('\n', '').lower()

        # we see lots of / in PDs, so let's split those and
        # extract the words from either side of the slash:
        kw_text = kw_text.replace('/', " ")

        # extract the word tokens with NLTK
        tokens = word_tokenize(kw_text)

        # what do we not want?
        # Note: there's probably a regex that would strip punctuation more cleanly
        punctuation = ['(', ')', ';', ':', '[', ']', ',', '.', '#', '%', "'s", '“', '”', '’']
        stop_words = stopwords.words('english')
        stop_words += additional_stopwords

        # quick list comprehension to strip out unwanted punctuation and stopwords
        words = [word for word in tokens if not word in stop_words and not word in punctuation]

        # for a quick primer on more great stuff we can do with NLTK, see
        # https://likegeeks.com/nlp-tutorial-using-python-nltk/
        # for now, we're going to just run our words lemmatization
        # to boil down to root words. See:
        # https://textminingonline.com/dive-into-nltk-part-iv-stemming-and-lemmatization
        lemmatizer = WordNetLemmatizer()
        lem_words = [lemmatizer.lemmatize(word) for word in words]
        # and now a second pass to pick up any verbs remaining
        keywords = [lemmatizer.lemmatize(word, pos='v') for word in lem_words]

        # we may not have to get into stemming, but we could.
        # For now, this is just stubbed.
        # If we did get into stemming, we'd probably want to build a data structure
        # with both the stem and the words in the PD that stem from it, 
        # or one representative word at least,
        # because the stems themselves aren't always clearly related.
        # For example, the stem of "provision" may be "provid".
        #stems = [stemmer.stem(word) for word in keywords]

        # And now get the frequency of our keywords
        freq = nltk.FreqDist(keywords)
        common_words = freq.most_common(50)

        # We can also show a plot of the words, if we want...
        # freq.plot(20, cumulative=False)

        # Rather than formatting with spaces, it may be better
        # to just output the words as comma-delimited text.
        # we could also, if we wanted, just skip printing them and just 
        # output csv or xls.
        for k, v in common_words:
            print(f'{k:<20} {v}')

if __name__ == "__main__":
    # execute only if run as a script
    get_keyword_frequency()