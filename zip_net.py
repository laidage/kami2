from train import Net 
import torch
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# , map_location='cpu'
# policy_net = Net().to(device)
# if os.path.exists("model/net.pth"):
#     policy_net.load_state_dict(torch.load("model/net.pth"))

# for param in policy_net.parameters():
#     param[key] = param[key].half()

params = torch.load("model/net.pth")
for key in params.keys():
    params[key] = params[key].half() # float16

torch.save(params, 'model/half_net.pth')