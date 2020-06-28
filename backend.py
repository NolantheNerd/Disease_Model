import random
import numpy as np

class Society:
    def __init__(self, pop, n_reg, pirt, tf, pi, pac, ttr, incp, dr, psd, quar, qd, cl, vf, sdd):
        """
        The society class is the top level backend class which the frontend 
        interfaces with directly. It is responsible for mananging all the 
        backend Person objects as well as providing a simple set of properties
        and methods for the frontend to access and display.

        Parameters
        ----------
        pop : int
            The population of the society, the number of Person objects to create.
            
        n_reg : int
            The number of distinct regions in which the Person objects can live.
            Can be between 1 and 9.
            
        pirt : float/int
            Stands for Percent of population Infected before Restricting Travel.
            Represents the percentage of the population which needs to be infected
            before restricting travel between regions.
            
        tf : float
            The percentage of the time, on any given non-traveling day, that a
            person will decide to travel.
            
        pi : float/int
            The probability of infection. If a healthy person is encountering a
            sick person, this represents the probability that they will also 
            become infected.
            
        pac : float/int
            Stands for Percent of infections which are Asymptomatic Cases. 
            Represents the percent of cases which remain asymptomatic the whole
            time.
            
        ttr : int
            The Time Taken to Recover in days. 
            
        incp : int
            The incubation period in days (time before asymptomatic cases show 
            symptoms).
            
        dr : float/int
            The death rate as a percent.
            
        psd : float/int
            The percent of people practicing social distancing.
            
        quar : bool
            Whether or not to quarantine the symptomatic.
            
        qd : int
            The number of days between the emergence of symptoms and quarantining.
            
        cl : bool
            Whether or not there is a central location that people in the region 
            visit.
            
        vf : int
            The percentage of the time, on any given non-traveling day, that a
            person will decide to go shopping at the central location.
            
        sdd : int
            The percentage of people sick before enforcing social distancing.

        Returns
        -------
        Society Object

        """
        # Store Society Specific Information
        self.n_reg = n_reg
        self.pirt = pirt/100
        self.sdd = sdd/100
        self.incp = incp
        self.quar = quar
        self.qd = qd*10
        
        self.travel_permitted = True
        self.social_distancing = False
        
        # Person Object List - This is where all the Person Objects live 
        # (Start with None so id == list index as id starts at 1)
        self.people = [None]
        
        # Prepare lists for different types of people - These lists only hold Person IDs
        self.healthy = list(range(2, pop + 1))
        self.asympt = [1]
        self.sympt = []
        self.recovered = []
        self.dead = []
        self.traveling = []
        self.shopping = []
        self.will_social_distance = sorted(random.sample(list(range(1, pop + 1)), int((psd/100)*pop)))
        self.quarantine = []
        
        # Region Definitions
        self.regions = {1: (((0, 1000), (0, 500)),), 2: (((0, 500), (0, 500)), ((500, 1000), (0, 500))),
                   3: (((0, 333), (0, 500)), ((333, 667), (0, 500)), ((667, 1000), (0, 500))),
                   4: (((0, 500), (0, 250)), ((500, 1000), (0, 250)), ((0, 500), (250, 500)), ((500, 1000), (250, 500))),
                   5: (((0, 500), (0, 250)), ((500, 1000), (0, 250)), ((0, 333), (250, 500)), ((333, 667), (250, 500)), ((667, 1000), (250, 500))),
                   6: (((0, 333), (0, 250)), ((333, 667), (0, 250)), ((667, 1000), (0, 250)), ((0, 333), (250, 500)), ((333, 667), (250, 500)), ((667, 1000), (250, 500))),
                   7: (((0, 333), (0, 250)), ((333, 667), (0, 250)), ((667, 1000), (0, 250)), ((0, 250), (250, 500)), ((250, 500), (250, 500)), ((500, 750), (250, 500)), ((750, 1000), (250, 500))),
                   8: (((0, 250), (0, 250)), ((250, 500), (0, 250)), ((500, 750), (0, 250)), ((750, 1000), (0, 250)), ((0, 250), (250, 500)), ((250, 500), (250, 500)), ((500, 750), (250, 500)), ((750, 1000), (250, 500))),
                   9: (((0, 333), (0, 167)), ((333, 667), (0, 167)), ((667, 1000), (0, 167)), ((0, 333), (167, 333)), ((333, 667), (167, 333)), ((667, 1000), (167, 333)), ((0, 333), (333, 500)), ((333, 667), (333, 500)), ((667, 1000), (333, 500)))}
        
        self.store_locations = {1: ((500, 250),), 2: ((250, 250), (750, 250)), 3: ((167, 250), (500, 250), (833, 250)),
                                4: ((250, 125), (750, 125), (250, 375), (750, 375)),
                                5: ((250, 125), (750, 125), (167, 375), (500, 375), (833, 375)),
                                6: ((167, 125), (500, 125), (833, 125), (167, 375), (500, 375), (833, 375)),
                                7: ((167, 125), (500, 125), (833, 125), (125, 375), (375, 375), (625, 375), (875, 375)),
                                8: ((125, 125), (375, 125), (625, 125), (875, 125), (125, 375), (375, 375), (625, 375), (875, 375)),
                                9: ((167, 83), (500, 83), (833, 83), (167, 250), (500, 250), (833, 250), (167, 417), (500, 417), (833, 417))}
        
        # Instantiate People
        # Start with One Asymptomatic Person
        self.people.append(Person(1, 0, self.regions[self.n_reg][0], pi, incp, pac, ttr, dr, tf, vf, True))
        
        # Add Remaining Healthy People
        for i in range(2, pop + 1):
            # Get Region to Assign Person to
            reg = (i-2)%self.n_reg
            
            # Add Person to Healthy List
            self.people.append(Person(i, reg, self.regions[self.n_reg][reg], pi, incp, pac, ttr, dr, tf, vf, False))
            
    
    def update_society(self):
        """
        The update_society method is used to update each Person in the society
        to their next stage so that a new frame can be drawn on the frontend.
        """
        # Get Locations of All Symptomatic and Asymptomatic People
        risk_locations_x, risk_locations_y = [], []
        for person in self.asympt + self.sympt:
            # "Fly Overs" and Quarantined People Can't Infect People
            if person not in self.traveling and not self.people[person].quarantined:
                risk_locations_x.append((self.people[person].x-5, self.people[person].x+5))
                risk_locations_y.append((self.people[person].y-5, self.people[person].y+5))
            
        # Update All People
        for person in self.recovered + self.sympt + self.asympt + self.healthy:
            if person in self.healthy:
                # Determine if person is Encountering a Sick Person
                encountering = False
                # Read healthy person's location once
                healthy_x, healthy_y = self.people[person].x, self.people[person].y
                # Check that the healthy person is not too close to any of the sick people
                for i in range(len(risk_locations_x)):
                    if (healthy_x > risk_locations_x[i][0] and healthy_x < risk_locations_x[i][1] and 
                        healthy_y > risk_locations_y[i][0] and healthy_y < risk_locations_y[i][1]):
                        encountering = True
                        break
            else:
                encountering = False
                
            # Prepare other Update Person Parameters
            start_trip, travel_to, new_reg, new_bds = False, None, None, None
            
            # Check if the Person Wants to Travel
            if self.people[person].just_started_traveling and self.n_reg > 1:
                start_trip = True
                
                # Pick a Region for the Person to Travel to
                regions = list(set(list(range(self.n_reg))) - {self.people[person].reg})
                new_reg = random.choice(regions)
                
                # Pick a Spot in the New Region to Move to
                new_bds = self.regions[self.n_reg][new_reg]
                new_x = random.uniform(new_bds[0][0] + 10, new_bds[0][1] - 10)
                new_y = random.uniform(new_bds[1][0] + 10, new_bds[1][1] - 10)
                travel_to = (new_x, new_y)
                
            # Check if the Person wants to go Shopping
            elif self.people[person].just_started_shopping:
                start_trip = True
                
                # Find Location of Store in Person's Region
                new_x, new_y = self.store_locations[self.n_reg][self.people[person].reg]
                travel_to = (new_x-5, new_y-5)
                
            self.people[person].update_person(encountering, start_trip, travel_to, new_reg, new_bds)
            
        # Remake ID Lists
        self.healthy = [self.people[person].id for person in list(range(1, len(self.people))) 
                        if self.people[person].healthy]
        self.asympt = [self.people[person].id for person in list(range(1, len(self.people))) 
                       if self.people[person].asympt]
        self.sympt = [self.people[person].id for person in list(range(1, len(self.people))) 
                      if self.people[person].sympt]
        self.recovered = [self.people[person].id for person in list(range(1, len(self.people))) 
                          if self.people[person].recovered]
        self.dead = [self.people[person].id for person in list(range(1, len(self.people))) 
                     if self.people[person].dead]
        self.traveling = [self.people[person].id for person in list(range(1, len(self.people)))
                          if self.people[person].traveling]
        self.shopping = [self.people[person].id for person in list(range(1, len(self.people)))
                         if self.people[person].shopping]
        self.quarantine = [self.people[person].id for person in list(range(1, len(self.people)))
                           if self.people[person].quarantined]
        
        # Block Travel if Too Many People are Infected
        if (len(self.sympt) + len(self.asympt))/len(self.people) > self.pirt:
            for person in range(1, len(self.people)):
                setattr(self.people[person], "restricted_from_traveling", True)
            self.travel_permitted = False
                
        # Permit Travel if Few Enough People are Infected
        else:
            for person in range(1, len(self.people)):
                setattr(self.people[person], "restricted_from_traveling", False)
            self.travel_permitted = True
                
        # Enforce Social Distancing If Enough People are Infected
        if (len(self.sympt) + len(self.asympt))/len(self.people) > self.sdd:
            for person in self.will_social_distance:
                # Travelers/Shoppers Social Distance After their Trip
                if not self.people[person].traveling and not self.people[person].shopping:
                    setattr(self.people[person], "social_distancing", True)
            self.social_distancing = True
                
        # Relax Social Distancing if Few Enough People are Infected
        else:
            for person in self.will_social_distance:
                setattr(self.people[person], "social_distancing", False)
            self.social_distancing = False
                
        # Move Symptomatic People to Quarantine if they Have Shown Symptoms for Enough Time
        if self.quar:
            for person in range(1, len(self.people)):
                if self.people[person].sympt and self.people[person].day1 == self.qd:
                    setattr(self.people[person], "quarantined", True)
                    setattr(self.people[person], "just_quarantined", True)
        

class Person:
    def __init__(self, id_, reg, reg_bd, pi, incp, pac, ttr, dr, tf, vf, start_sick=False):
        # Capture Instantiation Inputs
        self.id = id_
        self.reg = reg
        self.reg_bd = reg_bd
        self.pi = pi/100
        self.incp = incp*10
        self.pac = pac/100
        self.ttr = ttr*10
        self.dr = dr/100
        self.tf = tf/100
        self.vf = vf/100
        
        # Personal Stats
        self.time = 0
        self.healthy = not start_sick
        self.asympt = start_sick
        self.sympt = False
        self.traveling = False
        self.shopping = False
        self.just_started_traveling = False
        self.restricted_from_traveling = False
        self.just_started_shopping = False
        self.recovered = False
        self.dead = False
        self.social_distancing = False
        self.quarantined = False
        self.just_quarantined = False
        if self.asympt:
            self.day0 = int(self.time)
        
        # Location Information
        self.x = random.uniform(self.reg_bd[0][0] + 10, self.reg_bd[0][1] - 10)
        self.y = random.uniform(self.reg_bd[1][0] + 10, self.reg_bd[1][1] - 10)
        self.vx = 75*(random.random()-0.5)
        self.vy = 75*(random.random()-0.5)
        self.xs, self.ys = self.calc_pos(num=random.choice(range(500, 2500)))
        
        
    def update_person(self, encountering=False, start_trip=False, travel_to=None, new_reg=None, new_bds=None):
        """
        The update_person function is generally responsible for updating the 
        Person to the next time step. This involves iterating their clocks
        and calling both position and state updating functions with their
        appropriate parameters.

        Parameters
        ----------
        encountering : bool, optional
            Describes whether or not the Person is in direct contact with a 
            symptomatic or asymptomatic Person. The default is False.
            
        start_trip : bool, optional
            Indicates whether or not to update the future position list with
            travel to a particular destination. Used for traveling between
            regions or to a central location. The default is False.
            
        travel_to : 2-tuple or None, optional
            Specifies the location to travel directly to if start_trip. Ignored
            if start_trip is False. The default is None.
            
        new_reg : int, optional
            Specifies the new region that the person is moving to.
            
        new_bds : tuple, optional
            Specifies the boundaries of the new region that the person is moving
            to.

        """
        # Update Personal Times
        self.time += 1
        
        # Don't Progress Healing if Traveling Between Regions
        if (self.asympt or self.sympt) and not self.traveling:
            self.day0 += 1
        if self.sympt and not self.traveling:
            self.day1 += 1
            
        # Reset Just Started Traveling/Shopping
        self.just_started_traveling = False
        self.just_started_shopping = False
            
        # Update State and Position
        # Remove People in Quarantine from Simulation Area
        if self.just_quarantined:
            self.x, self.y = random.uniform(4, 90), random.uniform(4, 90)
        elif self.quarantined:
            pass
        else:
            self.update_position(start_trip, travel_to, new_reg, new_bds)
        self.update_state(encountering)
        
        # Reset Just Quarantined Variable
        self.just_quarantined = False
        
        
    def update_state(self, encountering=False):
        """
        The update_state function is responsible for updating the state of the
        Person, both in terms of their health, but also in terms of their 
        movement choices.

        Parameters
        ----------
        encountering : bool, optional
            Describes whether or not the Person is in direct contact with a 
            symptomatic or asymptomatic Person. The default is False.

        """
        # If Healthy but in Contact with a Sick Person, Check if they Get Infected
        if self.healthy and encountering:
            dice_roll = random.random()
            
            # Get Infected
            if dice_roll < self.pi:
                # Update State and Set Day0
                self.day0 = 0
                self.healthy = False
                self.asympt = True
                
        # Update Asymptomatic to Symptomatic if Incubation Period is Up and 
        # Not Permanently Asymptomatic
        if self.asympt and self.day0 == self.incp:
            dice_roll = random.random()
            
            # Becomes Symptomatic
            if dice_roll < (1 - self.pac):
                # Time Since Became Symptomatic
                self.day1 = 0
                self.asympt = False
                self.sympt = True
                
        # Update Sick People to Recovered or Dead
        if (self.asympt or self.sympt) and self.day0 == self.ttr:
            self.asympt = False
            self.sympt = False
            dice_roll = random.random()
            
            # Person Dies
            if dice_roll < self.dr:
                self.dead = True
                
            # Person Recovers
            else:
                self.recovered = True
                
        # Decide if Person should Start a Trip
        if not self.traveling and not self.restricted_from_traveling and not self.social_distancing:
            dice_roll = random.random()
            
            # Start a Trip to a New Region
            if dice_roll < self.tf:
                self.traveling = True
                self.just_started_traveling = True
                
        # Decide if Person should start a Trip to the Central Location
        if not self.traveling and not self.shopping and not self.social_distancing:
            dice_roll = random.random()
            
            # Start a Trip to the Store
            if dice_roll < self.vf:
                self.shopping = True
                self.just_started_shopping = True
                
        
    def update_position(self, start_trip=False, travel_to=None, new_reg=None, new_bds=None):
        """
        The update_position function is responsible for iterating the position
        of the person. That means creating new positions if necessary, and
        iterating the values of self.x and self.y.
        
        Parameters:
        -----------
        start_trip: bool
            Indicates whether or not to update the future position list with
            travel to a particular destination. Used for traveling between
            regions or to a central location. Default value is False.
            
        travel_to: 2-tuple or None
            Specifies the location to travel directly to if start_trip. Ignored
            if start_trip is False. Defaults to None.
            
        new_reg : int, optional
            Specifies the new region that the person is moving to.
            
        new_bds : tuple, optional
            Specifies the boundaries of the new region that the person is moving
            to.
        """
        # Overwrite future positions to take a direct trip (to new region or store)
        if start_trip:
            # Trip to a New Region
            if new_reg is not None:
                self.reg = new_reg
                self.reg_bd = new_bds
            new_xs, new_ys = self.travel_path(self.x, self.y, travel_to[0], travel_to[1])
            self.xs = np.concatenate([self.xs[:self.time], new_xs])
            self.ys = np.concatenate([self.ys[:self.time], new_ys])
            
        # Social Distancing
        elif self.social_distancing:
            self.xs = np.append(self.xs[:self.time], self.x)
            self.ys = np.append(self.ys[:self.time], self.y)
        
        # Create new position values if necessary
        elif self.time > len(self.xs) - 1:
            # If the person was on a trip, it must have just ended
            self.traveling = False
            self.shopping = False
            
            # Get new positions
            new_xs, new_ys = self.calc_pos(num=random.choice(range(500, 2500)))
            self.xs = np.concatenate([self.xs, new_xs])
            self.ys = np.concatenate([self.ys, new_ys])
            
        # Update Position
        self.x, self.y = self.xs[self.time], self.ys[self.time]
    
    
    def calc_pos(self, t=0.1, num=1000, size=10):
        init_x, init_y = float(self.x), float(self.y)
        xs = (t*np.arange(num))*(self.vx*np.ones(num))+self.x*np.ones(num)
        xb_check = np.nonzero(np.logical_or(xs <= self.reg_bd[0][0], xs >= self.reg_bd[0][1]-size))
        while len(xb_check[0]) > 0:
            self.x = xs[xb_check[0][0]-1]
            self.vx *= -1
            xs[xb_check[0][0]:] = (t*np.arange(num-xb_check[0][0]))*(self.vx*np.ones(num-xb_check[0][0]))+self.x*np.ones(num-xb_check[0][0])
            xb_check = np.nonzero(np.logical_or(xs <= self.reg_bd[0][0], xs >= self.reg_bd[0][1]-size))
        
        ys = (t*np.arange(num))*(self.vy*np.ones(num))+self.y*np.ones(num)
        yb_check = np.nonzero(np.logical_or(ys <= self.reg_bd[1][0], ys >= self.reg_bd[1][1]-size))
        while len(yb_check[0]) > 0:
            self.y = ys[yb_check[0][0]-1]
            self.vy *= -1
            ys[yb_check[0][0]:] = (t*np.arange(num-yb_check[0][0]))*(self.vy*np.ones(num-yb_check[0][0]))+self.y*np.ones(num-yb_check[0][0])
            yb_check = np.nonzero(np.logical_or(ys <= self.reg_bd[1][0], ys >= self.reg_bd[1][1]-size))
        
        self.x, self.y = init_x, init_y
        return xs, ys
    
    
    def travel_path(self, x, y, new_x, new_y):
        steps = max((int(np.ceil(np.sqrt((new_x-x)**2+(new_y-y)**2))/10), 3))
        return np.linspace(x, new_x, steps), np.linspace(y, new_y, steps)
        
