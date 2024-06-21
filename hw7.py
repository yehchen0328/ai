# 參考111010515林弘杰同學
# 參考https://github.com/ccc112b/py2cs/tree/master/03-%E4%BA%BA%E5%B7%A5%E6%99%BA%E6%85%A7/05-%E7%A5%9E%E7%B6%93%E7%B6%B2%E8%B7%AF/02-%E6%B7%B1%E5%BA%A6%E5%AD%B8%E7%BF%92/01-MNIST
import torch
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def init(self):
        super(Net, self).init()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=6, kernel_size=5, padding=2, stride=1)
        self.conv2 = nn.Conv2d(in_channels=6, out_channels=16, kernel_size=5)

        self.fc1 = nn.Linear(in_features=1655, out_features=120)
        self.fc2 = nn.Linear(in_features=120, out_features=84)
        self.fc3 = nn.Linear(in_features=84, out_features=10)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, kernel_size=2, stride=2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, kernel_size=2, stride=2)
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x