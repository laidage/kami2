import time
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import random
from collections import deque, namedtuple
from game_logic import Env
from itertools import count
import os
import logging
from torch.optim.lr_scheduler import MultiStepLR
logging.basicConfig(filename='logger.log', level=logging.INFO)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch.set_default_dtype(torch.float64)
Transition = namedtuple("Transition", ['state', 'action', 'reward', 'next_state', 'done'])


BATCH_SIZE = 128
GAMMA = 0.9
EPS = 0.9
STEPS_DONE = 0
TARGET_UPDATE = 10
COLORS = 5

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(5, 32, kernel_size=5, stride=1, dtype=torch.float64)
        self.bn1 = nn.BatchNorm2d(32, dtype=torch.float64)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=5, stride=1, dtype=torch.float64)
        self.bn2 = nn.BatchNorm2d(64, dtype=torch.float64)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=5, stride=1, dtype=torch.float64)
        self.bn3 = nn.BatchNorm2d(128, dtype=torch.float64)
        self.conv4 = nn.Conv2d(128, 512, kernel_size=3, stride=1, dtype=torch.float64)
        self.bn4 = nn.BatchNorm2d(512, dtype=torch.float64)
        # self.conv5 = nn.Conv2d(512, 1024, kernel_size=1, stride=1, dtype=torch.float64)
        # self.bn5 = nn.BatchNorm2d(1024, dtype=torch.float64)

        w, h = 10, 30
        def conv2d_size_out(size, kernel_size = 5, stride = 2):
            return (size - (kernel_size - 1) - 1) // stride  + 1
        convw = conv2d_size_out(conv2d_size_out(conv2d_size_out(w)))
        convh = conv2d_size_out(conv2d_size_out(conv2d_size_out(h)))
        # linear_input_size = convw * convh * 32
        # self.head = nn.Linear(linear_input_size, 300 * 5)
        self.head = nn.Linear(3072, 290 * 4, dtype=torch.float64)

    def forward(self, x):
        x = x.to(device)
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        x = F.relu(self.bn4(self.conv4(x)))
        # x = F.relu(self.bn5(self.conv5(x)))
        return self.head(x.view(x.size(0), -1))

def choose_action(state, env):
    # global EPS, STEPS_DONE
    rand = random.random()
     
    # if STEPS_DONE <= 490000:
    #     STEPS_DONE += 1
    # print(EPS)
    if rand <= EPS:
        # return policy_net(state).max(1)[1].view(1, 1)
        with torch.no_grad():
            return policy_net(state).max(1)[1].view(1, 1)
            # _, indices = torch.sort(policy_net(state), descending=True)
            # # # print(sorted[0], indices)
            # i = 0
            # while not env.valid(indices[0][i].view(1, 1).item()):
            #     i += 1
            # return indices[0][i].view(1, 1)
    else:
        return  torch.tensor([[random.randrange(290 * (COLORS - 1))]], device=device, dtype=torch.long)
        # print("random")
        # action =  torch.tensor([[random.randrange(300 * COLORS)]], device=device, dtype=torch.long)
        # while not env.valid(action.item()):
        #     action =  torch.tensor([[random.randrange(300 * COLORS)]], device=device, dtype=torch.long)
        # return action
    # if rand <= EPS:
    #     # return policy_net(state).max(1)[1].view(1, 1)
    #     with torch.no_grad():
    #         sorted, indices = torch.sort(policy_net(state), descending=True)
    #         # print(sorted[0], indices)
    #         i = 0
    #         while not env.valid(indices[0][i].view(1, 1).item()):
    #             i += 1
    #         return indices[0][i].view(1, 1)

    # else:
    #     action =  torch.tensor([[random.randrange(300 * COLORS)]], device=device, dtype=torch.long)
    #     while not env.valid(action.item()):
    #         action =  torch.tensor([[random.randrange(300 * COLORS)]], device=device, dtype=torch.long)
    #     return action


class ReplayMemory():
    # memory = deque()

    def __init__(self, capacity=20000):
        self.memory = deque([], capacity)
    
    def push(self, *args):
        self.memory.append(Transition(*args))

    def __len__(self):
        return len(self.memory)
    
    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)
        # result = []
        # for i in range(batch_size):
        #     item = random.choice(self.memory)
        #     result.append(item)
        # return torch.tensor(result)


policy_net = Net().to(device)
target_net = Net().to(device)
if os.path.exists("model/net.pth"):
    policy_net.load_state_dict(torch.load("model/net.pth"))
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()
optimizer = optim.Adam(policy_net.parameters(), lr=0.0001)
# scheduler = MultiStepLR(optimizer=optimizer, milestones=[4000, 40000, 80000, 300000], gamma=0.1)
replayMemory = ReplayMemory()

def optimize_model():
    if len(replayMemory) < BATCH_SIZE:
        return
    batch = replayMemory.sample(BATCH_SIZE)
    batch = Transition(*zip(*batch))
    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)
    next_state_batch = torch.cat(batch.next_state)
    dones = torch.cat(batch.done)
    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                          batch.next_state)), device=device, dtype=torch.bool)
                                        
    # final_mask = torch.tensor(tuple(map(lambda s: s is None,
    #                                       batch.next_state)), device=device, dtype=torch.bool)

    # final_state = torch.tensor([batch.state[index] for index, s in enumerate(batch.next_state)
    #                                             if s is None])
    # invalid_mask = torch.tensor(tuple(map(lambda s: s == False,
    #                                        batch.valid)), device=device, dtype=torch.bool)
    non_final_next_states = torch.cat([s for s in batch.next_state
                                                if s is not None])
    next_state_values = torch.zeros(BATCH_SIZE, device=device)
    # next_state_values = policy_net(state_batch).gather(1, action_batch).detach()
    state_action_values = policy_net(state_batch).gather(1, action_batch)
    # state_action_values[invalid_mask] = torch.tensor([ -999999.0 for item in batch.valid if not item]).unsqueeze(1)
    # next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0].detach()
    # next_state_values[final_mask]= state_action_values.squeeze(1)[final_mask]
    # next_state_batch = torch.cat(batch.next_state)
    # next_state_values = target_net(next_state_batch).max(1)[0].detach()
    
    # q_next = torch.zeros(BATCH_SIZE, device=device)
    q_next = target_net(next_state_batch).detach()
    q_next_eval = policy_net(next_state_batch).detach()
    q_a = q_next_eval.argmax(dim=1)
    q_a = torch.reshape(q_a,(-1,1))
    # q_a = q_next_eval.max(1)[1]
    # q_a= q_next_eval.max(1)[1].view(128, -1)
    
    expected_state_action_values =  GAMMA * q_next.gather(1, q_a) * (1 - dones).unsqueeze(1) + reward_batch.unsqueeze(1)
    # logging.info(next_state_values)
    # logging.info(reward_batch)
    # print(reward_batch.shape)
    

    # expected_state_action_values = GAMMA * next_state_values + reward_batch
    # expected_state_action_values[final_mask]= state_action_values.squeeze(1)[final_mask]
    loss_func = nn.SmoothL1Loss()
    # loss_func = nn.MSELoss()
    loss = loss_func(state_action_values, expected_state_action_values)
    logging.info(loss)

    optimizer.zero_grad()
    loss.backward()
    for param in policy_net.parameters():
        param.grad.data.clamp_(-1, 1)
    optimizer.step()
    # scheduler.step()


def train():
    episode = 200001
    # replayMemory = ReplayMemory()
    env = Env()
    global COLORS, STEPS_DONE, EPS
    for i in range(1, episode):
        # if STEPS_DONE <= 2490:
        #      EPS +=  0.0002
        if STEPS_DONE < 1000:
            EPS += 0.00009
        k = random.randint(1, 42)
        file_path = "config/"+ str(k)
        state, COLORS = env.load_config_file(file_path)
        # state, COLORS = env.load_config_file(file_path)
        # state, COLORS = env.random()
        state = torch.tensor(state, dtype=torch.float64).unsqueeze(0)
        # next_screen, _ = env.load_config_file(file_path)
        # state, COLORS = env.random()
        # state = torch.zeros(())
        # next_screen = torch.tensor(next_screen, dtype=torch.float64).unsqueeze(0)
        # current_screen = torch.tensor(current_screen, dtype=torch.float64).unsqueeze(0)
        # state =  current_screen
        
        # print(state)
        for t in count():
            logging.info("i: {} t: {}".format(i, t))
            action = choose_action(state, env)
            # print("action:", action.item())
            state_, reward, done = env.step(action.item())
            state_ = torch.tensor(state_, dtype=torch.float64).unsqueeze(0)
            done_int = 0
            # if done: 
            #     reward = 150
            if done:
                done_int = 1
            reward = torch.tensor([reward], dtype=torch.float64, device=device)
            done_int = torch.tensor([done_int], dtype=torch.int, device=device)
            replayMemory.push(state, action, reward, state_, done_int)
            
            state = state_
            optimize_model()
            if done:
                break
            # time.sleep(1)
        if i % 10 == 0:
            target_net.load_state_dict(policy_net.state_dict())
        if i % 100 == 0:
            torch.save(policy_net.state_dict(), "model/net.pth")
        # if i % 1000 == 0:
        #     print(optimizer.param_groups[0]['lr'])

if __name__ == "__main__":
    train()