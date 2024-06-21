#參考111010515林弘杰同學並理解後所完成
class Value:
   #儲存單一標量值及其梯度 
    def __init__(self, data, _children=(), _op=''):
        self.data = data
        self.grad = 0
        # 用於自動微分圖構建的內部變數
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op # 產生此節點的操作，用於graphviz/除錯等

    def __add__(self, other): # f=x+y
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')

        def _backward():
            self.grad += out.grad  # gx = gf
            other.grad += out.grad # gy = gf
        out._backward = _backward

        return out

    def __mul__(self, other): # f=x*y
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')

        def _backward():
            self.grad += other.data * out.grad # gx = y*gf  gx/gf = y
            other.grad += self.data * out.grad # gy = x*gf
        out._backward = _backward

        return out

    def __pow__(self, other): # f = x**n
        assert isinstance(other, (int, float)), "目前僅支援 int/float 的冪次"
        out = Value(self.data**other, (self,), f'**{other}')

        def _backward():
            self.grad += (other * self.data**(other-1)) * out.grad # gx = n (x**n-1)
        out._backward = _backward

        return out

    def relu(self):
        out = Value(0 if self.data < 0 else self.data, (self,), 'ReLU')

        def _backward():
            self.grad += (out.data > 0) * out.grad # gx = 1 if f>0 else 0
        out._backward = _backward

        return out

    def backward(self):

        # 對圖中的所有子節點進行拓撲排序
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)

        # 一次處理一個變量，並應用鏈式法則計算其梯度
        self.grad = 1
        for v in reversed(topo):
            v._backward()

    def __neg__(self): # -self
        return self * -1

    def __radd__(self, other): # other + self
        return self + other

    def __sub__(self, other): # self - other
        return self + (-other)

    def __rsub__(self, other): # other - self
        return other + (-self)

    def __rmul__(self, other): # other * self
        return self * other

    def __truediv__(self, other): # self / other
        return self * other**-1

    def __rtruediv__(self, other): # other / self
        return other * self**-1

    def __repr__(self): # 轉字串 -- https://www.educative.io/edpresso/what-is-the-repr-method-in-python
        return f"Value(data={self.data}, grad={self.grad})"