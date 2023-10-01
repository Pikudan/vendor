import numpy as np
import pymorphy3
from rank_bm25 import BM25Okapi
from tqdm import tqdm
from typing import List
import re

class BM25Model:
    def __init__(self, max_k=100, prefit=True):
        self.morph = pymorphy3.MorphAnalyzer()
        self.bm25 = None
        self.max_k = max_k
        if prefit:
            self.tokenized_corpus = np.load('../files/tokenized_tokenized_corpus_name_cat.npy', allow_pickle=True).tolist()
        else:
            self.tokenized_corpus = None

        
    def clear_text(self, text: str):
        text = re.sub('[",*+!:;<=>?@]^_`{|}~]', '', text)
        text = re.sub('\s\d+\s', '', text)
        return text
        
    def lemmatize(self, text):
        words = text.split() # разбиваем текст на слова
        res = list()
        for word in words:
            p = self.morph.parse(word)[0]
            nf = p.normal_form
            if nf not in res:
                res.append(nf)

        return list(res)
    
    def fit(self, corpus: List[str] = []):
        if self.tokenized_corpus is None:
            self.tokenized_corpus = [self.lemmatize(self.clear_text(sent)) for sent in tqdm(corpus)]
        self.bm25 = BM25Okapi(self.tokenized_corpus)
        
    def predict(self, query: str, top_k=30):
        '''Return top_k relevant indexes and their scores'''
        
        if self.bm25 is None:
            raise Exception("Fit model at first!")
            
        tokenized_query = self.lemmatize(self.clear_text(query))
        doc_scores = self.bm25.get_scores(tokenized_query)
        
        if top_k is None:
            n_positive = np.sum(np.array(doc_scores) > 0)
            top_k = np.max([n_positive, self.max_k])
            
        ind = np.argsort(doc_scores)[top_k:][::-1][:top_k]
        scores = sorted(doc_scores, reverse=True)[:top_k]
        return ind, scores