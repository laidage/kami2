import logging
logging.basicConfig(filename='test_model.log', level=logging.INFO)
from train import Net 
import torch
import os
from game_logic import Env
from itertools import count
import time

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# , map_location='cpu'
policy_net = Net().to(device)
if os.path.exists("model/net.pth"):
    policy_net.load_state_dict(torch.load("model/net.pth"))

def choose_action(state, env):
    with torch.no_grad():
            # print(policy_net(state))
            # # print(policy_net(state).view(1500,1)[183])
            return policy_net(state).max(1)[1].view(1, 1)
        # sorted, indices = torch.sort(policy_net(state), descending=True)
        # # # print(sorted[0], indices)
        # i = 0
        # while not env.valid(indices[0][i].view(1, 1).item()):
        #     i += 1
        # return indices[0][i].view(1, 1)


def test():
    env = Env()
    steps = []
    true_steps = []
    for i in range(1,43):
        state, _ = env.load_config_file("config/" + str(i))
        state = torch.tensor(state, dtype=torch.float64).unsqueeze(0)
        for t in count():
            # print(t)
            action = choose_action(state, env)
            # print(action)
            state_, reward, done = env.step(action.item())
            # print(reward)
            
            state_ = torch.tensor(state_, dtype=torch.float64).unsqueeze(0)
            state = state_
            # if t >= 2:
            #     time.sleep(10000)
            if done:
                # print(t+1)
                logging.info("{}:{}".format(i,t+1))
                steps.append(t+1)
                break
            if t > 100:
                steps.append(100)
                break
    with open("true_steps.log") as f:
        true_steps = f.readlines()
    # print(true_steps)
    # print(steps)
    wrong_steps = 0
    wrong_count = 0
    for i in range(0, 42):
        if steps[i] != int(true_steps[i]):
            wrong_steps += 1
            wrong_count += steps[i] - int(true_steps[i])
            print(i+1, steps[i], true_steps[i])
    print(wrong_steps)
    print(wrong_count)

if __name__ == "__main__":
    test()