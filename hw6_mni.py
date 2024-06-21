# 參考 111010515林弘杰同學
# 參考 https://github.com/ccc112b/py2gpt/blob/master/03b-MacroGrad/macrograd/engine.py
# 參考 https://github.com/newcodevelop/micrograd/blob/master/mnist.ipynb
import numpy as np
import math

class Tensor:

    def __init__(self, data, _children=(), _op=''):

        self.data = np.array(data)
        self.grad = np.zeros_like(self.data)
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op

    def matmul(self, other):

        out = Tensor(np.dot(self.data, other.data), (self, other), 'matmul')

        def _backward():

            self.grad += np.dot(out.grad, other.data.T)
            other.grad += np.dot(self.data.T, out.grad)

        out._backward = _backward

        return out

    def softmax(self):

        exps = np.exp(self.data - np.max(self.data, axis=1, keepdims=True))
        out_data = exps / np.sum(exps, axis=1, keepdims=True)
        out = Tensor(out_data, (self,), 'softmax')


        def _backward():

            for i, (o_grad, o_data) in enumerate(zip(out.grad, out.data)):

                jacobian_m = np.diag(o_data) - np.outer(o_data, o_data)
                self.grad[i] += np.dot(jacobian_m, o_grad)
        out._backward = _backward

        return out

    def cross_entropy(self, target):

        n = self.data.shape[0]
        clipped_probs = np.clip(self.data, 1e-12, 1 - 1e-12)
        out_data = -np.sum(target.data * np.log(clipped_probs)) / n
        out = Tensor(out_data, (self, target), 'cross_entropy')

        def _backward():
            self.grad += -target.data / clipped_probs / n
        out._backward = _backward

        return out

    def backward(self):

        topo = []
        visited = set()

        def build_topo(v):

            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)

        build_topo(self)

        self.grad = np.ones_like(self.data)

        for v in reversed(topo):
            v._backward()

    def __repr__(self):
        return f"Tensor(data={self.data}, grad={self.grad})"


# Utility function to one-hot encode labels
def one_hot(labels, num_classes):
    return np.eye(num_classes)[labels]

# Load and preprocess MNIST dataset
from keras.datasets import mnist
import keras

(x_train, y_train), (x_test, y_test) = mnist.load_data()
train_images = np.asarray(x_train, dtype=np.float32) / 255.0
test_images = np.asarray(x_test, dtype=np.float32) / 255.0
train_images = train_images.reshape(60000, 784)
test_images = test_images.reshape(10000, 784)
y_train = one_hot(y_train, 10)

# Forward function
def forward(X, Y, W):
    y_predW = X.matmul(W)
    probs = y_predW.softmax()
    loss = probs.cross_entropy(Y)
    return loss

# Training parameters
batch_size = 32
steps = 20000

X = Tensor(train_images)
Y = Tensor(y_train)
Wb = Tensor(np.random.randn(784, 10))

# Training loop
for step in range(steps):
    ri = np.random.permutation(train_images.shape[0])[:batch_size]
    Xb, yb = Tensor(train_images[ri]), Tensor(y_train[ri])
    lossb = forward(Xb, yb, Wb)
    lossb.backward()
    if step % 1000 == 0 or step == steps - 1:
        loss = forward(X, Y, Wb).data / X.data.shape[0]
        print(f'loss in step {step} is {loss}')
    Wb.data = Wb.data - 0.01 * Wb.grad
    Wb.grad = np.zeros_like(Wb.grad)
