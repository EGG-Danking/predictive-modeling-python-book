# -*- coding: utf-8 -*-
"""Penguins Classifier (Multiclass) - SOLUTIONS

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mNFyi-0YVpwwWF7jRptEug4s7mW67I9z

In this example, we will predict a penguin's species, given other identifying characteristics such as the penguin's mass and length, as well as which island the penguin lives on.

## Data Loading and Cleaning

https://github.com/mcnakhaee/palmerpenguins
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install palmerpenguins

from palmerpenguins import load_penguins

df = load_penguins()
df.rename(columns={"sex": "gender"}, inplace=True)
df["species"] = df["species"].str.upper()
df["island"] = df["island"].str.upper()
df["gender"] = df["gender"].str.upper()
df.head()

df["island"].value_counts()

df["year"].value_counts()

"""### Drop Nulls"""

df.info()

df.dropna(inplace=True)
df.info()

"""## Data Exploration"""

df.head()

df["species"].value_counts() # imbalanced ish hmm... we will do a benchmark round first, then we will consider different sampling methods

df["island"].value_counts()

"""### Relationships"""

import plotly.express as px

px.scatter(df, x="body_mass_g", y="island", color="species")

"""### Pairplots"""

from seaborn import pairplot

pairplot(df, hue="species")

"""### Correlation"""

#import plotly.express as px

def plot_correlation_matrix(df, method="pearson", height=450):
    """Params: method (str): "spearman" or "pearson". """

    cor_mat = df.corr(method=method, numeric_only=True)

    title= f"{method.title()} Correlation"

    fig = px.imshow(cor_mat,
                    height=height, # title=title,
                    text_auto= ".2f", # round to two decimal places
                    color_continuous_scale="Blues",
                    color_continuous_midpoint=0,
                    labels={"x": "Variable", "y": "Variable"},
    )
    # center title (h/t: https://stackoverflow.com/questions/64571789/)
    fig.update_layout(title={'text': title, 'x':0.485, 'xanchor': 'center'})
    fig.show()

# df.drop(columns=["Hour", "Minute"])
plot_correlation_matrix(df, method="spearman", height=450)

"""## X/Y Split"""

df.head()

target = "species"

x = df.drop(columns=[target, "year"])
y = df[target]

x.head()

"""## Data Encoding"""

one_hot_encode(x, columns=["island", "gender"], dtype=int)

from pandas import get_dummies as one_hot_encode

x = one_hot_encode(x, columns=["island", "gender"], dtype=int)
x

"""## Feature Scaling"""

x_scaled = (x - x.mean(axis=0)) / x.std(axis=0)
x_scaled.head()

x_scaled.mean(axis=0) # mean of all scaled columns should be around zero
x_scaled.std(axis=0) # std of all scaled columns should be around one

"""## Train Test Split"""

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.2, random_state=99)

print("TRAIN:", x_train.shape, y_train.shape)
print("TEST:", x_test.shape, y_test.shape)

"""## Model Training (Logistic Regression)"""

from sklearn.linear_model import LogisticRegression

model = LogisticRegression(random_state=99, C=1)

model.fit(x_train, y_train)

model.get_params()

model.classes_

model.coef_.shape

model.feature_names_in_

from pandas import Series, DataFrame

coef = DataFrame(model.coef_, columns=x_scaled.columns, index=model.classes_).T
coef

coef["ADELIE"].sort_values(ascending=False)

coef["CHINSTRAP"].sort_values(ascending=False)

coef["GENTOO"].sort_values(ascending=False)

"""## Evaluation"""

from sklearn.metrics import classification_report

y_pred = model.predict(x_test)
print(classification_report(y_test, y_pred))

"""### Confusion Matrix"""

from sklearn.metrics import confusion_matrix

print(confusion_matrix(y_test, y_pred, labels=model.classes_))

from sklearn.metrics import confusion_matrix
import plotly.express as px

def plot_confusion_matrix(y_true, y_pred, height=450, showscale=False, title=None, subtitle=None):
    # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
    # Confusion matrix whose i-th row and j-th column
    # ... indicates the number of samples with
    # ... true label being i-th class (ROW)
    # ... and predicted label being j-th class (COLUMN)
    cm = confusion_matrix(y_true, y_pred)

    class_names = sorted(y_test.unique().tolist())

    cm = confusion_matrix(y_test, y_pred, labels=class_names)

    title = title or "Confusion Matrix"
    if subtitle:
        title += f"<br><sup>{subtitle}</sup>"

    fig = px.imshow(cm, x=class_names, y=class_names, height=height,
                    labels={"x": "Predicted", "y": "Actual"},
                    color_continuous_scale="Blues", text_auto=True,
    )
    fig.update_layout(title={'text': title, 'x':0.485, 'xanchor': 'center'})
    fig.update_coloraxes(showscale=showscale)

    fig.show()


subtitle = f"Penguin Classification Model: {model.__class__.__name__}"
plot_confusion_matrix(y_test, y_pred, subtitle=subtitle, height=450)

"""### ROC-AUC"""

y_pred_proba = model.predict_proba(x_test)
print(y_pred_proba.shape)

from sklearn.metrics import roc_auc_score

def compute_roc_auc_score(y_test, y_pred_proba, is_multiclass=True):
    """NOTE: roc_auc_score uses average='macro' by default"""

    if is_multiclass:
        return roc_auc_score(y_true=y_test, y_score=y_pred_proba, multi_class="ovr")
    else:
        y_pred_proba_pos = y_pred_proba[:,1] # positive class (for binary classification)
        return roc_auc_score(y_true=y_test, y_score=y_pred_proba_pos)



compute_roc_auc_score(y_test, y_pred_proba)