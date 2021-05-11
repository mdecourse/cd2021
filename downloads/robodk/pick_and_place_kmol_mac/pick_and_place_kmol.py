from robolink import *
from robodk import *

# Calculate pyramid coordinate
def pyramid_calc(BALLS_SIDE=4):
    """Calculate a list of points (ball center) as if the balls were place in a pyramid"""
    #the number of balls can be calculated as: int(BALLS_SIDE*(BALLS_SIDE+1)*(2*BALLS_SIDE+1)/6)
    BALL_DIAMETER = 100
    xyz_list = []
    sqrt2 = 2**(0.5)
    for h in range(BALLS_SIDE):
        for i in range(BALLS_SIDE-h):
            for j in range(BALLS_SIDE-h):
                height = h*BALL_DIAMETER/sqrt2 + BALL_DIAMETER/2
                xyz_list = xyz_list + [[i*BALL_DIAMETER + (h+1)*BALL_DIAMETER*0.5, j*BALL_DIAMETER + (h+1)*BALL_DIAMETER*0.5, height]]
    return xyz_list
    

# Make a list of positions to place the objects
balls_list = pyramid_calc(4)

#print(len(frame1_list))
# 4*4 = 16
# 3*3 = 9
# 2*2 = 4
# 1+4+9+16 = 30

# height 50*sqrt(2)
'''
[

[50.0, 50.0, 50.0], [50.0, 150.0, 50.0], [50.0, 250.0, 50.0], [50.0, 350.0, 50.0], 

[150.0, 50.0, 50.0], [150.0, 150.0, 50.0], [150.0, 250.0, 50.0], [150.0, 350.0, 50.0], 

[250.0, 50.0, 50.0], [250.0, 150.0, 50.0], [250.0, 250.0, 50.0], [250.0, 350.0, 50.0], 

[350.0, 50.0, 50.0], [350.0, 150.0, 50.0], [350.0, 250.0, 50.0], [350.0, 350.0, 50.0], 


[100.0, 100.0, 120.71067811865474], [100.0, 200.0, 120.71067811865474], [100.0, 300.0, 120.71067811865474], 

[200.0, 100.0, 120.71067811865474], [200.0, 200.0, 120.71067811865474], [200.0, 300.0, 120.71067811865474], 

[300.0, 100.0, 120.71067811865474], [300.0, 200.0, 120.71067811865474], [300.0, 300.0, 120.71067811865474], 


[150.0, 150.0, 191.42135623730948], [150.0, 250.0, 191.42135623730948], 

[250.0, 150.0, 191.42135623730948], [250.0, 250.0, 191.42135623730948], 


[200.0, 200.0, 262.13203435596427]

]

'''
# https://github.com/RoboDK/RoboDK-API/blob/master/Python/robolink.py
# robodk_path variable to specify location of RoboDK.exe
RDK = Robolink(args=["-NEWINSTANCE", "-SKIPINI", "-EXIT_LAST_COM"])

# Add robot and the accompanied Base coordinate
robot = RDK.AddFile('Fanuc-M-710iC-50.robot')
# Get the default robot base frame
robot_frame = RDK.Item('Fanuc M-710iC/50 Base')
# Move the base frame to the origin
robot_frame.setPose(transl(0,0,0))

# Add a tool to an existing robot:
tool = RDK.AddFile('MainTool.tool', robot)

# Add table 1
table1_frame = RDK.AddFrame('Table 1')
table1_frame.setPose(transl(807.766544,-963.699898,41.478944))
table1_stl = RDK.AddFile('Table.stl', table1_frame)

# Add table 2
table2_frame = RDK.AddFrame('Table 2')
table2_frame.setPose(transl(926.465508,337.151529,94.871928))
table2_stl = RDK.AddFile('Table.stl', table2_frame)

# Add balls
# create a list with 30 elements
balls = [None for _ in range(30)]
layer = [16, 9, 4, 1]
count = 0
for i in range(len(balls_list)):
    # transl(balls_list)
    balls[i] = RDK.AddFile('ball.stl', table2_frame)
    balls[i].setPose(transl(balls_list[i]))
    count = count + 1
    if count <= 16:
        balls[i].setColor([1, 0, 0])
    elif count > 16 and count <= 25:
        balls[i].setColor([0, 1, 0])
    elif count > 25 and count <=29:
        balls[i].setColor([1, 1, 0])
    else:
        balls[i].setColor([0, 0, 1])
