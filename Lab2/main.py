import csv
import random
import math
from time import time



def sigmoid(z):
   
    if z >= 0:
        return 1.0 / (1.0 + (1.0 - z + z * z / 2.0))
    else:
        numerator = 1.0 + z + (z * z) / 2.0 + (z * z * z) / 6.0
        denominator = 1.0 + z + (z * z) / 2.0
        return numerator / denominator


def cross_entropy_loss(y_true, y_pred):
   
    m = len(y_true)
    loss = 0.0
    for i in range(m):
        y_p = max(min(y_pred[i], 1 - 1e-15), 1e-15)  
        loss += y_true[i] * math.log(y_p) + (1 - y_true[i]) * math.log(1 - y_p)
    return -loss / m



def predict_class(y_prob):
    
    return [1 if p >= 0.5 else 0 for p in y_prob]


def accuracy_score(y_true, y_pred):
    
    correct = sum([1 for yt, yp in zip(y_true, y_pred) if yt == yp])
    return correct / len(y_true)


def normalize(data):
    
    n_cols = len(data[0])
    normalized = []

    for col_idx in range(n_cols):
        column = [row[col_idx] for row in data]
        mean = sum(column) / len(column)
        std = (sum((x - mean) ** 2 for x in column) / len(column)) ** 0.5
        if std == 0:
            std = 1  
        normalized_col = [(x - mean) / std for x in column]
        for i in range(len(normalized_col)):
            if len(normalized) <= i:
                normalized.append([])
            normalized[i].append(normalized_col[i])
    return normalized


def read_csv(file_path):
    
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  
        data_rows = []
        labels = []
        for row in reader:
            try:
                features = list(map(float, row[:-1]))
                label = int(row[-1])
                data_rows.append(features)
                labels.append(label)
            except Exception as e:
                print(f"Ошибка чтения строки: {row} — {e}")
        return data_rows, labels


def split_data(X, y, test_size=0.2):
    
    split_idx = int(len(X) * (1 - test_size))
    return X[:split_idx], X[split_idx:], y[:split_idx], y[split_idx:]




class Perceptron:
    def __init__(self, n_features):
       
        self.n_features = n_features
        self.weights = [random.random() for _ in range(n_features)]
        self.bias = 0.0

    def forward(self, X):
       
        predictions = []
        for x in X:
            z = sum(w * xi for w, xi in zip(self.weights, x)) + self.bias
            a = sigmoid(z)
            predictions.append(a)
        return predictions

    def update_weights(self, X_batch, y_true, y_pred, learning_rate=0.1):
        
        m = len(y_true)
        dw = [0.0 for _ in range(self.n_features)]
        db = 0.0

        for i in range(m):
            error = y_pred[i] - y_true[i]
            for j in range(self.n_features):
                dw[j] += error * X_batch[i][j]
            db += error

        for j in range(self.n_features):
            self.weights[j] -= learning_rate * (dw[j] / m)
        self.bias -= learning_rate * (db / m)




def train_model(model, X_train, y_train, epochs=430, batch_size=100, learning_rate=0.1):
   
    m = len(X_train)
    print(f"Начало обучения. Всего эпох: {epochs}, размер батча: {batch_size}")

    start_time = time()

    for epoch in range(epochs):
        indices = list(range(m))
        random.shuffle(indices)
        X_shuffled = [X_train[i] for i in indices]
        y_shuffled = [y_train[i] for i in indices]

        for i in range(0, m, batch_size):
            X_batch = X_shuffled[i:i+batch_size]
            y_batch = y_shuffled[i:i+batch_size]

            y_pred = model.forward(X_batch)
            model.update_weights(X_batch, y_batch, y_pred, learning_rate)

        train_preds = model.forward(X_train[:10000])
        train_classes = predict_class(train_preds)
        loss = cross_entropy_loss(y_train[:10000], train_preds)
        acc = accuracy_score(y_train[:10000], train_classes)
        print(f"Эпоха {epoch+1}: Loss = {loss:.4f}, Accuracy = {acc:.4f}")

    end_time = time()
    print(f"Обучение завершено за {end_time - start_time:.2f} секунд")



if __name__ == "__main__":
    file_path = 'huge_perceptron_dataset.csv'  
    print("Загрузка данных...")
    X, y = read_csv(file_path)

    print("Нормализация признаков...")
    X = normalize(X)

    TEST_SIZE = 0.2
    X_train, X_test, y_train, y_test = split_data(X, y, TEST_SIZE)

    print("Создание модели перцептрона...")
    perceptron = Perceptron(n_features=len(X[0]))

    print("Начало обучения...")
    train_model(perceptron, X_train, y_train, epochs=430, batch_size=100, learning_rate=0.1)

    print("Оценка на тестовых данных...")
    test_preds = perceptron.forward(X_test)
    test_classes = predict_class(test_preds)
    test_acc = accuracy_score(y_test, test_classes)
    print(f"Точность на тестовой выборке: {test_acc:.4f}")

    if test_acc >= 0.85:
        print("✅ Условие выполнено: точность ≥ 85%")
    else:
        print("❌ Требуемая точность не достигнута.")