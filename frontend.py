import numpy as np
import tkinter as tk
import tkinter.font as tkFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from backend import Society

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
        self.sim_frame.grid(row=0, column=0, columnspan=3)
        
        # Canvas
        self.canvas = tk.Canvas(self.sim_frame, width=1000, height=500)
        self.canvas.grid(row=0, column=0)
        
        ### Toggle Frame ###
        self.tog_frame = tk.Frame(self.mainframe)
        self.tog_frame.grid(row=1, column=1, rowspan=3)
        
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
        pop_slider.set(500)
        
        # Cities Label
        cities_label = tk.Label(self.tog_frame, text="# of Regions:")
        cities_label.grid(row=1, column=0)
        
        # Cities Slider
        self.cities_var = tk.IntVar()
        cities_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=1, to=9, variable=self.cities_var)
        cities_slider.grid(row=1, column=1)
        cities_slider.set(5)
        
        # Death Rate Label
        dr_label = tk.Label(self.tog_frame, text="Death Rate (%):")
        dr_label.grid(row=1, column=2)
        
        # Death Rate Slider
        self.dr_var = tk.DoubleVar()
        dr_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=100, resolution=0.5, variable=self.dr_var)
        dr_slider.grid(row=1, column=3)
        dr_slider.set(1.5)
        
        # Restrict Travel Label
        rt_label = tk.Label(self.tog_frame, text="% Infected Before Restricting Travel:")
        rt_label.grid(row=2, column=0)
        
        # Restrict Travel Slider
        self.rt_var = tk.IntVar()
        rt_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=100, variable=self.rt_var)
        rt_slider.grid(row=2, column=1)
        rt_slider.set(10)
        
        # Travel Frequency Label
        tf_label = tk.Label(self.tog_frame, text="Travel Frequency")
        tf_label.grid(row=2, column=2)
        
        # Travel Frequency Slider
        self.tf_var = tk.DoubleVar()
        tf_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=1, resolution=0.01, variable=self.tf_var)
        tf_slider.grid(row=2, column=3)
        tf_slider.set(0.1)
        
        # Infectability Label
        ift_label = tk.Label(self.tog_frame, text="Probability of Infection:")
        ift_label.grid(row=3, column=0)
        
        # Infectability Slider
        self.ift_var = tk.IntVar()
        ift_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=1, to=100, variable=self.ift_var)
        ift_slider.grid(row=3, column=1)
        ift_slider.set(15)
        
        # Percent Asymptomatic Label
        pas_label = tk.Label(self.tog_frame, text="% of Asymptomatic Cases:")
        pas_label.grid(row=3, column=2)
        
        # Percent Asymptomatic Slider
        self.pas_var = tk.IntVar()
        pas_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=100, variable=self.pas_var)
        pas_slider.grid(row=3, column=3)
        pas_slider.set(50)
        
        # Incubation Period Label
        inc_label = tk.Label(self.tog_frame, text="Incubation Period:")
        inc_label.grid(row=4, column=0)
        
        # Incubation Period Slider
        self.inc_var = tk.IntVar()
        inc_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=1, to=140, variable=self.inc_var)
        inc_slider.grid(row=4, column=1)
        inc_slider.set(14)
        
        # Average Time to Recover Label
        ttr_label = tk.Label(self.tog_frame, text="Time Taken to Recover:")
        ttr_label.grid(row=4, column=2)
        
        # Average Time to Recover Slider
        self.ttr_var = tk.IntVar()
        ttr_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=1, to=150, variable=self.ttr_var)
        ttr_slider.grid(row=4, column=3)
        ttr_slider.set(48)
        
        # Quarantine Label
        quar_label = tk.Label(self.tog_frame, text="Quarantine the Sick:")
        quar_label.grid(row=5, column=0)
        
        # Quarantine Checkbox
        self.quar_var = tk.BooleanVar()
        quar_check = tk.Checkbutton(self.tog_frame, variable=self.quar_var)
        quar_check.grid(row=5, column=1)
        quar_check.select()
        
        # Quarantine Delay Label
        quard_label = tk.Label(self.tog_frame, text="Quarantine Delay:")
        quard_label.grid(row=5, column=2)
        
        # Quarantine Delay Slider
        self.quard_var = tk.IntVar()
        quard_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=30, variable=self.quard_var)
        quard_slider.grid(row=5, column=3)
        quard_slider.set(7)
        
        # Central Location Label
        cl_label = tk.Label(self.tog_frame, text="Central Location:")
        cl_label.grid(row=6, column=0)
        
        # Central Location Checkbox
        self.cl_var = tk.BooleanVar()
        cl_check = tk.Checkbutton(self.tog_frame, variable=self.cl_var)
        cl_check.grid(row=6, column=1)
        cl_check.select()
        
        # Central Location Frequency Label
        clf_label = tk.Label(self.tog_frame, text="Visitation Frequency:")
        clf_label.grid(row=6, column=2)
        
        # Central Location Frequency Slider
        self.clf_var = tk.DoubleVar()
        clf_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=1, resolution=0.01, variable=self.clf_var)
        clf_slider.grid(row=6, column=3)
        clf_slider.set(0.15)
        
        # Social Distancing Delay Label
        sdd_label = tk.Label(self.tog_frame, text="% Infected before Social Distancing")
        sdd_label.grid(row=7, column=0)
        
        # Social Distancing Delay Slider
        self.sdd_var = tk.IntVar()
        sdd_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=100, variable=self.sdd_var)
        sdd_slider.grid(row=7, column=1)
        sdd_slider.set(15)
        
        # SD Proportion Label
        sdp_label = tk.Label(self.tog_frame, text="% of People Social Distancing")
        sdp_label.grid(row=7, column=2)
        
        # SD Proportion Slider
        self.sdp_var = tk.IntVar()
        sdp_slider = tk.Scale(self.tog_frame, orient=tk.HORIZONTAL, from_=0, to=100, variable=self.sdp_var)
        sdp_slider.grid(row=7, column=3)
        sdp_slider.set(90)
        
        # Title Font
        title_font = tkFont.Font(family="Helvetica", size=16)
        
        ### Indicator Frame ###
        self.indicator_frame = tk.Frame(self.mainframe)
        self.indicator_frame.grid(row=1, column=2)
        
        # Travel Indicator Label
        travel_ind_label = tk.Label(self.indicator_frame, text="Travel:")
        travel_ind_label.grid(row=0, column=0)
        
        # Travel Indicator Light
        self.travel_ind_canvas = tk.Canvas(self.indicator_frame, width=25, height=25)
        self.travel_ind_canvas.grid(row=0, column=1)
        self.travel_ind_canvas.create_rectangle(0, 0, 25, 25, fill="#00FF00")
        
        # Social Distance Label
        sd_ind_label = tk.Label(self.indicator_frame, text="Social Distancing:")
        sd_ind_label.grid(row=0, column=2)
        
        # Social Distance Light
        self.sd_ind_canvas = tk.Canvas(self.indicator_frame, width=25, height=25)
        self.sd_ind_canvas.grid(row=0, column=3)
        self.sd_ind_canvas.create_rectangle(0, 0, 25, 25, fill="#FF0000")
        
        ### Quarantine Frame ###
        self.quarantine_frame = tk.Frame(self.mainframe)
        self.quarantine_frame.grid(row=2, column=2)
        
        # Quarantine Label
        quar_label = tk.Label(self.quarantine_frame, text="Quarantine Zone:", font=title_font)
        quar_label.grid(row=0, column=0)
        
        # Quarantine Canvas
        self.quar_canvas = tk.Canvas(self.quarantine_frame, width=100, height=100)
        self.quar_canvas.grid(row=0, column=1)
        
        ### Legend Frame ###
        legend_frame = tk.Frame(self.mainframe)
        legend_frame.grid(row=3, column=2, sticky=tk.N+tk.W)
        
        # Legend Title
        legend_title = tk.Label(legend_frame, text="Legend:", font=title_font)
        legend_title.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        
        # Healthy Canvas
        healthy_canvas = tk.Canvas(legend_frame, width=25, height=25)
        healthy_canvas.grid(row=1, column=0, sticky=tk.W)
        
        # Add Item to Healthy Canvas
        healthy_canvas.create_oval(5, 5, 25, 25, fill="#0000FF", outline=None)
        
        # Add Label to Healthy Item
        healthy_label = tk.Label(legend_frame, text="Healthy Person")
        healthy_label.grid(row=1, column=1)
        
        # Asmptomatic Canvas
        asympt_canvas = tk.Canvas(legend_frame, width=25, height=25)
        asympt_canvas.grid(row=2, column=0, sticky=tk.W)
        
        # Add Item to Asymptomatic Canvas
        asympt_canvas.create_oval(5, 5, 25, 25, fill="#FFFF00", outline=None)
        
        # Add Label to Asymptomatic Item
        asympt_label = tk.Label(legend_frame, text="Asymptomatic Person")
        asympt_label.grid(row=2, column=1)
        
        # Symptomatic Canvas
        sympt_canvas = tk.Canvas(legend_frame, width=25, height=25)
        sympt_canvas.grid(row=3, column=0, sticky=tk.W)
        
        # Add Item to Symptomatic Canvas
        sympt_canvas.create_oval(5, 5, 25, 25, fill="#FF0000", outline=None)
        
        # Add Label to Symptomatic Item
        sympt_label = tk.Label(legend_frame, text="Symptomatic Person")
        sympt_label.grid(row=3, column=1)
        
        # Recovered Canvas
        recovered_canvas = tk.Canvas(legend_frame, width=25, height=25)
        recovered_canvas.grid(row=4, column=0, sticky=tk.W)
        
        # Add Item to Recovered Canvas
        recovered_canvas.create_oval(5, 5, 25, 25, fill="#00FF00", outline=None)
        
        # Add Label to Recovered Item
        recovered_label = tk.Label(legend_frame, text="Recovered Person")
        recovered_label.grid(row=4, column=1)
        
        # Dead Canvas
        dead_canvas = tk.Canvas(legend_frame, width=25, height=25)
        dead_canvas.grid(row=5, column=0, sticky=tk.W)
        
        # Add Item to Dead Canvas
        dead_canvas.create_oval(5, 5, 25, 25, fill="#000000", outline=None)
        
        # Add Label to Dead Item
        dead_label = tk.Label(legend_frame, text="Dead Person")
        dead_label.grid(row=5, column=1)
        
        # Store Canvas
        store_canvas = tk.Canvas(legend_frame, width=25, height=25)
        store_canvas.grid(row=6, column=0, sticky=tk.W)
        
        # Add Item to Store Canvas
        store_canvas.create_rectangle(5, 5, 25, 25, fill="orange", width=1.5)
        
        # Add Label to Store Item
        store_label = tk.Label(legend_frame, text="Central Location")
        store_label.grid(row=6, column=1)
        
        # Region Canvas
        region_canvas = tk.Canvas(legend_frame, width=25, height=25)
        region_canvas.grid(row=7, column=0, sticky=tk.W)
        
        # Add Item to Region Canvas
        region_canvas.create_rectangle(5, 5, 25, 25, fill="", width=4)
        
        # Add Label to Region Item
        region_label = tk.Label(legend_frame, text="Region Boundary")
        region_label.grid(row=7, column=1)
        
        ### Plot Frame ###
        # Don't Create Plotting Object Until Start to Get Accurate Pop Num
        self.plot_frame = tk.Frame(self.mainframe)
        self.plot_frame.grid(row=1, column=0, rowspan=10)
        
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
                               self.cl_var.get(), self.clf_var.get(),
                               self.sdd_var.get())
        
        # Keep Track of Indicator Variables
        self.can_travel = self.society.travel_permitted
        self.must_social_distance = self.society.social_distancing
        
        # Setup Graphing Plot
        # Create Plotting Object
        self.plotter = Plotter((4, 4), self.pop_var.get())
        
        # Create Plotting Element
        self.plot_widget = FigureCanvasTkAgg(self.plotter.fig, master=self.plot_frame)
        self.plot_widget.draw()
        self.plot_widget.get_tk_widget().grid(row=0, column=0, rowspan=10)
        
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
        
        # Reset Graphing Element
        self.plot_widget.get_tk_widget().destroy()
        
        # Reset Canvases
        self.canvas.destroy()
        self.canvas = tk.Canvas(self.sim_frame, width=1000, height=500)
        self.canvas.grid(row=0, column=0)
        
        self.quar_canvas.destroy()
        self.quar_canvas = tk.Canvas(self.quarantine_frame, width=100, height=100)
        self.quar_canvas.grid(row=0, column=1)
        
        self.travel_ind_canvas.destroy()
        self.travel_ind_canvas = tk.Canvas(self.indicator_frame, width=25, height=25)
        self.travel_ind_canvas.grid(row=0, column=1)
        self.travel_ind_canvas.create_rectangle(0, 0, 25, 25, fill="#00FF00")
        
        self.sd_ind_canvas.destroy()
        self.sd_ind_canvas = tk.Canvas(self.indicator_frame, width=25, height=25)
        self.sd_ind_canvas.grid(row=0, column=3)
        self.sd_ind_canvas.create_rectangle(0, 0, 25, 25, fill="#FF0000")
        
        
    def update_simulation(self):
        # Clear Existing Items from Canvas
        self.canvas.delete("all")
        self.quar_canvas.delete("all")
        
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
                
        # Draw Quarantine Boundaries
        self.quar_canvas.create_line(4, 4, 100, 4, width=4)
        self.quar_canvas.create_line(4, 4, 4, 100, width=4)
        self.quar_canvas.create_line(100, 0, 100, 100, width=4)
        self.quar_canvas.create_line(0, 100, 100, 100, width=4)
        
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
            # Update Non-Quarantined Canvas
            if not person.quarantined:
                self.canvas.create_oval(person.x, person.y, person.x+10, person.y+10, fill=color, outline=None)
            
            # Update Quarantined Canvas
            elif self.quar_var.get():
                self.quar_canvas.create_oval(person.x, person.y, person.x+10, person.y+10, fill=color, outline=None)
                
                
        # Update Indicator Lights (only if values have changed)
        if self.society.travel_permitted != self.can_travel:
            self.can_travel = self.society.travel_permitted
            self.travel_ind_canvas.delete("all")
            if self.society.travel_permitted:
                trav_col = "#00FF00"
            else:
                trav_col = "#FF0000"
            self.travel_ind_canvas.create_rectangle(0, 0, 25, 25, fill=trav_col)
            self.travel_ind_canvas.update()
        
        if self.society.social_distancing != self.must_social_distance:
            self.must_social_distance = self.society.social_distancing
            self.sd_ind_canvas.delete("all")
            if self.society.social_distancing:
                sd_col = "#00FF00"
            else:
                sd_col = "#FF0000"
            self.sd_ind_canvas.create_rectangle(0, 0, 25, 25, fill=sd_col)
            self.sd_ind_canvas.update()
            
        self.canvas.update()
        self.quar_canvas.update()
        
        # Update Plot
        self.plotter.update_plot(len(self.society.healthy), len(self.society.asympt), 
                                 len(self.society.sympt), len(self.society.recovered),
                                 len(self.society.dead))
        self.plot_widget.draw()
        
            
    def close(self):
        # Kill Update Loop
        self.run_simulation = False
        self.root.destroy()
        
        
class Plotter:
    """
    The Plotter class is responsible for creating and maintaining a graphical
    representation of how the infection is spreading through the society. It
    makes extensive use of the matplotlib library for python.
    """
    
    def __init__(self, figsize, ylim=500):
        """
        The constructor creates the plotting environment including the figure
        and axis objects and prepares to collect all of the disease data.
        
        Parameters:
        -----------
        figsize : tuple
            A tuple with two elements representing the width and height of the
            figure object to be created.
            
        ylim : int
            The total number of memebers of the society.
        """
        # Create and Configure the Figure and Axis Objects
        self.fig = plt.figure(figsize=figsize, dpi=100, tight_layout=True)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Number of People")
        self.ax.set_title("Infection Curves")
        self.ax.set_ylim(0, ylim)
        self.ax.set_xticklabels([])
        self.ax.set_xticks([])
        
        # Prepare to Collect and Store the Demographic Data
        self.time = 0
        
        self.times = [0]
        self.healthy = [ylim-1]
        self.asympt = [1]
        self.sympt = [0]
        self.recovered = [0]
        self.dead = [0]
        
        self.ax.plot([],[])
        
    def update_plot(self, h, a, s, r, d):
        """
        The update_plot method is used to change the plot to reflect the current
        state of the society. This means passing the new demographic data to the 
        method and getting an updated version of the axis object back.
        
        Parameters:
        -----------
        h : int
            The new number of healthy people at the current time.
            
        a : int
            The new number of asymptomatic people at the current time.
            
        s : int
            The new number of symptomatic people at the current time.
            
        r : int
            The new number of recovered people at the current time.
            
        d : int
            The new number of dead people at the current time.
        """
        # Remove Old Plots from the Axis
        self.ax.cla()
        
        # Set the Labels, Axes and Title
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Number of People")
        self.ax.set_title("Infection Curves")
        self.ax.set_xticklabels([])
        self.ax.set_xticks([])
        
        # Increment the x value
        self.time += 1
        self.times.append(self.time)
        
        # Plot the Entire Set of x values
        self.ax.set_xlim((0, self.times[-1]))
        
        # Save all the Demographic Data
        self.healthy.append(h)
        self.asympt.append(a)
        self.sympt.append(s)
        self.recovered.append(r)
        self.dead.append(d)
        
        # Plot the Demographic Data
        self.ax.plot(self.times, self.healthy, c="#0000FF", zorder=5, linewidth=2, label="Healthy")
        self.ax.plot(self.times, self.asympt, c="#FFFF00", zorder=4, linewidth=2, label="Asymptomatic")
        self.ax.plot(self.times, self.sympt, c="#FF0000", zorder=3, linewidth=2, label="Symptomatic")
        self.ax.plot(self.times, self.recovered, c="#00FF00", zorder=2, linewidth=2, label="Recovered")
        self.ax.plot(self.times, self.dead, c="#000000", zorder=1, linewidth=2, label="Dead")

        
if __name__ == "__main__":
    obj = Disease_Simulator()
    
    