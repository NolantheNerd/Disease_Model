import random
import numpy as np

class Person:
    """
    Person is the class that incapsulates all of the people in the simulation.
    
    Parameters:
    -----------
        ttr: time to recover
        ip: infection probability
        incp: incubation period
        dp: death probability
        pas: percent asmyptomatic
    """
    def __init__(self, asympt=False, ttr=300, ip=100, incp=150, dp=0.4, pas=100, cur_reg=1, xlim=(0,1000), ylim=(0,500), n_reg=1, trav_freq=0):
        # Define Regions and Travel Variables
        self.n_reg = n_reg
        self.trav_freq = trav_freq
        self.cur_reg = cur_reg
        if n_reg == 1:
            self.can_travel = False
        else:
            self.can_travel = True
        self.traveling = False
        self.arrived = False
        self.regions = {1: (((0, 1000), (0, 500)),), 2: (((0, 500), (0, 500)), ((500, 1000), (0, 500))),
                   3: (((0, 333), (0, 500)), ((333, 667), (0, 500)), ((667, 1000), (0, 500))),
                   4: (((0, 500), (0, 250)), ((500, 1000), (0, 250)), ((0, 500), (250, 500)), ((500, 1000), (250, 500))),
                   5: (((0, 500), (0, 250)), ((500, 1000), (0, 250)), ((0, 333), (250, 500)), ((333, 667), (250, 500)), ((667, 1000), (250, 500))),
                   6: (((0, 333), (0, 250)), ((333, 667), (0, 250)), ((667, 1000), (0, 250)), ((0, 333), (250, 500)), ((333, 667), (250, 500)), ((667, 1000), (250, 500))),
                   7: (((0, 333), (0, 250)), ((333, 667), (0, 250)), ((667, 1000), (0, 250)), ((0, 250), (250, 500)), ((250, 500), (250, 500)), ((500, 750), (250, 500)), ((750, 1000), (250, 500))),
                   8: (((0, 250), (0, 250)), ((250, 500), (0, 250)), ((500, 750), (0, 250)), ((750, 1000), (0, 250)), ((0, 250), (250, 500)), ((250, 500), (250, 500)), ((500, 750), (250, 500)), ((750, 1000), (250, 500))),
                   9: (((0, 333), (0, 167)), ((333, 667), (0, 167)), ((667, 1000), (0, 167)), ((0, 333), (167, 333)), ((333, 667), (167, 333)), ((667, 1000), (167, 333)), ((0, 333), (333, 500)), ((333, 667), (333, 500)), ((667, 1000), (333, 500)))}
        
        # Societal Constants
        self.ttr = ttr*100
        self.ip = ip
        self.incp = incp*50
        self.dp = dp
        self.pas = pas
        self.size = 10
        
        # Init Time
        self.time = 0
        
        # Init State
        self.perm_asympt = False
        if not asympt:
            self.healthy = True
            self.asympt = False
        else:
            self.healthy = False
            self.asympt = True
            self.day0 = int(self.time)
            # Decide if permanently Asymptomatic
            dice_roll = random.random()
            if dice_roll < self.pas/100:
                self.perm_asympt = True
        self.sympt = False
        self.recovered = False
        self.dead = False
        
        # Initial Physics
        self.xlim = xlim
        self.ylim = ylim
        self.x = random.uniform(self.xlim[0]+self.size, self.xlim[1]-self.size)
        self.y = random.uniform(self.ylim[0]+self.size, self.ylim[1]-self.size)
        self.vx = 75*(random.random()-0.5)
        self.vy = 75*(random.random()-0.5)
        
        self.xs, self.ys = self.calc_pos(num=random.choice(range(500, 2500)))
        
        
    def calc_pos(self, t=0.1, num=1000, size=10):
        xs = (t*np.arange(num))*(self.vx*np.ones(num))+self.x*np.ones(num)
        xb_check = np.nonzero(np.logical_or(xs <= self.xlim[0], xs >= self.xlim[1]-size))
        while len(xb_check[0]) > 0:
            self.x = xs[xb_check[0][0]-1]
            self.vx *= -1
            xs[xb_check[0][0]:] = (t*np.arange(num-xb_check[0][0]))*(self.vx*np.ones(num-xb_check[0][0]))+self.x*np.ones(num-xb_check[0][0])
            xb_check = np.nonzero(np.logical_or(xs <= self.xlim[0], xs >= self.xlim[1]-size))
        
        ys = (t*np.arange(num))*(self.vy*np.ones(num))+self.y*np.ones(num)
        yb_check = np.nonzero(np.logical_or(ys <= self.ylim[0], ys >= self.ylim[1]-size))
        while len(yb_check[0]) > 0:
            self.y = ys[yb_check[0][0]-1]
            self.vy *= -1
            ys[yb_check[0][0]:] = (t*np.arange(num-yb_check[0][0]))*(self.vy*np.ones(num-yb_check[0][0]))+self.y*np.ones(num-yb_check[0][0])
            yb_check = np.nonzero(np.logical_or(ys <= self.ylim[0], ys >= self.ylim[1]-size))
        
        return xs, ys
    
    
    def start_travel(self):
        # Check if travel is possible
        if not self.traveling and self.can_travel:
            # Travel?
            dice_roll = random.random()
            if dice_roll < self.trav_freq/100:
                # Set Travel to True
                self.traveling = True
                
                # Choose region to move to
                
                
                new_xs, new_ys = self.travel_path(self.x, self.y)
    
    def travel_path(self, x, y, new_x, new_y):
        steps = max((int(np.ceil(np.sqrt((new_x-x)**2+(new_y-y)**2)/75)), 3))
        return np.linspace(x, new_x, steps), np.linspace(y, new_y, steps)
        
        
    def update(self, encountering=False):
        # Update the Location of the Person
        # Update Time and Position
        self.time += 1
        
        # Check if Next Position exists
        if self.time < len(self.xs):
            self.x, self.y = self.xs[self.time], self.ys[self.time]
        # Calculate More Positions
        else:
            new_xs, new_ys = self.calc_pos(num=random.choice(range(500, 2500)))
            self.xs = np.concatenate([self.xs, new_xs])
            self.ys = np.concatenate([self.ys, new_ys])
            self.x, self.y = self.xs[self.time], self.ys[self.time]
            
        # Update Health State
        # Chance getting sick
        if encountering and self.healthy:
            dice_roll = random.random()
            if dice_roll < self.ip/100:
                self.healthy = False
                self.asympt = True
                self.day0 = int(self.time)
                # Decide if Always Asymptomatic
                dice_roll = random.random()
                if dice_roll < self.pas/100:
                    self.perm_asympt = True
                    
        # Leave Incubation Period
        elif self.asympt and self.time-self.day0 >= self.incp and not self.perm_asympt:
            self.asympt = False
            self.sympt = True
            
        # Recover or Die
        elif (self.sympt or self.perm_asympt) and self.time-self.day0 >= self.ttr:
            # Permanently Asymptomatic People Can Recover
            self.asympt = False
            self.sympt = False
            dice_roll = random.random()
            if dice_roll < self.dp/100:
                self.dead = True
                self.can_travel = False
            else:
                self.recovered = True
                
                