import tkinter as tk
import random
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

#Function which is used to control most of the heating actions
def control_heating(temperatures, desired_temperatures, heat_loss_values,temp_outside, time_gradient):
    heating_temp=30
    actions = []
    #Rule 4: If the outdoor temperature is below a 15 celsius degrees check temperatures of the rooms and decide if heating needs to be turned on/off
    if temp_outside<15:
        for room, desired_temperature in desired_temperatures.items():
            temperature = temperatures[room]
            heat_loss = heat_loss_values[room]
            #Rule 1 If the current temperature is below the desired temperature, turn on the heating.
            if temperature < desired_temperature:
                actions.append(f"Turn on heating for {room}")
                #Estimation how temperature in the room changes after action
                #In real-world scenario function would change current room temparature from thermostat reading at the beggining of the function
                temperatures[room]+= heating_temp/(heat_loss*25)*(time_gradient/60)
            #Rule 2: If the current temperature is above the desired temperature, turn off the heating.
            else:
                actions.append(f"No heating needed for {room}")
                #Estimation how temperature in the room changes after action
                #In real-world scenario function would change current room temparature from thermostat reading at the beggining of the function
                temperatures[room]-= heating_temp*(heat_loss/0.25)*(time_gradient/60)
                if temperatures[room]<temp_outside:
                    temperatures[room]==temp_outside
    #Rule 3: If the outdoor temperature is above a certain threshold, turn off the heating.
    else:
        actions.append("No heating needed")
    return actions


class MyApp:
    def __init__(self, root):
        self.root = root
        self.running = False

        #Heating limit in minutes, default value is -1 which means no limit
        self.heating_limit=-1
        self.temperature_history = pd.DataFrame({
            "Timeframe": [],
            "Living Room": [],
            "Bedroom": [],
            "Kitchen": [],
            "Bathroom": []
        })
        self.step = 0
        self.previous_actions = 0

        # Define the initial temperatures for each room
        self.room_temperatures = {
            "Living Room": round(random.uniform(10, 25), 2),
            "Bedroom": round(random.uniform(10, 25), 2),
            "Kitchen": round(random.uniform(10, 25), 2),
            "Bathroom": round(random.uniform(10, 25), 2)
        }

        # Generate random desired temperatures for each room
        self.desired_temperatures = {
            "Living Room": round(random.uniform(15, 30), 2),
            "Bedroom": round(random.uniform(15, 30), 2),
            "Kitchen": round(random.uniform(15, 30), 2),
            "Bathroom": round(random.uniform(15, 30), 2)
        }

        # Generate random heat loss values for each room
        self.heat_loss_values = {
            "Living Room": round(random.uniform(0.01, 0.99), 2),
            "Bedroom": round(random.uniform(0.01, 0.99), 2),
            "Kitchen": round(random.uniform(0.01, 0.99), 2),
            "Bathroom": round(random.uniform(0.01, 0.99), 2)
        }
        self.temp_outside=10

        # Add the current temperature grid
        self.grid0 = tk.LabelFrame(root, text="Current Temperature (Celsius)")
        self.grid0.grid(row=0, column=0, padx=10, pady=10)
        #self.temperature_entries = self.create_labels_and_inputs(self.grid0, self.room_temperatures)
        self.temperature_labels = {}
        for i, (room, temp) in enumerate(self.room_temperatures.items()):
            label = tk.Label(self.grid0, text=f"{room}: {temp}")
            label.grid(row=i, column=0, padx=5, pady=5)
            self.temperature_labels[room] = label

        # Add the desired temperature grid
        self.grid1 = tk.LabelFrame(root, text="Desired Temperature (Celsius)")
        self.grid1.grid(row=0, column=1, padx=10, pady=10)
        self.temperature_entries = self.create_labels_and_inputs(self.grid1, self.desired_temperatures)
        
        # Add the heating loss grid
        self.grid2 = tk.LabelFrame(root, text="Heating Loss (0.01-0.99)")
        self.grid2.grid(row=0, column=2, padx=10, pady=10)
        self.heat_loss_entries = self.create_labels_and_inputs(self.grid2, self.heat_loss_values)

        # Heating limit
        label = tk.Label(root, text="Heating limit (Minutes)")
        label.grid(row=1,column=1,columnspan=1, padx=5, pady=5)
        self.heating_limit = tk.IntVar(value=1000)
        self.input_text = tk.Spinbox(root, from_=-1, to=50000, width=30, textvariable=self.heating_limit)
        self.input_text.grid(row=2,column=1,columnspan=1, padx=10, pady=10)

        # Time update gradient
        label = tk.Label(root, text="Time update (Seconds)")
        label.grid(row=3,column=1,columnspan=1, padx=5, pady=5)
        self.time_update = tk.IntVar(value=5)
        self.input_text = tk.Spinbox(root, from_=1, to=100, width=30, textvariable=self.time_update)
        self.input_text.grid(row=4, column=1,columnspan=1, padx=10, pady=10)

        
        # Buttons frame
        buttons_frame = tk.Frame(root)
        buttons_frame.grid(row=5, columnspan=3, pady=10)
        
        # Start button
        self.start_button = tk.Button(buttons_frame, text="Start", command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # Stop button
        self.stop_button = tk.Button(buttons_frame, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Save button
        self.save_button = tk.Button(buttons_frame, text="Save actions", command=self.save_to_file)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Plots button
        self.save_button = tk.Button(buttons_frame, text="Plot temp. changes", command=self.show_plots)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # Output text field
        self.output_text = tk.Text(root, height=10, width=100, state="disabled")
        self.output_text.grid(row=6, columnspan=3, padx=10, pady=10)

#Create grid of entries
    def create_labels_and_inputs(self, grid, values):
        labels = self.room_temperatures.keys()
        self.inputs = []
        entries = {}
        for i, label_text in enumerate(labels):
            label = tk.Label(grid, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5)
            
            entry = tk.Entry(grid)
            entry.insert(0, str(values[label_text]))
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.inputs.append(entry)
            entries[label_text] = entry
        return entries
    
#Sets up the parameters and starts the system loop
    def start(self):
        self.output_text.config(state="normal")
        self.limit = self.heating_limit.get()
        self.output_text.delete(1.0, tk.END)
        for room, entry in self.temperature_entries.items():
            self.desired_temperatures[room] = float(entry.get())
            # Update heat loss values from the input fields
        for room, entry in self.heat_loss_entries.items():
            self.heat_loss_values[room] = float(entry.get())
        self.output_text.insert(tk.END, f"Intital Temperatures: {self.room_temperatures}\n")
        self.output_text.insert(tk.END, f"Desired Temperatures: {self.desired_temperatures}\n")
        if not self.running:
            self.running = True
            self.run_system()

#Runs the loop with rule-based system
    def run_system(self):
        if self.limit<=0:
            self.output_text.insert(tk.END, "Heating limit exceeded\n")
            self.running = False
        if self.running:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            self.output_text.insert(tk.END, f"Actions at {current_time}:\n")
            actions = control_heating(self.room_temperatures, desired_temperatures=self.desired_temperatures, heat_loss_values=self.heat_loss_values,temp_outside=self.temp_outside, time_gradient=self.time_update.get())
            i=0
            for action in actions:
                if(self.step==0):
                    self.output_text.insert(tk.END, action + "\n")
                else:
                    if(action==self.previous_actions[i]):
                        room = list(self.desired_temperatures.keys())[i]
                        if "Turn on" in action:
                            self.output_text.insert(tk.END, f"Remain turned on for {room}" + "\n")
                        else:
                            self.output_text.insert(tk.END, f"Remain turned off for {room}" + "\n")
                    else:
                        self.output_text.insert(tk.END, action + "\n")
                    i=i+1
            self.previous_actions=actions
            self.step=self.step+1
            self.room_temperatures = {room: round(temperature, 2) for room, temperature in self.room_temperatures.items()}
            for room, temperature in self.room_temperatures.items():
                self.temperature_history.loc[(self.step-1), str(room)] = temperature
                self.temperature_history.loc[(self.step-1), "Timeframe"] = self.time_update.get()*self.step
            self.output_text.insert(tk.END, "Room Temperatures: " + str(self.room_temperatures) + "\n")
            self.output_text.insert(tk.END, "-------------------\n")
            for room in self.room_temperatures.keys():
                self.temperature_labels[room].config(text=f"{room}: {self.room_temperatures[room]}")
            self.limit-=self.time_update.get()/60
            self.root.after(self.time_update.get()*1000, self.run_system)


    #Functions stops the system        
    def stop(self):
        #Stop the system
        if self.running:
            self.running = False
        #Informs about stopping the system
        self.output_text.insert(tk.END, "System has stopped. Heating turned off\n")
        self.output_text.insert(tk.END, "-------------------\n")
        self.output_text.config(state="disabled")
        #Resets the number of steps to 0
        self.step=0
    
    #Function saves the output of the system to text file
    def save_to_file(self):
        content = self.output_text.get("1.0", tk.END)
        with open("output.txt", "w") as file:
            file.write(content)

    #Function plots the changes of temperatures over time in diffrent rooms     
    def show_plots(self):
        plt.gcf()
        self.temperature_history.set_index('Timeframe', inplace=True)
        for room in self.desired_temperatures.keys():
            plt.plot(self.temperature_history[room], label=room)
        plt.grid()
        plt.axis(ymin=0,ymax=40)
        plt.title("Temperatures changes")
        plt.ylabel('Temperature')
        plt.xlabel('Time (Seconds)')
        plt.legend(loc='best')
        plt.show()

        
root = tk.Tk()
root.title("Intelligent Heating Control")
# set fixed window size value
root.minsize(820, 550)
root.maxsize(820, 550)
#Start the app  
app = MyApp(root)
root.mainloop()