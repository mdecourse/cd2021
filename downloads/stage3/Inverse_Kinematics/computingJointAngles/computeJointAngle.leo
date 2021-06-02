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
<v t="leo.20210602170649.1"><vh>imported files</vh>
<v t="leo.20210602170649.2"><vh>@path ./</vh>
<v t="leo.20210602170649.3"><vh>@clean irb4600.lua</vh>
<v t="leo.20210602170649.4"><vh>sysCall_init (irb4600.lua)</vh></v>
<v t="leo.20210602170649.5"><vh>configurationValidationCallback (irb4600.lua)</vh></v>
<v t="leo.20210602170649.6"><vh>sysCall_actuation (irb4600.lua)</vh></v>
<v t="leo.20210602170649.7"><vh>sysCall_cleanup (irb4600.lua)</vh></v>
</v>
<v t="leo.20210602170649.8"><vh>@clean lbr4p_base.lua</vh>
<v t="leo.20210602170649.9"><vh>sysCall_init (lbr4p_base.lua)</vh></v>
<v t="leo.20210602170649.10"><vh>sysCall_actuation (lbr4p_base.lua)</vh></v>
</v>
<v t="leo.20210602170649.11"><vh>@clean revolute_joint.lua</vh>
<v t="leo.20210602170649.12"><vh>sysCall_init (revolute_joint.lua)</vh></v>
<v t="leo.20210602170649.13"><vh>sysCall_actuation (revolute_joint.lua)</vh></v>
</v>
<v t="leo.20210602170649.14"><vh>@clean revolute_joint0.lua</vh>
<v t="leo.20210602170649.15"><vh>sysCall_init (revolute_joint0.lua)</vh></v>
<v t="leo.20210602170649.16"><vh>sysCall_actuation (revolute_joint0.lua)</vh></v>
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
<t tx="leo.20210602170649.1"></t>
<t tx="leo.20210602170649.10">applyJoints=function(jointHandles,joints)
    for i=1,#jointHandles,1 do
        sim.setJointPosition(jointHandles[i],joints[i])
    end
end
function sysCall_actuation()
    local dummyHandle=targets[cnt1+1]
    local m=sim.getObjectMatrix(dummyHandle,-1)
    sim.setObjectMatrix(ikTarget,-1,m)
    state=sim.getConfigForTipPose(ikGroup,jh,0.5,100)
    if state then
        applyJoints(jh,state)
    end
    cnt2=cnt2+1
    if cnt2&gt;9 then
        cnt2=0
        cnt1=cnt1+1
        if cnt1&gt;3 then
            cnt1=0
        end
    end
end
</t>
<t tx="leo.20210602170649.11">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210602170649.12">function sysCall_init()
    h=sim.getObjectAssociatedWithScript(sim.handle_self)
    amplitude=0.5
    speed=1
end
</t>
<t tx="leo.20210602170649.13">function sysCall_actuation()
    sim.setJointPosition(h,math.sin(sim.getSimulationTime()*speed)*amplitude)
end
</t>
<t tx="leo.20210602170649.14">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210602170649.15">function sysCall_init()
    h=sim.getObjectAssociatedWithScript(sim.handle_self)
    amplitude=0.6
    speed=0.46
end
</t>
<t tx="leo.20210602170649.16">function sysCall_actuation()
    sim.setJointPosition(h,math.sin(sim.getSimulationTime()*speed)*amplitude)
end
</t>
<t tx="leo.20210602170649.2"></t>
<t tx="leo.20210602170649.3">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210602170649.4">function sysCall_init()
    simJointHandles={}
    for i=1,6,1 do
        simJointHandles[i]=sim.getObjectHandle('IRB4600_joint'..i)
    end
    simTip=sim.getObjectHandle('IRB4600_IkTip')
    simBase=sim.getObjectHandle('IRB4600')
    targets={sim.getObjectHandle('testTarget1'),sim.getObjectHandle('testTarget2'),sim.getObjectHandle('testTarget3'),sim.getObjectHandle('testTarget4')}
    cnt1=0
    cnt2=0
    -- Now build a kinematic chain and 2 IK groups (undamped and damped) inside of the IK plugin environment,
    -- based on the kinematics of the blue robot:
    ikJointHandles={}
    ikEnv=simIK.createEnvironment() -- create an IK environment
    local ikBase=simIK.createDummy(ikEnv) -- create a dummy in the IK environemnt
    simIK.setObjectMatrix(ikEnv,ikBase,-1,sim.getObjectMatrix(simBase,-1)) -- set that dummy into the same pose as its CoppeliaSim counterpart
    local parent=ikBase
    for i=1,#simJointHandles,1 do -- loop through all joints
        ikJointHandles[i]=simIK.createJoint(ikEnv,simIK.jointtype_revolute) -- create a joint in the IK environment
        simIK.setJointMode(ikEnv,ikJointHandles[i],simIK.jointmode_ik) -- set it into IK mode
        local cyclic,interv=sim.getJointInterval(simJointHandles[i])
        simIK.setJointInterval(ikEnv,ikJointHandles[i],cyclic,interv) -- set the same joint limits as its CoppeliaSim counterpart joint
        simIK.setJointPosition(ikEnv,ikJointHandles[i],sim.getJointPosition(simJointHandles[i])) -- set the same joint position as its CoppeliaSim counterpart joint
        simIK.setObjectMatrix(ikEnv,ikJointHandles[i],-1,sim.getObjectMatrix(simJointHandles[i],-1)) -- set the same object pose as its CoppeliaSim counterpart joint
        simIK.setObjectParent(ikEnv,ikJointHandles[i],parent,true) -- set its corresponding parent
        parent=ikJointHandles[i]
    end
    ikTip=simIK.createDummy(ikEnv) -- create the tip dummy in the IK environment
    simIK.setObjectMatrix(ikEnv,ikTip,-1,sim.getObjectMatrix(simTip,-1)) -- set that dummy into the same pose as its CoppeliaSim counterpart
    simIK.setObjectParent(ikEnv,ikTip,parent,true) -- attach it to the kinematic chain
    ikTarget=simIK.createDummy(ikEnv) -- create the target dummy in the IK environment
    simIK.setObjectMatrix(ikEnv,ikTarget,-1,sim.getObjectMatrix(simTip,-1)) -- set that dummy into the same pose as its CoppeliaSim counterpart
    simIK.setLinkedDummy(ikEnv,ikTip,ikTarget) -- link the two dummies
    ikGroup=simIK.createIkGroup(ikEnv) -- create an IK group
    simIK.setIkGroupCalculation(ikEnv,ikGroup,simIK.method_pseudo_inverse,0,3) -- set its resolution method to undamped
    local ikElementHandle=simIK.addIkElement(ikEnv,ikGroup,ikTip) -- add an IK element to that IK group
    simIK.setIkElementBase(ikEnv,ikGroup,ikElementHandle,ikBase) -- specify the base of that IK element
    simIK.setIkElementConstraints(ikEnv,ikGroup,ikElementHandle,simIK.constraint_pose) -- specify the constraints of that IK element
    simIK.setIkElementPrecision(ikEnv,ikGroup,ikElementHandle,{0.00005,0.1*math.pi/180})
end
</t>
<t tx="leo.20210602170649.5">applyJoints=function(jointHandles,joints)
    for i=1,#jointHandles,1 do
        sim.setJointPosition(jointHandles[i],joints[i])
    end
end
function configurationValidationCallback(config)
    sim.addLog(sim.verbosity_scriptinfos,"Hello from validation callback")
    -- Here you could check for collisions, and other test. If the configuration is valid, return true
    return true
end
</t>
<t tx="leo.20210602170649.6">function sysCall_actuation()
    local dummyHandle=targets[cnt1+1]
    local m=sim.getObjectMatrix(dummyHandle,-1)
    simIK.setObjectMatrix(ikEnv,ikTarget,-1,m)
    -- Search for a configuration for a maximum of 100 ms:
    local startTime=sim.getSystemTimeInMs(-1)
    while sim.getSystemTimeInMs(startTime)&lt;100 do
        local validationCB=''
        -- uncomment following if you need to perform additional checks for a found configuration:
        --local validationCB='configurationValidationCallback@IRB4600'
        local state=simIK.getConfigForTipPose(ikEnv,ikGroup,ikJointHandles,0.65,10000,{1,1,1,0.1},validationCB)
        if state then
            applyJoints(simJointHandles,state)
            break
        end
    end
    cnt2=cnt2+1
    if cnt2&gt;20 then
        cnt2=0
        cnt1=cnt1+1
        if cnt1&gt;3 then
            cnt1=0
        end
    end
end
</t>
<t tx="leo.20210602170649.7">function sysCall_cleanup()
    simIK.eraseEnvironment(ikEnv)
end
</t>
<t tx="leo.20210602170649.8">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210602170649.9">function sysCall_init()
    jh={-1,-1,-1,-1,-1,-1,-1}
    for i=1,7,1 do
        jh[i]=sim.getObjectHandle('j'..i)
    end
    ikGroup=sim.getIkGroupHandle('ik')
    ikTarget=sim.getObjectHandle('target')
    targets={sim.getObjectHandle('testTarget5'),sim.getObjectHandle('testTarget6'),sim.getObjectHandle('testTarget7'),sim.getObjectHandle('testTarget8')}
    cnt1=0
    cnt2=0
end
</t>
</tnodes>
</leo_file>
