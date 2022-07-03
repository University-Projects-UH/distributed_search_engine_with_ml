from .text_utils import TextPreprocessingTools
from .vector import Vector

A = 0.4

class Doc:
    def __init__(self, text: str):
        tpt = TextPreprocessingTools()
        self.text = text
        self.terms = tpt.run_pipeline(text).split(" ")
        self.build_freq()
        self.calculate_tfi()


    def add_terms(self, new_terms):
        if(len(new_terms) == 0):
            return
        self.terms.extend(new_terms)
        self.build_freq()
        self.calculate_tfi()


    def __lt__(self, other):
        return len(self.terms) < len(other.terms)


    def build_freq(self):
        self.freq = Vector()
        for term in self.terms:
            try:
                self.freq[term] += 1
            except:
                self.freq[term] = 1


    def calculate_tfi(self):
        self.tfi = Vector()
        max_freq = max(self.freq.values())

        for term in self.freq:
            self.tfi[term] = self.freq.vector[term] / max_freq


    def calculate_wi(self, idf, is_query = False):
        self.wi = Vector()

        for term in self.tfi:
            if(idf.__contains__(term) == False):
                continue
            if(is_query):
                self.wi[term] =  (A + ((1 - A) * self.tfi.vector[term])) * idf.vector[term]
            else:
                self.wi[term] = self.tfi.vector[term] * idf.vector[term]

        self.wi.calculate_norm()

