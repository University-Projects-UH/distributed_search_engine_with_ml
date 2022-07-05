import random
import numpy as np

class CBOW:

    LEARNING_RATE = 0.1

    def __init__(self, docs_tokens, word_embeddings):
        self.vocabulary = {}
        self.vocabulary_ind = {}
        self.inv_vocabulary = []
        self.docs_tokens = docs_tokens
        embed_dict = word_embeddings.embed_dict


        for doc_tokens in docs_tokens:
            for token in doc_tokens:
                try:
                    self.vocabulary[token] = embed_dict[token]
                except:
                    pass


        for i, token in enumerate(self.vocabulary.keys()):
            self.vocabulary_ind[token] = i
            self.inv_vocabulary.append(token)

        self.n = word_embeddings.vector_dimension
        self.v = len(self.vocabulary.keys())

        # W -> V * N
        self.w = []
        for key in self.vocabulary.keys():
            wi = []
            embed = self.vocabulary[key]

            for wik in embed:
                wi.append(wik)

            self.w.append(wi)

        self.w_ = []
        for _ in range(self.n):
            self.w_.append([random.random() for _ in range(self.v)])


    def get_word_index(self, word):
        try:
            return self.vocabulary_ind[word]
        except:
            return None


    def get_encoded_vector(self, word):
        ind = self.get_word_index(word)
        if(ind is None):
            return None

        v = [0] * self.v
        v[ind] = 1
        return v


    # train model with the docs
    def train_model(self, window = 4, iterations = 1000):
        mid: int = (window + 1) // 2

        training_data = []
        for doc_tokens in self.docs_tokens:
            doc_tokens_len = len(doc_tokens)
            for i in range(window, doc_tokens_len):
                context: list = doc_tokens[i - window :i + 1]
                target = context[mid]
                context.pop(mid)

                training_data.append((context, target))

        while(iterations > 0):
            for context, target in training_data:
                self.train(context[0], target)

            iterations -= 1


    def train(self, word_input, word_target):
        input_v = self.get_encoded_vector(word_input)
        target_index = self.get_word_index(word_target)
        if(input_v is None or target_index is None):
            return

        h, y = self.forward(input_v)
        self.back_propagation(input_v, y, h, target_index)


    def predict(self, context: str):
        input_v = self.get_encoded_vector(context)
        if(input_v is None):
            return None

        _, y  = self.forward(input_v)
        max_i = 0
        for i in range(1, self.v):
            if(y[i] > y[max_i]):
                max_i = i

        return self.inv_vocabulary[max_i]


    # matrix transpose
    def transpose(self, a: 'list[list]'):
        n = len(a)
        m = len(a[0])
        result = [[0] * n for _ in range(m)]

        for i in range(n):
            for j in range(m):
                result[j][i] = a[i][j]

        return result


    # matrix multiplication
    def multiply(self, a: 'list[list]', b: 'list[list]'):
        result = []
        n = len(a)
        m = len(b[0])
        K = len(a[0])
        for i in range(n):
            result.append([])
            for j in range(m):
                result[i].append(0)
                for k in range(K):
                    result[i][-1] += a[i][k] * b[k][j]

        return result

    # sigma function simga(ui) = yi
    # yi = e^(ui) / sum (e^uj), j in [0 ... v)
    def sigma(self, u: list):
        sum_ = sum([np.exp(uj) for uj in u])
        return [np.exp(ui) / sum_ for ui in u]


    # e is the prediction error, we want to minimize e, because e
    # is the derivate of E regard u
    # ei = yi - ti
    # where ti is 1 if and only if the ith word is the expected, otherwise
    # ti is equal to zero
    # E = -log(y)
    def calculate_e(self, y, target_index):
        e = []
        for i in range(self.v):
            e.append(y[i] - (1 if i == target_index else 0))

        return e


    def forward(self, input_v: list):
        # input layer -> hidden layer
        h = self.multiply([input_v], self.w)
        # hidden layer -> output layer
        u = self.multiply(h, self.w_)
        # sigma activation function
        y = self.sigma(u[0])
        return h, y


    def back_propagation(self, input_v, y, h, target_index):
        # error prediction
        e = self.calculate_e(y, target_index)
        # next we calculate the derivate of E with regard w_
        dw_ = []
        for i in range(self.n):
            dw_.append([])
            for j in range(self.v):
                dw_ij = e[j] * h[0][i] * self.LEARNING_RATE
                dw_[i].append(dw_ij)

        # EH is the derivate of E with regard h
        # EHi = sum (ej * w'ij) j in [0 ... v]
        EH = []
        for i in range(self.n):
            EH.append(0)
            for j in range(self.v):
                EH[i] += e[j] * self.w_[i][j] * self.LEARNING_RATE

        # next we calculate the derivate of E with regard w
        dw = self.multiply(self.transpose([input_v]), [EH])


        # update w_ (weights of hidden layer to output layer)
        for i in range(self.n):
            for j in range(self.v):
                self.w_[i][j] -= dw_[i][j]

        # update w (weights of input layer to hidden layer)
        for i in range(self.v):
            for j in range(self.n):
                self.w[i][j] -= dw[i][j]


