import numpy as np

class ToilletPaperAg():

    def __init__(self,env) -> None:
        self.env = env
        self.price_average = 0
        self.current_percepts = env.initial_percepts()
        self.usage_average = self.current_percepts['tpnumber']
        self.usage = self.current_percepts['tpnumber']
        self.age = 0
        self.usage_std = 0
        self.to_buy = 0
        self.spendings = 0 

    def act(self):
         
        tpnumber_t_1 = self.current_percepts['tpnumber'] 
        
        self.usage_std = 100

        self.to_buy = max(self.usage_average + self.usage_std*4 - self.current_percepts['tpnumber'],0) 
        self.spendings = self.to_buy * self.current_percepts['price']

        action = {'to_buy':self.to_buy}
        
        self.current_percepts = self.env.change_state(action)
        self.age += 1
        
        tpnumber_t = self.current_percepts['tpnumber']
        
        self.usage = tpnumber_t_1 + self.to_buy - tpnumber_t 
        self.usage_average = (self.usage_average * (self.age - 1) + self.usage)/self.age

class MazeAgentDFS():

    def __init__(self,env):
        self.env = env
        self.percepts = env.initial_percepts()
        self.F = [[self.percepts['position']]]

    def act(self):

        while self.F:
            path = self.F.pop(-1)

            self.percepts = self.env.change_state({'path':path.copy()})

            if self.percepts['goal']:
                break
            else:
                for n in self.percepts['available_neighbors']:
                    if n not in path:
                        self.F.insert(-1,path + [n])

        self.env.draw_best(path)


class MazeAgentBranchAndBound():

    def __init__(self,env,bound):
        self.env = env
        self.percepts = env.initial_percepts()
        self.F = [[self.percepts['position']]]
        self.bound = bound
        self.best_path = []

    def cost(self, path):
        return len(path)-1

    def heuristic(self, path):
        nk = path[-1]
        goal = self.env.maze._goal
        return np.abs(nk[0] - goal[0]) + np.abs(nk[1] - goal[1])

    def act(self):

        while self.F:
            path = self.F.pop(-1)
            c = self.cost(path)
            h = self.heuristic(path)

            if c + h <= self.bound:

                self.percepts = self.env.change_state({'path':path.copy()})

                if self.percepts['goal']:
                    self.best_path = path
                    self.bound = c 
                else:
                    for n in self.percepts['available_neighbors']:
                        if n not in path:
                            self.F.insert(-1,path + [n])

        self.env.draw_best(self.best_path)
        print(self.bound)
