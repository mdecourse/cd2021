from robolink import *
from robodk import *

RDK = Robolink(args=["-NEWINSTANCE", "-SKIPINI", "-EXIT_LAST_COM"], robodk_path='c:/robodk/bin/robodk.exe')

# Add robot
robot = RDK.AddFile('Fanuc-M-710iC-50.robot')
# Get robot frame
robot_frame = RDK.Item('Fanuc M-710iC/50 Base') 
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
