"""
"""
import os, random
import cv2

# Directories
MAIN_DIR       = os.path.dirname(os.path.realpath(__file__))
SCENES         = os.path.join(MAIN_DIR, 'src', 'scenes')
COPPELIA_DIR   = os.path.join(MAIN_DIR, 'coppeliasim')

# V-Rep
sim_port       = 19998
local_ip       = '127.0.0.1'

# Simulation parameters
simulation_steps = 5000

# Agent
position_history_length = 200 # Length of the deque of position history of the agent

# Lidar
lidar_angle  = 270. # Angle of the LIDAR (-135:135)
scan_rate    = 10    # Scan rate (not really relevant in the simulation)
distance_no_detection_mm = 10
detection_margin         = 2
offset_mm                = 50

# SLAM parameters
steps_slam   = 1       # Perform SLAM every n steps of the simulation
scale_factor = 800     # Scaling factor of the map
image_size   = 500    # Size of the SLAM image NxN
window_size  = 800    # Size of the opencv window
map_size     = 20      # Map size in meters
map_quality  = 50     # Fidelity of the map
hole_width   = 200
sigma_xy     = 200
sigma_theta  = 20
max_search_iter = 20000

# Visualization
canny_filter = True                # Use canny edge detection filter
colormap = cv2.COLORMAP_SUMMER     # Colormap if canny filter is not used
agent_scale_factor = 1000          # For correctly displaying the agent's position
agent_color = (100,100,100)       
agent_radius = 10                  # Size of the drawn agent
agent_center_scale = 50            # Length of the center line
draw_closest = False                # Draw lines towards the closest objects on left/right
closest_line_color = (150,150,255) 
closest_line_scale = scale_factor / map_size
speed_limit = 5
draw_dist = False
