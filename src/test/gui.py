import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance
import requests
import asyncio
import httpx

# Sample points
points = {
    "Point A": (0, 0, 0),
    "Point B": (1, 1, 1),
    "Point C": (2, 0, 1),
    "Point D": (-1, -1, -1)
}

class Memory():
    
    def __init__(self,):
        self.sections = {}
    def update_sections(self,newsec):
        self.sections = newsec
        
memory = Memory()

def plot_section(sectionname: str):

    # calc 
    point_calc = []
    for section in memory.sections:
        if section.get("name").find(sectionname) ==0 :
            points = section.get("points")
            point_disp = []
            for point in points:
                h = point.get("h")
                v = point.get("v")
                l = point.get("l")
                point_disp.append([h,v,l])
            point_calc.append(point_disp)

    point_arr = np.array(point_calc)

    ax.clear()
    ax.set_title("Section name")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # Plot the points
    for label, coords in points.items():
        ax.scatter(*coords, label=label)
        ax.text(*coords, label, fontsize=9)

    ax.legend()
    canvas.draw()

def refresh_sections():
    try:
        response = requests.get("http://localhost:8000/data/get-dummysections").json()
        if response:
            memory.update_sections(response)
        update_sections_dropdown()
    except:
        tk.messagebox.showerror("Error", "Cannot refresh sections")

# Function to calculate the distance between two points
def calculate_distance():
    p1 = point1_var.get()
    p2 = point2_var.get()
    if p1 and p2 and p1 != p2:
        dist = distance.euclidean(points[p1], points[p2])
        result_label.config(text=f"Distance: {dist:.2f}")
    else:
        result_label.config(text="Invalid selection")

# Function to refresh the plot
def refresh_plot():
    ax.clear()
    ax.set_title("Section name")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # Plot the points
    for label, coords in points.items():
        ax.scatter(*coords, label=label)
        ax.text(*coords, label, fontsize=9)

    ax.legend()
    canvas.draw()

# Function to add a new point
def add_section():
    name = new_section_name.get().strip()
    try:
        if name:
            new_section_name.set("")
            refresh_plot()
            update_dropdowns()
    except ValueError:
        tk.messagebox.showerror("Error", "Invalid coordinates. Use format: x,y,z")

# Update dropdown options
def update_dropdowns():
    dropdown_options = list(points.keys())
    point1_menu["values"] = dropdown_options
    point2_menu["values"] = dropdown_options

def update_sections_dropdown():
    sections_dropdown = list()
    for section in memory.sections:
        sections_dropdown.append(section.get('name'))
    section_menu["values"] = sections_dropdown

# Create the main window
root = tk.Tk()
root.title("3D Points Viewer and Distance Calculator")

# Top frame for inputs
top_frame = tk.Frame(root, padx=10, pady=10)
top_frame.pack(fill="x")

# New point input
tk.Label(top_frame, text="New section name:").grid(row=0, column=0, padx=5, pady=5)
new_section_name = tk.StringVar()
tk.Entry(top_frame, textvariable=new_section_name).grid(row=0, column=1, padx=5, pady=5)

tk.Button(top_frame, text="New section", command=add_section).grid(row=0, column=2, padx=5, pady=5)

tk.Button(top_frame, text="Refresh", command=refresh_sections).grid(row=0, column=4, padx=5, pady=5)

# Dropdowns for distance calculation
tk.Label(top_frame, text="Select section").grid(row=3, column=0, padx=5, pady=5)
selected_section = tk.StringVar()
section_menu = ttk.Combobox(top_frame, textvariable=selected_section)
section_menu.grid(row=3, column=1, padx=5, pady=5)

tk.Button(top_frame, text="Plot", command=plot_section).grid(row=3, column=4, padx=5, pady=5)

# Dropdowns for distance calculation
tk.Label(top_frame, text="Select Point 1:").grid(row=1, column=0, padx=5, pady=5)
point1_var = tk.StringVar()
point1_menu = ttk.Combobox(top_frame, textvariable=point1_var)
point1_menu.grid(row=1, column=1, padx=5, pady=5)

tk.Label(top_frame, text="Select Point 2:").grid(row=1, column=2, padx=5, pady=5)
point2_var = tk.StringVar()
point2_menu = ttk.Combobox(top_frame, textvariable=point2_var)
point2_menu.grid(row=1, column=3, padx=5, pady=5)

tk.Button(top_frame, text="Calculate Distance", command=calculate_distance).grid(row=1, column=4, padx=5, pady=5)

result_label = tk.Label(top_frame, text="Distance: N/A", font=("Arial", 12))
result_label.grid(row=2, column=0, columnspan=5, pady=10)

# Matplotlib figure
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill="both", expand=True)

# Initialize plot and dropdowns
refresh_plot()
update_dropdowns()
refresh_sections()

# Run the application
root.mainloop()
