from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay

class SVMModel():
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.load_data()
        
    def load_data(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.3, random_state=42)
        self.X_val, self.X_test, self.y_val, self.y_test = train_test_split(self.X_test, self.y_test, test_size=0.5, random_state=42)

    def train_model(self):
        self.model = svm.SVC(kernel='rbf')
        self.model.fit(self.X_train, self.y_train)

    def get_accuracies(self):
        self.train_model()
        train_predictions = self.model.predict(self.X_train)
        val_predictions = self.model.predict(self.X_val)
        self.test_predictions = self.model.predict(self.X_test)

        train_accuracy = accuracy_score(self.y_train, train_predictions)
        val_accuracy = accuracy_score(self.y_val, val_predictions)
        test_accuracy = accuracy_score(self.y_test, self.test_predictions)
        print("Training accuracy: ", train_accuracy)
        print("Validation accuracy: ", val_accuracy)
        print("Test accuracy: ", test_accuracy)

    def model_report(self):
        print("Random Forest Model Report:\n", classification_report(self.y_test, self.test_predictions))

    def plot_cm(self):
        rf_cm = confusion_matrix(self.y_test, self.test_predictions)
        ConfusionMatrixDisplay(rf_cm).plot()