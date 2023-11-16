import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score,f1_score
import joblib
class DataPreprocessor():
    
    def __init__(self, path):
        self.df = pd.read_csv(path)

    def preprocess(self):
        # Convert label(state) into 0,1
        labels = {"successful":1, "failed":0}
        self.df["state"] = self.df["state"].map(labels)

        # Drop unnecesary columns    
        df = self.df.drop('Unnamed: 0',axis=1)

        return df
class Model:
    def __init__(self,df: pd.DataFrame, model):
        self.model = model
        self.df = df
        # Split the dataframe into Features and Labels

        self.X = self.df.drop('state',axis=1) # Features
        self.y = self.df['state'] # Labels

        # Split the data into training and testing sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=15)

    def pipeline(self):
        # Create a pipeline
        cols = ["country","parent_category","sub_category"]
        ohe = OneHotEncoder(handle_unknown = "ignore")
        ohe.fit(self.X[cols])

        column_trans = make_column_transformer((OneHotEncoder(categories=ohe.categories_),
                                                cols),
                                                remainder='passthrough')

        pipe = make_pipeline(column_trans, self.model)
        pipe.fit(self.X_train, self.y_train)
        return pipe
    
    def dump(self):
        joblib.dump(self.pipeline(), open("models/success_pred_model.pkl", "wb"))

    def evaulate(self):
        y_pred = self.pipeline().predict(self.X_test)
        print("Accuracy:",accuracy_score(self.y_test,y_pred))
        print("F1_score:",f1_score(self.y_test,y_pred))

if __name__ == "__main__":
    preprocessor = DataPreprocessor("data/data.csv")
    df = preprocessor.preprocess()
    knn = KNeighborsClassifier()
    model = Model(df, knn)
    model.dump()
    model.evaulate()