from .doc import Doc
from .vector import Vector
import math


class VectorialModel:
    RELEVANT_PERCENTAGE = 0.15
    EPS = 1e-6
    
    def __init__(self, docs_text: 'list[str]'):
        self.term_universe = Vector()
        self.docs = []
        for text in docs_text:
            doc = Doc(text)
            for term in doc.freq:
                try:
                    self.term_universe[term] += 1
                except:
                    self.term_universe[term] = 1
            self.docs.append(doc)

        self.calculate_idf()
        self.calculate_weight_of_docs()

    
    # idf = log( N / ni ) where:
    # N -> total documents
    # ni -> total documents where the term ti appears
    def calculate_idf(self):
        self.idf = Vector()

        for term in self.term_universe:
            self.idf[term] = math.log(len(self.docs) / self.term_universe[term], 10)


    def calculate_weight_of_docs(self):
        for doc in self.docs:
            doc.calculate_wi(self.idf)


    # correlation calculated by cosine similarity
    def correlation(self, vector_a: Vector, vector_b: Vector):
        sum_t = 0
        # iterate for the vector with minor len
        max_vector = vector_a if len(vector_a) >= len(vector_b) else vector_b
        min_vector = vector_a if len(vector_a) < len(vector_b) else vector_b
        for term in min_vector:
            if(max_vector.__contains__(term)):
                sum_t += min_vector[term] * max_vector[term]

        if(sum_t < self.EPS):
            return 0

        if(vector_a.norm * vector_b.norm < self.EPS):
            return 100000

        return sum_t / (vector_a.norm * vector_b.norm)

    # The first n documents of the ranking are considered relevants
    def query(self, text: str, n = 20):
        
        query_doc = Doc(text)
        query_doc.calculate_wi(self.idf)
        
        ranking = []
        index = 0
        for doc in self.docs:
            rank = self.correlation(doc.wi, query_doc.wi)
            if(rank > self.RELEVANT_PERCENTAGE):
                ranking.append([rank, doc, index])
            index += 1

        ranking = sorted(ranking, reverse=True)

        return ranking[:min(n, len(ranking))]
