# -*- coding: utf-8 -*-
"""NLP - Text Vectorization DEMO (Fall 2024)

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gOX8j3Orm2nJn-9uYF7M53kSkyFhzYJS

We're going to use TFIDF for vectorizing text / obtaining word embeddings.
"""

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

"""## Data Loading"""

from pandas import DataFrame

df = DataFrame({"text": [
    "the quick brown fox ate",
    "the slow brown dog walked",
    "the quick red dog ran",
    "the lazy yellow fox slept"
]})
df.index = df["text"]
df

x = df["text"]

"""## Vectorization

### Count Vectorizer (Bag of Words)

https://scikit-learn.org/1.5/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
"""

from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer()

print("---------------")
print("BAG OF WORDS:")
embeddings = cv.fit_transform(x)
feature_names = cv.get_feature_names_out()
embeddings_df = DataFrame(embeddings.todense(), columns=feature_names, index=x.index)
embeddings_df

cv.get_params()

cv.get_feature_names_out()

cv.vocabulary_

"""### Term Frequency - Inverse Document Frequency (TF-IDF)

https://scikit-learn.org/1.5/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
"""

from sklearn.feature_extraction.text import TfidfVectorizer

tv = TfidfVectorizer()

print("---------------")
print("TFIDF:")
embeddings = tv.fit_transform(x)
tokens = tv.get_feature_names_out()
embeddings_df = DataFrame(embeddings.todense(), columns=tokens, index=x.index)
embeddings_df.round(3)

tv.get_params()

tv.get_feature_names_out()

tv.vocabulary_

"""### Exploring TF-IDF Options

#### Stopword Removal

Remove stopwords:
"""

tv = TfidfVectorizer(stop_words="english")

embeddings = tv.fit_transform(x)
tokens = tv.get_feature_names_out()
embeddings_df = DataFrame(embeddings.todense(), columns=tokens, index=x.index)
embeddings_df.round(3)

"""#### N-Grams

N-gram tokens instead of single word tokens:
"""

tv = TfidfVectorizer(ngram_range=(1,2))

embeddings = tv.fit_transform(x)
tokens = tv.get_feature_names_out()
embeddings_df = DataFrame(embeddings.todense(), columns=tokens, index=x.index)
embeddings_df.round(3)

"""#### Max Features

Keep the X most frequent features:
"""

tv = TfidfVectorizer(max_features=4) # stop_words="english"

embeddings = tv.fit_transform(x)
tokens = tv.get_feature_names_out()
embeddings_df = DataFrame(embeddings.todense(), columns=tokens, index=x.index)
embeddings_df.round(3)

"""#### Token Frequency Range

Min and max frequency limits. Keep tokens appearing in more than min % of documents, and less than max % of documents.
"""

tv = TfidfVectorizer(min_df=0.5, max_df=0.9)

embeddings = tv.fit_transform(x)
tokens = tv.get_feature_names_out()
embeddings_df = DataFrame(embeddings.todense(), columns=tokens, index=x.index)
embeddings_df.round(3)

"""#### Custom Tokenizer

Custom tokenizer function (for example if you want to use stems / lemmas instead).

Here we are using pre-trained NLP model from the Spacy package:
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install -U spacy
# !python -m spacy download en_core_web_sm

import spacy

nlp = spacy.load("en_core_web_sm")

def lemmatizer(text):
    return [token.lemma_ for token in nlp(text)]

def lemmatizer_nostop(text):
    return [token.lemma_ for token in nlp(text) if not token.is_stop and not token.is_punct]

my_sentance = "the customers complained about the batteries"
print(lemmatizer(my_sentance))
print(lemmatizer_nostop(my_sentance))

tv = TfidfVectorizer(tokenizer=lemmatizer)

embeddings = tv.fit_transform(x)
tokens = tv.get_feature_names_out()
embeddings_df = DataFrame(embeddings.todense(), columns=tokens, index=x.index)
embeddings_df.round(3)

tv = TfidfVectorizer(tokenizer=lemmatizer_nostop)

embeddings = tv.fit_transform(x)
tokens = tv.get_feature_names_out()
embeddings_df = DataFrame(embeddings.todense(), columns=tokens, index=x.index)
embeddings_df.round(3)