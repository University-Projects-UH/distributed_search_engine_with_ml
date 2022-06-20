class VectorialModel:
    def __init__(self, docs):
        self.term_universe = {}
        self.doc_vecs = []
        for doc in docs:
            doc = Doc(doc)
            for term in doc.freq:
                if(self.term_universe.__contains__(term) == False):
                    self.term_universe[term] = 1
                else:
                    self.term_universe[term] += 1
            self.docs.append(doc)

        self.calculate_idf()
        self.calculate_weight_of_docs()
