# Simple Keyword Analysis

Provides a simple extraction and analysis of the most commonly used words in `pdf` or `txt` files, using
the Python [Natural Language Toolkit](https://www.nltk.org/).

If you have more complex text extraction needs, 
you may want to take a look at the [Doc Processing Toolkit](https://github.com/18F/doc_processing_toolkit).


## Installation
First, download the repo:
`git clone https://github.com/18F/text-analysis.git`

We recommend using `pipenv` to install dependencies and run things safely in a virtualenv.
You'll set that up by running 
`pipenv install` from within the repo.

Your virtualenv should be using Python 3.x.

If you don't have `pipenv`, you should be able to install it by running `brew install pipenv`. 
Check the [Pipenv documentation](https://pypi.org/project/pipenv/) for details.


## Usage

First, drop the files you want to analyze into the `files` directory.

Then activate your virtual environment: `pipenv shell`

If this is your first time running this, or if you haven't used it in a long time, 
be sure the NLTK modules are up-to-date by running `python update_nltk.py`

Then run `python keyword_analysis.py`



## Dependencies

These should all be installed for you when  you run `pip install` but if you're curious about
what's happening under the hood:

[PyPDF2](https://pypi.org/project/PyPDF2/) is used to read PDF files.
[NLTK](https://www.nltk.org/) handles the textual analysis.
