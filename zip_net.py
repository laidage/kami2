import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

params = torch.load("model/net.pth")
for key in params.keys():
    params[key] = params[key].half() # float16

torch.save(params, 'model/half_net.pth')