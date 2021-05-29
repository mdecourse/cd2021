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
<v t="leo.20210526155936.1"><vh>About W14 task</vh>
<v t="leo.20210529151306.1"><vh>mtbrobot_w14</vh></v>
</v>
<v t="leo.20210529164809.1"><vh>reference</vh></v>
<v t="leo.20210529215420.1"><vh>force sensor</vh></v>
<v t="leo.20210529155453.1"><vh>recursive importer</vh></v>
<v t="leo.20210529155606.1"><vh>imported files</vh>
<v t="leo.20210529155606.2"><vh>@path ./</vh>
<v t="leo.20210529155606.8"><vh>@clean mtbrobot_w14.lua</vh>
<v t="leo.20210529155606.9"><vh>sysCall_init (mtbrobot_w14.lua)</vh></v>
<v t="leo.20210529155606.10"><vh>sysCall_actuation (mtbrobot_w14.lua)</vh></v>
<v t="leo.20210529155606.11"><vh>sysCall_sensing (mtbrobot_w14.lua)</vh></v>
<v t="leo.20210529155606.12"><vh>sysCall_cleanup (mtbrobot_w14.lua)</vh></v>
<v t="leo.20210529155606.13"><vh>insertBox (mtbrobot_w14.lua)</vh></v>
</v>
<v t="leo.20210529155606.18"><vh>@clean suctionpad_w14.lua</vh>
<v t="leo.20210529155606.19"><vh>sysCall_init (suctionpad_w14.lua)</vh></v>
<v t="leo.20210529155606.20"><vh>sysCall_cleanup (suctionpad_w14.lua)</vh></v>
<v t="leo.20210529155606.21"><vh>sysCall_sensing (suctionpad_w14.lua)</vh></v>
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
<t tx="leo.20210526155936.1">https://www.coppeliarobotics.com/helpFiles/en/robotLanguageIntegrationTutorial.htm

目前 MTB_robot 是一項四軸機械手臂, 採用特殊的指令語言令 robot 移動, 並利用 suction pad 執行 pick and place

請各組設法去除原有的特殊控制語法, 編寫一組通用的 lua 程式完成上述 MTB_robot 取放 block 的操作流程.</t>
<t tx="leo.20210529151306.1">直接以 lua 驅動 robot</t>
<t tx="leo.20210529155453.1">'''Recursively import all python files in a directory and clean the result.'''
# ctrl + b to execute

c.recursiveImport(
    dir_ = r'./',
    kind = '@clean', # The new best practice.
    safe_at_file = False,
    theTypes = ['.lua'] 
)</t>
<t tx="leo.20210529155606.1"></t>
<t tx="leo.20210529155606.10">function sysCall_actuation() 
    --degree = 2.math.pi/180
    --sim.setJointTargetPosition(axis1, 30*degree)
    --sim.setObjectPosition(mtb3, -1, {0.2, 0.3, 0.2})
    
    --sim.setJointPosition(axis1, -math.pi*0.5)
    
    message, auxiliaryData=sim.getSimulatorMessage()
        while message ~= -1 do
            key=auxiliaryData[1]
            sim.addStatusbarMessage('key:'..key)
            if (message==sim.message_keypress) then
                if (auxiliaryData[1]==112) then --p
sim.setScriptSimulationParameter(sim.getScriptAssociatedWithObject(suctionPad),'active','true')
                end -- if
                if (auxiliaryData[1]==113) then --q
sim.setScriptSimulationParameter(sim.getScriptAssociatedWithObject(suctionPad),'active','false')
                end -- if
                if (auxiliaryData[1]==114) then --r
                     rotation1 = rotation1 + 5*deg
                     sim.setJointPosition(axis1, rotation1)
                end -- if
                if (auxiliaryData[1]==108) then --r
                     rotation1 = rotation1 - 5*deg
                     sim.setJointPosition(axis1, rotation1)
                end -- if
           end  -- if
    message, auxiliaryData=sim.getSimulatorMessage()
        end -- while
end -- function
</t>
<t tx="leo.20210529155606.11">function sysCall_sensing() 
--[[
    -- Read Proximity sensor (0= nothing detected, 1 = object detected)
    local res = sim.readProximitySensor(proximity)

    -- Check if possible to insert an new box
    if (sim.getSimulationTime()-T_last_inserted &gt; T_insert) and not hasStopped then
        insertBox()
    end

    -- If proximity sensor detects an object, stop the belt, stop inserting objects
    if res == 1 and not hasStopped then
        if boolList[1] then
            sim.setScriptSimulationParameter(sim.handle_self,"conveyorBeltVelocity",0)
            deltaTime = sim.getSimulationTime()-T_last_inserted
            hasStopped = true
        else
            local box = table.remove(boxList,1)
            local boxDummy = table.remove(boxDummyList,1)
            table.remove(boolList,1)

            sim.removeObject(box)
            sim.removeObject(boxDummy)
        end
    end

    -- If proximity sensor detects nothing and belt has stopped, start belt, continue inserting
    if res == 0 and hasStopped then
        sim.setScriptSimulationParameter(sim.handle_self,"conveyorBeltVelocity",beltSpeed)
        hasStopped = false
        T_last_inserted = sim.getSimulationTime()-deltaTime
    end
    
]]--
end
</t>
<t tx="leo.20210529155606.12">function sysCall_cleanup() 
end 
</t>
<t tx="leo.20210529155606.13">function insertBox()
    -- Generate random numbers
    local rand1 = math.random()
    local rand2 = math.random()
    local rand3 = math.random()
    -- Generate random disturbances on position and orientation
    local dx = (2*rand1-1)*0.1
    local dy = (2*rand2-1)*0.1
    local dphi = (2*rand3-1)*0.5
    local disturbedCoordinates = {0,0,0}
    disturbedCoordinates[1] = insertCoordinate[1]+dx
    disturbedCoordinates[2] = insertCoordinate[2]+dy
    disturbedCoordinates[3] = insertCoordinate[3]
    -- Copy and paste box and boxDummy
    local insertedObjects = sim.copyPasteObjects({box,boxDummy},0)
    -- Update last inserted box time
    T_last_inserted = sim.getSimulationTime()
    -- Move and rotate
    sim.setObjectPosition(insertedObjects[1],-1,disturbedCoordinates)
    sim.setObjectOrientation(insertedObjects[1],-1,{0,0,dphi})
    -- Store handles to boxes and dummies
    table.insert(boxList,insertedObjects[1])
    table.insert(boxDummyList,insertedObjects[2]) 
    -- Decide if object is good or bad
    local decision = math.random() 
    if decision &lt;= goodPercentage then
    -- Object is good, assign goodColor
        sim.setShapeColor(insertedObjects[1],nil,sim.colorcomponent_ambient_diffuse,goodColor)
        table.insert(boolList,true)
    else
    -- Object is bad, assign random color
        sim.setShapeColor(insertedObjects[1],nil,sim.colorcomponent_ambient_diffuse,{rand1,rand2,rand3})
        table.insert(boolList,false)
    end
end
</t>
<t tx="leo.20210529155606.18">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210529155606.19">function sysCall_init() 
    s=sim.getObjectHandle('suctionPadSensor')
    l=sim.getObjectHandle('suctionPadLoopClosureDummy1')
    l2=sim.getObjectHandle('suctionPadLoopClosureDummy2')
    b=sim.getObjectHandle('suctionPad')
    suctionPadLink=sim.getObjectHandle('suctionPadLink')

    infiniteStrength=sim.getScriptSimulationParameter(sim.handle_self,'infiniteStrength')
    maxPullForce=sim.getScriptSimulationParameter(sim.handle_self,'maxPullForce')
    maxShearForce=sim.getScriptSimulationParameter(sim.handle_self,'maxShearForce')
    maxPeelTorque=sim.getScriptSimulationParameter(sim.handle_self,'maxPeelTorque')

    sim.setLinkDummy(l,-1)
    sim.setObjectParent(l,b,true)
    m=sim.getObjectMatrix(l2,-1)
    sim.setObjectMatrix(l,-1,m)
end

</t>
<t tx="leo.20210529155606.2"></t>
<t tx="leo.20210529155606.20">function sysCall_cleanup() 
--[[
    sim.setLinkDummy(l,-1)
    sim.setObjectParent(l,b,true)
    m=sim.getObjectMatrix(l2,-1)
    sim.setObjectMatrix(l,-1,m)
]]--
end 

</t>
<t tx="leo.20210529155606.21">function sysCall_sensing() 
    parent=sim.getObjectParent(l)
    if (sim.getScriptSimulationParameter(sim.handle_self,'active')==false) then
        if (parent~=b) then
            sim.setLinkDummy(l,-1)
            sim.setObjectParent(l,b,true)
            m=sim.getObjectMatrix(l2,-1)
            sim.setObjectMatrix(l,-1,m)
        end
    else
        if (parent==b) then
            -- Here we want to detect a respondable shape, and then connect to it with a force sensor (via a loop closure dummy dummy link)
            -- However most respondable shapes are set to "non-detectable", so "sim.readProximitySensor" or similar will not work.
            -- But "sim.checkProximitySensor" or similar will work (they don't check the "detectable" flags), but we have to go through all shape objects!
            index=0
            while true do
                shape=sim.getObjects(index,sim.object_shape_type)
                if (shape==-1) then
                    break
                end
                if (shape~=b) and (sim.getObjectInt32Parameter(shape,sim.shapeintparam_respondable)~=0) and (sim.checkProximitySensor(s,shape)==1) then
                    -- Ok, we found a respondable shape that was detected
                    -- We connect to that shape:
                    -- Make sure the two dummies are initially coincident:
                    sim.setObjectParent(l,b,true)
                    m=sim.getObjectMatrix(l2,-1)
                    sim.setObjectMatrix(l,-1,m)
                    -- Do the connection:
                    sim.setObjectParent(l,shape,true)
                    sim.setLinkDummy(l,l2)
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
                        sim.setLinkDummy(l,-1)
                        sim.setObjectParent(l,b,true)
                        m=sim.getObjectMatrix(l2,-1)
                        sim.setObjectMatrix(l,-1,m)
                    end
                end
            end
        end
    end
    if (sim.getSimulationState()==sim.simulation_advancing_lastbeforestop) then
        sim.setLinkDummy(l,-1)
        sim.setObjectParent(l,b,true)
        m=sim.getObjectMatrix(l2,-1)
        sim.setObjectMatrix(l,-1,m)
    end
end 
</t>
<t tx="leo.20210529155606.8">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210529155606.9">function sysCall_init() 
    axis1=sim.getObjectHandle('MTB_axis1')
    axis2=sim.getObjectHandle('MTB_axis2')
    axis3=sim.getObjectHandle('MTB_axis3')
    axis4=sim.getObjectHandle('MTB_axis4')
    mtb3=sim.getObjectHandle('MTB_link3Respondable')
    suctionPad=sim.getObjectHandle('suctionPad')
    rotation1 = 0
    deg = math.pi/180
end
</t>
<t tx="leo.20210529164809.1">@language lua
function sysCall_init()
         
    jointHandles={{-1,-1,-1},{-1,-1,-1},{-1,-1,-1}}
    firstPartTorqueSensorHandles={-1,-1,-1}
    for i=0,2,1 do
        if (i~=1) then
            jointHandles[i+1][1]=sim.getObjectHandle('BarrettHand_jointA_'..i)
        end
        jointHandles[i+1][2]=sim.getObjectHandle('BarrettHand_jointB_'..i)
        jointHandles[i+1][3]=sim.getObjectHandle('BarrettHand_jointC_'..i)
        firstPartTorqueSensorHandles[i+1]=sim.getObjectHandle('BarrettHand_fingerSensor'..i)
    end
    communicationTube=sim.tubeOpen(0,'BarrettGripperState'..sim.getNameSuffix(nil),1)
    
    closing=false
    fingerAngle=0
    closing=flase
    firstPartLocked={false,false,false}
    needFullOpening={0,0,0}
    firstPartTorqueOvershootCount={0,0,0}
    firstPartTorqueOvershootCountRequired=1
    firstPartMaxTorque=0.9
    closingVel=60*math.pi/180
    openingVel=-120*math.pi/180
    closingOpeningTorque=1
    for i=1,3,1 do
        sim.setObjectInt32Parameter(jointHandles[i][2],sim.jointintparam_motor_enabled,1)
        sim.setObjectInt32Parameter(jointHandles[i][2],sim.jointintparam_ctrl_enabled,0)
        sim.setObjectInt32Parameter(jointHandles[i][3],sim.jointintparam_motor_enabled,1)
        sim.setObjectInt32Parameter(jointHandles[i][3],sim.jointintparam_ctrl_enabled,1)
        sim.setJointTargetVelocity(jointHandles[i][2],-closingVel)
        sim.setJointTargetVelocity(jointHandles[i][3],-closingVel/3)
        sim.setJointForce(jointHandles[i][2],closingOpeningTorque)
        sim.setJointForce(jointHandles[i][3],closingOpeningTorque)
    end
    
end

function sysCall_cleanup() 
 
end 

function sysCall_actuation() 
    
    data=sim.tubeRead(communicationTube)
    if (data) then
        closing=sim.unpackInt32Table(data,0,1)[1]~=0
        fingerAngle=sim.unpackFloatTable(data,1,1)[1]
    end
    
    sim.setJointTargetPosition(jointHandles[1][1],-math.pi*0.5+fingerAngle)
    sim.setJointTargetPosition(jointHandles[3][1],-math.pi*0.5+fingerAngle)
    
    for i=1,3,1 do
        if (closing)and(needFullOpening[1]~=2)and(needFullOpening[2]~=2)and(needFullOpening[3]~=2) then
            if (firstPartLocked[i]) then
                sim.setJointTargetVelocity(jointHandles[i][3],closingVel/3)
            else
                r,f,t=sim.readForceSensor(firstPartTorqueSensorHandles[i])
                if (r&gt;0)and(math.abs(t[3])&gt;firstPartMaxTorque) then
                    firstPartTorqueOvershootCount[i]=firstPartTorqueOvershootCount[i]+1
                else
                    firstPartTorqueOvershootCount[i]=0
                end
                if (firstPartTorqueOvershootCount[i]&gt;=firstPartTorqueOvershootCountRequired) then
                    needFullOpening[i]=1
                    firstPartLocked[i]=true
                    -- First joint is now locked and holding the position:
                    sim.setObjectInt32Parameter(jointHandles[i][2],sim.jointintparam_ctrl_enabled,1)
                    sim.setJointForce(jointHandles[i][2],closingOpeningTorque*100)
                    sim.setJointTargetPosition(jointHandles[i][2],sim.getJointPosition(jointHandles[i][2]))
                    -- second joint is now not in position control anymore:
                    sim.setObjectInt32Parameter(jointHandles[i][3],sim.jointintparam_ctrl_enabled,0)
                    sim.setJointTargetVelocity(jointHandles[i][3],closingVel/3)
                else
                    sim.setJointTargetVelocity(jointHandles[i][2],closingVel)
                    sim.setJointTargetPosition(jointHandles[i][3],(45*math.pi/180)+sim.getJointPosition(jointHandles[i][2])/3)
                end
            end
        else
            if (needFullOpening[i]==1) then
                needFullOpening[i]=2
            end
            sim.setJointTargetVelocity(jointHandles[i][3],openingVel/3)
            if (firstPartLocked[i]) then
                jv=sim.getJointPosition(jointHandles[i][3])
                if (jv&lt;45.5*math.pi/180) then
                    firstPartLocked[i]=false -- we unlock the first part
                    sim.setObjectInt32Parameter(jointHandles[i][2],sim.jointintparam_ctrl_enabled,0)
                    sim.setJointForce(jointHandles[i][2],closingOpeningTorque)
                    sim.setJointTargetVelocity(jointHandles[i][2],openingVel)
                end
            else
                if (needFullOpening[i]~=0) then
                    jv3=sim.getJointPosition(jointHandles[i][3])
                    jv2=sim.getJointPosition(jointHandles[i][2])
                    if (jv3&lt;45.5*math.pi/180)and(jv2&lt;2*math.pi/180) then
                        needFullOpening[i]=0
                        -- second joint is now again in position control:
                        sim.setObjectInt32Parameter(jointHandles[i][3],sim.jointintparam_ctrl_enabled,1)
                        sim.setJointTargetPosition(jointHandles[i][3],(45*math.pi/180)+sim.getJointPosition(jointHandles[i][2])/3)
                    end
                else
                    sim.setJointTargetVelocity(jointHandles[i][2],openingVel)
                    sim.setJointTargetPosition(jointHandles[i][3],(45*math.pi/180)+sim.getJointPosition(jointHandles[i][2])/3)
                end
            end
        end
    end
end 

</t>
<t tx="leo.20210529215420.1">Force sensors are initially rigid links between two shapes that are able to measure transmitted forces and torques. The rigidity of force sensors is conditional, in the sense that force sensors can be broken if a certain condition arises (e.g. if a force or torque threshold is overshot). Following figure illustrates an application using a force sensor:

A force sensor is only operational during simulation if it is dynamically enabled. It means the child of the force sensor need to be dynamically enabled.

In CoppeliaSim, only a limited number of objects will be dynamically simulated. Those are shapes, joints and force sensors, but it will depend on the scene structure and object properties, whether a given object will be dynamically simulated. </t>
</tnodes>
</leo_file>
