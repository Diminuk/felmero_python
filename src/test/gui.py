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

HORIZONTAL_MAX = 228000
VERTICAL_MAX = 228000

LENGTH_OFFSET = 170 + 35 - 2 + 18 

V_SCALE = [
    1729, 2158, 2593, 3029, 3467, 
    3892, 4328, 4784, 5233, 5668, 
    6103, 6549, 7003, 7428, 7863, 
    8314, 8777, 9212, 9648, 10097, 
    10551, 10980, 11432, 11879, 12334, 
    12780, 13217, 13663, 14112, 14545, 
    14990, 15436, 15887, 16333, 16756, 
    17210, 17656, 18092, 18544, 18993, 
    19449, 19892, 20331, 20786, 21232,
    21668, 22113, 22559, 23012, 23448, 
    23878, 24329, 24776, 25220, 25666,
    26115, 26571
]
MM_CSALE = np.arange(200,3050,50)


def convert_to_xyz(h, v, l):
    # Normalize h and v to radians between 0 and 2π using numpy
    h_angle = (h % HORIZONTAL_MAX) * (2 * np.pi / HORIZONTAL_MAX)
    v_angle = (v % VERTICAL_MAX) * (2 * np.pi / VERTICAL_MAX)

    v_angle += np.pi/2
    # Compute the radial distance r
    #r = (l - LENGTH_V_OFFSET)*(LENGTH_MAX_VALUE_MM/ (LENGTH_MAX-LENGTH_V_OFFSET)) + LENGTH_OFFSET
    #r = p(l)
    #r = (l-VOLTAGE_ZERO)*((3000-17)/VOLTAGE_3000)+LENGTH_OFFSET
    r = np.interp([l],V_SCALE, MM_CSALE) + LENGTH_OFFSET
    # Convert spherical to Cartesian coordinates
    x = r * np.sin(v_angle) * np.cos(h_angle)
    y = r * np.sin(v_angle) * np.sin(h_angle)
    z = r * np.cos(v_angle)
    

    return x, y, z

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
        self.data_np = np.array([])
    def update_sections(self,newsec):
        self.sections = newsec
    def update_data_np(self,new):
        self.data_np = new
        
memory = Memory()

def plot_section():
    if not selected_section.get():
        tk.messagebox.showerror("Error", "No section selected")
        return
    # calc 
    point_calc = []
    for section in memory.sections:
        if section.get("name").find(selected_section.get()) ==0 :
            points = section.get("points")
            point_disp = []
            for point in points:
                h = point.get("h")
                v = point.get("v")
                l = point.get("l")
                point_disp.append([h,v,l])
            point_calc.append(point_disp)

    point_arr = np.array(point_calc)

    data_cartesian = []
    for section in point_calc:
        section_cartesian = [convert_to_xyz(h, v, l) for h, v, l in section]
        #section_cartesian = [convert_to_xyz(h, 0, l) for h, v, l in section]
        data_cartesian.append(section_cartesian)

    data_np  = np.array(data_cartesian)

    memory.update_data_np(data_np)

    point1_menu["values"] = list(np.arange(0,len(data_np[0][:,0]), 1))
    point2_menu["values"] = list(np.arange(0,len(data_np[0][:,0]), 1))

    ax.clear()
    ax.set_title(selected_section.get())
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.view_init(elev=90, azim=-90, roll=0)

    colors = ['r', 'g', 'b']
    for i, section in enumerate(data_np):
        x, y, z = section[:, 0], section[:, 1], section[:, 2]
        ax.scatter(x, y, z, color=colors[i % len(colors)], label=f'Section {i+1}', s=5)
        for i in range(len(section[:,0])):
            ax.text(section[i, 0][0],section[i, 1][0],section[i, 2][0],f"{i}",fontsize=8)
    ax.axis("equal")

    
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
    p1 = int(point1_var.get())
    p2 =int(point2_var.get())
    if p1 and p2 and p1 != p2 and p1 < len(memory.data_np[0][:,0]) and p2 < len(memory.data_np[0][:,0]):
        print(memory.data_np[0][p1][0])
        print(memory.data_np[0][p2][0])
        
        dist = distance.euclidean(memory.data_np[0][p1][0],memory.data_np[0][p2][0])
        result_label.config(text=f"Distance: {dist:.2f} mm")
    else:
        result_label.config(text="Invalid selection")



# Function to add a new point
def add_section():
    name = new_section_name.get().strip()
    try:
        if name:
            new_section_name.set("")
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
update_dropdowns()
refresh_sections()

# Run the application
root.mainloop()
