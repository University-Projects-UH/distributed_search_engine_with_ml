import numpy as np
from scipy import spatial
from sklearn.neighbors import KDTree

VECTOR_DIMENSION = 100

class WordEmbeddings:
    def __init__(self, root_path = "."):
        self.embed_dict = {}
        self.vector_dimension = VECTOR_DIMENSION

        with open(f"{root_path}/glove6B/glove.6B.{VECTOR_DIMENSION}d.txt", 'r') as f:
            for line in f:
                values = line.split()
                word = values[0]
                vector = np.array(values[1:], 'float32')
                self.embed_dict[word] = vector
        
        self.kd_tree = KDTree(list(self.embed_dict.values()))
        self.keys = list(self.embed_dict.keys())

    def vectors_distance(self, vector_a, vector_b):
        return spatial.distance.euclidean(vector_a, vector_b)

    # brute force
    def find_similar_word(self, word, count = 2):
        embed = self.embed_dict[word]

        nearest = sorted(self.embed_dict.keys(), key=lambda word_a: \
                         self.vectors_distance(self.embed_dict[word_a], embed))
        return nearest[:count]

    # kdtree
    def find_similar_word_kdtree(self, word, count = 2):
        try:
            embed = self.embed_dict[word]
        except:
            return []

        _, nearests = self.kd_tree.query([embed], k = count + 1)
        return [self.keys[nearest] for nearest in nearests[0][:1]]
