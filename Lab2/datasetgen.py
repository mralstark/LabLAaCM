import random
import csv
import time

num_samples = 1_000_000
num_features = 30
output_file = "huge_perceptron_dataset.csv"

weights = [0.3, 0.2, -0.5, 0.7] + [0.0] * (num_features - 4)

def generate_sample():
    
    features = [random.random() for _ in range(num_features)]
    
    logit = sum(w * x for w, x in zip(weights, features)) + random.gauss(0, 0.1)
    
    y = 1 if logit > 0.5 else 0
    
    return features, y

start_time = time.time()

with open(output_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    
    header = [f"x{i}" for i in range(num_features)] + ["y"]
    writer.writerow(header)
    
    for i in range(num_samples):
        if i % 10000 == 0:
            print(f"Сгенерировано {i} строк...")
        
        features, y = generate_sample()
        writer.writerow(features + [y])

end_time = time.time()
print(f"Файл '{output_file}' успешно сохранён.")
print(f"Время выполнения: {end_time - start_time:.2f} секунд")