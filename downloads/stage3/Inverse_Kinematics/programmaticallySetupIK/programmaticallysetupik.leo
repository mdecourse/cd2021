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
<v t="leo.20210602200835.1"><vh>sim.handle_self</vh></v>
<v t="leo.20210602201605.1"><vh>sim.getObjectMatrix</vh></v>
<v t="leo.20210602204142.1"><vh>simIK</vh></v>
<v t="leo.20210529155453.1"><vh>recursive importer</vh></v>
<v t="leo.20210602170939.1"><vh>imported files</vh>
<v t="leo.20210602202348.1"><vh>Inverse Kinematics</vh></v>
<v t="leo.20210602170939.2"><vh>@path ./</vh>
<v t="leo.20210602170939.3"><vh>@clean beam.lua</vh>
<v t="leo.20210602170939.4"><vh>sysCall_init (beam.lua)</vh></v>
<v t="leo.20210602170939.5"><vh>sysCall_actuation (beam.lua)</vh></v>
</v>
<v t="leo.20210602170939.6"><vh>@clean robota.lua</vh>
<v t="leo.20210602170939.7"><vh>sysCall_init (robota.lua)</vh></v>
<v t="leo.20210602170939.8"><vh>sysCall_cleanup (robota.lua)</vh></v>
<v t="leo.20210602170939.9"><vh>sysCall_actuation (robota.lua)</vh></v>
</v>
<v t="leo.20210602170939.10"><vh>@clean robotb.lua</vh>
<v t="leo.20210602170939.11"><vh>sysCall_init (robotb.lua)</vh></v>
<v t="leo.20210602170939.12"><vh>sysCall_actuation (robotb.lua)</vh></v>
<v t="leo.20210602170939.13"><vh>sysCall_cleanup (robotb.lua)</vh></v>
</v>
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
<t tx="leo.20210602170939.1"></t>
<t tx="leo.20210602170939.10">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210602170939.11">-- use program to setup IK group
function sysCall_init()
    -- Take a few handles from the blue robot:
    simBase=sim.getObjectHandle('RobotB')
    simTip=sim.getObjectHandle('RobotB_tip')
    simTarget=sim.getObjectHandle('RobotB_target')
    simJoints={}
    for i=1,6,1 do
        simJoints[i]=sim.getObjectHandle('RobotB_joint'..i)
    end

    -- Now build a kinematic chain and 2 IK groups (undamped and damped) inside of the IK plugin environment,
    -- based on the kinematics of the blue robot:
    ikJoints={}
    ikEnv=simIK.createEnvironment() -- create an IK environment
    local ikBase=simIK.createDummy(ikEnv) -- create a dummy in the IK environemnt
    simIK.setObjectMatrix(ikEnv,ikBase,-1,sim.getObjectMatrix(simBase,-1)) -- set that dummy into the same pose as its CoppeliaSim counterpart
    local parent=ikBase
    for i=1,#simJoints,1 do -- loop through all joints
        ikJoints[i]=simIK.createJoint(ikEnv,simIK.jointtype_revolute) -- create a joint in the IK environment
        simIK.setJointMode(ikEnv,ikJoints[i],simIK.jointmode_ik) -- set it into IK mode
        local cyclic,interv=sim.getJointInterval(simJoints[i])
        simIK.setJointInterval(ikEnv,ikJoints[i],cyclic,interv) -- set the same joint limits as its CoppeliaSim counterpart joint
        simIK.setJointPosition(ikEnv,ikJoints[i],sim.getJointPosition(simJoints[i])) -- set the same joint position as its CoppeliaSim counterpart joint
        simIK.setObjectMatrix(ikEnv,ikJoints[i],-1,sim.getObjectMatrix(simJoints[i],-1)) -- set the same object pose as its CoppeliaSim counterpart joint
        simIK.setObjectParent(ikEnv,ikJoints[i],parent,true) -- set its corresponding parent
        -- 依據 robot link hierarchy 設定各 joint 從屬關係
        parent=ikJoints[i]
    end
    ikTip=simIK.createDummy(ikEnv) -- create the tip dummy in the IK environment
    simIK.setObjectMatrix(ikEnv,ikTip,-1,sim.getObjectMatrix(simTip,-1)) -- set that dummy into the same pose as its CoppeliaSim counterpart
    simIK.setObjectParent(ikEnv,ikTip,parent,true) -- attach it to the kinematic chain
    ikTarget=simIK.createDummy(ikEnv) -- create the target dummy in the IK environment
    simIK.setObjectMatrix(ikEnv,ikTarget,-1,sim.getObjectMatrix(simTarget,-1)) -- set that dummy into the same pose as its CoppeliaSim counterpart
    simIK.setLinkedDummy(ikEnv,ikTip,ikTarget) -- link the two dummies
    ikGroup_undamped=simIK.createIkGroup(ikEnv) -- create an IK group
    simIK.setIkGroupCalculation(ikEnv,ikGroup_undamped,simIK.method_pseudo_inverse,0,20) -- set its resolution method to undamped
    simIK.setIkGroupFlags(ikEnv,ikGroup_undamped,1+2+4+8) -- make sure the robot doesn't shake if the target position/orientation wasn't reached
    local ikElementHandle=simIK.addIkElement(ikEnv,ikGroup_undamped,ikTip) -- add an IK element to that IK group
    simIK.setIkElementBase(ikEnv,ikGroup_undamped,ikElementHandle,ikBase) -- specify the base of that IK element
    simIK.setIkElementConstraints(ikEnv,ikGroup_undamped,ikElementHandle,simIK.constraint_pose) -- specify the constraints of that IK element
    ikGroup_damped=simIK.createIkGroup(ikEnv) -- create another IK group
    simIK.setIkGroupCalculation(ikEnv,ikGroup_damped,simIK.method_damped_least_squares,0.3,100) -- set its resolution method to damped
    local ikElementHandle=simIK.addIkElement(ikEnv,ikGroup_damped,ikTip) -- add an IK element to that IK group
    simIK.setIkElementBase(ikEnv,ikGroup_damped,ikElementHandle,ikBase) -- specify the base of that IK element
    simIK.setIkElementConstraints(ikEnv,ikGroup_damped,ikElementHandle,simIK.constraint_pose) -- specify the constraints of that IK element
end

</t>
<t tx="leo.20210602170939.12">function sysCall_actuation()
    simIK.setObjectMatrix(ikEnv,ikTarget,-1,sim.getObjectMatrix(simTarget,-1)) -- reflect the pose of the target dummy to its counterpart in the IK environment

    if simIK.handleIkGroup(ikEnv,ikGroup_undamped)==simIK.result_fail then -- try to solve with the undamped method
        -- the position/orientation could not be reached.
       simIK.handleIkGroup(ikEnv,ikGroup_damped) -- try to solve with the damped method
        if not ikFailedReportHandle then -- We display a IK failure report message
            ikFailedReportHandle=sim.displayDialog("IK failure report","RobotB: IK solver failed.",sim.dlgstyle_message,false,"",nil,{1,0.7,0,0,0,0})
        end
    else
        if ikFailedReportHandle then
            sim.endDialog(ikFailedReportHandle) -- We close any report message about IK failure
            ikFailedReportHandle=nil
        end
    end
    
    for i=1,#simJoints,1 do
        sim.setJointPosition(simJoints[i],simIK.getJointPosition(ikEnv,ikJoints[i])) -- apply the joint values computed in the IK environment to their CoppeliaSim joint counterparts
    end
end 

</t>
<t tx="leo.20210602170939.13">function sysCall_cleanup() 
    simIK.eraseEnvironment(ikEnv) -- erase the IK environment
end 
</t>
<t tx="leo.20210602170939.2"></t>
<t tx="leo.20210602170939.3">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210602170939.4">function sysCall_init()
    -- sim.handle_self is the handle of the object associated with the script currently executing
    h=sim.getObjectHandle(sim.handle_self)
    initM=sim.getObjectMatrix(h,-1)
end

</t>
<t tx="leo.20210602170939.5">function sysCall_actuation()
    local t=sim.getSimulationTime()
    local p={0.11*math.sin(t*1),0.07*math.sin(t*1.2),0.05*math.sin(t*1.6)}
    local e={0.1*math.sin(t*0.5),0.05*math.sin(t*0.3),0.025*math.sin(t)}
    local m=sim.buildMatrix(p,e)
    m=sim.multiplyMatrices(initM,m)
    sim.setObjectMatrix(h,-1,m)
end
</t>
<t tx="leo.20210602170939.6">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210602170939.7">-- IK setup by using GUI method
function sysCall_init() 
    ik_undamped=sim.getIkGroupHandle('RobotA_undamped')
    ik_damped=sim.getIkGroupHandle('RobotA_damped')
end

</t>
<t tx="leo.20210602170939.8">function sysCall_cleanup() 
 
end 

</t>
<t tx="leo.20210602170939.9">function sysCall_actuation() 
    if sim.handleIkGroup(ik_undamped)==sim.ikresult_fail then
        -- the position/orientation could not be reached.
        sim.handleIkGroup(ik_damped) -- Apply a damped resolution method
        if not ikFailedReportHandle then -- We display a IK failure report message
            ikFailedReportHandle=sim.displayDialog("IK failure report","RobotA: IK solver failed.",sim.dlgstyle_message,false,"",nil,{1,0.7,0,0,0,0})
        end
    else
        if ikFailedReportHandle then
            sim.endDialog(ikFailedReportHandle) -- We close any report message about IK failure
            ikFailedReportHandle=nil
        end
    end
end 
</t>
<t tx="leo.20210602200835.1">sim.handle_self, in order to retrieve the handle of the object associated with the script currently executing.</t>
<t tx="leo.20210602201605.1">https://www.coppeliarobotics.com/helpFiles/en/regularApi/simGetObjectMatrix.htm
Retrieves the transformation matrix of an object. 

initM=sim.getObjectMatrix(h,-1) get absolute transformation matrix of h
</t>
<t tx="leo.20210602202348.1">https://www.coppeliarobotics.com/helpFiles/en/inverseKinematicsTutorial.htm

https://www.coppeliarobotics.com/helpFiles/en/solvingIkAndFk.htm

https://www.coppeliarobotics.com/helpFiles/en/coppeliaKinematicsRoutines-api.htm

https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctions.htm#simxCallScriptFunction</t>
<t tx="leo.20210602204142.1">https://www.coppeliarobotics.com/helpFiles/en/simIK.htm

simIK.constraint_position=simIK.constraint_x|simIK.constraint_y|simIK.constraint_z, 

simIK.constraint_orientation=simIK.constraint_alpha_beta|simIK.constraint_gamma, 

and 

simIK.constraint_pose=simIK.constraint_position|simIK.constraint_orientation</t>
</tnodes>
</leo_file>
