# Random Forest

import pandas as pd
import numpy as np
from sklearn.metrics import classification_report,confusion_matrix,ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()


df = pd.read_csv('Nov27_Final_Dataset.csv')
#print(df.head())
#print(df.info())

"""

Best accuracy comes with 'danceability','energy','loudness','speechiness'

"""

feature_df = df[['danceability', 'energy', 'loudness','speechiness']]
popular_df = df['popular'].astype('bool')

print(feature_df.isnull().sum())

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

# Independent Variable
X = np.asarray(feature_df)

# Dependent Variable
y = np.asarray(popular_df)

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.3, random_state=100)

forest = RandomForestClassifier(n_estimators=100, random_state=100)

forest.fit(X_train,y_train)
y_predict = forest.predict(X_test)

# Cross validation
rf_cv_scores = cross_val_score(forest, X_train, y_train, cv=10, scoring='accuracy')
print ("RF 10-Fold Cross-Validation Scores:%s"%rf_cv_scores)
print ("RF 10-Fold Mean Cross-Validation Score:%3.4f"%(rf_cv_scores.mean()))
print(classification_report(y_test, y_predict))
print(f"Mean accuracy: {forest.score(X_test, y_test)}")

# Generate confusion matrix using built-in ConfusionMatrixDisplay function

cm = confusion_matrix(y_test, y_predict, normalize='true')
class_labels = ['True', 'False']
cmd = ConfusionMatrixDisplay(cm,display_labels=class_labels)

cmd.plot()
plt.title('RF Classfier Confusion Matrix')
plt.xlabel('Actual Popular Song')
plt.ylabel('Predicted Popular Song')
plt.grid(False)

plt.savefig("RF_confusion.jpg") # Save plot as image in current directory


from sklearn.metrics import roc_curve, auc

# Predict probabilities on the test set
y_prob = forest.predict_proba(X_test)[:, 1]

# Set characteristics
fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

# Interpolation
interp_fpr = np.linspace(0, 1, 100)
interp_tpr = np.interp(interp_fpr, fpr, tpr)

# Plot ROC curve
plt.figure(figsize=(8, 8))
plt.plot(interp_fpr, interp_tpr, color='darkorange', lw=2, label=f'AUC = {roc_auc:.2f}')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('SVM ROC Curve')
plt.legend(loc='lower right')
plt.show()