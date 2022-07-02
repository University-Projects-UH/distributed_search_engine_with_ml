from scipy import spatial
from .doc import Doc
from .vector import Vector
import math
#from .word_embeddings import WordEmbeddings
import numpy as np


class VectorialModel:
    RELEVANT_PERCENTAGE = 0.12
    EPS = 1e-6
    
    def __init__(self, docs_text: 'list[str]'):
        self.term_universe = Vector()
        self.docs = []
        #self.word_embeddings = WordEmbeddings("./model/word_embeddings")
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


    def get_word_idf(self, word):
        try:
            freq = self.term_universe[word]
        except:
            freq = 1

        return math.log(len(self.docs) / freq, 10)
    

    # IDF-AWE(q) = ( 1 / sum (IDF(wordi) ) ) * sum( IDF(wordi) * wordi_vector )
    # wordi is the word embedding of qi term of the query
    def get_idf_awe(self, wordi_array):
        AWE_vector = np.zeros(self.word_embeddings.vector_dimension, dtype=float)
        sum_IDF = 0
        embed_dict = self.word_embeddings.embed_dict
        for words_pair in wordi_array:
            similar = words_pair[0]
            word = words_pair[1]

            sum_IDF +=  self.get_word_idf(similar)
            AWE_vector += embed_dict[similar] * self.get_word_idf(word)

        return AWE_vector * ( 1 / sum_IDF )

    
    def closet_term(self, idf_awe, word_embedding):
        return np.exp(spatial.distance.cosine(word_embedding, idf_awe))


    def get_query_expansion(self, query_doc):
        wordi_array = []
        count = int(math.sqrt(len(query_doc.terms)))
        for term in query_doc.terms:
            # word embeddings related with qi term
            similar_words = self.word_embeddings.find_similar_word_kdtree(term, count)
            if(len(similar_words) == 0):
                continue
            
            for w in similar_words:
                wordi_array.append([w, term])

        idf_awe_vector = self.get_idf_awe(wordi_array)
        wordi_ranking = []
        for words_pair in wordi_array:
            similar = words_pair[0]
            rank = self.closet_term(idf_awe_vector, self.word_embeddings.embed_dict[similar])
            wordi_ranking.append([rank, similar])

        wordi_ranking = sorted(wordi_ranking, reverse=True)
        return [words_pair[1] for words_pair in wordi_ranking][:min(count, len(wordi_ranking))]


    # The first n documents of the ranking are considered relevants
    def query(self, text: str):
        
        query_doc = Doc(text)
        print(query_doc.terms)
        #query_doc.add_terms(self.get_query_expansion(query_doc))
        query_doc.calculate_wi(self.idf)
        print(query_doc.terms)
        
        ranking = []
        index = 0
        for doc in self.docs:
            rank = self.correlation(doc.wi, query_doc.wi)
            if(rank > self.RELEVANT_PERCENTAGE):
                ranking.append([rank, doc, index])
            index += 1

        ranking = sorted(ranking, reverse=True)

        return ranking[:min(40, len(ranking))]
