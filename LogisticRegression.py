# Rodrigo Luís Zimmermann
import numpy as np # linear algebra
import pandas as pd # data processing

dt = pd.read_csv("mushrooms.csv")
print(dt.shape)
dt.head()

ttype= {"p":0,"e":1}          
dt["class"] = [ttype[item] for item in dt["class"]]

dt_1 = pd.get_dummies(dt)
print(dt_1.shape)
dt_1.head()

"""Treinamento"""

X,y=dt_1.drop(["class"],axis=1),dt_1["class"]
from sklearn.model_selection import train_test_split
X_tr,X_ts,y_tr,y_ts= train_test_split(X, y, test_size=0.33, random_state=42)

class logistic_regression:
    
    # initialize variables
    def __init__(self):
        
        self.classes = None
        self.theta=[]
        self.lmd = 0
        
        # learning rate
        self.alpha = 0.1
        
        # number of iterations
        self.num_iter = 5000
        
    # Sigmoid Function 
    def sigmoid(self,z):
        return 1 / (1 + np.exp(-z))
  
    # Cost Function
    def cost(self, h, y):
        return (-y * np.log(h) - (1 - y) * np.log(1 - h)).mean()
  
    # Gradient Descent Function
    def gradientdescent(self, X, y):
        # select initial values zero
        theta = np.zeros(X.shape[1])
        
        # save costs
        costs = [] 
        
        # train model for n-iterations
        for i in range(self.num_iter):
            
            # compute y-hat
            z = np.dot(X, theta)
            
            # sigmoid 
            h = self.sigmoid(z)
            
            # get cost
            cost = self.cost(h, y)
            
        gradient = np.dot(X.T, (h - y)) / y.size 
        # upgrade the theta
        theta = theta - self.alpha * gradient    
        return theta , costs


    def predict(self, X_test):
        
        # add in intercept
        intercept = np.ones((X_test.shape[0], 1))
        X_test = np.concatenate((intercept, X_test), axis=1)
        
        # save predictions
        pred_test = np.zeros((len(self.classes),len(X_test)))
        
        # run predictions for each model
        for i in range(len(self.classes)):
            pred_test[i,:] = self.sigmoid(np.dot(X_test,self.theta[i])) 
        
        # Select max probability
        prediction_test = np.argmax(pred_test, axis=0)
        return prediction_test
    
    def train(self,X_train, y_train):
        # Adding intercept
        intercept = np.ones((X_train.shape[0], 1))
        X_train = np.concatenate((intercept, X_train), axis=1)
        
        # one vs rest
        self.classes=set(y_train)
        self.t=[]
        
        # train model for each class
        for clss in self.classes:
            
            # set the labels to 0 and 1
            ynew = np.array(y_train == clss, dtype = int)
            
            # compute gradient
            theta_onevsrest,costs_onevsrest=self.gradientdescent(X_train, ynew)
            
            # save weight
            self.theta.append(theta_onevsrest)

    
ob = logistic_regression()
ob.train(X_tr,y_tr)
y_pred = ob.predict(X_ts)

"""Relatório de classificação"""

from sklearn.metrics import classification_report,confusion_matrix
print(classification_report(y_ts, y_pred))

"""Matrix de confusão"""

import matplotlib.pyplot as plt
import itertools

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title, weight='bold', fontsize=16)
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, fontsize=14)
    plt.yticks(tick_marks, classes, fontsize=14)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center", fontsize=12, weight='bold',
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label', fontsize=16, weight='bold')
    plt.xlabel('Predicted label', fontsize=16, weight='bold')

"""Resultado final com a matriz de confusão"""

# Compute confusion matrix
cnf_matrix = confusion_matrix(y_ts, y_pred)
np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
plt.figure(figsize=(10, 10))
plot_confusion_matrix(cnf_matrix, classes=list(ob.classes),normalize=True,
                      title='Normalized Confusion Matrix')
plt.show()

"""Random Forest"""

from sklearn.model_selection import train_test_split

mushrooms_df = pd.read_csv("mushrooms.csv")
mushrooms_df.columns

X_train, X_test, y_train, y_test = train_test_split(mushrooms_df.drop("class", axis=1), mushrooms_df["class"])
X_train.head(3)

"""Treino"""

def transform_labels_to_01(labels, pos_lab):
    return [1 if y == pos_lab else 0 for y in labels]

y_train_01 = transform_labels_to_01(y_train, 'e')
y_test_01 = transform_labels_to_01(y_test, 'e')

"""Selecionando o modelo"""

from sklearn.preprocessing import OneHotEncoder

one_hot = OneHotEncoder()
X_train_tr = one_hot.fit_transform(X_train)

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

rnd_clf = RandomForestClassifier()
params = {
    "n_estimators": [40, 100],
    "max_leaf_nodes": [20, 30]
}

grid_cv = GridSearchCV(rnd_clf, params, verbose=3, cv=3, scoring="f1")
grid_cv.fit(X_train_tr, y_train_01)

"""Validação utilizando o teste do dataset"""

best_clf = grid_cv.best_estimator_
from sklearn.pipeline import Pipeline

full_pipeline = Pipeline([
    ("one_hot", one_hot),
    ("clf", best_clf)
])

from sklearn.metrics import f1_score

y_pred = full_pipeline.predict(X_test)
f1_score(y_test_01, y_pred)

from sklearn.metrics import classification_report,confusion_matrix
print(classification_report(y_test_01, y_pred))