from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score
from data_input import LoadData

# TODO: Next semester implement split, files, and test the model once training data obtained
class SVMModel():
    def __init__(self, files):
        self.files = files
        self.load_data()
        
    def load_data(self):
        # change paramters of LoadData once we figure out how to handle all data once collected
        self.dataframe = LoadData('2024-11-23_23-37-50-480147_HR.csv', '2024-11-23_23-37-50-480147_EA.csv').dataframe
        self.y = self.dataframe[['label']]
        self.X = self.dataframe.drop(['label'], axis=1)
        # NOTE: needs to be modified when more data obtained (likely going to have a dataframe for each sample)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)

    def train_model(self):
        # TODO: Once user study done (have data) test different kernels
        self.model = svm.SVC(kernel='poly')
        self.model.fit(self.X_train, self.y_train)

    def get_accuracies(self):
        self.train_model()
        train_predictions = self.model.predict(self.X_train)
        test_predictions = self.model.predict(self.X_test)

        train_accuracy = accuracy_score(self.y_train, train_predictions)
        test_accuracy = accuracy_score(self.y_test, test_predictions)
        print("Training accuracy: ", train_accuracy)
        print("Test accuracy: ", test_accuracy)