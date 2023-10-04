import xgboost as xgb
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

'''
split_data: 주어진 데이터를 훈련 세트와 테스트 세트로 분할한다.
train_model: 주어진 데이터로 XGBoost 모델을 훈련한다.
predict: 훈련된 모델을 사용하여 테스트 데이터에 대한 예측을 수행한다.
evaluate_accuracy: 예측 결과의 정확도를 평가한다.
save_model: 훈련된 모델을 파일로 저장한다.
load_model: 저장된 모델 파일을 로드한다.
'''

class ModelTraining:
    def __init__(self, data, features, label):
        self.data = data
        self.features = data[features]
        self.label = data[label]
        self.model = None

    def split_data(self, test_size=0.3, random_state=156):
        x_train, x_test, y_train, y_test = train_test_split(self.features, self.label, test_size=test_size, random_state=random_state)
        return x_train, x_test, y_train, y_test

    def train_model(self, x_train, y_train, params=None):
        if params is None:
            params = {
                "objective": "multi:softmax",
                "num_class": 7,
                "max_depth": 7,
                "learning_rate": 0.06,
                "n_estimators": 700,
                "eval_metric": 'mlogloss',
                "random_state": 42
            }

        self.model = xgb.XGBClassifier(**params)
        self.model.fit(x_train, y_train)
        return self.model

    def predict(self, x_test):
        if self.model:
            return self.model.predict(x_test)
        else:
            raise ValueError("Model is not trained yet!")

    def evaluate_accuracy(self, y_test, y_pred):
        return accuracy_score(y_test, y_pred)

    def save_model(self, filename):
        if self.model:
            self.model.save_model(filename)
        else:
            raise ValueError("Model is not trained yet!")

    def load_model(self, filename):
        self.model = xgb.XGBClassifier()
        self.model.load_model(filename)
