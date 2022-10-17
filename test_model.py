import logging
logging.basicConfig(filename='test_model.log', level=logging.INFO)
from net import Net 
import torch
import os
from game_logic2 import Env
from itertools import count
import time

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch.set_default_dtype(torch.float16)
# , map_location='cpu'
policy_net = Net().to(device)
if os.path.exists("model/half_net.pth"):
    policy_net.load_state_dict(torch.load("model/half_net.pth"))

def choose_action(state, env):
    with torch.no_grad():
        before = time.time()
        action =  policy_net(state).max(1)[1].view(1, 1)
        after = time.time()
        print(after -before)
        return action

def tran_state(state, color_nums):
        trans_state = []
        for color_index in range(5):
            if color_index >= color_nums:
                trans_state.append([[-1 for _ in range(15)] for _ in range(20)])
                continue
            types = []
            for column_index in range(20):
                column = [0 for _ in range(15)]
                if column_index % 4 == 1 or column_index % 4 == 2: 
                    column[14] = -1
                types.append(column)
            trans_state.append(types)
        for i in range(20):
            for j in range(len(state[i])):
                color = state[i][j]
                trans_state[color][i][j] = 1
        return trans_state
                

def test():
    env = Env()
    steps = []
    true_steps = []
    for i in range(1,43):
        state, _, color_nums, _ = env.load_config_file("config/" + str(i))
        state = tran_state(state, color_nums)
        state = torch.tensor(state, dtype=torch.half).unsqueeze(0)
        for t in count():
            # print(t)
            action = choose_action(state, env)
            if i == 36 and t == 0:
                print(action)
            # print(action)
            state_, _, done = env.step(action.item())
            # print(reward)
            state_ = tran_state(state_, color_nums)
            state_ = torch.tensor(state_, dtype=torch.half).unsqueeze(0)
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