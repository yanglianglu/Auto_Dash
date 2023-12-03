from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import pandas as pd
import utils.database_utils as db
import sys
import os

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


class LogisticRegressionModel:
    def __init__(self):

        df = pd.read_csv(os.path.join(
            os.path.dirname(__file__), "./sentiment-training-data.csv"), delimiter=",", encoding="latin-1")
        df = df.rename(
            columns={
                "neutral": "Sentiment",
                "According to Gran , the company has no plans to move all production to Russia , although that is where the company is growing .": "Sentence",
            }
        )

        train_df, test_df = train_test_split(
            df, test_size=0.2, random_state=123)
        X_train = train_df["Sentence"]
        X_test = test_df["Sentence"]
        y_train = train_df["Sentiment"]
        y_test = test_df["Sentiment"]

        pipeline = Pipeline(
            [
                ("tfidf_vect", TfidfVectorizer(stop_words="english")),
                ("lr_clf", LogisticRegression(solver="liblinear")),
            ]
        )

        params = {
            "tfidf_vect__ngram_range": [(1, 1), (1, 2), (1, 3)],
            "tfidf_vect__max_df": [0.5, 0.75, 1.0],
            "lr_clf__C": [1, 5, 10],
        }

        grid_cv_pipe = GridSearchCV(
            pipeline, param_grid=params, cv=3, scoring="accuracy", verbose=1
        )
        grid_cv_pipe.fit(X_train, y_train)
        print("Optimized Hyperparameters: ", grid_cv_pipe.best_params_)

        self.model = grid_cv_pipe

    # # Accuracy
    # pred = grid_cv_pipe.predict(X_test)
    # print("Optimized Accuracy Score: {0: .3f}".format(accuracy_score(y_test, pred)))

    def predict(self, x):
        return self.model.predict(x)


# Example Usage
if __name__ == "__main__":

    # Get documents from elasticsearch
    client = db.create_client()
    res = db.search_documents(client, "documents", {"match_all": {}})
    docs = res["hits"]["hits"]

    # Map documents into headlines
    titles = [doc["_source"]["title"] for doc in docs]

    # Format test data
    x = pd.DataFrame(titles, columns=["Text"])

    # Perform prediction
    model = LogisticRegressionModel()
    print(x["Text"])
    print(model.predict(x["Text"]))
