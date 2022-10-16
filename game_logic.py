import random
from collections import deque


from torch import randint

class Env:
    def __init__(self):
        self.colors = 5
        self.rest_of_colors = []
        self.state = []

    def tran_state(self):
        state = []
        for color_index in range(5):
            if color_index >= self.colors:
                state.append([[-1 for _ in range(15)] for _ in range(20)])
                continue
            types = []
            for column_index in range(20):
                column = [0 for _ in range(15)]
                if column_index % 4 == 1 or column_index % 4 == 2: 
                    column[14] = -1
                types.append(column)
            state.append(types)
        for i in range(20):
            for j in range(len(self.state[i])):
                color = self.state[i][j]
                state[color][i][j] = 1
        # for i in range(20):
        #     column = []
        #     for j in range(len(self.state[i])):
        #         column.append(self.state[i][j])
        #     if i % 2 == 1:
        #         column.append(-1) 
        #     state.append(column)
        return state

    def random(self):
        self.colors = random.randint(2, 5)
        self.rest_of_colors = [i for i in range(0, self.colors)]
        self.state = []

        for i in range(20):
            max_index = 14 if i % 4 == 1 or i % 4 == 2 else 15
            column = []
            for j in range(max_index):
                column.append(random.randint(0, self.colors-1))
            self.state.append(column)
        over, _ = self.game_over()
        if over:
            self.state[0][0] = (self.state[0][0] + 1) % self.colors
        
        return self.tran_state(), self.colors

    def load_config_file(self, file):
        self.state = []
        with open(file, 'r') as f:
            lines = f.readlines()
            self.colors = int(lines[0])
            self.min_steps = int(lines[1])
            self.rest_of_colors = [i for i in range(0, self.colors)]
            color_rgbs = []
            for i in range(self.colors):
                color_rgbs.append(eval(lines[i+1]))
            for line in lines[self.colors+1:]:
                self.state.append(eval(line))
        # for i in range(len(self.state)):
        #     print(i, ": ", self.state[i])
        return self.tran_state(), self.colors

    

    def game_over(self):
        # color = self.state[0][0]
        # for column in self.state:
        #     for item in column:
        #         if item != color:
        #             return False
        # return True
        # print(self.rest_of_colors)
        reward = -1
        for color in self.rest_of_colors:
            if not any(color in column for column in self.state):
                self.rest_of_colors.remove(color)
                reward = 3
        if len(self.rest_of_colors) == 1:
            return True, 10
        return False, reward

    def deque_util(self, deq, x, y, color):
        # if (x, y) not in deq:
        #     deq.append((x, y))
        #     self.state[x][y] = color
        deq.append((x, y))
        self.state[x][y] = color

    def valid(self, action):
        color = action // 300
        index = action - color * 300
        x = index // 15
        y = index % 15
        # print("befored_color: ", self.state[x][y])
        # print("color: ", color)
        if (y == 14 and (x % 4 == 1 or x % 4 == 2)) or (color >= self.colors) or (self.state[x][y] == color):
            return False
        #  or (color not in self.rest_of_colors)
        return True

    # def valid(se)

    def step(self, action):
        color = action // 290
        index = action - color * 290
        # if index % 29 >= 15:
        #     y = (index % 29) - 15
        #     x = (index // 29) * 2 + 1
        # else:
        #     y = index % 29
        #     x = (index // 29) * 2
        four_columns = index // (29 * 2)
        index = index - four_columns * 29 * 2
        if index < 15:
            y = index
            x = four_columns * 4
        elif index < 15 + 14:
            y = index - 15
            x = four_columns * 4 + 1
        elif index < 15 + 14 + 14:
            y = index - 29
            x = four_columns * 4 + 2
        else:
            y = index - 43
            x = four_columns * 4 + 3
        
        # temp = color + 1
        # temp = temp - 2 if temp > 2 else temp - 3
        rest_colors = self.rest_of_colors[:]
        # print(rest_colors)
        rest_colors.remove(self.state[x][y])
        # print(rest_colors)
        color = rest_colors[color % len(rest_colors)]
        # print(x, y, color)
        # print(self.state)
        
        # color = (self.state[x][y] + temp)  % self.colors
        
        # print(type(action))
        
        # color = action // 300
        # index = action - color * 300
        # x = index // 15
        # y = index % 15
        # print(x, y, color)
        # if not self.valid(action):
        #     # print("not valid")
        #     return self.tran_state(), -1, False, False
        # if (y == 14 and (x % 4 == 1 or x % 4 == 2)):
        #     return self.tran_state(), -200, False
        # if (color >= self.colors):
        #     return self.tran_state(), -100, False 
        # if (self.state[x][y] == color):
        #     return self.tran_state(), -50, False
        # if (color not in self.rest_of_colors):
        #     return self.tran_state(), -20, False
        before_color = self.state[x][y]
        deq = deque()
        deq.append((x, y))
        self.state[x][y] = color

        while len(deq) != 0:
            # print("here?")
            x, y = deq.pop()
            if x-1 >= 0 and len(self.state[x-1]) > y and self.state[x - 1][y] == before_color:
                self.deque_util(deq, x-1, y, color)
            if x+1 < 20 and len(self.state[x+1]) > y and self.state[x + 1][y] == before_color:
                self.deque_util(deq, x+1, y, color)
            if x % 4 == 0:
                if x + 1 < 20 and y - 1 >= 0 and self.state[x+1][y-1] == before_color:
                    self.deque_util(deq, x+1, y-1, color)
            elif x % 4 == 1:
                if x - 1 >= 0 and len(self.state[x-1]) > y + 1 and self.state[x-1][y+1] == before_color:
                    self.deque_util(deq, x-1, y+1, color)
            elif x % 4 == 2:
                if x + 1 < 20 and len(self.state[x+1]) > y + 1 and self.state[x+1][y+1] == before_color:
                    self.deque_util(deq, x+1, y+1, color)
            else:
                if x - 1 >=0 and y - 1 >= 0 and self.state[x-1][y-1] == before_color:
                    self.deque_util(deq, x-1, y-1, color)
        
        # for i in range(len(self.state)):
        #     print(i, ": ", self.state[i])
        # print(self.state)
        done, reward = self.game_over()
        return self.tran_state(), reward, done
