# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 17:51:44 2021

@author: ys.leng
"""
import nltk
nltk.download()

from nltk.corpus import treebank


sentence = """At eight o'clock on Thursday morning Arthur didn't feel very good."""
tokens = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokens)

t = treebank.parsed_sents('wsj_0001.mrg')[0]
t.draw()

nltk.corpus.stopwords.words('english')


from nltk.corpus import brown
brown.words()
brown.categories()
reviews_words = brown.words(categories='reviews')
len(reviews_words)


from nltk.stem import PorterStemmer,WordNetLemmatizer
from nltk.tokenize import word_tokenize,sent_tokenize
ps = PorterStemmer()
new_text = 'importantance of caving as explained by cavers'
words = word_tokenize(new_text)
[print(ps.stem(w)) for w in words]

lemmatizer = WordNetLemmatizer()
print(lemmatizer.lemmatize('feet'))
print(lemmatizer.lemmatize('geese'))
print(lemmatizer.lemmatize('loving','v'))

doc = 'Google is an America multinational technology company'
tokenized_doc = nltk.word_tokenize(doc)
tagged_sentences = nltk.pos_tag(tokenized_doc)
ne_chunked_sents = nltk.ne_chunk(tagged_sentences)

named_entities = []
for tagged_tree in ne_chunked_sents:
    if hasattr(tagged_tree,'label'):
        entity_name = ' '.join(c[0] for c in tagged_tree.leaves())
        entity_type = tagged_tree.label()
        named_entities.append((entity_name,entity_type))
print(named_entities)

from string import punctuation
punctuation




















