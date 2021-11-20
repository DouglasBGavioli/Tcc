
from gensim.models import KeyedVectors


def input(word):
    modelo = KeyedVectors.load_word2vec_format("docs/cbow_s300.txt")
    words = modelo.most_similar(word, topn=8)
    return words
