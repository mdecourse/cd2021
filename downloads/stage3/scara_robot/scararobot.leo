<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2"/>
<globals/>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="leo.20210526194338.1"><vh>@settings</vh>
<v t="leo.20210526194338.2"><vh>@data qt-gui-plugin-style-sheet</vh></v>
<v t="leo.20210526194338.3"><vh>@string initial_split_orientation = horizontal</vh></v>
</v>
<v t="leo.20210522214903.1"><vh>recursive importer</vh></v>
<v t="leo.20210526194137.1"><vh>@clean scararobot.lua</vh></v>
<v t="leo.20210526194307.1"><vh>@clean scararobot2.lua</vh></v>
</vnodes>
<tnodes>
<t tx="leo.20210522214903.1">'''Recursively import all python files in a directory and clean the result.'''
# ctrl + b to execute

c.recursiveImport(
    dir_ = r'./',
    kind = '@clean', # The new best practice.
    safe_at_file = False,
    theTypes = ['.lua'] 
)</t>
<t tx="leo.20210526194137.1">@language lua
@tabwidth -4
sim.setThreadAutomaticSwitch(false)
sim.switchThread()

threadFunction=function()
    while sim.getSimulationState()~=sim.simulation_advancing_abouttostop do
        sim.setJointTargetPosition(gripper,gripperOpen)
        sim.followPath(target,Path,1,0,manipVelocity)
        sim.setJointTargetPosition(gripper,gripperClose)
        sim.wait(gripperActionTime)
        sim.followPath(target,Path0,1,0,manipVelocity) 
        sim.setJointTargetPosition(gripper,gripperOpen)
        sim.wait(gripperActionTime)
        sim.followPath(target,Path1,1,0,manipVelocity*0.2)
        sim.wait(stopTime)
        sim.followPath(target,Path4,1,0,manipVelocity)
        sim.setJointTargetPosition(gripper,gripperClose)
        sim.wait(gripperActionTime)
        sim.followPath(target,Path5,1,0,manipVelocity) 
        sim.setJointTargetPosition(gripper,gripperOpen)
        sim.wait(gripperActionTime)
        sim.followPath(target,Path6,1,0,manipVelocity*0.2)
        sim.wait(stopTime)
        sim.followPath(target,Path11,1,0,manipVelocity)
        sim.setJointTargetPosition(gripper,gripperClose)
        sim.wait(gripperActionTime)
        sim.followPath(target,Path12,1,0,manipVelocity) 
        sim.setJointTargetPosition(gripper,gripperOpen)
        sim.wait(gripperActionTime)
        sim.followPath(target,Path13,1,0,manipVelocity*0.2)
        sim.wait(stopTime)
        sim.followPath(target,Path17,1,0,manipVelocity)
        sim.setJointTargetPosition(gripper,gripperClose)
        sim.wait(gripperActionTime)
        sim.followPath(target,Path18,1,0,manipVelocity) 
        sim.setJointTargetPosition(gripper,gripperOpen)
        sim.wait(gripperActionTime)
        sim.followPath(target,Path19,1,0,manipVelocity*0.2)
        sim.wait(stopTime)
        sim.stopSimulation()
    end
end

Path=sim.getObjectHandle("Path")
Path0=sim.getObjectHandle("Path0")
Path1=sim.getObjectHandle("Path1")
Path4=sim.getObjectHandle("Path4")
Path5=sim.getObjectHandle("Path5")
Path6=sim.getObjectHandle("Path6")
Path11=sim.getObjectHandle("Path13")
Path12=sim.getObjectHandle("Path11")
Path13=sim.getObjectHandle("Path12")
Path17=sim.getObjectHandle("Path17")
Path18=sim.getObjectHandle("Path18")
Path19=sim.getObjectHandle("Path19")
target=sim.getObjectHandle("Scara_target")
gripper=sim.getObjectHandle("Gripper_J")
manipVelocity=1
gripperOpen=0.04
gripperClose=0
gripperActionTime=1
stopTime=10
defaultPosition=sim.getObjectPosition(target,-1)
defaultOrientation=sim.getObjectOrientation(target,-1)

res,err=xpcall(threadFunction,function(err) return debug.traceback(err) end)
if not res then
    sim.addStatusbarMessage('Lua runtime error: '..err)
end</t>
<t tx="leo.20210526194307.1">@language lua
@tabwidth -4
sim.setThreadAutomaticSwitch(false)
sim.switchThread()

threadFunction=function()
    while sim.getSimulationState()~=sim.simulation_advancing_abouttostop do
        sim.wait(Time)
        sim.setJointTargetPosition(gripper2,gripperOpen2)
        sim.followPath(target2,Path2,1,0,manipVelocity2*0.2)
        sim.setJointTargetPosition(gripper2,gripperClose)
        sim.wait(gripperActionTime)
        sim.followPath(target2,Path3,1,0,manipVelocity2) 
        sim.setJointTargetPosition(gripper2,gripperOpen2)
        sim.wait(gripperActionTime)
        sim.followPath(target2,Path4,1,0,manipVelocity2*0.2)
        sim.wait(Time)
        sim.followPath(target2,Path8,1,0,manipVelocity2*0.2)
        sim.setJointTargetPosition(gripper2,gripperClose)
        sim.wait(gripperActionTime)
        sim.followPath(target2,Path9,1,0,manipVelocity2) 
        sim.setJointTargetPosition(gripper2,gripperOpen2)
        sim.wait(gripperActionTime)
        sim.followPath(target2,Path10,1,0,manipVelocity2*0.2)
        sim.wait(Time)
        sim.followPath(target2,Path14,1,0,manipVelocity2*0.2)
        sim.setJointTargetPosition(gripper2,gripperClose)
        sim.wait(gripperActionTime)
        sim.followPath(target2,Path15,1,0,manipVelocity2) 
        sim.setJointTargetPosition(gripper2,gripperOpen2)
        sim.wait(gripperActionTime)
        sim.followPath(target2,Path16,1,0,manipVelocity2*0.2)
        sim.wait(stopTime)
        --sim.stopSimulation()
    end
end

Path2=sim.getObjectHandle("Path2")
Path3=sim.getObjectHandle("Path3")
Path4=sim.getObjectHandle("Path7")
Path8=sim.getObjectHandle("Path9")
Path9=sim.getObjectHandle("Path8")
Path10=sim.getObjectHandle("Path10")
Path14=sim.getObjectHandle("Path14")
Path15=sim.getObjectHandle("Path15")
Path16=sim.getObjectHandle("Path16")
target2=sim.getObjectHandle("Scara_target2")
gripper2=sim.getObjectHandle("Gripper_J0")
manipVelocity2=1
gripperOpen2=0.04
gripperClose=0
gripperActionTime=1
stopTime=15
Time=10
defaultPosition=sim.getObjectPosition(target2,-1)
defaultOrientation=sim.getObjectOrientation(target2,-1)

res,err=xpcall(threadFunction,function(err) return debug.traceback(err) end)
if not res then
    sim.addStatusbarMessage('Lua runtime error: '..err)
endssage('Lua runtime error: '..err)
end</t>
<t tx="leo.20210526194338.1"></t>
<t tx="leo.20210526194338.2">QTreeWidget {
    /* These apply to the selected item, but not to editing items.*/
    background-color: #ffffec; /* Leo's traditional tree color */
    selection-color: black; /* was white */
    selection-background-color: lightgrey;
    /* font-family: SansSerif; */
    /*font-family: DejaVu Sans Mono;*/
    font-family:YaHei Mono;
    /* 標題字型大小設定 */
    font-size: 30px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal, italic,oblique */
 }

/* Headline edit widgets */
QTreeWidget QLineEdit {
    background-color: cornsilk;
    selection-color: white;
    selection-background-color: blue;
    /*font-family: DejaVu Sans Mono;*/    
    font-family:YaHei Mono;
    /* 沒有特別對應字型大小 */
    font-size: 30px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal, italic,oblique */
}

/* The log panes */
QTextEdit {
    background-color: #f2fdff;
    selection-color: red;
    selection-background-color: blue;
    /* font-family: Courier New; */
    font-family:YaHei Mono;
    /* log font 大小 */
    font-size: 30px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal, italic,oblique */
}

/* The body pane */
QTextEdit#richTextEdit {
    background-color: #fdf5f5; /* A kind of pink. */
    selection-color: white;
    selection-background-color: red;
    /*font-family: DejaVu Sans Mono;*/
    /* font-family: Courier New; */
    font-family:YaHei Mono;
    /* 內文字型大小 */
    font-size: 30px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

QLabel {
    font-family:YaHei Mono;'CherryPy', 'pytz', 'mako', 'beautifulsoup4', 'pymysql', 'peewee'
    /* 下方的 Minibuffer 標題字型大小 */
    font-size: 30px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

/* Editor labels */
QLineEdit#editorLabel {
    background-color: #ffffec;
    font-family:YaHei Mono;
    /* 沒有直接對應字型大小 */
    font-size: 30px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
    border: 2px;
    margin: 2px;
}</t>
<t tx="leo.20210526194338.3">horizontal: body pane to the left
vertical: body pane on the botton</t>
</tnodes>
</leo_file>
