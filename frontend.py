import tkinter as tk
from backend import Society, Person

class Disease_Simulator:
    def __init__(self):
        # Define Region Boundaries
        self.region_lines = {1: (()), 2: ((500, 0, 500, 500),), 3: ((333, 0, 333, 500), (667, 0, 667, 500)),
                        4: ((500, 0, 500, 500), (0, 250, 1000, 250)), 
                        5: ((500, 0, 500, 250), (0, 250, 1000, 250), (333, 250, 333, 500), (667, 250, 667, 500)),
                        6: ((0, 250, 1000, 250), (333, 0, 333, 500), (667, 0, 667, 500)),
                        7: ((0, 250, 1000, 250), (333, 0, 333, 250), (667, 0, 667, 250), (250, 250, 250, 500), (500, 250, 500, 500), (750, 250, 750, 500)),
                        8: ((0, 250, 1000, 250), (250, 0, 250, 500), (500, 0, 500, 500), (750, 0, 750, 500)),
                        9: ((0, 167, 1000, 167), (0, 333, 1000, 333), (333, 0, 333, 500), (667, 0, 667, 500))}
        
        self.store_locations = {1: ((500, 250),), 2: ((250, 250), (750, 250)), 3: ((167, 250), (500, 250), (833, 250)),
                                4: ((250, 125), (750, 125), (250, 375), (750, 375)),
                                5: ((250, 125), (750, 125), (167, 375), (500, 375), (833, 375)),
                                6: ((167, 125), (500, 125), (833, 125), (167, 375), (500, 375), (833, 375)),
                                7: ((167, 125), (500, 125), (833, 125), (125, 375), (375, 375), (625, 375), (875, 375)),
                                8: ((125, 125), (375, 125), (625, 125), (875, 125), (125, 375), (375, 375), (625, 375), (875, 375)),
                                9: ((167, 83), (500, 83), (833, 83), (167, 250), (500, 250), (833, 250), (167, 417), (500, 417), (833, 417))}
        
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
        quit_button.grid(row=8, column=3)
        
        # Reset Button
        reset_button = tk.Button(self.tog_frame, text="Reset", command=self.reset_simulation)
        reset_button.grid(row=8, column=1)
        
        # Go Button
        self.go_button = tk.Button(self.tog_frame, text="Start Simulation", command=self.start_simulation)
        self.go_button.grid(row=8, column=0)
        
        # Population Label
        pop_label = tk.Label(self.tog_frame, text="Population:")
        pop_label.grid(row=0, column=0)
        
        # Population Slider
        self.pop_var = tk.IntVar()
        pop_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=100, to=1000, variable=self.pop_var, length=370)
        pop_slider.grid(row=0, column=1, columnspan=3)
        
        # Cities Label
        cities_label = tk.Label(self.tog_frame, text="# of Regions:")
        cities_label.grid(row=1, column=0)
        
        # Cities Slider
        self.cities_var = tk.IntVar()
        cities_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=1, to=9, variable=self.cities_var)
        cities_slider.grid(row=1, column=1)
        
        # Death Rate Label
        dr_label = tk.Label(self.tog_frame, text="Death Rate (%):")
        dr_label.grid(row=1, column=2)
        
        # Death Rate Slider
        self.dr_var = tk.DoubleVar()
        dr_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=100, resolution=0.5, variable=self.dr_var)
        dr_slider.grid(row=1, column=3)
        
        # Restrict Travel Label
        rt_label = tk.Label(self.tog_frame, text="% Infected Before Restricting Travel:")
        rt_label.grid(row=2, column=0)
        
        # Restrict Travel Slider
        self.rt_var = tk.IntVar()
        rt_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=100, variable=self.rt_var)
        rt_slider.grid(row=2, column=1)
        
        # Travel Frequency Label
        tf_label = tk.Label(self.tog_frame, text="Travel Frequency")
        tf_label.grid(row=2, column=2)
        
        # Travel Frequency Slider
        self.tf_var = tk.DoubleVar()
        tf_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=1, resolution=0.01, variable=self.tf_var)
        tf_slider.grid(row=2, column=3)
        
        # Infectability Label
        ift_label = tk.Label(self.tog_frame, text="Probability of Infection:")
        ift_label.grid(row=3, column=0)
        
        # Infectability Slider
        self.ift_var = tk.IntVar()
        ift_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=1, to=100, variable=self.ift_var)
        ift_slider.grid(row=3, column=1)
        
        # Percent Asymptomatic Label
        pas_label = tk.Label(self.tog_frame, text="% of Asymptomatic Cases:")
        pas_label.grid(row=3, column=2)
        
        # Percent Asymptomatic Slider
        self.pas_var = tk.IntVar()
        pas_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=100, variable=self.pas_var)
        pas_slider.grid(row=3, column=3)
        
        # Incubation Period Label
        inc_label = tk.Label(self.tog_frame, text="Incubation Period:")
        inc_label.grid(row=4, column=0)
        
        # Incubation Period Slider
        self.inc_var = tk.IntVar()
        inc_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=1, to=30, variable=self.inc_var)
        inc_slider.grid(row=4, column=1)
        
        # Average Time to Recover Label
        ttr_label = tk.Label(self.tog_frame, text="Time Taken to Recover:")
        ttr_label.grid(row=4, column=2)
        
        # Average Time to Recover Slider
        self.ttr_var = tk.IntVar()
        ttr_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=1, to=30, variable=self.ttr_var)
        ttr_slider.grid(row=4, column=3)
        
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
        self.cl_var = tk.BooleanVar()
        cl_check = tk.Checkbutton(self.tog_frame, variable=self.cl_var)
        cl_check.grid(row=6, column=1)
        
        # Central Location Frequency Label
        clf_label = tk.Label(self.tog_frame, text="Visitation Frequency:")
        clf_label.grid(row=6, column=2)
        
        # Central Location Frequency Slider
        self.clf_var = tk.DoubleVar()
        clf_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=1, resolution=0.01, variable=self.clf_var)
        clf_slider.grid(row=6, column=3)
        
        # Social Distancing Delay Label
        sdd_label = tk.Label(self.tog_frame, text="% Infected before Social Distancing")
        sdd_label.grid(row=7, column=0)
        
        # Social Distancing Delay Slider
        self.sdd_var = tk.IntVar()
        sdd_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=1, variable=self.sdd_var)
        sdd_slider.grid(row=7, column=1)
        
        # SD Proportion Label
        sdp_label = tk.Label(self.tog_frame, text="% of People Social Distancing")
        sdp_label.grid(row=7, column=2)
        
        # SD Proportion Slider
        self.sdp_var = tk.IntVar()
        sdp_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=100, variable=self.sdp_var)
        sdp_slider.grid(row=7, column=3)
        
        self.root.mainloop()
        
        
    def start_simulation(self):
        # Disable Start Button
        self.go_button.config(state=tk.DISABLED)
        
        # Create Society Object
        self.society = Society(self.pop_var.get(), self.cities_var.get(), 
                               self.rt_var.get(), self.tf_var.get(),
                               self.ift_var.get(), self.pas_var.get(),
                               self.ttr_var.get(), self.inc_var.get(),
                               self.dr_var.get(), self.sdp_var.get(),
                               self.quar_var.get(), self.quard_var.get(),
                               self.cl_var.get(), self.clf_var.get())
        
        # Run Update Loop
        self.run_simulation = True
        while self.run_simulation:
            self.update_simulation()
            self.society.update_society()
            
            
    def reset_simulation(self):
        # Break Update Loop
        self.run_simulation = False
        
        # Enable Start Button
        self.go_button.config(state=tk.ACTIVE)
        
        # Reset Canvas
        self.canvas.destroy()
        self.canvas = tk.Canvas(self.sim_frame, width=1000, height=500)
        self.canvas.grid(row=0, column=0)
        
        
    def update_simulation(self):
        # Clear Existing Items from Canvas
        self.canvas.delete("all")
        
        # Draw Region Boundaries
        self.canvas.create_line(3, 3, 1000, 3, width=4)
        self.canvas.create_line(3, 3, 3, 500, width=4)
        self.canvas.create_line(1000, 0, 1000, 500, width=4)
        self.canvas.create_line(0, 500, 1000, 500, width=4)
        
        for line in self.region_lines[self.cities_var.get()]:
            self.canvas.create_line(line[0], line[1], line[2], line[3], width=4)
            
        # Draw Central Locations
        if self.cl_var.get():
            for store in self.store_locations[self.cities_var.get()]:
                self.canvas.create_rectangle(store[0]-5, store[1]-5, store[0]+5, store[1]+5, fill="orange", width=1.5)
        
        # Draw Each Person
        for person in self.society.people[1:]:
            if person.healthy:
                color = "#0000FF"
            elif person.asympt:
                color = "#FFFF00"
            elif person.sympt:
                color = "#FF0000"
            elif person.recovered:
                color = "#00FF00"
            elif person.dead:
                color = "#000000"
            self.canvas.create_oval(person.x, person.y, person.x+10, person.y+10, fill=color, outline=None)
            
        self.canvas.update()
            
    def close(self):
        # Kill Update Loop
        self.run_simulation = False
        self.root.destroy()
        
if __name__ == "__main__":
    obj = Disease_Simulator()
    
    