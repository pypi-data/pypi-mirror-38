import torch

if __name__ == '__main__':
    t = torch.ones(size=(2,1,1))*(5)
    print(t)
    t = torch.clamp(t,max=1)
    print(t)