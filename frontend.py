import tkinter as tk
from backend import Society, Person

class Disease_Simulator:
    def __init__(self):
        # Base Values
        self.size = 10
        
        # Init Value Storage
        self.healthy = {}
        self.sympt = {}
        self.asympt = {}
        self.recovered = {}
        self.dead = {}
        self.traveling = {}
        
        # Frame Value
        self.frame = 0
        
        # Root Window
        self.root = tk.Tk()
        self.root.title("Covid-19 Simulation")
        
        ### Mainframe ###
        self.mainframe = tk.Frame(self.root)
        self.mainframe.grid(row=0, column=0)
        
        ### Plot Frame ###
        self.plot_frame = tk.Frame(self.mainframe)
        self.plot_frame.grid(row=0, column=0)
        
        ### Simulator Frame ###
        self.sim_frame = tk.Frame(self.mainframe)
        self.sim_frame.grid(row=0, column=1)
        
        # Canvas
        self.canvas = tk.Canvas(self.sim_frame, width=1000, height=500)
        self.canvas.grid(row=0, column=0)
        
        ### Toggle Frame ###
        self.tog_frame = tk.Frame(self.mainframe)
        self.tog_frame.grid(row=1, column=0, columnspan=2)
        
        # Quit Button
        quit_button = tk.Button(self.tog_frame, text="Quit", command=self.close)
        quit_button.grid(row=7, column=3)
        
        # Reset Button
        reset_button = tk.Button(self.tog_frame, text="Reset", command=self.reset_simulation)
        reset_button.grid(row=7, column=1)
        
        # Go Button
        self.go_button = tk.Button(self.tog_frame, text="Start Simulation", command=self.start_simulation)
        self.go_button.grid(row=7, column=0)
        
        # Population Label
        pop_label = tk.Label(self.tog_frame, text="Population:")
        pop_label.grid(row=0, column=0)
        
        # Population Slider
        self.pop_var = tk.IntVar()
        pop_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=100, to=1000, variable=self.pop_var)
        pop_slider.grid(row=0, column=1)
        
        # Cities Label
        cities_label = tk.Label(self.tog_frame, text="# of Regions:")
        cities_label.grid(row=0, column=2)
        
        # Cities Slider
        self.cities_var = tk.IntVar()
        cities_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=1, to=9, variable=self.cities_var)
        cities_slider.grid(row=0, column=3)
        
        # Restrict Travel Label
        rt_label = tk.Label(self.tog_frame, text="% Infected Before Restricting Travel:")
        rt_label.grid(row=1, column=0)
        
        # Restrict Travel Slider
        self.rt_var = tk.IntVar()
        rt_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=100, variable=self.rt_var)
        rt_slider.grid(row=1, column=1)
        
        # Travel Frequency Label
        tf_label = tk.Label(self.tog_frame, text="Travel Frequency")
        tf_label.grid(row=1, column=2)
        
        # Travel Frequency Slider
        self.tf_var = tk.IntVar()
        tf_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=365, variable=self.tf_var)
        tf_slider.grid(row=1, column=3)
        
        # Death Rate Label
        dr_label = tk.Label(self.tog_frame, text="Death Rate (%):")
        dr_label.grid(row=4, column=0)
        
        # Death Rate Slider
        self.dr_var = tk.IntVar()
        dr_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=100, resolution=0.5, variable=self.dr_var)
        dr_slider.grid(row=4, column=1)
        
        # SD Proportion Label
        sdp_label = tk.Label(self.tog_frame, text="% of People Social Distancing")
        sdp_label.grid(row=4, column=2)
        
        # SD Proportion Slider
        self.sdp_var = tk.IntVar()
        sdp_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=100, variable=self.sdp_var)
        sdp_slider.grid(row=4, column=3)
        
        # Quarantine Label
        quar_label = tk.Label(self.tog_frame, text="Quarantine the Sick:")
        quar_label.grid(row=5, column=0)
        
        # Quarantine Checkbox
        self.quar_var = tk.IntVar()
        quar_check = tk.Checkbutton(self.tog_frame, variable=self.quar_var)
        quar_check.grid(row=5, column=1)
        
        # Quarantine Delay Label
        quard_label = tk.Label(self.tog_frame, text="Quarantine Delay:")
        quard_label.grid(row=5, column=2)
        
        # Quarantine Delay Slider
        self.quard_var = tk.IntVar()
        quard_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=30, variable=self.quard_var)
        quard_slider.grid(row=5, column=3)
        
        # Central Location Label
        cl_label = tk.Label(self.tog_frame, text="Central Location:")
        cl_label.grid(row=6, column=0)
        
        # Central Location Checkbox
        self.cl_var = tk.IntVar()
        cl_check = tk.Checkbutton(self.tog_frame, variable=self.cl_var)
        cl_check.grid(row=6, column=1)
        
        # Central Location Frequency Label
        clf_label = tk.Label(self.tog_frame, text="Visitation Frequency:")
        clf_label.grid(row=6, column=2)
        
        # Central Location Frequency Slider
        self.clf_var = tk.IntVar()
        clf_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=1, to=30, variable=self.clf_var)
        clf_slider.grid(row=6, column=3)
        
        # Infectability Label
        ift_label = tk.Label(self.tog_frame, text="Probability of Infection:")
        ift_label.grid(row=2, column=0)
        
        # Infectability Slider
        self.ift_var = tk.IntVar()
        ift_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=1, to=100, variable=self.ift_var)
        ift_slider.grid(row=2, column=1)
        
        # Percent Asymptomatic Label
        pas_label = tk.Label(self.tog_frame, text="% of Asymptomatic Cases:")
        pas_label.grid(row=2, column=2)
        
        # Percent Asymptomatic Slider
        self.pas_var = tk.IntVar()
        pas_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=100, variable=self.pas_var)
        pas_slider.grid(row=2, column=3)
        
        # Average Time to Recover Label
        ttr_label = tk.Label(self.tog_frame, text="Time Taken to Recover:")
        ttr_label.grid(row=3, column=0)
        
        # Average Time to Recover Slider
        self.ttr_var = tk.IntVar()
        ttr_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=1, to=30, variable=self.ttr_var)
        ttr_slider.grid(row=3, column=1)
        
        # Incubation Period Label
        inc_label = tk.Label(self.tog_frame, text="Incubation Period:")
        inc_label.grid(row=3, column=2)
        
        # Incubation Period Slider
        self.inc_var = tk.IntVar()
        inc_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=30, variable=self.inc_var)
        inc_slider.grid(row=3, column=3)
        
        self.root.mainloop()
        
        
    def start_simulation(self):
        self.society = Society(self.pop_var.get(), self.cities_var.get(), 
                               self.rt_var.get(), self.tf_var.get(),
                               self.ift_var.get(), self.pas_var.get(),
                               self.ttr_var.get(), self.inc_var.get(),
                               self.dr_var.get(), self.sdp_var.get(),
                               self.quar_var.get(), self.quard_var.get(),
                               self.cl_var.get(), self.clf_var.get())
    

class Disease_Simulator_:
    def __init__(self):
        # Base Values
        self.size = 10
        
        # Init Value Storage
        self.healthy = {}
        self.sympt = {}
        self.asympt = {}
        self.recovered = {}
        self.dead = {}
        self.traveling = {}
        
        # Frame Value
        self.frame = 0
        
        # Root Window
        self.root = tk.Tk()
        self.root.title("Covid-19 Simulation")
        
        ### Mainframe ###
        self.mainframe = tk.Frame(self.root)
        self.mainframe.grid(row=0, column=0)
        
        ### Plot Frame ###
        self.plot_frame = tk.Frame(self.mainframe)
        self.plot_frame.grid(row=0, column=0)
        
        ### Simulator Frame ###
        self.sim_frame = tk.Frame(self.mainframe)
        self.sim_frame.grid(row=0, column=1)
        
        # Canvas
        self.canvas = tk.Canvas(self.sim_frame, width=1000, height=500)
        self.canvas.grid(row=0, column=0)
        
        ### Toggle Frame ###
        self.tog_frame = tk.Frame(self.mainframe)
        self.tog_frame.grid(row=1, column=0, columnspan=2)
        
        # Quit Button
        quit_button = tk.Button(self.tog_frame, text="Quit", command=self.close)
        quit_button.grid(row=7, column=3)
        
        # Reset Button
        reset_button = tk.Button(self.tog_frame, text="Reset", command=self.reset_simulation)
        reset_button.grid(row=7, column=1)
        
        # Go Button
        self.go_button = tk.Button(self.tog_frame, text="Start Simulation", command=self.start_simulation)
        self.go_button.grid(row=7, column=0)
        
        # Population Label
        pop_label = tk.Label(self.tog_frame, text="Population:")
        pop_label.grid(row=0, column=0)
        
        # Population Slider
        self.pop_var = tk.IntVar()
        pop_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=100, to=1000, variable=self.pop_var)
        pop_slider.grid(row=0, column=1)
        
        # Cities Label
        cities_label = tk.Label(self.tog_frame, text="# of Regions:")
        cities_label.grid(row=0, column=2)
        
        # Cities Slider
        self.cities_var = tk.IntVar()
        cities_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=1, to=9, variable=self.cities_var)
        cities_slider.grid(row=0, column=3)
        
        # Restrict Travel Label
        rt_label = tk.Label(self.tog_frame, text="% Infected Before Restricting Travel:")
        rt_label.grid(row=1, column=0)
        
        # Restrict Travel Slider
        self.rt_var = tk.IntVar()
        rt_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=100, variable=self.rt_var)
        rt_slider.grid(row=1, column=1)
        
        # Travel Frequency Label
        tf_label = tk.Label(self.tog_frame, text="Travel Frequency")
        tf_label.grid(row=1, column=2)
        
        # Travel Frequency Slider
        self.tf_var = tk.IntVar()
        tf_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=365, variable=self.tf_var)
        tf_slider.grid(row=1, column=3)
        
        # Death Rate Label
        dr_label = tk.Label(self.tog_frame, text="Death Rate (%):")
        dr_label.grid(row=4, column=0)
        
        # Death Rate Slider
        self.dr_var = tk.IntVar()
        dr_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=100, resolution=0.5, variable=self.dr_var)
        dr_slider.grid(row=4, column=1)
        
        # SD Proportion Label
        sdp_label = tk.Label(self.tog_frame, text="% of People Social Distancing")
        sdp_label.grid(row=4, column=2)
        
        # SD Proportion Slider
        self.sdp_var = tk.IntVar()
        sdp_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=100, variable=self.sdp_var)
        sdp_slider.grid(row=4, column=3)
        
        # Quarantine Label
        quar_label = tk.Label(self.tog_frame, text="Quarantine the Sick:")
        quar_label.grid(row=5, column=0)
        
        # Quarantine Checkbox
        self.quar_var = tk.IntVar()
        quar_check = tk.Checkbutton(self.tog_frame, variable=self.quar_var)
        quar_check.grid(row=5, column=1)
        
        # Quarantine Delay Label
        quard_label = tk.Label(self.tog_frame, text="Quarantine Delay:")
        quard_label.grid(row=5, column=2)
        
        # Quarantine Delay Slider
        self.quard_var = tk.IntVar()
        quard_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=30, variable=self.quard_var)
        quard_slider.grid(row=5, column=3)
        
        # Central Location Label
        cl_label = tk.Label(self.tog_frame, text="Central Location:")
        cl_label.grid(row=6, column=0)
        
        # Central Location Checkbox
        self.cl_var = tk.IntVar()
        cl_check = tk.Checkbutton(self.tog_frame, variable=self.cl_var)
        cl_check.grid(row=6, column=1)
        
        # Central Location Frequency Label
        clf_label = tk.Label(self.tog_frame, text="Visitation Frequency:")
        clf_label.grid(row=6, column=2)
        
        # Central Location Frequency Slider
        self.clf_var = tk.IntVar()
        clf_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=1, to=30, variable=self.clf_var)
        clf_slider.grid(row=6, column=3)
        
        # Infectability Label
        ift_label = tk.Label(self.tog_frame, text="Probability of Infection:")
        ift_label.grid(row=2, column=0)
        
        # Infectability Slider
        self.ift_var = tk.IntVar()
        ift_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=1, to=100, variable=self.ift_var)
        ift_slider.grid(row=2, column=1)
        
        # Percent Asymptomatic Label
        pas_label = tk.Label(self.tog_frame, text="% of Asymptomatic Cases:")
        pas_label.grid(row=2, column=2)
        
        # Percent Asymptomatic Slider
        self.pas_var = tk.IntVar()
        pas_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=100, variable=self.pas_var)
        pas_slider.grid(row=2, column=3)
        
        # Average Time to Recover Label
        ttr_label = tk.Label(self.tog_frame, text="Time Taken to Recover:")
        ttr_label.grid(row=3, column=0)
        
        # Average Time to Recover Slider
        self.ttr_var = tk.IntVar()
        ttr_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=1, to=30, variable=self.ttr_var)
        ttr_slider.grid(row=3, column=1)
        
        # Incubation Period Label
        inc_label = tk.Label(self.tog_frame, text="Incubation Period:")
        inc_label.grid(row=3, column=2)
        
        # Incubation Period Slider
        self.inc_var = tk.IntVar()
        inc_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=30, variable=self.inc_var)
        inc_slider.grid(row=3, column=3)
        
        self.root.mainloop()
        
        
    def reset_simulation(self):
        # Stop update loop
        self.run_simulation = False
        
        # Enable Start Button
        self.go_button.config(state=tk.ACTIVE)
        
        # Reset Frame Value
        self.frame = 0
        
        # Reset Storage
        self.healthy = {}
        self.sympt = {}
        self.asympt = {}
        self.recovered = {}
        self.dead = {}
        self.traveling = {}
        
        # Reset Canvas
        self.canvas.destroy()
        self.canvas = tk.Canvas(self.sim_frame, width=1000, height=500)
        self.canvas.grid(row=0, column=0)
        
    
    def start_simulation(self):
        # Predefine Region Boundaries
        regions = {1: (((0, 1000), (0, 500)),), 2: (((0, 500), (0, 500)), ((500, 1000), (0, 500))),
                   3: (((0, 333), (0, 500)), ((333, 667), (0, 500)), ((667, 1000), (0, 500))),
                   4: (((0, 500), (0, 250)), ((500, 1000), (0, 250)), ((0, 500), (250, 500)), ((500, 1000), (250, 500))),
                   5: (((0, 500), (0, 250)), ((500, 1000), (0, 250)), ((0, 333), (250, 500)), ((333, 667), (250, 500)), ((667, 1000), (250, 500))),
                   6: (((0, 333), (0, 250)), ((333, 667), (0, 250)), ((667, 1000), (0, 250)), ((0, 333), (250, 500)), ((333, 667), (250, 500)), ((667, 1000), (250, 500))),
                   7: (((0, 333), (0, 250)), ((333, 667), (0, 250)), ((667, 1000), (0, 250)), ((0, 250), (250, 500)), ((250, 500), (250, 500)), ((500, 750), (250, 500)), ((750, 1000), (250, 500))),
                   8: (((0, 250), (0, 250)), ((250, 500), (0, 250)), ((500, 750), (0, 250)), ((750, 1000), (0, 250)), ((0, 250), (250, 500)), ((250, 500), (250, 500)), ((500, 750), (250, 500)), ((750, 1000), (250, 500))),
                   9: (((0, 333), (0, 167)), ((333, 667), (0, 167)), ((667, 1000), (0, 167)), ((0, 333), (167, 333)), ((333, 667), (167, 333)), ((667, 1000), (167, 333)), ((0, 333), (333, 500)), ((333, 667), (333, 500)), ((667, 1000), (333, 500)))}
        
        region_lines = {1: (()), 2: ((500, 0, 500, 500),), 3: ((333, 0, 333, 500), (667, 0, 667, 500)),
                        4: ((500, 0, 500, 500), (0, 250, 1000, 250)), 
                        5: ((500, 0, 500, 250), (0, 250, 1000, 250), (333, 250, 333, 500), (667, 250, 667, 500)),
                        6: ((0, 250, 1000, 250), (333, 0, 333, 500), (667, 0, 667, 500)),
                        7: ((0, 250, 1000, 250), (333, 0, 333, 250), (667, 0, 667, 250), (250, 250, 250, 500), (500, 250, 500, 500), (750, 250, 750, 500)),
                        8: ((0, 250, 1000, 250), (250, 0, 250, 500), (500, 0, 500, 500), (750, 0, 750, 500)),
                        9: ((0, 167, 1000, 167), (0, 333, 1000, 333), (333, 0, 333, 500), (667, 0, 667, 500))}
        
        # Get Region Data
        nrs = self.cities_var.get()
        reg = regions[nrs]
        
        # Disable Start Button
        self.go_button.config(state=tk.DISABLED)
        
        # Start by Having One Asymptomatic Person, And Draw Him
        self.asympt[1] = Person(asympt=True, ip=self.ift_var.get(), ttr=self.ttr_var.get(), 
                                incp=self.inc_var.get(), pas=self.pas_var.get(), dp=self.dr_var.get(), xlim=reg[0][0], ylim=reg[0][1],
                                n_reg=nrs, cur_reg=1, trav_freq=self.tf_var.get())
        self.canvas.create_oval(self.asympt[1].x, self.asympt[1].y, self.asympt[1].x+10, self.asympt[1].y+10, fill="#FFFF00", outline=None)
        
        # Populate the Remaining People as Healthy
        for cnt, i in enumerate(range(2, self.pop_var.get()+1)):
            self.healthy[i] = Person(ip=self.ift_var.get(), ttr=self.ttr_var.get(), 
                                     incp=self.inc_var.get(), pas=self.pas_var.get(),
                                     dp=self.dr_var.get(), xlim=reg[cnt%nrs][0], ylim=reg[cnt%nrs][1],
                                     n_reg=nrs, cur_reg=cnt%nrs+1, trav_freq=self.tf_var.get())
            self.canvas.create_oval(self.healthy[i].x, self.healthy[i].y, self.healthy[i].x+10, self.healthy[i].y+10, fill="#0000FF", outline=None)
        
        # Draw Regions
        self.canvas.create_line(3, 3, 1000, 3, width=4)
        self.canvas.create_line(3, 3, 3, 500, width=4)
        self.canvas.create_line(1000, 0, 1000, 500, width=4)
        self.canvas.create_line(0, 500, 1000, 500, width=4)
        
        for line in region_lines[self.cities_var.get()]:
            self.canvas.create_line(line[0], line[1], line[2], line[3], width=4)
        
        # Continue to Update the Simulation
        self.run_simulation = True
        while self.run_simulation:
            self.update_simulation()
            
    
    def update_simulation(self):
        # Move all of the recovered people
        new_traveling = []
        for person in self.recovered.keys():
            self.recovered[person].update()
            self.canvas.coords(person, self.recovered[person].x, self.recovered[person].y, self.recovered[person].x+10, self.recovered[person].y+10)
            if self.recovered[person].traveling:
                new_traveling.append(person)
                
        # Update all of the Symptomatic People
        danger_x, danger_y = [], []
        new_recovered, new_dead = [], []
        for person in self.sympt.keys():
            self.sympt[person].update()
            self.canvas.coords(person, self.sympt[person].x, self.sympt[person].y, self.sympt[person].x+10, self.sympt[person].y+10)
            # Reassign Symptomatic People to the Recovered Class
            if self.sympt[person].recovered:
                new_recovered.append(person)
                self.canvas.itemconfig(person, fill="#00FF00")
            # Reassign Symptomatic People to the Dead Class
            elif self.sympt[person].dead:
                new_dead.append(person)
                self.canvas.itemconfig(person, fill="#000000")
            # They are still symptomatic, record their infection radius
            else:
                danger_x.append((self.sympt[person].x-self.size/2, self.sympt[person].x+self.size/2))
                danger_y.append((self.sympt[person].y-self.size/2, self.sympt[person].y+self.size/2))
                
        # Update all of the Asymptomatic People
        new_sympt = []
        for person in self.asympt.keys():
            self.asympt[person].update()
            self.canvas.coords(person, self.asympt[person].x, self.asympt[person].y, self.asympt[person].x+10, self.asympt[person].y+10)
            # Reassign People to the Symptomatic Class
            if self.asympt[person].sympt:
                new_sympt.append(person)
                self.canvas.itemconfig(person, fill="#FF0000")
            elif self.asympt[person].recovered:
                new_recovered.append(person)
                self.canvas.itemconfig(person, fill="#00FF00")
            elif self.asympt[person].dead:
                new_dead.append(person)
                self.canvas.itemconfig(person, fill="#000000")
            if (self.asympt[person].sympt or self.asympt[person].asympt):
                # Add their location to the recorded danger areas
                danger_x.append((self.asympt[person].x-self.size/2, self.asympt[person].x+self.size/2))
                danger_y.append((self.asympt[person].y-self.size/2, self.asympt[person].y+self.size/2))
                
        # Update Healthy People
        new_asympt = []
        for person in self.healthy.keys():
            # Check if a Healthy Person is Encountering a Sick Person
            encountering = False
            for j in range(len(danger_x)):
                if self.healthy[person].x > danger_x[j][0] and self.healthy[person].x < danger_x[j][1] and self.healthy[person].y > danger_y[j][0] and self.healthy[person].y < danger_y[j][1]:
                    encountering = True
                    break
            # Update the persons health status and location
            self.healthy[person].update(encountering)
            self.canvas.coords(person, self.healthy[person].x, self.healthy[person].y, self.healthy[person].x+10, self.healthy[person].y+10)
            if self.healthy[person].asympt:
                new_asympt.append(person)
                self.canvas.itemconfig(person, fill="#FFFF00")
                
        # Move people to the correct lists based on their change in status
        for person in new_recovered:
            # Symptomatic Person Recovered
            try:
                self.recovered[person] = self.sympt[person]
                del self.sympt[person]
            # Asymptomatic Person Recovered
            except KeyError:
                self.recovered[person] = self.asympt[person]
                del self.asympt[person]
        for person in new_dead:
            # Symptomatic Person Dies
            try:
                self.dead[person] = self.sympt[person]
                del self.sympt[person]
            except KeyError:
                self.dead[person] = self.asympt[person]
                del self.asympt[person]
        for person in new_sympt:
            self.sympt[person] = self.asympt[person]
            del self.asympt[person]
        for person in new_asympt:
            self.asympt[person] = self.healthy[person]
            del self.healthy[person]
            
        # Redraw canvas
        self.canvas.update()
            
        
    def close(self):
        self.root.destroy()
        
if __name__ == "__main__":
    obj = Disease_Simulator()
    
    