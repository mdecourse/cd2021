<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2"/>
<globals/>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="leo.20210522214552.1"><vh>@settings</vh>
<v t="leo.20210522214552.2"><vh>@data qt-gui-plugin-style-sheet</vh></v>
<v t="leo.20210522214552.3"><vh>@string initial_split_orientation = horizontal</vh></v>
</v>
<v t="leo.20210522214903.1"><vh>recursive importer</vh></v>
<v t="leo.20210527141258.1"><vh>imported files</vh>
<v t="leo.20210527141258.2"><vh>@path ./</vh>
<v t="leo.20210527141258.3"><vh>@clean base.lua</vh>
<v t="leo.20210527141258.4"><vh>signal_switch (base.lua)</vh></v>
<v t="leo.20210527141258.5"><vh>sysCall_threadmain (base.lua)</vh></v>
</v>
<v t="leo.20210527141258.6"><vh>@clean rotate.lua</vh>
<v t="leo.20210527141258.7"><vh>sysCall_init (rotate.lua)</vh></v>
<v t="leo.20210527141258.8"><vh>sysCall_actuation (rotate.lua)</vh></v>
<v t="leo.20210527141258.9"><vh>sysCall_sensing (rotate.lua)</vh></v>
<v t="leo.20210527141258.10"><vh>sysCall_cleanup (rotate.lua)</vh></v>
</v>
<v t="leo.20210527141258.11"><vh>@clean suctionpad.lua</vh>
<v t="leo.20210527141258.12"><vh>sysCall_init (suctionpad.lua)</vh></v>
<v t="leo.20210527141258.13"><vh>sysCall_cleanup (suctionpad.lua)</vh></v>
<v t="leo.20210527141258.14"><vh>sysCall_sensing (suctionpad.lua)</vh></v>
</v>
<v t="leo.20210527141258.15"><vh>@clean suctionpad0.lua</vh>
<v t="leo.20210527141258.16"><vh>sysCall_init (suctionpad0.lua)</vh></v>
<v t="leo.20210527141258.17"><vh>sysCall_cleanup (suctionpad0.lua)</vh></v>
<v t="leo.20210527141258.18"><vh>sysCall_sensing (suctionpad0.lua)</vh></v>
</v>
<v t="leo.20210527141258.19"><vh>@clean suctionpad1.lua</vh>
<v t="leo.20210527141258.20"><vh>sysCall_init (suctionpad1.lua)</vh></v>
<v t="leo.20210527141258.21"><vh>sysCall_cleanup (suctionpad1.lua)</vh></v>
<v t="leo.20210527141258.22"><vh>sysCall_sensing (suctionpad1.lua)</vh></v>
</v>
<v t="leo.20210527141258.23"><vh>@clean suctionpad2.lua</vh>
<v t="leo.20210527141258.24"><vh>sysCall_init (suctionpad2.lua)</vh></v>
<v t="leo.20210527141258.25"><vh>sysCall_cleanup (suctionpad2.lua)</vh></v>
<v t="leo.20210527141258.26"><vh>sysCall_sensing (suctionpad2.lua)</vh></v>
</v>
<v t="leo.20210527141258.27"><vh>@clean suctionpad3.lua</vh>
<v t="leo.20210527141258.28"><vh>sysCall_init (suctionpad3.lua)</vh></v>
<v t="leo.20210527141258.29"><vh>sysCall_cleanup (suctionpad3.lua)</vh></v>
<v t="leo.20210527141258.30"><vh>sysCall_sensing (suctionpad3.lua)</vh></v>
</v>
<v t="leo.20210527141258.31"><vh>@clean suctionpad4.lua</vh>
<v t="leo.20210527141258.32"><vh>sysCall_init (suctionpad4.lua)</vh></v>
<v t="leo.20210527141258.33"><vh>sysCall_cleanup (suctionpad4.lua)</vh></v>
<v t="leo.20210527141258.34"><vh>sysCall_sensing (suctionpad4.lua)</vh></v>
</v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="leo.20210522214552.1"></t>
<t tx="leo.20210522214552.2">QTreeWidget {
    /* These apply to the selected item, but not to editing items.*/
    background-color: #ffffec; /* Leo's traditional tree color */
    selection-color: black; /* was white */
    selection-background-color: lightgrey;
    /* font-family: SansSerif; */
    /*font-family: DejaVu Sans Mono;*/
    font-family:YaHei Mono;
    /* 標題字型大小設定 */
    font-size: 20px;
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
    font-size: 20px;
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
    font-size: 20px;
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
    font-size: 20px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

QLabel {
    font-family:YaHei Mono;'CherryPy', 'pytz', 'mako', 'beautifulsoup4', 'pymysql', 'peewee'
    /* 下方的 Minibuffer 標題字型大小 */
    font-size: 20px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

/* Editor labels */
QLineEdit#editorLabel {
    background-color: #ffffec;
    font-family:YaHei Mono;
    /* 沒有直接對應字型大小 */
    font-size: 20px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
    border: 2px;
    margin: 2px;
}</t>
<t tx="leo.20210522214552.3">horizontal: body pane to the left
vertical: body pane on the botton</t>
<t tx="leo.20210522214903.1">'''Recursively import all python files in a directory and clean the result.'''
# ctrl + b to execute

c.recursiveImport(
    dir_ = r'./',
    kind = '@clean', # The new best practice.
    safe_at_file = False,
    theTypes = ['.lua'] 
)</t>
<t tx="leo.20210527141258.1"></t>
<t tx="leo.20210527141258.10">function sysCall_cleanup()
    -- do some clean-up here
end
</t>
<t tx="leo.20210527141258.11">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210527141258.12">function sysCall_init() 
    modelBase1=sim.getObjectAssociatedWithScript(sim.handle_self)
    robotBase1=modelBase1
    while true do
        robotBase1=sim.getObjectParent(robotBase1)
        if robotBase1==-1 then
            robotName1='Base'
            break
        end
        robotName1=sim.getObjectName(robotBase1)
        suffix,suffixlessName=sim.getNameSuffix(robotName1)
        if suffixlessName=='Base' then
            break
        end
    end
    sa=sim.getObjectHandle('suctionPadSensor')
    la=sim.getObjectHandle('suctionPadLoopClosureDummy1')
    l2a=sim.getObjectHandle('suctionPadLoopClosureDummy2')
    ba=sim.getObjectHandle('suctionPad')
    suctionPadLink=sim.getObjectHandle('suctionPadLink')
    local gripperBase=sim.getObjectAssociatedWithScript(sim.handle_self)
    infiniteStrength=sim.getScriptSimulationParameter(sim.handle_self,'infiniteStrength')
    maxPullForce=sim.getScriptSimulationParameter(sim.handle_self,'maxPullForce')
    maxShearForce=sim.getScriptSimulationParameter(sim.handle_self,'maxShearForce')
    maxPeelTorque=sim.getScriptSimulationParameter(sim.handle_self,'maxPeelTorque')
    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end
</t>
<t tx="leo.20210527141258.13">function sysCall_cleanup() 
    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end 
</t>
<t tx="leo.20210527141258.14">function sysCall_sensing() 
    parent=sim.getObjectParent(la)
    local sig=sim.getIntegerSignal(robotName1 .."call_1")
    if (not sig) or (sig==0) then
        if (parent~=ba) then
            sim.setLinkDummy(la,-1)
            sim.setObjectParent(la,ba,true)
            ma=sim.getObjectMatrix(l2a,-1)
            sim.setObjectMatrix(la,-1,ma)
        end
    else
        if (parent==ba) then
            -- Here we want to detect a respondable shape, and then connect to it with a force sensor (via a loop closure dummy dummy link)
            -- However most respondable shapes are set to "non-detectable", so "sim.readProximitySensor" or similar will not work.
            -- But "sim.checkProximitySensor" or similar will work (they don't check the "detectable" flags), but we have to go through all shape objects!
            index=0
            while true do
                shape=sim.getObjects(index,sim.object_shape_type)
                if (shape==-1) then
                    break
                end
                if (shape~=ba) and (sim.getObjectInt32Parameter(shape,sim.shapeintparam_respondable)~=0) and (sim.checkProximitySensor(sa,shape)==1) then
                    -- Ok, we found a respondable shape that was detected
                    -- We connect to that shape:
                    -- Make sure the two dummies are initially coincident:
                    sim.setObjectParent(la,ba,true)
                    ma=sim.getObjectMatrix(l2a,-1)
                    sim.setObjectMatrix(la,-1,ma)
                    -- Do the connection:
                    sim.setObjectParent(la,shape,true)
                    sim.setLinkDummy(la,l2a)
                    break
                end
                index=index+1
            end
        else
            -- Here we have an object attached
            if (infiniteStrength==false) then
                -- We might have to conditionally beak it apart!
                result,force,torque=sim.readForceSensor(suctionPadLink) -- Here we read the median value out of 5 values (check the force sensor prop. dialog)
                if (result&gt;0) then
                    breakIt=false
                    if (force[3]&gt;maxPullForce) then breakIt=true end
                    sf=math.sqrt(force[1]*force[1]+force[2]*force[2])
                    if (sf&gt;maxShearForce) then breakIt=true end
                    if (torque[1]&gt;maxPeelTorque) then breakIt=true end
                    if (torque[2]&gt;maxPeelTorque) then breakIt=true end
                    if (breakIt) then
                        -- We break the link:
                        sim.setLinkDummy(la,-1)
                        sim.setObjectParent(la,ba,true)
                        ma=sim.getObjectMatrix(l2a,-1)
                        sim.setObjectMatrix(la,-1,ma)
                    end
                end
            end
        end
    end
end 
</t>
<t tx="leo.20210527141258.15">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210527141258.16">function sysCall_init() 
    modelBase2=sim.getObjectAssociatedWithScript(sim.handle_self)
    robotBase2=modelBase2
    while true do
        robotBase2=sim.getObjectParent(robotBase2)
        if robotBase2==-1 then
            robotName2='Base'
            break
        end
        robotName2=sim.getObjectName(robotBase2)
        suffix,suffixlessName=sim.getNameSuffix(robotName2)
        if suffixlessName=='Base' then
            break
        end
    end
    sa=sim.getObjectHandle('suctionPadSensor#0')
    la=sim.getObjectHandle('suctionPadLoopClosureDummy1#0')
    l2a=sim.getObjectHandle('suctionPadLoopClosureDummy2#0')
    ba=sim.getObjectHandle('suctionPad#0')
    suctionPadLink=sim.getObjectHandle('suctionPadLink#0')
    local gripperBase=sim.getObjectAssociatedWithScript(sim.handle_self)
    infiniteStrength=sim.getScriptSimulationParameter(sim.handle_self,'infiniteStrength')
    maxPullForce=sim.getScriptSimulationParameter(sim.handle_self,'maxPullForce')
    maxShearForce=sim.getScriptSimulationParameter(sim.handle_self,'maxShearForce')
    maxPeelTorque=sim.getScriptSimulationParameter(sim.handle_self,'maxPeelTorque')
    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end
</t>
<t tx="leo.20210527141258.17">function sysCall_cleanup() 
    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end 
</t>
<t tx="leo.20210527141258.18">function sysCall_sensing() 
    parent=sim.getObjectParent(la)
    local sig=sim.getIntegerSignal(robotName2 .."call_2")
    if (not sig) or (sig==0) then
        if (parent~=ba) then
            sim.setLinkDummy(la,-1)
            sim.setObjectParent(la,ba,true)
            ma=sim.getObjectMatrix(l2a,-1)
            sim.setObjectMatrix(la,-1,ma)
        end
    else
        if (parent==ba) then
            -- Here we want to detect a respondable shape, and then connect to it with a force sensor (via a loop closure dummy dummy link)
            -- However most respondable shapes are set to "non-detectable", so "sim.readProximitySensor" or similar will not work.
            -- But "sim.checkProximitySensor" or similar will work (they don't check the "detectable" flags), but we have to go through all shape objects!
            index=0
            while true do
                shape=sim.getObjects(index,sim.object_shape_type)
                if (shape==-1) then
                    break
                end
                if (shape~=ba) and (sim.getObjectInt32Parameter(shape,sim.shapeintparam_respondable)~=0) and (sim.checkProximitySensor(sa,shape)==1) then
                    -- Ok, we found a respondable shape that was detected
                    -- We connect to that shape:
                    -- Make sure the two dummies are initially coincident:
                    sim.setObjectParent(la,ba,true)
                    ma=sim.getObjectMatrix(l2a,-1)
                    sim.setObjectMatrix(la,-1,ma)
                    -- Do the connection:
                    sim.setObjectParent(la,shape,true)
                    sim.setLinkDummy(la,l2a)
                    break
                end
                index=index+1
            end
        else
            -- Here we have an object attached
            if (infiniteStrength==false) then
                -- We might have to conditionally beak it apart!
                result,force,torque=sim.readForceSensor(suctionPadLink) -- Here we read the median value out of 5 values (check the force sensor prop. dialog)
                if (result&gt;0) then
                    breakIt=false
                    if (force[3]&gt;maxPullForce) then breakIt=true end
                    sf=math.sqrt(force[1]*force[1]+force[2]*force[2])
                    if (sf&gt;maxShearForce) then breakIt=true end
                    if (torque[1]&gt;maxPeelTorque) then breakIt=true end
                    if (torque[2]&gt;maxPeelTorque) then breakIt=true end
                    if (breakIt) then
                        -- We break the link:
                        sim.setLinkDummy(la,-1)
                        sim.setObjectParent(la,ba,true)
                        ma=sim.getObjectMatrix(l2a,-1)
                        sim.setObjectMatrix(la,-1,ma)
                    end
                end
            end
        end
    end
end 
</t>
<t tx="leo.20210527141258.19">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210527141258.2"></t>
<t tx="leo.20210527141258.20">function sysCall_init() 
    modelBase3=sim.getObjectAssociatedWithScript(sim.handle_self)
    robotBase3=modelBase3
    while true do
        robotBase3=sim.getObjectParent(robotBase3)
        if robotBase3==-1 then
            robotName3='Base'
            break
        end
        robotName3=sim.getObjectName(robotBase3)
        suffix,suffixlessName=sim.getNameSuffix(robotName3)
        if suffixlessName=='Base' then
            break
        end
    end
    sa=sim.getObjectHandle('suctionPadSensor')
    la=sim.getObjectHandle('suctionPadLoopClosureDummy1')
    l2a=sim.getObjectHandle('suctionPadLoopClosureDummy2')
    ba=sim.getObjectHandle('suctionPad')
    suctionPadLink=sim.getObjectHandle('suctionPadLink')
    local gripperBase=sim.getObjectAssociatedWithScript(sim.handle_self)
    infiniteStrength=sim.getScriptSimulationParameter(sim.handle_self,'infiniteStrength')
    maxPullForce=sim.getScriptSimulationParameter(sim.handle_self,'maxPullForce')
    maxShearForce=sim.getScriptSimulationParameter(sim.handle_self,'maxShearForce')
    maxPeelTorque=sim.getScriptSimulationParameter(sim.handle_self,'maxPeelTorque')
    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end
</t>
<t tx="leo.20210527141258.21">function sysCall_cleanup() 
    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end 
</t>
<t tx="leo.20210527141258.22">function sysCall_sensing() 
    parent=sim.getObjectParent(la)
    local sig=sim.getIntegerSignal(robotName3 .."call_3")
    if (not sig) or (sig==0) then
        if (parent~=ba) then
            sim.setLinkDummy(la,-1)
            sim.setObjectParent(la,ba,true)
            ma=sim.getObjectMatrix(l2a,-1)
            sim.setObjectMatrix(la,-1,ma)
        end
    else
        if (parent==ba) then
            -- Here we want to detect a respondable shape, and then connect to it with a force sensor (via a loop closure dummy dummy link)
            -- However most respondable shapes are set to "non-detectable", so "sim.readProximitySensor" or similar will not work.
            -- But "sim.checkProximitySensor" or similar will work (they don't check the "detectable" flags), but we have to go through all shape objects!
            index=0
            while true do
                shape=sim.getObjects(index,sim.object_shape_type)
                if (shape==-1) then
                    break
                end
                if (shape~=ba) and (sim.getObjectInt32Parameter(shape,sim.shapeintparam_respondable)~=0) and (sim.checkProximitySensor(sa,shape)==1) then
                    -- Ok, we found a respondable shape that was detected
                    -- We connect to that shape:
                    -- Make sure the two dummies are initially coincident:
                    sim.setObjectParent(la,ba,true)
                    ma=sim.getObjectMatrix(l2a,-1)
                    sim.setObjectMatrix(la,-1,ma)
                    -- Do the connection:
                    sim.setObjectParent(la,shape,true)
                    sim.setLinkDummy(la,l2a)
                    break
                end
                index=index+1
            end
        else
            -- Here we have an object attached
            if (infiniteStrength==false) then
                -- We might have to conditionally beak it apart!
                result,force,torque=sim.readForceSensor(suctionPadLink) -- Here we read the median value out of 5 values (check the force sensor prop. dialog)
                if (result&gt;0) then
                    breakIt=false
                    if (force[3]&gt;maxPullForce) then breakIt=true end
                    sf=math.sqrt(force[1]*force[1]+force[2]*force[2])
                    if (sf&gt;maxShearForce) then breakIt=true end
                    if (torque[1]&gt;maxPeelTorque) then breakIt=true end
                    if (torque[2]&gt;maxPeelTorque) then breakIt=true end
                    if (breakIt) then
                        -- We break the link:
                        sim.setLinkDummy(la,-1)
                        sim.setObjectParent(la,ba,true)
                        ma=sim.getObjectMatrix(l2a,-1)
                        sim.setObjectMatrix(la,-1,ma)
                    end
                end
            end
        end
    end
end 
</t>
<t tx="leo.20210527141258.23">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210527141258.24">function sysCall_init() 
    modelBase4=sim.getObjectAssociatedWithScript(sim.handle_self)
    robotBase4=modelBase4
    while true do
        robotBase4=sim.getObjectParent(robotBase4)
        if robotBase4==-1 then
            robotName4='Base'
            break
        end
        robotName4=sim.getObjectName(robotBase4)
        suffix,suffixlessName=sim.getNameSuffix(robotName4)
        if suffixlessName=='Base' then
            break
        end
    end
    sa=sim.getObjectHandle('suctionPadSensor#2')
    la=sim.getObjectHandle('suctionPadLoopClosureDummy1#2')
    l2a=sim.getObjectHandle('suctionPadLoopClosureDummy2#2')
    ba=sim.getObjectHandle('suctionPad')
    suctionPadLink=sim.getObjectHandle('suctionPadLink#2')
    local gripperBase=sim.getObjectAssociatedWithScript(sim.handle_self)
    infiniteStrength=sim.getScriptSimulationParameter(sim.handle_self,'infiniteStrength')
    maxPullForce=sim.getScriptSimulationParameter(sim.handle_self,'maxPullForce')
    maxShearForce=sim.getScriptSimulationParameter(sim.handle_self,'maxShearForce')
    maxPeelTorque=sim.getScriptSimulationParameter(sim.handle_self,'maxPeelTorque')
    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end
</t>
<t tx="leo.20210527141258.25">function sysCall_cleanup() 
    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end 
</t>
<t tx="leo.20210527141258.26">function sysCall_sensing() 
    parent=sim.getObjectParent(la)
    local sig=sim.getIntegerSignal(robotName4 .."call_4")
    if (not sig) or (sig==0) then
        if (parent~=ba) then
            sim.setLinkDummy(la,-1)
            sim.setObjectParent(la,ba,true)
            ma=sim.getObjectMatrix(l2a,-1)
            sim.setObjectMatrix(la,-1,ma)
        end
    else
        if (parent==ba) then
            -- Here we want to detect a respondable shape, and then connect to it with a force sensor (via a loop closure dummy dummy link)
            -- However most respondable shapes are set to "non-detectable", so "sim.readProximitySensor" or similar will not work.
            -- But "sim.checkProximitySensor" or similar will work (they don't check the "detectable" flags), but we have to go through all shape objects!
            index=0
            while true do
                shape=sim.getObjects(index,sim.object_shape_type)
                if (shape==-1) then
                    break
                end
                if (shape~=ba) and (sim.getObjectInt32Parameter(shape,sim.shapeintparam_respondable)~=0) and (sim.checkProximitySensor(sa,shape)==1) then
                    -- Ok, we found a respondable shape that was detected
                    -- We connect to that shape:
                    -- Make sure the two dummies are initially coincident:
                    sim.setObjectParent(la,ba,true)
                    ma=sim.getObjectMatrix(l2a,-1)
                    sim.setObjectMatrix(la,-1,ma)
                    -- Do the connection:
                    sim.setObjectParent(la,shape,true)
                    sim.setLinkDummy(la,l2a)
                    break
                end
                index=index+1
            end
        else
            -- Here we have an object attached
            if (infiniteStrength==false) then
                -- We might have to conditionally beak it apart!
                result,force,torque=sim.readForceSensor(suctionPadLink) -- Here we read the median value out of 5 values (check the force sensor prop. dialog)
                if (result&gt;0) then
                    breakIt=false
                    if (force[3]&gt;maxPullForce) then breakIt=true end
                    sf=math.sqrt(force[1]*force[1]+force[2]*force[2])
                    if (sf&gt;maxShearForce) then breakIt=true end
                    if (torque[1]&gt;maxPeelTorque) then breakIt=true end
                    if (torque[2]&gt;maxPeelTorque) then breakIt=true end
                    if (breakIt) then
                        -- We break the link:
                        sim.setLinkDummy(la,-1)
                        sim.setObjectParent(la,ba,true)
                        ma=sim.getObjectMatrix(l2a,-1)
                        sim.setObjectMatrix(la,-1,ma)
                    end
                end
            end
        end
    end
end 
</t>
<t tx="leo.20210527141258.27">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210527141258.28">function sysCall_init() 
    modelBase5=sim.getObjectAssociatedWithScript(sim.handle_self)
    robotBase5=modelBase5
    while true do
        robotBase5=sim.getObjectParent(robotBase5)
        if robotBase5==-1 then
            robotName5='Base'
            break
        end
        robotName5=sim.getObjectName(robotBase5)
        suffix,suffixlessName=sim.getNameSuffix(robotName5)
        if suffixlessName=='Base' then
            break
        end
    end
    sa=sim.getObjectHandle('suctionPadSensor#3')
    la=sim.getObjectHandle('suctionPadLoopClosureDummy1#3')
    l2a=sim.getObjectHandle('suctionPadLoopClosureDummy2#3')
    ba=sim.getObjectHandle('suctionPad')
    suctionPadLink=sim.getObjectHandle('suctionPadLink#3')
    local gripperBase=sim.getObjectAssociatedWithScript(sim.handle_self)
    infiniteStrength=sim.getScriptSimulationParameter(sim.handle_self,'infiniteStrength')
    maxPullForce=sim.getScriptSimulationParameter(sim.handle_self,'maxPullForce')
    maxShearForce=sim.getScriptSimulationParameter(sim.handle_self,'maxShearForce')
    maxPeelTorque=sim.getScriptSimulationParameter(sim.handle_self,'maxPeelTorque')
    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end
</t>
<t tx="leo.20210527141258.29">function sysCall_cleanup() 
    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end 
</t>
<t tx="leo.20210527141258.3">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210527141258.30">function sysCall_sensing() 
    parent=sim.getObjectParent(la)
    local sig=sim.getIntegerSignal(robotName5 .."call_5")
    if (not sig) or (sig==0) then
        if (parent~=ba) then
            sim.setLinkDummy(la,-1)
            sim.setObjectParent(la,ba,true)
            ma=sim.getObjectMatrix(l2a,-1)
            sim.setObjectMatrix(la,-1,ma)
        end
    else
        if (parent==ba) then
            -- Here we want to detect a respondable shape, and then connect to it with a force sensor (via a loop closure dummy dummy link)
            -- However most respondable shapes are set to "non-detectable", so "sim.readProximitySensor" or similar will not work.
            -- But "sim.checkProximitySensor" or similar will work (they don't check the "detectable" flags), but we have to go through all shape objects!
            index=0
            while true do
                shape=sim.getObjects(index,sim.object_shape_type)
                if (shape==-1) then
                    break
                end
                if (shape~=ba) and (sim.getObjectInt32Parameter(shape,sim.shapeintparam_respondable)~=0) and (sim.checkProximitySensor(sa,shape)==1) then
                    -- Ok, we found a respondable shape that was detected
                    -- We connect to that shape:
                    -- Make sure the two dummies are initially coincident:
                    sim.setObjectParent(la,ba,true)
                    ma=sim.getObjectMatrix(l2a,-1)
                    sim.setObjectMatrix(la,-1,ma)
                    -- Do the connection:
                    sim.setObjectParent(la,shape,true)
                    sim.setLinkDummy(la,l2a)
                    break
                end
                index=index+1
            end
        else
            -- Here we have an object attached
            if (infiniteStrength==false) then
                -- We might have to conditionally beak it apart!
                result,force,torque=sim.readForceSensor(suctionPadLink) -- Here we read the median value out of 5 values (check the force sensor prop. dialog)
                if (result&gt;0) then
                    breakIt=false
                    if (force[3]&gt;maxPullForce) then breakIt=true end
                    sf=math.sqrt(force[1]*force[1]+force[2]*force[2])
                    if (sf&gt;maxShearForce) then breakIt=true end
                    if (torque[1]&gt;maxPeelTorque) then breakIt=true end
                    if (torque[2]&gt;maxPeelTorque) then breakIt=true end
                    if (breakIt) then
                        -- We break the link:
                        sim.setLinkDummy(la,-1)
                        sim.setObjectParent(la,ba,true)
                        ma=sim.getObjectMatrix(l2a,-1)
                        sim.setObjectMatrix(la,-1,ma)
                    end
                end
            end
        end
    end
end 
</t>
<t tx="leo.20210527141258.31">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210527141258.32">function sysCall_init() 
    modelBase6=sim.getObjectAssociatedWithScript(sim.handle_self)
    robotBase6=modelBase6
    while true do
        robotBase6=sim.getObjectParent(robotBase6)
        if robotBase6==-1 then
            robotName6='Base'
            break
        end
        robotName6=sim.getObjectName(robotBase6)
        suffix,suffixlessName=sim.getNameSuffix(robotName6)
        if suffixlessName=='Base' then
            break
        end
    end
    sa=sim.getObjectHandle('suctionPadSensor#4')
    la=sim.getObjectHandle('suctionPadLoopClosureDummy1#4')
    l2a=sim.getObjectHandle('suctionPadLoopClosureDummy2#4')
    ba=sim.getObjectHandle('suctionPad#4')
    suctionPadLink=sim.getObjectHandle('suctionPadLink#4')
    local gripperBase=sim.getObjectAssociatedWithScript(sim.handle_self)
    infiniteStrength=sim.getScriptSimulationParameter(sim.handle_self,'infiniteStrength')
    maxPullForce=sim.getScriptSimulationParameter(sim.handle_self,'maxPullForce')
    maxShearForce=sim.getScriptSimulationParameter(sim.handle_self,'maxShearForce')
    maxPeelTorque=sim.getScriptSimulationParameter(sim.handle_self,'maxPeelTorque')
    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end
</t>
<t tx="leo.20210527141258.33">function sysCall_cleanup() 
    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end 
</t>
<t tx="leo.20210527141258.34">function sysCall_sensing() 
    parent=sim.getObjectParent(la)
    local sig=sim.getIntegerSignal(robotName6 .."call_6")
    if (not sig) or (sig==0) then
        if (parent~=ba) then
            sim.setLinkDummy(la,-1)
            sim.setObjectParent(la,ba,true)
            ma=sim.getObjectMatrix(l2a,-1)
            sim.setObjectMatrix(la,-1,ma)
        end
    else
        if (parent==ba) then
            -- Here we want to detect a respondable shape, and then connect to it with a force sensor (via a loop closure dummy dummy link)
            -- However most respondable shapes are set to "non-detectable", so "sim.readProximitySensor" or similar will not work.
            -- But "sim.checkProximitySensor" or similar will work (they don't check the "detectable" flags), but we have to go through all shape objects!
            index=0
            while true do
                shape=sim.getObjects(index,sim.object_shape_type)
                if (shape==-1) then
                    break
                end
                if (shape~=ba) and (sim.getObjectInt32Parameter(shape,sim.shapeintparam_respondable)~=0) and (sim.checkProximitySensor(sa,shape)==1) then
                    -- Ok, we found a respondable shape that was detected
                    -- We connect to that shape:
                    -- Make sure the two dummies are initially coincident:
                    sim.setObjectParent(la,ba,true)
                    ma=sim.getObjectMatrix(l2a,-1)
                    sim.setObjectMatrix(la,-1,ma)
                    -- Do the connection:
                    sim.setObjectParent(la,shape,true)
                    sim.setLinkDummy(la,l2a)
                    break
                end
                index=index+1
            end
        else
            -- Here we have an object attached
            if (infiniteStrength==false) then
                -- We might have to conditionally beak it apart!
                result,force,torque=sim.readForceSensor(suctionPadLink) -- Here we read the median value out of 5 values (check the force sensor prop. dialog)
                if (result&gt;0) then
                    breakIt=false
                    if (force[3]&gt;maxPullForce) then breakIt=true end
                    sf=math.sqrt(force[1]*force[1]+force[2]*force[2])
                    if (sf&gt;maxShearForce) then breakIt=true end
                    if (torque[1]&gt;maxPeelTorque) then breakIt=true end
                    if (torque[2]&gt;maxPeelTorque) then breakIt=true end
                    if (breakIt) then
                        -- We break the link:
                        sim.setLinkDummy(la,-1)
                        sim.setObjectParent(la,ba,true)
                        ma=sim.getObjectMatrix(l2a,-1)
                        sim.setObjectMatrix(la,-1,ma)
                    end
                end
            end
        end
    end
end 
</t>
<t tx="leo.20210527141258.4">function signal_switch(singal,enable)
    modelBase1=sim.getObjectAssociatedWithScript(sim.handle_self)
    modelBase2=sim.getObjectAssociatedWithScript(sim.handle_self)
    modelBase3=sim.getObjectAssociatedWithScript(sim.handle_self)
    modelBase4=sim.getObjectAssociatedWithScript(sim.handle_self)
    modelBase5=sim.getObjectAssociatedWithScript(sim.handle_self)
    modelBase6=sim.getObjectAssociatedWithScript(sim.handle_self)
    modelName1=sim.getObjectName(modelBase1)
    modelName2=sim.getObjectName(modelBase2)
    modelName3=sim.getObjectName(modelBase3)
    modelName4=sim.getObjectName(modelBase4)
    modelName5=sim.getObjectName(modelBase5)
    modelName6=sim.getObjectName(modelBase6)
    if singal==1 or singal==12 then
        sim.setIntegerSignal(modelName1 .."call_1",enable)
    end
    if singal==2 or singal==11 then
        sim.setIntegerSignal(modelName2 .."call_2",enable)
    end
    if singal==3 or singal==10 then
        sim.setIntegerSignal(modelName3 .."call_3",enable)
    end
    if singal==4 or singal==9 then
        sim.setIntegerSignal(modelName4 .."call_4",enable)
    end
    if singal==5 or singal==8 then
        sim.setIntegerSignal(modelName5 .."call_5",enable)
    end
    if singal==6 or singal==7 then
        sim.setIntegerSignal(modelName6 .."call_6",enable)
    end
end
</t>
<t tx="leo.20210527141258.5">function sysCall_threadmain()
    joint01=sim.getObjectHandle('X')
    joint02=sim.getObjectHandle('Y')
    joint03=sim.getObjectHandle('Z')
    jointr=sim.getObjectHandle('Rotate')
    tt=1
    long_t=1.5
    long_long_t=3 --time set
    rotate_deg=0 --pad rotate
    atz=0  --altitude set
    setx=0.5
    setpx=-0.5 --center pick set
    sety=-0.16
    setpy=-0.16 --center fall set
    local pick_high={"0.0645","0.134","0.2025","0.2768"} --pick up high set
    local fall_high={"0.05","0.12","0.18","0.26"} --fall high set
    local high_up={"0","0","0.05","0.12"}
    cube=1              -- set cube
    ball_pick_time=0    --total ball we pick
    ball_put_time=31     --total ball we put
    while (ball_pick_time&lt;60) do
        for ball=1,6,1 do    --pick the ball
            ball_pick_time=ball_pick_time+1 --total time we pick
            i=1
            unit=0
            level=0
            while level &lt; ball_pick_time do  --find which level and place should be of the xy coordinates
                unit=unit+1
                level=level+unit^2
            end
            finding_XY=ball_pick_time   --this is the XY on that floor
            while(i&lt;=unit-1) do            
                finding_XY=finding_XY-(i^2) 
                i=i+1
            end
            X_Pos=finding_XY%unit       -- the X and Y coordinates(by balls)
             if X_Pos==0 then
                X_Pos=unit
            end
            Y_Pos=(math.ceil(finding_XY/unit)) 
            BaseX=setx-((unit-1)*0.05)--now we need to find the 0 of the xy
            BaseY=sety-((unit-1)*0.05)
            sim.setJointTargetPosition(joint01,BaseX+(0.1*(X_Pos-1))) --move to Position
            sim.wait(tt)
            sim.setJointTargetPosition(joint02,BaseY+(0.1*(Y_Pos-1)))
            sim.wait(tt)
            signal_switch(ball,1) --switch pad on
            sim.setJointTargetPosition(joint03,-pick_high[unit])--pick the pall
            sim.wait(tt)
            sim.setJointTargetPosition(joint03,atz-high_up[unit]) --after pick up we dont need to go that high
            sim.wait(tt)
            rotate_deg=rotate_deg+60  --rotate the pad
            sim.setJointTargetPosition(jointr,rotate_deg*math.pi/180)
            sim.wait(tt)
            sim.wait(tt)
        end
        sim.wait(long_t)
        sim.setJointTargetPosition(joint01,0)
        sim.setJointTargetPosition(joint02,0)
        sim.setJointTargetPosition(joint03,0)
        sim.wait(long_t)
        for ball=1,6,1 do --put the ball
            ball_put_time=ball_put_time-1
            i=1
            unit=0
            level=0
            while level &lt; ball_put_time do  --find which level and place should be of the xy coordinates
                unit=unit+1
                level=level+unit^2
            end
            finding_XY=ball_put_time   --this is the XY on that floor
            while(i&lt;=unit-1) do            
                finding_XY=finding_XY-(i^2) 
                i=i+1
            end
            X_Pos=finding_XY%unit       -- the X and Y coordinates(by balls)
             if X_Pos==0 then
                X_Pos=unit
            end
            Y_Pos=(math.ceil(finding_XY/unit)) 
            BaseX=setpx-((unit-1)*0.05)--now we need to find the 0 of the xy
            BaseY=setpy-((unit-1)*0.05)
            rotate_deg=rotate_deg-60  --rotate the pad
            sim.setJointTargetPosition(jointr,rotate_deg*math.pi/180)
            sim.wait(tt)
            sim.setJointTargetPosition(joint01,BaseX+(0.1*(X_Pos-1))) --move to Position
            sim.wait(tt)
            sim.setJointTargetPosition(joint02,BaseY+(0.1*(Y_Pos-1)))
            sim.wait(tt)
            sim.setJointTargetPosition(joint03,-fall_high[unit])--pick the pall
            sim.wait(tt)
            signal_switch(ball+6,0) --switch pad off
            sim.wait(tt)
            sim.setJointTargetPosition(joint03,atz-high_up[unit]) --after pick up we dont need to go that high
            sim.wait(tt)
            sim.wait(tt)
        end
        sim.wait(long_t)
        sim.setJointTargetPosition(joint01,0)
        sim.setJointTargetPosition(joint02,0)
        sim.setJointTargetPosition(joint03,0)
        sim.wait(long_t)
        if ball_pick_time==30 then
            pick_high={"0.07","0.138","0.2085","0.28"}
            setx=-setx
            setpx=-setpx
            ball_pick_time=0
            ball_put_time=31
        end
    end
end
</t>
<t tx="leo.20210527141258.6">@path ./
@others
-- See the user manual or the available code snippets for additional callback functions and details
@language lua
@tabwidth -4
</t>
<t tx="leo.20210527141258.7">function sysCall_init()
    -- do some initialization here
    jointr=sim.getObjectHandle('Rotate')
end
</t>
<t tx="leo.20210527141258.8">function sysCall_actuation()
    -- put your actuation code here
end
</t>
<t tx="leo.20210527141258.9">function sysCall_sensing()
    aa=(sim.getJointPosition(jointr)*180/math.pi)
    print(math.floor(aa))
end
</t>
</tnodes>
</leo_file>
