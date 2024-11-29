import numpy as np

HORIZONTAL_MAX = 16383
VERTICAL_MAX = 16383
LENGTH_MAX = 16383
LENGTH_MAX_VALUE = 3000

def find_sphere_center(points, radius):
    X = np.array([p[0] for p in points])
    Y = np.array([p[1] for p in points])
    Z = np.array([p[2] for p in points])
    
    A = np.c_[2*X, 2*Y, 2*Z, np.ones(len(X))]
    B = X**2 + Y**2 + Z**2 - radius**2
    
    coeff, *_ = np.linalg.lstsq(A, B, rcond=None)
    Cx, Cy, Cz, _ = coeff
    
    return Cx, Cy, Cz

def convert_to_xyz(h, v, l):
    # Normalize h and v to radians between 0 and 2π using numpy
    h_angle = (h % HORIZONTAL_MAX) * (2 * np.pi / HORIZONTAL_MAX)
    v_angle = (v % VERTICAL_MAX) * (2 * np.pi / VERTICAL_MAX)
    
    # Compute the radial distance r
    r = (l / LENGTH_MAX) * LENGTH_MAX
    
    # Convert spherical to Cartesian coordinates
    x = r * np.cos(v_angle) * np.cos(h_angle)
    y = r * np.cos(v_angle) * np.sin(h_angle)
    z = r * np.sin(v_angle)
    
    return x, y, z