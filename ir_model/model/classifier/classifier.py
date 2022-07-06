from sklearn import naive_bayes, model_selection
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

class Classifier:
    def __init__(self, docs_list):
        df = pd.DataFrame()
        df['text_tokenized'] = [" ".join(doc.terms) for doc in docs_list]
        df['label'] = [doc.label for doc in docs_list]

        Train_X, _, Train_Y, _ = \
            model_selection.train_test_split(df['text_tokenized'], df['label'], test_size=0.3)

        self.Encoder = LabelEncoder()
        Train_Y = self.Encoder.fit_transform(Train_Y)

        self.vec_tfidf = TfidfVectorizer()
        self.vec_tfidf.fit(Train_X)

        Train_X_Tfidf = self.vec_tfidf.transform(Train_X)

        self.Naive = naive_bayes.MultinomialNB()
        self.Naive.fit(Train_X_Tfidf,Train_Y)


        # Classifier - Algorithm - SVM
        # fit the training dataset on the classifier
        # start_time = time.time()
        # SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
        # SVM.fit(Train_X_Tfidf,Train_Y)
        # predict the labels on validation dataset
        # predictions_SVM = SVM.predict(Test_X_Tfidf)
        # Use accuracy_score function to get the accuracy
        # print("SVM Accuracy Score -> ",accuracy_score(predictions_SVM, Test_Y)*100)
        # print(time.time() - start_time)
        # start_time = time.time()
        # predictions_SVM = SVM.predict(Train_X_Tfidf)
        # print("SVM Accuracy Score -> ",accuracy_score(predictions_SVM, Train_Y)*100)
        # print(time.time() - start_time)

    def predict(self, doc):
        tfidf_doc_terms = self.vec_tfidf.transform([" ".join(doc.terms)])
        result = self.Naive.predict(tfidf_doc_terms)
        return self.Encoder.inverse_transform(result)[0]


