# ultimate
A very simpe neural network implemention for python

## Installation
pip install ultimate

## Why Ultimate?
+ Super tiny and super easy
+ Support feature importance
+ Support missing values
+ Support am2/a2m2/am2l/a2m2l activation functions
+ Support hardmse/hardmax loss functions

## How To Use?
<pre>
# let's use a simple example to learn how to use
from ultimate.mlp import MLP
import numpy as np

# generate sample
X = np.linspace(-np.pi, np.pi, num=5000).reshape(-1, 1)
Y = np.sin(X)
print(X.shape, Y.shape)

# train and predict
mlp = MLP(layer_size=[X.shape[1], 8, 8, 8, 1], loss_type="mse")
mlp.train(X, Y, epoch_train=100, epoch_decay=10, verbose=1)
pred = mlp.predict(X)

# show the result
import matplotlib.pyplot as plt  
plt.plot(X, pred)
plt.show()
</pre>

## Examples
+ [Feature Importance](https://www.kaggle.com/anycode/feature-importance-using-nn)
+ [Image Regression](https://www.kaggle.com/anycode/image-regression)
+ [Iris Classification](https://www.kaggle.com/anycode/image-regression)
+ [MNIST Recognition](https://www.kaggle.com/anycode/mnist-recognition)