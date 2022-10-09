from train import Net 
import torch
import os
from game_logic import Env
from itertools import count

def test_none():
    net = Net()
    none = net(None)
    print(none)

if __name__ == "__main__":
    test_none()