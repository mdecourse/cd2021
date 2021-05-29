<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2"/>
<globals/>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="leo.20210526153741.1"><vh>@settings</vh>
<v t="leo.20210526153741.2"><vh>@data qt-gui-plugin-style-sheet</vh></v>
<v t="leo.20210526153741.3"><vh>@string initial_split_orientation = horizontal</vh></v>
</v>
<v t="leo.20210529155453.1"><vh>recursive importer</vh></v>
<v t="leo.20210529202339.1"><vh>imported files</vh>
<v t="leo.20210529202339.2"><vh>@path ./</vh>
<v t="leo.20210529202339.3"><vh>@clean fosbase.lua</vh>
<v t="leo.20210529202339.4"><vh>sysCall_init (fosbase.lua)</vh></v>
<v t="leo.20210529202339.5"><vh>sysCall_actuation (fosbase.lua)</vh></v>
</v>
<v t="leo.20210529202339.6"><vh>@clean s1.lua</vh></v>
<v t="leo.20210529202339.7"><vh>@clean s2.lua</vh></v>
<v t="leo.20210529202339.8"><vh>@clean s3.lua</vh></v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="leo.20210526153741.1"></t>
<t tx="leo.20210526153741.2">QTreeWidget {
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
<t tx="leo.20210526153741.3">horizontal: body pane to the left
vertical: body pane on the botton</t>
<t tx="leo.20210529155453.1">'''Recursively import all python files in a directory and clean the result.'''
# ctrl + b to execute

c.recursiveImport(
    dir_ = r'./',
    kind = '@clean', # The new best practice.
    safe_at_file = False,
    theTypes = ['.lua'] 
)</t>
<t tx="leo.20210529202339.1"></t>
<t tx="leo.20210529202339.2"></t>
<t tx="leo.20210529202339.3">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210529202339.4">function sysCall_init() 
    velocity=0
    velocity2=0
    velocity3=0
    velocity4=0
    velocity5=0
    velocity6=0
    velocity7=0
    velocity8=0
-----------
    sliding_b = 0
    sliding_r = 0
-----------
    left_joint_b1=sim.getObjectHandle('left_R1')
    left_joint_b2=sim.getObjectHandle('left_R2')
    left_joint_b3=sim.getObjectHandle('left_R3')
    left_joint_b4=sim.getObjectHandle('left_R4')
    left_slider_b1=sim.getObjectHandle('left_S1')
    left_slider_b2=sim.getObjectHandle('left_S2')
    left_slider_b3=sim.getObjectHandle('left_S3')
    left_slider_b4=sim.getObjectHandle('left_S4')
-----------
    right_joint_r1=sim.getObjectHandle('right_R1')
    right_joint_r2=sim.getObjectHandle('right_R2')
    right_joint_r3=sim.getObjectHandle('right_R3')
    right_joint_r4=sim.getObjectHandle('right_R4')
    right_slider_r1=sim.getObjectHandle('right_S1')
    right_slider_r2=sim.getObjectHandle('right_S2')
    right_slider_r3=sim.getObjectHandle('right_S3')
    right_slider_r4=sim.getObjectHandle('right_S4')
end
</t>
<t tx="leo.20210529202339.5">function sysCall_actuation()
        sim.setJointTargetPosition(left_joint_b1,velocity)
        sim.setJointTargetPosition(left_joint_b2,velocity2)
        sim.setJointTargetPosition(left_joint_b3,velocity3)
        sim.setJointTargetPosition(left_joint_b4,velocity4)
        sim.setJointTargetPosition(right_joint_r1,velocity5)
        sim.setJointTargetPosition(right_joint_r2,velocity6)
        sim.setJointTargetPosition(right_joint_r3,velocity7)
        sim.setJointTargetPosition(right_joint_r4,velocity8)
---------------------
        sim.setJointTargetPosition(left_slider_b1,sliding_b)
        sim.setJointTargetPosition(left_slider_b2,sliding_b)
        sim.setJointTargetPosition(left_slider_b3,sliding_b)
        sim.setJointTargetPosition(left_slider_b4,sliding_b)
        sim.setJointTargetPosition(right_slider_r1,sliding_r)
        sim.setJointTargetPosition(right_slider_r2,sliding_r)
        sim.setJointTargetPosition(right_slider_r3,sliding_r)
        sim.setJointTargetPosition(right_slider_r4,sliding_r)
    message,auxiliaryData=sim.getSimulatorMessage()
        while message ~= -1 do
key=auxiliaryData[1]
sim.addStatusbarMessage('key:'..key)
            if (message==sim.message_keypress) then
-----------------player_B
                if (auxiliaryData[1]==119)then --w
                    velocity=100
                    velocity2=100
                    velocity3=100
                    velocity4=100
                end
                if (auxiliaryData[1]==103) then --g
                    -- goalkeeper kick keypress(g)
                     velocity = -100 
                end
                if (auxiliaryData[1]==104) then
                    -- guard kick keypress(h) 
                     velocity2 = -100 
                end
                if (auxiliaryData[1]==106) then
                    -- midfield kick keypress(j) 
                     velocity3 = -100 
                end
                if (auxiliaryData[1]==107) then
                    -- forward kick keypress(k)
                     velocity4 = -100 
                end
                if (auxiliaryData[1]==97) then
                    -- left key
                    if (sliding_b &gt;= 0.05) then 
                    else sliding_b = sliding_b + 0.01
sim.addStatusbarMessage('sliding_b:'..sliding_b)
                    end
                end
                if (auxiliaryData[1]==100) then
                    -- right key
                    if (sliding_b &lt;= -0.05) then 
                    else sliding_b = sliding_b - 0.01
sim.addStatusbarMessage('sliding_b:'..sliding_b)
                    end
                end
-------------------player_R
                if (auxiliaryData[1]==2007)then
                    velocity5=100
                    velocity6=100
                    velocity7=100
                    velocity8=100
                end
                if (auxiliaryData[1]==49) then
                    -- goalkeeper kick keypress(1)
                     velocity5 = -100 
                end
                if (auxiliaryData[1]==50) then
                    -- guard kick keypress(2)
                     velocity6 = -100 
                end
                if (auxiliaryData[1]==51) then
                    -- midfield kick keypress(3)
                     velocity7 = -100 
                end
                if (auxiliaryData[1]==2001) then
                    -- forward kick keypress(enter)
                     velocity8 = -100 
                end
                if (auxiliaryData[1]==2009) then
                    -- left key
                    if (sliding_r &gt;= 0.05) then 
                    else sliding_r = sliding_r + 0.01
sim.addStatusbarMessage('sliding_r:'..sliding_r)
                    end
                end
                if (auxiliaryData[1]==2010) then
                    -- right key
                    if (sliding_r &lt;= -0.05) then 
                    else sliding_r = sliding_r - 0.01
sim.addStatusbarMessage('sliding_r:'..sliding_r)
                    end
                end
            end
            message,auxiliaryData=sim.getSimulatorMessage()
        end
----
end
</t>
<t tx="leo.20210529202339.6">@path ./
threadFunction=function()
    while sim.getSimulationState()~=sim.simulation_advancing_abouttostop do
        -- Read the keyboard messages (make sure the focus is on the main window, scene view):
message,auxiliaryData=sim.getSimulatorMessage()
        while message~=-1 do
key=auxiliaryData[1]
sim.addStatusbarMessage('key:'..key)
            if (message==sim.message_keypress) then
                if (auxiliaryData[1]==100) then
                    -- right key D
                    if(sliding &gt;=0.25) then
                    else sliding = sliding + 0.01
sim.addStatusbarMessage('sliding:'..sliding)
                    end
                end
                if (auxiliaryData[1]==97) then
                    -- left key A
                    if(sliding &lt;= -0.25) then
                    else sliding = sliding - 0.01
sim.addStatusbarMessage('sliding:'..sliding)
                    end
                end
            end
message,auxiliaryData=sim.getSimulatorMessage()
        end
        sim.setJointTargetPosition(slider, sliding)
        -- Since this script is threaded, don't waste time here:
        sim.switchThread() -- Resume the script at next simulation loop start
    end
end
-- Put some initialization code here:
-- Retrieving of some handles and setting of some initial values:
slider=sim.getObjectHandle("S1")
sliding = 0
-- Here we execute the regular thread code:
res,err=xpcall(threadFunction,function(err) return debug.traceback(err) end)
if not res then
    sim.addStatusbarMessage('Lua runtime error: '..err)
end
-- Put some clean-up code here:
@language lua
@tabwidth -4
</t>
<t tx="leo.20210529202339.7">@path ./
threadFunction=function()
    while sim.getSimulationState()~=sim.simulation_advancing_abouttostop do
        -- Read the keyboard messages (make sure the focus is on the main window, scene view):
message,auxiliaryData=sim.getSimulatorMessage()
        while message~=-1 do
key=auxiliaryData[1]
sim.addStatusbarMessage('key:'..key)
            if (message==sim.message_keypress) then
                if (auxiliaryData[1]==119) then
                    --  front key W
                    if(sliding &gt;=0.25) then
                    else sliding = sliding + 0.01
sim.addStatusbarMessage('sliding:'..sliding)
                    end
                end
                if (auxiliaryData[1]==115) then
                    --  behind key S
                    if(sliding &lt;= -0.25) then
                    else sliding = sliding - 0.01
sim.addStatusbarMessage('sliding:'..sliding)
                    end
                end
            end
message,auxiliaryData=sim.getSimulatorMessage()
        end
        sim.setJointTargetPosition(slider, sliding)
        -- Since this script is threaded, don't waste time here:
        sim.switchThread() -- Resume the script at next simulation loop start
    end
end
-- Put some initialization code here:
-- Retrieving of some handles and setting of some initial values:
slider=sim.getObjectHandle("S2")
sliding = 0
-- Here we execute the regular thread code:
res,err=xpcall(threadFunction,function(err) return debug.traceback(err) end)
if not res then
    sim.addStatusbarMessage('Lua runtime error: '..err)
end
-- Put some clean-up code here:
@language lua
@tabwidth -4
</t>
<t tx="leo.20210529202339.8">@path ./
threadFunction=function()
    while sim.getSimulationState()~=sim.simulation_advancing_abouttostop do
        -- Read the keyboard messages (make sure the focus is on the main window, scene view):
message,auxiliaryData=sim.getSimulatorMessage()
        while message~=-1 do
key=auxiliaryData[1]
sim.addStatusbarMessage('key:'..key)
            if (message==sim.message_keypress) then
                if (auxiliaryData[1]==2010) then
                    --  catch key 
                    if(sliding &gt;=0.25) then
                    else sliding = sliding + 0.05
sim.addStatusbarMessage('sliding:'..sliding)
                    end
                end
                if (auxiliaryData[1]==2009) then
                    --  place key 
                    if(sliding &lt;= -0.25) then
                    else sliding = sliding - 0.05
sim.addStatusbarMessage('sliding:'..sliding)
                    end
                end
            end
message,auxiliaryData=sim.getSimulatorMessage()
        end
        sim.setJointTargetPosition(slider, sliding)
        -- Since this script is threaded, don't waste time here:
        sim.switchThread() -- Resume the script at next simulation loop start
    end
end
-- Put some initialization code here:
-- Retrieving of some handles and setting of some initial values:
slider=sim.getObjectHandle("S4")
sliding = 0
-- Here we execute the regular thread code:
res,err=xpcall(threadFunction,function(err) return debug.traceback(err) end)
if not res then
    sim.addStatusbarMessage('Lua runtime error: '..err)
end
-- Put some clean-up code here:
@language lua
@tabwidth -4
</t>
</tnodes>
</leo_file>
