import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class VehicleSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Road Vehicle Dynamics & Fuel Simulation")
        self.root.geometry("900x700")
        self.root.configure(bg='#2C3E50')
        
        # Variables
        self.scenario_var = tk.IntVar(value=1)
        self.entries = {}
        self.entry_widgets = {}  # Store actual Entry widgets
        
        # Create main container
        self.main_frame = tk.Frame(root, bg='#2C3E50')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.show_welcome_screen()
    
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    
    def show_welcome_screen(self):
        """Display welcome screen"""
        self.clear_frame()
        
        # Title frame
        title_frame = tk.Frame(self.main_frame, bg='#34495E', pady=30)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="VEHICLE DYNAMICS SIMULATOR",
            font=('Arial', 28, 'bold'),
            fg='#ECF0F1',
            bg='#34495E'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Advanced Road Vehicle Aerodynamic and Fuel Consumption Analysis",
            font=('Arial', 12),
            fg='#BDC3C7',
            bg='#34495E'
        )
        subtitle_label.pack(pady=5)
        
        # Content frame
        content_frame = tk.Frame(self.main_frame, bg='#2C3E50')
        content_frame.pack(expand=True, fill=tk.BOTH, pady=50)
        
        # Description
        desc_text = """
        
        """
        
        desc_label = tk.Label(
            content_frame,
            text=desc_text,
            font=('Arial', 11),
            fg='#ECF0F1',
            bg='#2C3E50',
            justify=tk.LEFT
        )
        desc_label.pack(pady=20)
        
        # Start button
        start_button = tk.Button(
            content_frame,
            text="START SIMULATION",
            font=('Arial', 16, 'bold'),
            bg='#27AE60',
            fg='white',
            activebackground='#229954',
            activeforeground='white',
            padx=40,
            pady=15,
            cursor='hand2',
            command=self.show_parameter_input
        )
        start_button.pack(pady=30)
        
        # Footer
        footer_label = tk.Label(
            self.main_frame,
            text="KIG2013 - Computer Programming",
            font=('Arial', 9),
            fg='#95A5A6',
            bg='#2C3E50'
        )
        footer_label.pack(side=tk.BOTTOM, pady=10)
    
    def show_parameter_input(self):
        """Display parameter input screen"""
        self.clear_frame()
        
        # Header
        header_frame = tk.Frame(self.main_frame, bg='#34495E', pady=15)
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(
            header_frame,
            text="INPUT PARAMETERS",
            font=('Arial', 22, 'bold'),
            fg='#ECF0F1',
            bg='#34495E'
        )
        header_label.pack()
        
        # Scrollable container
        container = tk.Frame(self.main_frame, bg='#2C3E50')
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        canvas = tk.Canvas(container, bg='#2C3E50', highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)

        scrollable_frame = tk.Frame(canvas, bg='#2C3E50')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        input_frame = scrollable_frame
        
        # Vehicle Parameters Section
        self.create_section_header(input_frame, "VEHICLE PARAMETERS", 0)
        
        vehicle_params = [
            ("Vehicle Mass (kg)", "mass", "1000", "[500-5000]"),
            ("Vehicle Width (m)", "width", "2.0", "[1.0-3.0]"),
            ("Vehicle Height (m)", "height", "2.0", "[1.0-3.0]"),
            ("Vehicle Length (m)", "length", "5.0", "[2.0-8.0]"),
            ("Engine Efficiency", "efficiency", "0.4", "[0.1-0.5]")
        ]
        
        row = 1
        for label, key, default, range_info in vehicle_params:
            self.create_input_row(input_frame, label, key, default, range_info, row)
            row += 1
        
        # Trip Parameters Section
        self.create_section_header(input_frame, "TRIP PARAMETERS", row)
        row += 1
        
        trip_params = [
            ("Travel Distance (km)", "distance", "100", "[1-500]"),
            ("Initial Speed (km/h)", "speed", "90", "[10-200]")
        ]
        
        for label, key, default, range_info in trip_params:
            self.create_input_row(input_frame, label, key, default, range_info, row)
            row += 1
        
        # Scenario Selection Section
        self.create_section_header(input_frame, "DRIVING SCENARIO", row)
        row += 1
        
        scenario_frame = tk.Frame(input_frame, bg='#34495E', padx=20, pady=15)
        scenario_frame.grid(row=row, column=0, columnspan=3, sticky='ew', pady=10, padx=20)
        
        scenarios = [
            ("Urban Driving (Stop-and-go)", 1),
            ("Highway Driving (Acceleration/Deceleration)", 2),
            ("Sport Driving (Variable speed)", 3)
        ]
        
        for text, value in scenarios:
            rb = tk.Radiobutton(
                scenario_frame,
                text=text,
                variable=self.scenario_var,
                value=value,
                font=('Arial', 11),
                fg='#ECF0F1',
                bg='#34495E',
                selectcolor='#2C3E50',
                activebackground='#34495E',
                activeforeground='#ECF0F1'
            )
            rb.pack(anchor='w', pady=5)
        
        row += 1
        
        # Buttons
        button_frame = tk.Frame(input_frame, bg='#2C3E50')
        button_frame.grid(row=row, column=0, columnspan=3, pady=20)
        
        back_button = tk.Button(
            button_frame,
            text="BACK",
            font=('Arial', 12, 'bold'),
            bg='#95A5A6',
            fg='white',
            activebackground='#7F8C8D',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.show_welcome_screen
        )
        back_button.pack(side=tk.LEFT, padx=10)
        
        submit_button = tk.Button(
            button_frame,
            text="RUN SIMULATION",
            font=('Arial', 12, 'bold'),
            bg='#27AE60',
            fg='white',
            activebackground='#229954',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.run_simulation
        )
        submit_button.pack(side=tk.LEFT, padx=10)
    
    def create_section_header(self, parent, text, row):
        """Create section header"""
        header_frame = tk.Frame(parent, bg='#16A085', padx=15, pady=10)
        header_frame.grid(row=row, column=0, columnspan=3, sticky='ew', pady=(20, 10), padx=20)
        
        label = tk.Label(
            header_frame,
            text=text,
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#16A085'
        )
        label.pack(anchor='w')
    
    def create_input_row(self, parent, label_text, key, default_value, range_info, row):
        """Create input field row"""
        # Label
        label = tk.Label(
            parent,
            text=label_text,
            font=('Arial', 11),
            fg='#ECF0F1',
            bg='#2C3E50',
            anchor='w'
        )
        label.grid(row=row, column=0, sticky='w', padx=(40, 10), pady=8)
        
        # Entry
        entry = tk.Entry(
            parent,
            font=('Arial', 11),
            width=15,
            bg='#34495E',
            fg='white',
            insertbackground='white'
        )
        entry.insert(0, default_value)
        entry.grid(row=row, column=1, padx=10, pady=8)
        self.entry_widgets[key] = entry  # Store the Entry widget
        
        # Range info
        range_label = tk.Label(
            parent,
            text=range_info,
            font=('Arial', 9),
            fg='#95A5A6',
            bg='#2C3E50'
        )
        range_label.grid(row=row, column=2, sticky='w', padx=10, pady=8)
    
    def validate_inputs(self):
        """Validate all input parameters"""
        try:
            mass = float(self.entry_widgets['mass'].get())
            if not (500 <= mass <= 5000):
                raise ValueError("Vehicle mass must be between 500 and 5000 kg")
            
            width = float(self.entry_widgets['width'].get())
            if not (1.0 <= width <= 3.0):
                raise ValueError("Vehicle width must be between 1.0 and 3.0 m")
            
            height = float(self.entry_widgets['height'].get())
            if not (1.0 <= height <= 3.0):
                raise ValueError("Vehicle height must be between 1.0 and 3.0 m")
            
            length = float(self.entry_widgets['length'].get())
            if not (2.0 <= length <= 8.0):
                raise ValueError("Vehicle length must be between 2.0 and 8.0 m")
            
            efficiency = float(self.entry_widgets['efficiency'].get())
            if not (0.1 <= efficiency <= 0.5):
                raise ValueError("Engine efficiency must be between 0.1 and 0.5")
            
            distance = float(self.entry_widgets['distance'].get())
            if not (1 <= distance <= 500):
                raise ValueError("Travel distance must be between 1 and 500 km")
            
            speed = float(self.entry_widgets['speed'].get())
            if not (10 <= speed <= 200):
                raise ValueError("Initial speed must be between 10 and 200 km/h")
            
            return True
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return False
    
    def run_simulation(self):
        """Run C++ simulation"""
        if not self.validate_inputs():
            return
        
        params = {}
        for key, entry in self.entry_widgets.items():
            params[key] = entry.get()
        
        # Show loading screen
        self.show_loading_screen()
        
        # Prepare input file
        try:
            with open('vehicle_input.txt', 'w') as f:
                f.write(f"{params['mass']}\n")
                f.write(f"{params['width']}\n")
                f.write(f"{params['height']}\n")
                f.write(f"{params['length']}\n")
                f.write(f"{params['efficiency']}\n")
                f.write(f"{params['distance']}\n")
                f.write(f"{params['speed']}\n")
                f.write(f"{self.scenario_var.get()}\n")
                f.write("1\n")  # Confirmation
            
            # Run C++ executable with input file
            if os.path.exists('vehicle_sim.exe'):
                with open('vehicle_input.txt', 'r') as input_file:
                    result = subprocess.run(
                        ['vehicle_sim.exe'],
                        stdin=input_file,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                
                if result.returncode == 0:
                    self.root.after(1000, self.show_results)
                else:
                    messagebox.showerror("Simulation Error", f"C++ simulation failed:\n{result.stderr}")
                    self.show_parameter_input()
            else:
                messagebox.showerror("Error", "vehicle_sim.exe not found. Please compile the C++ code first.")
                self.show_parameter_input()
                
        except Exception as e:
            messagebox.showerror("Error", f"Simulation failed: {str(e)}")
            self.show_parameter_input()
    
    def show_loading_screen(self):
        """Display loading screen"""
        self.clear_frame()
        
        loading_frame = tk.Frame(self.main_frame, bg='#2C3E50')
        loading_frame.pack(expand=True)
        
        loading_label = tk.Label(
            loading_frame,
            text="RUNNING SIMULATION",
            font=('Arial', 24, 'bold'),
            fg='#ECF0F1',
            bg='#2C3E50'
        )
        loading_label.pack(pady=20)
        
        status_label = tk.Label(
            loading_frame,
            text=" ",
            font=('Arial', 12),
            fg='#95A5A6',
            bg='#2C3E50'
        )
        status_label.pack(pady=10)
        
        self.root.update()
    
    def show_results(self):
        """Display simulation results"""
        self.clear_frame()
        
        try:
            # Read results
            csv_file = f"vehicle_simulation_scenario_{self.scenario_var.get()}.csv"
            
            if not os.path.exists(csv_file):
                messagebox.showerror("Error", f"Results file {csv_file} not found")
                self.show_parameter_input()
                return
            
            # Read CSV and calculate statistics
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            
            if len(data) == 0:
                messagebox.showerror("Error", "No data in results file")
                self.show_parameter_input()
                return
            
            # Calculate statistics
            total_fuel = float(data[-1]['cumulative_fuel'])
            speeds = [float(row['speed']) for row in data]
            avg_speed = sum(speeds) / len(speeds)
            max_speed = max(speeds)
            
            # Calculate distance
            total_distance = sum(float(row['speed']) for row in data[1:])
            
            fuel_per_100km = (total_fuel / total_distance) * 100000 if total_distance > 0 else 0
            
            results = {
                'Total Fuel': f"{total_fuel:.3f} L",
                'Fuel Consumption': f"{fuel_per_100km:.2f} L/100km",
                'Average Speed': f"{avg_speed * 3.6:.2f} km/h",
                'Maximum Speed': f"{max_speed * 3.6:.2f} km/h",
                'Total Distance': f"{total_distance / 1000:.2f} km"
            }
            
            # Header
            header_frame = tk.Frame(self.main_frame, bg='#34495E', pady=15)
            header_frame.pack(fill=tk.X)
            
            header_label = tk.Label(
                header_frame,
                text="SIMULATION RESULTS",
                font=('Arial', 22, 'bold'),
                fg='#ECF0F1',
                bg='#34495E'
            )
            header_label.pack()
            
            # Results frame
            results_frame = tk.Frame(self.main_frame, bg='#2C3E50')
            results_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)
            
            # Display results
            row = 0
            for key, value in results.items():
                label_frame = tk.Frame(results_frame, bg='#34495E', padx=20, pady=15)
                label_frame.grid(row=row, column=0, columnspan=2, sticky='ew', pady=5)
                
                key_label = tk.Label(
                    label_frame,
                    text=key + ":",
                    font=('Arial', 14, 'bold'),
                    fg='#ECF0F1',
                    bg='#34495E',
                    anchor='w'
                )
                key_label.pack(side=tk.LEFT, padx=(0, 20))
                
                value_label = tk.Label(
                    label_frame,
                    text=value,
                    font=('Arial', 14),
                    fg='#27AE60',
                    bg='#34495E',
                    anchor='e'
                )
                value_label.pack(side=tk.RIGHT)
                
                row += 1
            
            # Buttons
            button_frame = tk.Frame(self.main_frame, bg='#2C3E50')
            button_frame.pack(pady=20)
            
            graphs_button = tk.Button(
                button_frame,
                text="VIEW GRAPHS",
                font=('Arial', 12, 'bold'),
                bg='#3498DB',
                fg='white',
                activebackground='#2980B9',
                padx=20,
                pady=10,
                cursor='hand2',
                command=self.show_graphs
            )
            graphs_button.pack(side=tk.LEFT, padx=10)
            
            new_button = tk.Button(
                button_frame,
                text="NEW SIMULATION",
                font=('Arial', 12, 'bold'),
                bg='#27AE60',
                fg='white',
                activebackground='#229954',
                padx=20,
                pady=10,
                cursor='hand2',
                command=self.show_parameter_input
            )
            new_button.pack(side=tk.LEFT, padx=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display results: {str(e)}")
            self.show_parameter_input()
    
    def show_graphs(self):
        """Display graphs"""
        self.clear_frame()
        
        # Header
        header_frame = tk.Frame(self.main_frame, bg='#34495E', pady=15)
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(
            header_frame,
            text="SIMULATION GRAPHS",
            font=('Arial', 22, 'bold'),
            fg='#ECF0F1',
            bg='#34495E'
        )
        header_label.pack()
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Read data
        csv_file = f"vehicle_simulation_scenario_{self.scenario_var.get()}.csv"
        
        try:
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            
            # Prepare data
            time = [float(row['time']) for row in data]
            speed = [float(row['speed']) * 3.6 for row in data]  # Convert to km/h
            drag = [float(row['drag']) for row in data]
            fuel = [float(row['cumulative_fuel']) for row in data]
            
            # Speed vs Time
            self.create_graph_tab(notebook, "Speed Profile", time, speed, 
                                "Time (s)", "Speed (km/h)", "Speed vs Time", 'blue')
            
            # Drag vs Time
            self.create_graph_tab(notebook, "Drag Force", time, drag,
                                "Time (s)", "Drag Force (N)", "Aerodynamic Drag vs Time", 'red')
            
            # Fuel vs Time
            self.create_graph_tab(notebook, "Fuel Consumption", time, fuel,
                                "Time (s)", "Cumulative Fuel (L)", "Fuel Consumption vs Time", 'green')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load graph data: {str(e)}")
        
        # Back button
        button_frame = tk.Frame(self.main_frame, bg='#2C3E50')
        button_frame.pack(pady=10)
        
        back_button = tk.Button(
            button_frame,
            text="BACK TO RESULTS",
            font=('Arial', 12, 'bold'),
            bg='#95A5A6',
            fg='white',
            activebackground='#7F8C8D',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.show_results
        )
        back_button.pack()
    
    def create_graph_tab(self, notebook, tab_name, x_data, y_data, xlabel, ylabel, title, color):
        """Create a graph tab"""
        tab_frame = tk.Frame(notebook, bg='white')
        notebook.add(tab_frame, text=tab_name)
        
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(x_data, y_data, color=color, linewidth=2)
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        canvas = FigureCanvasTkAgg(fig, master=tab_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def main():
    root = tk.Tk()
    app = VehicleSimulatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()