from sklearn.model_selection import train_test_split
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV

df = pd.read_csv ('Na_data.csv')
df = df[df.Desc.notnull()]
#print(df.shape)

# Split the data into training and testing sets
train_data, test_data, train_labels, test_labels = train_test_split(
    df['Desc'], df['class'], test_size=0.2, random_state=42
)
#print('Traindata ', train_data)
#print('Test data ', test_data)

# Make pipeline
model = make_pipeline(
    CountVectorizer(),
    MultinomialNB()
)
model.fit(train_data, train_labels)

# Make predictions on the test set
#predictions = model.predict(test_data)

# Evaluate the performance of the classifier
#accuracy = accuracy_score(test_labels, predictions)
#report = classification_report(test_labels, predictions)

#print(f"Accuracy: {accuracy}")
#print("Classification Report:")
#print(report)
###########################################################
print('###################################')
# Hyperparameter tuning for CountVectorizer and Multinomial Naive Bayes
param_grid= {'countvectorizer__stop_words': [None, 'english'], 'countvectorizer__lowercase': [True, False], 'multinomialnb__alpha': [0.01, 0.1, 0.5, 1.0, 2.0]}


grid_search = GridSearchCV(model, param_grid, cv=5)
grid_search.fit(train_data, train_labels)

# Get the best hyperparameters
best_params = grid_search.best_params_

# Update the model with the best hyperparameters
model.set_params(**best_params)

# Retrain the model on the full training set
model.fit(train_data, train_labels)

# Make predictions on the test set with the tuned model
predictions_tuned = model.predict(test_data)

# Evaluate the performance of the tuned classifier
accuracy_tuned = accuracy_score(test_labels, predictions_tuned)
report_tuned = classification_report(test_labels, predictions_tuned)

print("Tuned Model Results:")
print(f"Best Hyperparameters: {best_params}")
print(f"Tuned Model Accuracy: {accuracy_tuned}")
print("Tuned Model Classification Report:")
print(report_tuned)