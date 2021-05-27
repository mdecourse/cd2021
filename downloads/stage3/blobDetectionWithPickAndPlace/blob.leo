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
<v t="leo.20210528002346.1"><vh>suction pad</vh></v>
<v t="leo.20210528001331.1"><vh>setLinkDummy</vh></v>
<v t="leo.20210528001540.1"><vh>setObjectParent</vh></v>
<v t="leo.20210528002109.1"><vh>getObjectMatrix</vh></v>
<v t="leo.20210522214903.1"><vh>recursive importer</vh></v>
<v t="leo.20210528000742.1"><vh>imported files</vh>
<v t="leo.20210528000742.2"><vh>@path ./</vh>
<v t="leo.20210528000742.3"><vh>@clean blob.lua</vh>
<v t="leo.20210528000742.4"><vh>sysCall_init (blob.lua)</vh></v>
<v t="leo.20210528000742.5"><vh>sysCall_cleanup (blob.lua)</vh></v>
</v>
<v t="leo.20210528000742.6"><vh>@clean blobdetection.lua</vh>
<v t="leo.20210528000742.7"><vh>sysCall_init (blobdetection.lua)</vh></v>
<v t="leo.20210528000742.8"><vh>sysCall_vision (blobdetection.lua)</vh></v>
</v>
<v t="leo.20210528000742.9"><vh>@clean blobdetectioncamera.lua</vh>
<v t="leo.20210528000742.10"><vh>sysCall_init (blobdetectioncamera.lua)</vh></v>
<v t="leo.20210528000742.11"><vh>sysCall_cleanup (blobdetectioncamera.lua)</vh></v>
<v t="leo.20210528000742.12"><vh>sysCall_actuation (blobdetectioncamera.lua)</vh></v>
</v>
<v t="leo.20210528000742.13"><vh>@clean detectionbox.lua</vh>
<v t="leo.20210528000742.14"><vh>sysCall_init (detectionbox.lua)</vh></v>
<v t="leo.20210528000742.15"><vh>sysCall_sensing (detectionbox.lua)</vh></v>
</v>
<v t="leo.20210528000742.16"><vh>@clean irb360.lua</vh>
<v t="leo.20210528000742.17"><vh>sysCall_threadmain (irb360.lua)</vh></v>
</v>
<v t="leo.20210528000742.18"><vh>@clean irb360looptarget.lua</vh>
<v t="leo.20210528000742.19"><vh>sysCall_init (irb360looptarget.lua)</vh></v>
<v t="leo.20210528000742.20"><vh>sysCall_cleanup (irb360looptarget.lua)</vh></v>
<v t="leo.20210528000742.21"><vh>sysCall_sensing (irb360looptarget.lua)</vh></v>
<v t="leo.20210528000742.22"><vh>sysCall_actuation (irb360looptarget.lua)</vh></v>
</v>
<v t="leo.20210528000742.23"><vh>@clean irb360looptarget0.lua</vh>
<v t="leo.20210528000742.24"><vh>sysCall_init (irb360looptarget0.lua)</vh></v>
<v t="leo.20210528000742.25"><vh>sysCall_cleanup (irb360looptarget0.lua)</vh></v>
<v t="leo.20210528000742.26"><vh>sysCall_sensing (irb360looptarget0.lua)</vh></v>
<v t="leo.20210528000742.27"><vh>sysCall_actuation (irb360looptarget0.lua)</vh></v>
</v>
<v t="leo.20210528000742.28"><vh>@clean irb360_0.lua</vh>
<v t="leo.20210528000742.29"><vh>sysCall_threadmain (irb360_0.lua)</vh></v>
</v>
<v t="leo.20210528000742.30"><vh>@clean largedetectionbox.lua</vh>
<v t="leo.20210528000742.31"><vh>sysCall_init (largedetectionbox.lua)</vh></v>
<v t="leo.20210528000742.32"><vh>sysCall_sensing (largedetectionbox.lua)</vh></v>
</v>
<v t="leo.20210528000742.33"><vh>@clean shortconveyorbelt.lua</vh>
<v t="leo.20210528000742.34"><vh>sysCall_init (shortconveyorbelt.lua)</vh></v>
<v t="leo.20210528000742.35"><vh>sysCall_cleanup (shortconveyorbelt.lua)</vh></v>
<v t="leo.20210528000742.36"><vh>sysCall_actuation (shortconveyorbelt.lua)</vh></v>
</v>
<v t="leo.20210528000742.37"><vh>@clean suctionpad.lua</vh>
<v t="leo.20210528000742.38"><vh>sysCall_init (suctionpad.lua)</vh></v>
<v t="leo.20210528000742.39"><vh>sysCall_cleanup (suctionpad.lua)</vh></v>
<v t="leo.20210528000742.40"><vh>sysCall_sensing (suctionpad.lua)</vh></v>
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
<t tx="leo.20210528000742.1"></t>
<t tx="leo.20210528000742.10">function sysCall_init()
    camera=sim.getObjectHandle('blobDetectionCamera_camera')
    baseObject=sim.getObjectAssociatedWithScript(sim.handle_self)
    conveyor=sim.getObjectHandle('whiteConveyor')
    res=sim.getVisionSensorResolution(camera)
    lastImageAnalysisTime=0
    lastLowestBlobDetectionPositionY=100
    lastLowestBlobDetectionTime=0
end
</t>
<t tx="leo.20210528000742.11">function sysCall_cleanup() 
end 
</t>
<t tx="leo.20210528000742.12">function sysCall_actuation() 
    t=sim.getSimulationTime()
    camPos=sim.getObjectPosition(camera,-1)
    imageAnalysisFrequency=sim.getScriptSimulationParameter(sim.getScriptAssociatedWithObject(baseObject),'imageAnalysisFrequency')
    if (t-lastImageAnalysisTime&gt;1/imageAnalysisFrequency) then
        cv=sim.getScriptSimulationParameter(sim.getScriptAssociatedWithObject(conveyor),'conveyorBeltVelocity')
        lastImageAnalysisTime=t
        sim.handleVisionSensor(camera) -- the image processing camera is handled explicitely, since we do not need to execute that command at each simulation pass
        result,t0,t1=sim.readVisionSensor(camera) -- Here we read the image processing camera!
        if (t1) then -- in t1 we should have the blob information if the camera was set-up correctly
            blobCount=t1[1]
            dataSizePerBlob=t1[2]
            lowestYofDetection=100
            -- Now we go through all blobs:
            for i=1,blobCount,1 do
                blobSize=t1[2+(i-1)*dataSizePerBlob+1]
                blobOrientation=t1[2+(i-1)*dataSizePerBlob+2]
                blobPos={t1[2+(i-1)*dataSizePerBlob+3],t1[2+(i-1)*dataSizePerBlob+4]}
                blobBoxDimensions={t1[2+(i-1)*dataSizePerBlob+5],t1[2+(i-1)*dataSizePerBlob+6]}
                if (blobBoxDimensions[1]&gt;blobBoxDimensions[2]) then
                    tmp=blobBoxDimensions[1]
                    blobBoxDimensions[1]=blobBoxDimensions[2]
                    blobBoxDimensions[2]=tmp
                    blobOrientation=blobOrientation+math.pi/2
                end
                if (blobSize&gt;0.01)and(blobPos[2]&gt;0.2)and(blobPos[2]&lt;0.8) then
                    blobCol=sim.getVisionSensorImage(camera,res[1]*blobPos[1],res[2]*blobPos[2],1,1)
                    if (blobCol[1]&gt;blobCol[2])and(blobCol[1]&gt;blobCol[3]) then
                        colorCode=1
                    end
                    if (blobCol[2]&gt;blobCol[1])and(blobCol[2]&gt;blobCol[3]) then
                        colorCode=2
                    end
                    if (blobCol[3]&gt;blobCol[1])and(blobCol[3]&gt;blobCol[2]) then
                        colorCode=3
                    end
                    if (blobSize&gt;0.02) then
                        blobColIntensity=(blobCol[1]+blobCol[2]+blobCol[3])/3
                        shapeType=2 -- T
                        -- Now check the orientation of the T (up or down). We test a point that is supposed to be in the left or right T wings:
                        coord={0,0}
                        coord[1]=blobPos[1]+blobBoxDimensions[1]*0.37*math.cos(blobOrientation)-blobBoxDimensions[2]*0.45*math.sin(blobOrientation)
                        coord[2]=blobPos[2]+blobBoxDimensions[1]*0.37*math.sin(blobOrientation)+blobBoxDimensions[2]*0.45*math.cos(blobOrientation)
                        blobCol=sim.getVisionSensorImage(camera,res[1]*coord[1],res[2]*coord[2],1,1)
                        pointIntensity=(blobCol[1]+blobCol[2]+blobCol[3])/3
                        if (math.abs(pointIntensity-blobColIntensity)&gt;0.1) then
                            blobOrientation=blobOrientation+math.pi
                        end
                    else
                        shapeType=1 -- I
                    end
                    absPosX=camPos[1]+(0.5-blobPos[1])*0.55 -- 0.55 is to have a match between camera coordinates and space coordinates
                    absPosY=camPos[2]+(0.5-blobPos[2])*0.55
                    -- Following condition is so that we don't detect two same blobs that were detected at different times:
                    if (absPosY&lt;(lastLowestBlobDetectionPositionY+cv*(t-lastLowestBlobDetectionTime)-0.05)) then
                        packedBlobData=sim.packInt32Table({shapeType,colorCode})..sim.packFloatTable({absPosX,absPosY,t,blobOrientation})
                        info=sim.getStringSignal('shapeInfos')
                        if (not info) then
                            info=packedBlobData
                        else
                            info=packedBlobData..info
                        end
                        sim.setStringSignal('shapeInfos',info) -- this string signal is available to the two robots
                    end
                    if (absPosY&lt;lowestYofDetection) then
                        lowestYofDetection=absPosY
                    end
                end
            end
            lastLowestBlobDetectionPositionY=lowestYofDetection
            lastLowestBlobDetectionTime=t
        end
    end
end 
</t>
<t tx="leo.20210528000742.13">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210528000742.14">function sysCall_init()
    sensor=sim.getObjectHandle('deletionBox_sensor')
    uiH=simGetUIHandle('sinkCounter')
    destroyedCount=0
    updateUI(uiH,destroyedCount)
end
</t>
<t tx="leo.20210528000742.15">updateUI=function(uiHandle,number)
    if (previousCounter~=number) then
        activeCol={1.0,0.1,0.1}
        passiveCol={0.1,0.1,0.1}
        c=math.fmod(number,1000)
        for i=0,2,1 do
            d=math.floor(c/(10^(2-i)))
            b=100+i*10
            if (d==0) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,activeCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,passiveCol)
                simSetUIButtonColor(uiHandle,b+4,activeCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,activeCol)
            end
            if (d==1) then
                simSetUIButtonColor(uiHandle,b+0,passiveCol)
                simSetUIButtonColor(uiHandle,b+1,passiveCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,passiveCol)
                simSetUIButtonColor(uiHandle,b+4,passiveCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,passiveCol)
            end
            if (d==2) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,passiveCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,activeCol)
                simSetUIButtonColor(uiHandle,b+4,activeCol)
                simSetUIButtonColor(uiHandle,b+5,passiveCol)
                simSetUIButtonColor(uiHandle,b+6,activeCol)
            end
            if (d==3) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,passiveCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,activeCol)
                simSetUIButtonColor(uiHandle,b+4,passiveCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,activeCol)
            end
            if (d==4) then
                simSetUIButtonColor(uiHandle,b+0,passiveCol)
                simSetUIButtonColor(uiHandle,b+1,activeCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,activeCol)
                simSetUIButtonColor(uiHandle,b+4,passiveCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,passiveCol)
            end
            if (d==5) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,activeCol)
                simSetUIButtonColor(uiHandle,b+2,passiveCol)
                simSetUIButtonColor(uiHandle,b+3,activeCol)
                simSetUIButtonColor(uiHandle,b+4,passiveCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,activeCol)
            end
            if (d==6) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,activeCol)
                simSetUIButtonColor(uiHandle,b+2,passiveCol)
                simSetUIButtonColor(uiHandle,b+3,activeCol)
                simSetUIButtonColor(uiHandle,b+4,activeCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,activeCol)
            end
            if (d==7) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,passiveCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,passiveCol)
                simSetUIButtonColor(uiHandle,b+4,passiveCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,passiveCol)
            end
            if (d==8) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,activeCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,activeCol)
                simSetUIButtonColor(uiHandle,b+4,activeCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,activeCol)
            end
            if (d==9) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,activeCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,activeCol)
                simSetUIButtonColor(uiHandle,b+4,passiveCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,activeCol)
            end
            c=c-d*(10^(2-i))
        end
    end
    previousCounter=number
end
function sysCall_sensing()
    local res,dist,pt,objHandle=sim.readProximitySensor(sensor)
    if res&gt;0 then
        local p=sim.getModelProperty(objHandle)
        if sim.boolAnd32(p,sim.modelproperty_not_model)~=0 then
            objHandle=sim.getObjectParent(objHandle)
        end
        sim.removeModel(objHandle)
        destroyedCount=destroyedCount+1
        updateUI(uiH,destroyedCount)
    end
end
</t>
<t tx="leo.20210528000742.16">@path ./
-- This threaded script handles the motion of the IRB360 robot. It can be controlled
-- in forward or inverse kinematics, but in this case it is only controlled in inverse kinematics
------------------------------------------------------------------------------
-- The functions sim.moveToPosition and sim.moveToJointPositions are DEPRECATED.
-- Try using following much more powerful functions instead:
-- simRMLPosition or simRMLVelocity
------------------------------------------------------------------------------
setFkMode=function()
    -- disable the platform positional constraints:
    sim.setIkElementProperties(mainIkTask,ikModeTipDummy,0)
    -- Set the driving joints into passive mode (not taken into account during IK resolution):
    sim.setJointMode(fkDrivingJoints[1],sim.jointmode_passive,0)
    sim.setJointMode(fkDrivingJoints[2],sim.jointmode_passive,0)
    sim.setJointMode(fkDrivingJoints[3],sim.jointmode_passive,0)
end
setIkMode=function()
    -- Make sure the target position is at the same position at the tip position:
    local p=sim.getObjectPosition(ikModeTipDummy,irb360Base)
    sim.setJointPosition(ikDrivingJoints[1],p[1]-initialPosition[1])
    sim.setJointPosition(ikDrivingJoints[2],p[2]-initialPosition[2])
    sim.setJointPosition(ikDrivingJoints[3],p[3]-initialPosition[3])
    -- enable the platform positional constraints:
    sim.setIkElementProperties(mainIkTask,ikModeTipDummy,sim.ik_x_constraint+sim.ik_y_constraint+sim.ik_z_constraint)
    -- Set the base joints into ik mode (taken into account during IK resolution):
    sim.setJointMode(fkDrivingJoints[1],sim.jointmode_ik,0)
    sim.setJointMode(fkDrivingJoints[2],sim.jointmode_ik,0)
    sim.setJointMode(fkDrivingJoints[3],sim.jointmode_ik,0)
end
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210528000742.17">function sysCall_threadmain()
    -- Initialization:
    sim.setThreadSwitchTiming(2) -- Default timing for automatic thread switching
    sim.wait(2)
    -- Retrieve some values:
    mainIkTask=sim.getIkGroupHandle('irb360_mainTask')
    ikModeTipDummy=sim.getObjectHandle('irb360_ikTip')
    ikModeTargetDummy=sim.getObjectHandle('irb360_ikTarget')
    -- Following are the joints that we control when in FK mode:
    fkDrivingJoints={-1,-1,-1,-1}
    fkDrivingJoints[1]=sim.getObjectHandle('irb360_drivingJoint1')
    fkDrivingJoints[2]=sim.getObjectHandle('irb360_drivingJoint2')
    fkDrivingJoints[3]=sim.getObjectHandle('irb360_drivingJoint3')
    fkDrivingJoints[4]=sim.getObjectHandle('irb360_motor')
    -- Following are the joints that we control when in IK mode (we use joints in order to be able to use the sim.moveToJointPositions command here too):
    ikDrivingJoints={-1,-1,-1,-1}
    ikDrivingJoints[1]=sim.getObjectHandle('irb360_cartesianX')
    ikDrivingJoints[2]=sim.getObjectHandle('irb360_cartesianY')
    ikDrivingJoints[3]=sim.getObjectHandle('irb360_cartesianZ')
    ikDrivingJoints[4]=sim.getObjectHandle('irb360_motor')
    conveyor=sim.getObjectHandle('whiteConveyor#')
    suctionPad=sim.getObjectHandle('suctionPad')
    irb360Base=sim.getObjectAssociatedWithScript(sim.handle_self)
    angularVelocity=math.pi
    angularAccel=4*math.pi
    linearVelocity=2
    linearAccel=10
    angleToLinearCoeff=0.0001 -- anything small
    pickupHeight=0.7085 
    -- The 'sim.moveToJointPositions' command, as used below, will drive all joints simultaneously (they start
    -- and stop at the same time). In order to be able to drive the central axis much faster than the other
    -- joints, we applied a trick: the rotational motor is built on top of another motor ('irb360_motorAux')
    -- that is linearly dependent of the first one (motorAux=3*motor). So if we drive the axis motor to x degrees,
    -- the total rotation will be 4x degrees. So we have to remember to feed always 1/4 of the desired angular
    -- value for the central axis.
    -- First, make sure we are in initial position:
    setFkMode()
    --sim.moveToJointPositions(fkDrivingJoints,{12*math.pi/180,12*math.pi/180,12*math.pi/180,0},angularVelocity,angularAccel)
    --sim.wait(99999)
    sim.moveToJointPositions(fkDrivingJoints,{0,0,0,0},angularVelocity,angularAccel)
    initialPosition=sim.getObjectPosition(ikModeTipDummy,irb360Base)
    zeroPos=sim.getObjectPosition(ikModeTipDummy,-1)
    setIkMode()
    stackOccupancy={{nil,nil,nil},{nil,nil,nil}} -- for I and T stacks (each one of them has red, green and blue components)
    dropPositions={{{nil,nil,nil,nil},{nil,nil,nil,nil},{nil,nil,nil,nil}},{{nil,nil,nil,nil},{nil,nil,nil,nil},{nil,nil,nil,nil}}} -- for I and T stacks (each one of them has red, green and blue components)
    stackOccupancy={{{},{}},{{},{}}}
    dropPositions={{{{},{},{}},{{},{},{}}},{{{},{},{}},{{},{},{}}}}
    for i=1,2,1 do
        for j=1,2,1 do
            for k=1,3,1 do
                stackOccupancy[i][j][k]=10
                for l=1,4,1 do
                    dropPositions[i][j][k][l]=nil
                end
            end
        end
    end
    local offCorrX=-0.01
    local offCorrY=-0.02
    local dropH=0.017
    local maxDist=0.64
    for i=-1,10,1 do
        local suffix='#'
        if i&gt;=0 then
            suffix=i..'#'
        end
        container=sim.getObjectHandle('TcontainerRed'..suffix..'@silentError')
        for j=1,2,1 do
            if container&gt;=0 and not dropPositions[j][2][1][1] then
                p=sim.getObjectPosition(container,irb360Base)
                p[1]=p[1]+offCorrX
                p[2]=p[2]+offCorrY
                o=sim.getObjectOrientation(container,irb360Base)
                d=math.sqrt(p[1]*p[1]+p[2]*p[2])
                if d&lt;maxDist then
                    local r,grouping=sim.getObjectInt32Parameter(container,sim.shapeintparam_compound)
                    if grouping then
                        stackOccupancy[j][2][1]=0
                    else
                        stackOccupancy[j][2][1]=-9999 -- this contains in not a container, just a drop location
                    end
                    dropPositions[j][2][1][1]=p[1]
                    dropPositions[j][2][1][2]=p[2]
                    dropPositions[j][2][1][3]=dropH
                    dropPositions[j][2][1][4]=o[3]
                    break
                end
            end
        end
        container=sim.getObjectHandle('TcontainerGreen'..suffix..'@silentError')
        for j=1,2,1 do
            if container&gt;=0 and not dropPositions[j][2][2][1] then
                p=sim.getObjectPosition(container,irb360Base)
                p[1]=p[1]+offCorrX
                p[2]=p[2]+offCorrY
                o=sim.getObjectOrientation(container,irb360Base)
                d=math.sqrt(p[1]*p[1]+p[2]*p[2])
                if d&lt;maxDist then
                    local r,grouping=sim.getObjectInt32Parameter(container,sim.shapeintparam_compound)
                    if grouping~=0 then
                        stackOccupancy[j][2][2]=0
                    else
                        stackOccupancy[j][2][2]=-9999 -- this container in not a container, just a drop location
                    end
                    dropPositions[j][2][2][1]=p[1]
                    dropPositions[j][2][2][2]=p[2]
                    dropPositions[j][2][2][3]=dropH
                    dropPositions[j][2][2][4]=o[3]
                    break
                end
            end
        end
        container=sim.getObjectHandle('TcontainerBlue'..suffix..'@silentError')
        for j=1,2,1 do
            if container&gt;=0 and not dropPositions[j][2][3][1] then
                p=sim.getObjectPosition(container,irb360Base)
                p[1]=p[1]+offCorrX
                p[2]=p[2]+offCorrY
                o=sim.getObjectOrientation(container,irb360Base)
                d=math.sqrt(p[1]*p[1]+p[2]*p[2])
                if d&lt;maxDist then
                    local r,grouping=sim.getObjectInt32Parameter(container,sim.shapeintparam_compound)
                    if grouping~=0 then
                        stackOccupancy[j][2][3]=0
                    else
                        stackOccupancy[j][2][3]=-9999 -- this container in not a container, just a drop location
                    end
                    dropPositions[j][2][3][1]=p[1]
                    dropPositions[j][2][3][2]=p[2]
                    dropPositions[j][2][3][3]=dropH
                    dropPositions[j][2][3][4]=o[3]
                    break
                end
            end
        end
        container=sim.getObjectHandle('IcontainerRed'..suffix..'@silentError')
        for j=1,2,1 do
            if container&gt;=0 and not dropPositions[j][1][1][1] then
                p=sim.getObjectPosition(container,irb360Base)
                p[1]=p[1]+offCorrX
                p[2]=p[2]+offCorrY
                o=sim.getObjectOrientation(container,irb360Base)
                d=math.sqrt(p[1]*p[1]+p[2]*p[2])
                if d&lt;maxDist then
                    local r,grouping=sim.getObjectInt32Parameter(container,sim.shapeintparam_compound)
                    if grouping~=0 then
                        stackOccupancy[j][1][1]=0
                    else
                        stackOccupancy[j][1][1]=-9999 -- this container in not a container, just a drop location
                    end
                    dropPositions[j][1][1][1]=p[1]
                    dropPositions[j][1][1][2]=p[2]
                    dropPositions[j][1][1][3]=dropH
                    dropPositions[j][1][1][4]=o[3]
                    break
                end
            end
        end
        container=sim.getObjectHandle('IcontainerGreen'..suffix..'@silentError')
        for j=1,2,1 do
            if container&gt;=0 and not dropPositions[j][1][2][1] then
                p=sim.getObjectPosition(container,irb360Base)
                p[1]=p[1]+offCorrX
                p[2]=p[2]+offCorrY
                o=sim.getObjectOrientation(container,irb360Base)
                d=math.sqrt(p[1]*p[1]+p[2]*p[2])
                if d&lt;maxDist then
                    local r,grouping=sim.getObjectInt32Parameter(container,sim.shapeintparam_compound)
                    if grouping~=0 then
                        stackOccupancy[j][1][2]=0
                    else
                        stackOccupancy[j][1][2]=-9999 -- this container in not a container, just a drop location
                    end
                    dropPositions[j][1][2][1]=p[1]
                    dropPositions[j][1][2][2]=p[2]
                    dropPositions[j][1][2][3]=dropH
                    dropPositions[j][1][2][4]=o[3]
                    break
                end
            end
        end
        container=sim.getObjectHandle('IcontainerBlue'..suffix..'@silentError')
        for j=1,2,1 do
            if container&gt;=0 and not dropPositions[j][1][3][1] then
                p=sim.getObjectPosition(container,irb360Base)
                p[1]=p[1]+offCorrX
                p[2]=p[2]+offCorrY
                o=sim.getObjectOrientation(container,irb360Base)
                d=math.sqrt(p[1]*p[1]+p[2]*p[2])
                if d&lt;maxDist then
                    local r,grouping=sim.getObjectInt32Parameter(container,sim.shapeintparam_compound)
                    if grouping~=0 then
                        stackOccupancy[j][1][3]=0
                    else
                        stackOccupancy[j][1][3]=-9999 -- this container in not a container, just a drop location
                    end
                    dropPositions[j][1][3][1]=p[1]
                    dropPositions[j][1][3][2]=p[2]
                    dropPositions[j][1][3][3]=dropH
                    dropPositions[j][1][3][4]=o[3]
                    break
                end
            end
        end
    end
    local j=0
    local irbMatrixInv=sim.getObjectMatrix(irb360Base,-1)
    irbMatrixInv=simGetInvertedMatrix(irbMatrixInv)
    while sim.getSimulationState()~=sim.simulation_advancing_abouttostop do
        t=sim.getSimulationTime()
        dt=sim.getSimulationTimeStep()
        cv=sim.getScriptSimulationParameter(sim.getScriptAssociatedWithObject(conveyor),'conveyorBeltVelocity')
        -- Get the information about the shape positions etc:
        sim.setThreadAutomaticSwitch(false) -- lock thread switching for a short moment, so that we don't corrupt the 'shapeInfos' signal (another thread could be modifying that signal too)
        info=sim.getStringSignal('shapeInfos')
        if (info) then
            -- Each shape info has 24 bytes (6*4), so loop through all info:
            local fullBreak=false
            for i=string.len(info)/24,1,-1 do
                data=string.sub(info,(i-1)*24+1,(i-1)*24+24)
                newInfo=""
                if (i~=1) then
                    newInfo=newInfo..string.sub(info,1,(i-1)*24+0)
                end
                if (i~=string.len(info)/24) then
                    newInfo=newInfo..string.sub(info,(i-1)*24+24+1)
                end
                intData=sim.unpackInt32Table(data,0,2)
                floatData=sim.unpackFloatTable(data,2,4)
                shapeCurrentPos={floatData[1],floatData[2]+(t-floatData[3])*cv,0}
                local relPos=sim.multiplyVector(irbMatrixInv,shapeCurrentPos)
                local sideDistPickOk=math.abs(relPos[2])&lt;0.4
                pt=sim.getObjectPosition(ikModeTargetDummy,-1)
                for kk=1,2,1 do
                    j=j+1
                    if j&gt;2 then
                        j=1
                    end
                    if (shapeCurrentPos[2]&gt;zeroPos[2])and(shapeCurrentPos[2]&lt;zeroPos[2]+0.1)and(stackOccupancy[j][intData[1]][intData[2]]&lt;5)and sideDistPickOk then
                        -- Ok, we can pickup this shape if the drop position is valid!
                        rotAngle=-floatData[4]
                        if (intData[1]==1) then
                            rotAngle=rotAngle+math.pi/2 -- I shape
                        end
                        if dropPositions[j][intData[1]][intData[2]][1] then
                            -- Ok, the drop position is valid
                            dropPos={dropPositions[j][intData[1]][intData[2]][1],dropPositions[j][intData[1]][intData[2]][2],dropPositions[j][intData[1]][intData[2]][3],dropPositions[j][intData[1]][intData[2]][4]/4+rotAngle/4}
                            -- First store an updated shape info (where we removed the info of the shape we are going to pick up):
                            sim.setStringSignal('shapeInfos',newInfo)
                            sim.setThreadAutomaticSwitch(true) -- Now we can allow for thread switches too since we updated the 'shapeInfos' signal
                            -- The pickup movement will be with infinite acceleration to avoid to heavy calculations:
                            sim.setJointPosition(ikDrivingJoints[1],0)
                            sim.setJointPosition(ikDrivingJoints[2],0)
                            sim.setJointPosition(ikDrivingJoints[3],0)
                            p={shapeCurrentPos[1],shapeCurrentPos[2]+(0.5+dt)*cv,pickupHeight+0.01}
                            dp={p[1]-pt[1],p[2]-pt[2],p[3]-pt[3]}
                            dist=math.sqrt(dp[1]*dp[1]+dp[2]*dp[2]+dp[3]*dp[3])
                            sim.moveToPosition(ikModeTargetDummy,-1,p,nil,dist/0.5)
                            p[2]=p[2]+0.25*cv
                            p[3]=pickupHeight
                            pt=sim.getObjectPosition(ikModeTargetDummy,-1)
                            dp={p[1]-pt[1],p[2]-pt[2],p[3]-pt[3]}
                            dist=math.sqrt(dp[1]*dp[1]+dp[2]*dp[2]+dp[3]*dp[3])
                            sim.moveToPosition(ikModeTargetDummy,-1,p,nil,dist/0.25)
                            -- We are just above the shape. Activate the suction pad:
                            sim.setScriptSimulationParameter(sim.getScriptAssociatedWithObject(suctionPad),'active','true')
                            -- Now follow the movement of the conveyor for 1/4 of a second:
                            p[2]=p[2]+0.25*cv
                            p[3]=pickupHeight
                            pt=sim.getObjectPosition(ikModeTargetDummy,-1)
                            dp={p[1]-pt[1],p[2]-pt[2],p[3]-pt[3]}
                            dist=math.sqrt(dp[1]*dp[1]+dp[2]*dp[2]+dp[3]*dp[3])
                            sim.moveToPosition(ikModeTargetDummy,-1,p,nil,dist/0.25) -- not exactly cv, but ok
                            -- Now lift up (while still moving a bit forward:
                            p[2]=p[2]+0.25*cv
                            p[3]=pickupHeight+0.1
                            pt=sim.getObjectPosition(ikModeTargetDummy,-1)
                            dp={p[1]-pt[1],p[2]-pt[2],p[3]-pt[3]}
                            dist=math.sqrt(dp[1]*dp[1]+dp[2]*dp[2]+dp[3]*dp[3])
                            sim.moveToPosition(ikModeTargetDummy,-1,p,nil,dist/0.25) -- not exactly cv, but ok
                            sim.wait(0.25)
                            -- Now we move the tip with the auxiliary joints.
                            -- This part doesn't use infinite acceleration:
                            sim.setThreadAutomaticSwitch(false) -- we don't wanna be interrupted in next section:
                            sim.setObjectPosition(ikModeTargetDummy,sim.handle_parent,{0,0,0})
                            setIkMode()
                            sim.setThreadAutomaticSwitch(true)
                            sim.moveToJointPositions(ikDrivingJoints,dropPos,linearVelocity,linearAccel,angleToLinearCoeff)
                            sim.wait(0.25)
                            -- Deactivate the suction pad:
                            sim.setScriptSimulationParameter(sim.getScriptAssociatedWithObject(suctionPad),'active','false')
                            stackOccupancy[j][intData[1]][intData[2]]=stackOccupancy[j][intData[1]][intData[2]]+1
                            sim.wait(0.25)
                            -- Move back to the zero position:
                            sim.moveToJointPositions(ikDrivingJoints,{0,0,0,0},linearVelocity,linearAccel,angleToLinearCoeff)
                            fullBreak=true
                            break
                        end
                    end
                end
                if fullBreak then
                    break
                end
            end
            sim.setThreadAutomaticSwitch(true) -- Important to allow for thread switches again
        else
            sim.setThreadAutomaticSwitch(true) -- Important to allow for thread switches again
            sim.switchThread() -- don't waste time waiting
        end
    end
end
</t>
<t tx="leo.20210528000742.18">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210528000742.19">function sysCall_init()
    sim.setScriptAttribute(sim.handle_self,sim.childscriptattribute_automaticcascadingcalls,false) 
    allIkTasks={-1,-1,-1,-1,-1,-1,-1,-1}
    allIkTasks[1]=sim.getIkGroupHandle('irb360_mainTask')
    allIkTasks[2]=sim.getIkGroupHandle('irb360_bridge')
    allIkTasks[3]=sim.getIkGroupHandle('irb360_bridge0')
    allIkTasks[4]=sim.getIkGroupHandle('irb360_bridge1')
    allIkTasks[5]=sim.getIkGroupHandle('irb360_bridge2')
    allIkTasks[6]=sim.getIkGroupHandle('irb360_bridge3')
    allIkTasks[7]=sim.getIkGroupHandle('irb360_bridge4')
    allIkTasks[8]=sim.getIkGroupHandle('irb360_axis')
    baseObjectHandle=sim.getObjectHandle('irb360')
end
</t>
<t tx="leo.20210528000742.2"></t>
<t tx="leo.20210528000742.20">-- We handle inverse kinematics explicitely in this script, so that we can control
-- what happens if an IK task fails
function sysCall_cleanup() 
end 
</t>
<t tx="leo.20210528000742.21">function sysCall_sensing() 
end 
</t>
<t tx="leo.20210528000742.22">function sysCall_actuation() 
    -- Now save the robot joint configuration in case IK fails at the next stage.
    -- We have to explore the tree structure of the model:
    toExplore={baseObjectHandle}
    jointsAndTheirPositions={}
    while (#toExplore&gt;0) do
        obj=toExplore[#toExplore]
        table.remove(toExplore,#toExplore)
        if (sim.getObjectType(obj)==sim.object_joint_type) then
            table.insert(jointsAndTheirPositions,obj)
            table.insert(jointsAndTheirPositions,sim.getJointPosition(obj))
        end
        index=0
        child=sim.getObjectChild(obj,index)
        while (child~=-1) do
            table.insert(toExplore,child)
            index=index+1
            child=sim.getObjectChild(obj,index)
        end
    end
    --Execute the IK tasks (order matters!):
    ikFailed=false
    for i=1,#allIkTasks,1 do
        if (sim.handleIkGroup(allIkTasks[i])==sim.ikresult_fail) then
            ikFailed=true
            break
        end
    end
    -- Now restore to the initial configuration if an IK task failed, and display a message:
    if (ikFailed) then
        for i=0,(#jointsAndTheirPositions)/2-1,1 do
            sim.setJointPosition(jointsAndTheirPositions[2*i+1],jointsAndTheirPositions[2*i+2])
        end
        if (ikFailedReportHandle==nil) then -- We display a IK failure report message
            ikFailedReportHandle=sim.displayDialog(sim.getObjectName(baseObjectHandle),"IK solver failed.",sim.dlgstyle_message,false,"",nil,{1,0.7,0,0,0,0})
        end
    else
        if (ikFailedReportHandle) then
            sim.endDialog(ikFailedReportHandle) -- We close any report message about IK failure
            ikFailedReportHandle=nil
        end
    end
end 
</t>
<t tx="leo.20210528000742.23">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210528000742.24">function sysCall_init()
    sim.setScriptAttribute(sim.handle_self,sim.childscriptattribute_automaticcascadingcalls,false) 
    allIkTasks={-1,-1,-1,-1,-1,-1,-1,-1}
    allIkTasks[1]=sim.getIkGroupHandle('irb360_mainTask')
    allIkTasks[2]=sim.getIkGroupHandle('irb360_bridge')
    allIkTasks[3]=sim.getIkGroupHandle('irb360_bridge0')
    allIkTasks[4]=sim.getIkGroupHandle('irb360_bridge1')
    allIkTasks[5]=sim.getIkGroupHandle('irb360_bridge2')
    allIkTasks[6]=sim.getIkGroupHandle('irb360_bridge3')
    allIkTasks[7]=sim.getIkGroupHandle('irb360_bridge4')
    allIkTasks[8]=sim.getIkGroupHandle('irb360_axis')
    baseObjectHandle=sim.getObjectHandle('irb360')
end
</t>
<t tx="leo.20210528000742.25">function sysCall_cleanup() 
end 
</t>
<t tx="leo.20210528000742.26">function sysCall_sensing() 
end
</t>
<t tx="leo.20210528000742.27">function sysCall_actuation() 
-- We handle inverse kinematics explicitely in this script, so that we can control
-- what happens if an IK task fails
    -- Now save the robot joint configuration in case IK fails at the next stage.
    -- We have to explore the tree structure of the model:
    toExplore={baseObjectHandle}
    jointsAndTheirPositions={}
    while (#toExplore&gt;0) do
        obj=toExplore[#toExplore]
        table.remove(toExplore,#toExplore)
        if (sim.getObjectType(obj)==sim.object_joint_type) then
            table.insert(jointsAndTheirPositions,obj)
            table.insert(jointsAndTheirPositions,sim.getJointPosition(obj))
        end
        index=0
        child=sim.getObjectChild(obj,index)
        while (child~=-1) do
            table.insert(toExplore,child)
            index=index+1
            child=sim.getObjectChild(obj,index)
        end
    end
    --Execute the IK tasks (order matters!):
    ikFailed=false
    for i=1,#allIkTasks,1 do
        if (sim.handleIkGroup(allIkTasks[i])==sim.ikresult_fail) then
            ikFailed=true
            break
        end
    end
    -- Now restore to the initial configuration if an IK task failed, and display a message:
    if (ikFailed) then
        for i=0,(#jointsAndTheirPositions)/2-1,1 do
            sim.setJointPosition(jointsAndTheirPositions[2*i+1],jointsAndTheirPositions[2*i+2])
        end
        if (ikFailedReportHandle==nil) then -- We display a IK failure report message
            ikFailedReportHandle=sim.displayDialog(sim.getObjectName(baseObjectHandle),"IK solver failed.",sim.dlgstyle_message,false,"",nil,{1,0.7,0,0,0,0})
        end
    else
        if (ikFailedReportHandle) then
            sim.endDialog(ikFailedReportHandle) -- We close any report message about IK failure
            ikFailedReportHandle=nil
        end
    end
end 
</t>
<t tx="leo.20210528000742.28">@path ./
-- This threaded script handles the motion of the IRB360 robot. It can be controlled
-- in forward or inverse kinematics, but in this case it is only controlled in inverse kinematics
------------------------------------------------------------------------------
-- The functions sim.moveToPosition and sim.moveToJointPositions are DEPRECATED.
-- Try using following much more powerful functions instead:
-- simRMLPosition or simRMLVelocity
------------------------------------------------------------------------------
setFkMode=function()
    -- disable the platform positional constraints:
    sim.setIkElementProperties(mainIkTask,ikModeTipDummy,0)
    -- Set the driving joints into passive mode (not taken into account during IK resolution):
    sim.setJointMode(fkDrivingJoints[1],sim.jointmode_passive,0)
    sim.setJointMode(fkDrivingJoints[2],sim.jointmode_passive,0)
    sim.setJointMode(fkDrivingJoints[3],sim.jointmode_passive,0)
end
setIkMode=function()
    -- Make sure the target position is at the same position at the tip position:
    local p=sim.getObjectPosition(ikModeTipDummy,irb360Base)
    sim.setJointPosition(ikDrivingJoints[1],p[1]-initialPosition[1])
    sim.setJointPosition(ikDrivingJoints[2],p[2]-initialPosition[2])
    sim.setJointPosition(ikDrivingJoints[3],p[3]-initialPosition[3])
    -- enable the platform positional constraints:
    sim.setIkElementProperties(mainIkTask,ikModeTipDummy,sim.ik_x_constraint+sim.ik_y_constraint+sim.ik_z_constraint)
    -- Set the base joints into ik mode (taken into account during IK resolution):
    sim.setJointMode(fkDrivingJoints[1],sim.jointmode_ik,0)
    sim.setJointMode(fkDrivingJoints[2],sim.jointmode_ik,0)
    sim.setJointMode(fkDrivingJoints[3],sim.jointmode_ik,0)
end
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210528000742.29">function sysCall_threadmain()
    -- Initialization:
    sim.setThreadSwitchTiming(2) -- Default timing for automatic thread switching
    sim.wait(2)
    -- Retrieve some values:
    mainIkTask=sim.getIkGroupHandle('irb360_mainTask')
    ikModeTipDummy=sim.getObjectHandle('irb360_ikTip')
    ikModeTargetDummy=sim.getObjectHandle('irb360_ikTarget')
    -- Following are the joints that we control when in FK mode:
    fkDrivingJoints={-1,-1,-1,-1}
    fkDrivingJoints[1]=sim.getObjectHandle('irb360_drivingJoint1')
    fkDrivingJoints[2]=sim.getObjectHandle('irb360_drivingJoint2')
    fkDrivingJoints[3]=sim.getObjectHandle('irb360_drivingJoint3')
    fkDrivingJoints[4]=sim.getObjectHandle('irb360_motor')
    -- Following are the joints that we control when in IK mode (we use joints in order to be able to use the sim.moveToJointPositions command here too):
    ikDrivingJoints={-1,-1,-1,-1}
    ikDrivingJoints[1]=sim.getObjectHandle('irb360_cartesianX')
    ikDrivingJoints[2]=sim.getObjectHandle('irb360_cartesianY')
    ikDrivingJoints[3]=sim.getObjectHandle('irb360_cartesianZ')
    ikDrivingJoints[4]=sim.getObjectHandle('irb360_motor')
    conveyor=sim.getObjectHandle('whiteConveyor#')
    suctionPad=sim.getObjectHandle('suctionPad')
    irb360Base=sim.getObjectAssociatedWithScript(sim.handle_self)
    angularVelocity=math.pi
    angularAccel=4*math.pi
    linearVelocity=2
    linearAccel=10
    angleToLinearCoeff=0.0001 -- anything small
    pickupHeight=0.7085 
    -- The 'sim.moveToJointPositions' command, as used below, will drive all joints simultaneously (they start
    -- and stop at the same time). In order to be able to drive the central axis much faster than the other
    -- joints, we applied a trick: the rotational motor is built on top of another motor ('irb360_motorAux')
    -- that is linearly dependent of the first one (motorAux=3*motor). So if we drive the axis motor to x degrees,
    -- the total rotation will be 4x degrees. So we have to remember to feed always 1/4 of the desired angular
    -- value for the central axis.
    -- First, make sure we are in initial position:
    setFkMode()
    --sim.moveToJointPositions(fkDrivingJoints,{12*math.pi/180,12*math.pi/180,12*math.pi/180,0},angularVelocity,angularAccel)
    --sim.wait(99999)
    sim.moveToJointPositions(fkDrivingJoints,{0,0,0,0},angularVelocity,angularAccel)
    initialPosition=sim.getObjectPosition(ikModeTipDummy,irb360Base)
    zeroPos=sim.getObjectPosition(ikModeTipDummy,-1)
    setIkMode()
    stackOccupancy={{nil,nil,nil},{nil,nil,nil}} -- for I and T stacks (each one of them has red, green and blue components)
    dropPositions={{{nil,nil,nil,nil},{nil,nil,nil,nil},{nil,nil,nil,nil}},{{nil,nil,nil,nil},{nil,nil,nil,nil},{nil,nil,nil,nil}}} -- for I and T stacks (each one of them has red, green and blue components)
    stackOccupancy={{{},{}},{{},{}}}
    dropPositions={{{{},{},{}},{{},{},{}}},{{{},{},{}},{{},{},{}}}}
    for i=1,2,1 do
        for j=1,2,1 do
            for k=1,3,1 do
                stackOccupancy[i][j][k]=10
                for l=1,4,1 do
                    dropPositions[i][j][k][l]=nil
                end
            end
        end
    end
    local offCorrX=-0.01
    local offCorrY=-0.02
    local dropH=0.017
    local maxDist=0.64
    for i=-1,10,1 do
        local suffix='#'
        if i&gt;=0 then
            suffix=i..'#'
        end
        container=sim.getObjectHandle('TcontainerRed'..suffix..'@silentError')
        for j=1,2,1 do
            if container&gt;=0 and not dropPositions[j][2][1][1] then
                p=sim.getObjectPosition(container,irb360Base)
                p[1]=p[1]+offCorrX
                p[2]=p[2]+offCorrY
                o=sim.getObjectOrientation(container,irb360Base)
                d=math.sqrt(p[1]*p[1]+p[2]*p[2])
                if d&lt;maxDist then
                    local r,grouping=sim.getObjectInt32Parameter(container,sim.shapeintparam_compound)
                    if grouping then
                        stackOccupancy[j][2][1]=0
                    else
                        stackOccupancy[j][2][1]=-9999 -- this contains in not a container, just a drop location
                    end
                    dropPositions[j][2][1][1]=p[1]
                    dropPositions[j][2][1][2]=p[2]
                    dropPositions[j][2][1][3]=dropH
                    dropPositions[j][2][1][4]=o[3]
                    break
                end
            end
        end
        container=sim.getObjectHandle('TcontainerGreen'..suffix..'@silentError')
        for j=1,2,1 do
            if container&gt;=0 and not dropPositions[j][2][2][1] then
                p=sim.getObjectPosition(container,irb360Base)
                p[1]=p[1]+offCorrX
                p[2]=p[2]+offCorrY
                o=sim.getObjectOrientation(container,irb360Base)
                d=math.sqrt(p[1]*p[1]+p[2]*p[2])
                if d&lt;maxDist then
                    local r,grouping=sim.getObjectInt32Parameter(container,sim.shapeintparam_compound)
                    if grouping~=0 then
                        stackOccupancy[j][2][2]=0
                    else
                        stackOccupancy[j][2][2]=-9999 -- this container in not a container, just a drop location
                    end
                    dropPositions[j][2][2][1]=p[1]
                    dropPositions[j][2][2][2]=p[2]
                    dropPositions[j][2][2][3]=dropH
                    dropPositions[j][2][2][4]=o[3]
                    break
                end
            end
        end
        container=sim.getObjectHandle('TcontainerBlue'..suffix..'@silentError')
        for j=1,2,1 do
            if container&gt;=0 and not dropPositions[j][2][3][1] then
                p=sim.getObjectPosition(container,irb360Base)
                p[1]=p[1]+offCorrX
                p[2]=p[2]+offCorrY
                o=sim.getObjectOrientation(container,irb360Base)
                d=math.sqrt(p[1]*p[1]+p[2]*p[2])
                if d&lt;maxDist then
                    local r,grouping=sim.getObjectInt32Parameter(container,sim.shapeintparam_compound)
                    if grouping~=0 then
                        stackOccupancy[j][2][3]=0
                    else
                        stackOccupancy[j][2][3]=-9999 -- this container in not a container, just a drop location
                    end
                    dropPositions[j][2][3][1]=p[1]
                    dropPositions[j][2][3][2]=p[2]
                    dropPositions[j][2][3][3]=dropH
                    dropPositions[j][2][3][4]=o[3]
                    break
                end
            end
        end
        container=sim.getObjectHandle('IcontainerRed'..suffix..'@silentError')
        for j=1,2,1 do
            if container&gt;=0 and not dropPositions[j][1][1][1] then
                p=sim.getObjectPosition(container,irb360Base)
                p[1]=p[1]+offCorrX
                p[2]=p[2]+offCorrY
                o=sim.getObjectOrientation(container,irb360Base)
                d=math.sqrt(p[1]*p[1]+p[2]*p[2])
                if d&lt;maxDist then
                    local r,grouping=sim.getObjectInt32Parameter(container,sim.shapeintparam_compound)
                    if grouping~=0 then
                        stackOccupancy[j][1][1]=0
                    else
                        stackOccupancy[j][1][1]=-9999 -- this container in not a container, just a drop location
                    end
                    dropPositions[j][1][1][1]=p[1]
                    dropPositions[j][1][1][2]=p[2]
                    dropPositions[j][1][1][3]=dropH
                    dropPositions[j][1][1][4]=o[3]
                    break
                end
            end
        end
        container=sim.getObjectHandle('IcontainerGreen'..suffix..'@silentError')
        for j=1,2,1 do
            if container&gt;=0 and not dropPositions[j][1][2][1] then
                p=sim.getObjectPosition(container,irb360Base)
                p[1]=p[1]+offCorrX
                p[2]=p[2]+offCorrY
                o=sim.getObjectOrientation(container,irb360Base)
                d=math.sqrt(p[1]*p[1]+p[2]*p[2])
                if d&lt;maxDist then
                    local r,grouping=sim.getObjectInt32Parameter(container,sim.shapeintparam_compound)
                    if grouping~=0 then
                        stackOccupancy[j][1][2]=0
                    else
                        stackOccupancy[j][1][2]=-9999 -- this container in not a container, just a drop location
                    end
                    dropPositions[j][1][2][1]=p[1]
                    dropPositions[j][1][2][2]=p[2]
                    dropPositions[j][1][2][3]=dropH
                    dropPositions[j][1][2][4]=o[3]
                    break
                end
            end
        end
        container=sim.getObjectHandle('IcontainerBlue'..suffix..'@silentError')
        for j=1,2,1 do
            if container&gt;=0 and not dropPositions[j][1][3][1] then
                p=sim.getObjectPosition(container,irb360Base)
                p[1]=p[1]+offCorrX
                p[2]=p[2]+offCorrY
                o=sim.getObjectOrientation(container,irb360Base)
                d=math.sqrt(p[1]*p[1]+p[2]*p[2])
                if d&lt;maxDist then
                    local r,grouping=sim.getObjectInt32Parameter(container,sim.shapeintparam_compound)
                    if grouping~=0 then
                        stackOccupancy[j][1][3]=0
                    else
                        stackOccupancy[j][1][3]=-9999 -- this container in not a container, just a drop location
                    end
                    dropPositions[j][1][3][1]=p[1]
                    dropPositions[j][1][3][2]=p[2]
                    dropPositions[j][1][3][3]=dropH
                    dropPositions[j][1][3][4]=o[3]
                    break
                end
            end
        end
    end
    local j=0
    local irbMatrixInv=sim.getObjectMatrix(irb360Base,-1)
    irbMatrixInv=simGetInvertedMatrix(irbMatrixInv)
    while sim.getSimulationState()~=sim.simulation_advancing_abouttostop do
        t=sim.getSimulationTime()
        dt=sim.getSimulationTimeStep()
        cv=sim.getScriptSimulationParameter(sim.getScriptAssociatedWithObject(conveyor),'conveyorBeltVelocity')
        -- Get the information about the shape positions etc:
        sim.setThreadAutomaticSwitch(false) -- lock thread switching for a short moment, so that we don't corrupt the 'shapeInfos' signal (another thread could be modifying that signal too)
        info=sim.getStringSignal('shapeInfos')
        if (info) then
            -- Each shape info has 24 bytes (6*4), so loop through all info:
            local fullBreak=false
            for i=string.len(info)/24,1,-1 do
                data=string.sub(info,(i-1)*24+1,(i-1)*24+24)
                newInfo=""
                if (i~=1) then
                    newInfo=newInfo..string.sub(info,1,(i-1)*24+0)
                end
                if (i~=string.len(info)/24) then
                    newInfo=newInfo..string.sub(info,(i-1)*24+24+1)
                end
                intData=sim.unpackInt32Table(data,0,2)
                floatData=sim.unpackFloatTable(data,2,4)
                shapeCurrentPos={floatData[1],floatData[2]+(t-floatData[3])*cv,0}
                local relPos=sim.multiplyVector(irbMatrixInv,shapeCurrentPos)
                local sideDistPickOk=math.abs(relPos[2])&lt;0.4
                pt=sim.getObjectPosition(ikModeTargetDummy,-1)
                for kk=1,2,1 do
                    j=j+1
                    if j&gt;2 then
                        j=1
                    end
                    if (shapeCurrentPos[2]&gt;zeroPos[2])and(shapeCurrentPos[2]&lt;zeroPos[2]+0.1)and(stackOccupancy[j][intData[1]][intData[2]]&lt;5)and sideDistPickOk then
                        -- Ok, we can pickup this shape if the drop position is valid!
                        rotAngle=-floatData[4]
                        if (intData[1]==1) then
                            rotAngle=rotAngle+math.pi/2 -- I shape
                        end
                        if dropPositions[j][intData[1]][intData[2]][1] then
                            -- Ok, the drop position is valid
                            dropPos={dropPositions[j][intData[1]][intData[2]][1],dropPositions[j][intData[1]][intData[2]][2],dropPositions[j][intData[1]][intData[2]][3],dropPositions[j][intData[1]][intData[2]][4]/4+rotAngle/4}
                            -- First store an updated shape info (where we removed the info of the shape we are going to pick up):
                            sim.setStringSignal('shapeInfos',newInfo)
                            sim.setThreadAutomaticSwitch(true) -- Now we can allow for thread switches too since we updated the 'shapeInfos' signal
                            -- The pickup movement will be with infinite acceleration to avoid to heavy calculations:
                            sim.setJointPosition(ikDrivingJoints[1],0)
                            sim.setJointPosition(ikDrivingJoints[2],0)
                            sim.setJointPosition(ikDrivingJoints[3],0)
                            p={shapeCurrentPos[1],shapeCurrentPos[2]+(0.5+dt)*cv,pickupHeight+0.01}
                            dp={p[1]-pt[1],p[2]-pt[2],p[3]-pt[3]}
                            dist=math.sqrt(dp[1]*dp[1]+dp[2]*dp[2]+dp[3]*dp[3])
                            sim.moveToPosition(ikModeTargetDummy,-1,p,nil,dist/0.5)
                            p[2]=p[2]+0.25*cv
                            p[3]=pickupHeight
                            pt=sim.getObjectPosition(ikModeTargetDummy,-1)
                            dp={p[1]-pt[1],p[2]-pt[2],p[3]-pt[3]}
                            dist=math.sqrt(dp[1]*dp[1]+dp[2]*dp[2]+dp[3]*dp[3])
                            sim.moveToPosition(ikModeTargetDummy,-1,p,nil,dist/0.25)
                            -- We are just above the shape. Activate the suction pad:
                            sim.setScriptSimulationParameter(sim.getScriptAssociatedWithObject(suctionPad),'active','true')
                            -- Now follow the movement of the conveyor for 1/4 of a second:
                            p[2]=p[2]+0.25*cv
                            p[3]=pickupHeight
                            pt=sim.getObjectPosition(ikModeTargetDummy,-1)
                            dp={p[1]-pt[1],p[2]-pt[2],p[3]-pt[3]}
                            dist=math.sqrt(dp[1]*dp[1]+dp[2]*dp[2]+dp[3]*dp[3])
                            sim.moveToPosition(ikModeTargetDummy,-1,p,nil,dist/0.25) -- not exactly cv, but ok
                            -- Now lift up (while still moving a bit forward:
                            p[2]=p[2]+0.25*cv
                            p[3]=pickupHeight+0.1
                            pt=sim.getObjectPosition(ikModeTargetDummy,-1)
                            dp={p[1]-pt[1],p[2]-pt[2],p[3]-pt[3]}
                            dist=math.sqrt(dp[1]*dp[1]+dp[2]*dp[2]+dp[3]*dp[3])
                            sim.moveToPosition(ikModeTargetDummy,-1,p,nil,dist/0.25) -- not exactly cv, but ok
                            sim.wait(0.25)
                            -- Now we move the tip with the auxiliary joints.
                            -- This part doesn't use infinite acceleration:
                            sim.setThreadAutomaticSwitch(false) -- we don't wanna be interrupted in next section:
                            sim.setObjectPosition(ikModeTargetDummy,sim.handle_parent,{0,0,0})
                            setIkMode()
                            sim.setThreadAutomaticSwitch(true)
                            sim.moveToJointPositions(ikDrivingJoints,dropPos,linearVelocity,linearAccel,angleToLinearCoeff)
                            sim.wait(0.25)
                            -- Deactivate the suction pad:
                            sim.setScriptSimulationParameter(sim.getScriptAssociatedWithObject(suctionPad),'active','false')
                            stackOccupancy[j][intData[1]][intData[2]]=stackOccupancy[j][intData[1]][intData[2]]+1
                            sim.wait(0.25)
                            -- Move back to the zero position:
                            sim.moveToJointPositions(ikDrivingJoints,{0,0,0,0},linearVelocity,linearAccel,angleToLinearCoeff)
                            fullBreak=true
                            break
                        end
                    end
                end
                if fullBreak then
                    break
                end
            end
            sim.setThreadAutomaticSwitch(true) -- Important to allow for thread switches again
        else
            sim.setThreadAutomaticSwitch(true) -- Important to allow for thread switches again
            sim.switchThread() -- don't waste time waiting
        end
    end
end
</t>
<t tx="leo.20210528000742.3">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210528000742.30">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210528000742.31">function sysCall_init()
    sensor=sim.getObjectHandle('largeDeletionBox_sensor')
    uiH=simGetUIHandle('largeSinkCounter')
    destroyedCount=0
    updateUI(uiH,destroyedCount)
end
</t>
<t tx="leo.20210528000742.32">updateUI=function(uiHandle,number)
    if (previousCounter~=number) then
        activeCol={1.0,1.0,0.1}
        passiveCol={0.1,0.1,0.1}
        c=math.fmod(number,1000)
        for i=0,2,1 do
            d=math.floor(c/(10^(2-i)))
            b=100+i*10
            if (d==0) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,activeCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,passiveCol)
                simSetUIButtonColor(uiHandle,b+4,activeCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,activeCol)
            end
            if (d==1) then
                simSetUIButtonColor(uiHandle,b+0,passiveCol)
                simSetUIButtonColor(uiHandle,b+1,passiveCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,passiveCol)
                simSetUIButtonColor(uiHandle,b+4,passiveCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,passiveCol)
            end
            if (d==2) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,passiveCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,activeCol)
                simSetUIButtonColor(uiHandle,b+4,activeCol)
                simSetUIButtonColor(uiHandle,b+5,passiveCol)
                simSetUIButtonColor(uiHandle,b+6,activeCol)
            end
            if (d==3) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,passiveCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,activeCol)
                simSetUIButtonColor(uiHandle,b+4,passiveCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,activeCol)
            end
            if (d==4) then
                simSetUIButtonColor(uiHandle,b+0,passiveCol)
                simSetUIButtonColor(uiHandle,b+1,activeCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,activeCol)
                simSetUIButtonColor(uiHandle,b+4,passiveCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,passiveCol)
            end
            if (d==5) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,activeCol)
                simSetUIButtonColor(uiHandle,b+2,passiveCol)
                simSetUIButtonColor(uiHandle,b+3,activeCol)
                simSetUIButtonColor(uiHandle,b+4,passiveCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,activeCol)
            end
            if (d==6) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,activeCol)
                simSetUIButtonColor(uiHandle,b+2,passiveCol)
                simSetUIButtonColor(uiHandle,b+3,activeCol)
                simSetUIButtonColor(uiHandle,b+4,activeCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,activeCol)
            end
            if (d==7) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,passiveCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,passiveCol)
                simSetUIButtonColor(uiHandle,b+4,passiveCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,passiveCol)
            end
            if (d==8) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,activeCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,activeCol)
                simSetUIButtonColor(uiHandle,b+4,activeCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,activeCol)
            end
            if (d==9) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,activeCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,activeCol)
                simSetUIButtonColor(uiHandle,b+4,passiveCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,activeCol)
            end
            c=c-d*(10^(2-i))
        end
    end
    previousCounter=number
end
function sysCall_sensing()
    local res,dist,pt,objHandle=sim.readProximitySensor(sensor)
    if res&gt;0 then
        local p=sim.getModelProperty(objHandle)
        if sim.boolAnd32(p,sim.modelproperty_not_model)~=0 then
            objHandle=sim.getObjectParent(objHandle)
        end
        sim.removeModel(objHandle)
        destroyedCount=destroyedCount+1
        updateUI(uiH,destroyedCount)
    end
end
</t>
<t tx="leo.20210528000742.33">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210528000742.34">function sysCall_init()
    pathHandle=sim.getObjectHandle("ShortConveyorBeltPath")
    forwarder=sim.getObjectHandle('ConveyorBelt_forwarder')
    sim.setPathTargetNominalVelocity(pathHandle,0) -- for backward compatibility
end
</t>
<t tx="leo.20210528000742.35">function sysCall_cleanup() 
end 
</t>
<t tx="leo.20210528000742.36">function sysCall_actuation() 
    beltVelocity=sim.getScriptSimulationParameter(sim.handle_self,"conveyorBeltVelocity")
    local dt=sim.getSimulationTimeStep()
    local pos=sim.getPathPosition(pathHandle)
    pos=pos+beltVelocity*dt
    sim.setPathPosition(pathHandle,pos) -- update the path's intrinsic position
    -- Here we "fake" the transportation pads with a single static rectangle that we dynamically reset
    -- at each simulation pass (while not forgetting to set its initial velocity vector) :
    local relativeLinearVelocity={beltVelocity,0,0}
    -- Reset the dynamic rectangle from the simulation (it will be removed and added again)
    sim.resetDynamicObject(forwarder)
    -- Compute the absolute velocity vector:
    local m=sim.getObjectMatrix(forwarder,-1)
    m[4]=0 -- Make sure the translation component is discarded
    m[8]=0 -- Make sure the translation component is discarded
    m[12]=0 -- Make sure the translation component is discarded
    local absoluteLinearVelocity=sim.multiplyVector(m,relativeLinearVelocity)
    -- Now set the initial velocity of the dynamic rectangle:
    sim.setObjectFloatParameter(forwarder,sim.shapefloatparam_init_velocity_x,absoluteLinearVelocity[1])
    sim.setObjectFloatParameter(forwarder,sim.shapefloatparam_init_velocity_y,absoluteLinearVelocity[2])
    sim.setObjectFloatParameter(forwarder,sim.shapefloatparam_init_velocity_z,absoluteLinearVelocity[3])
end 
</t>
<t tx="leo.20210528000742.37">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210528000742.38">function sysCall_init()
    s=sim.getObjectHandle('suctionPadSensor')
    l=sim.getObjectHandle('suctionPadLoopClosureDummy1')
    l2=sim.getObjectHandle('suctionPadLoopClosureDummy2')
    b=sim.getObjectHandle('suctionPadBodyRespondable')
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
<t tx="leo.20210528000742.39">-- This script is in charge of giving the suction pad its functionality
function sysCall_cleanup() 
end 
</t>
<t tx="leo.20210528000742.4">function sysCall_init()
    -- Prepare a floating view with the camera views:
    cam=sim.getObjectAssociatedWithScript(sim.handle_self)
    view=sim.floatingViewAdd(0.9,0.9,0.2,0.2,0)
    sim.adjustView(view,cam,64)
end
</t>
<t tx="leo.20210528000742.40">function sysCall_sensing() 
    parent=sim.getObjectParent(l)
    if (sim.getScriptSimulationParameter(sim.handle_self,'active')==false) then
        -- when active is falase 
        -- b=sim.getObjectHandle('suctionPadBodyRespondable')
        if (parent~=b) then
            -- unlink the dummy
            -- l=sim.getObjectHandle('suctionPadLoopClosureDummy1') 
            sim.setLinkDummy(l,-1)
            -- set l object parent as b
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
<t tx="leo.20210528000742.5">function sysCall_cleanup() 
end 
</t>
<t tx="leo.20210528000742.6">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210528000742.7">function sysCall_init()
end
</t>
<t tx="leo.20210528000742.8">function sysCall_vision(inData)
    -- callback function automatically added for backward compatibility
    -- (vision sensor have no filters anymore, but rather a callback function where image processing can be performed)
    local retVal={}
    retVal.trigger=false
    retVal.packedPackets={}
    simVision.sensorImgToWorkImg(inData.handle)
    -- simVision.intensityScaleOnWorkImg(inData.handle,1.000000,0.000000,true)
    simVision.selectiveColorOnWorkImg(inData.handle,{0.500000,0.900000,0.500000},{0.500000,0.100000,0.400000},false,true,false)
    local trig,packedPacket=simVision.blobDetectionOnWorkImg(inData.handle,0.150000,0.000000,false) 
    if trig 
        then retVal.trigger=true 
    end 
    if packedPacket 
        then retVal.packedPackets[#retVal.packedPackets+1]=packedPacket 
    end
    simVision.sensorImgToWorkImg(inData.handle)
    simVision.workImgToSensorImg(inData.handle)
    return retVal
end
</t>
<t tx="leo.20210528000742.9">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210528001331.1">simSetLinkDummy / sim.setLinkDummy
Description 	Defines (or breaks) a dummy-dummy link pair. Useful to create dynamic loop closure constraints on the fly (among others). See also sim.getLinkDummy.
C synopsis 	simInt simSetLinkDummy(simInt dummyHandle,simInt linkedDummyHandle)
C parameters 	
dummyHandle: handle of the first dummy in the dummy-dummy link pair.
linkedDummyHandle: handle of the second dummy in the dummy-dummy link pair. Set to -1 to unlink the first dummy.</t>
<t tx="leo.20210528001540.1">Description 	Sets an object's parent object. See also sim.getObjectParent.
C synopsis 	simInt simSetObjectParent(simInt objectHandle,simInt parentObjectHandle,simBool keepInPlace)
C parameters 	
objectHandle: handle of the object that will become child of the parent object. Can be combined with sim_handleflag_assembly (simply add sim_handleflag_assembly to objectHandle), if the two objects can be assembled via a predefined assembly transformation (refer to the assembling option in the object common properties). In that case, parentObjectHandle can't be -1, and keepInPlace should be set to false.
parentObjectHandle: handle of the object that will become parent, or -1 if the object should become parentless.
keepInPlace: indicates whether the object's absolute position and orientation should stay same</t>
<t tx="leo.20210528002109.1">sim.getObjectMatrix

Description 	Retrieves the transformation matrix of an object. See also the other matrix/transformation functions.
C synopsis 	simInt simGetObjectMatrix(simInt objectHandle,simInt relativeToObjectHandle,simFloat* matrix)
C parameters 	
objectHandle: handle of the object. Can be combined with sim_handleflag_reljointbaseframe (see next argument)
relativeToObjectHandle: indicates relative to which reference frame we want the matrix. Specify -1 to retrieve the absolute transformation matrix, sim_handle_parent to retrieve the transformation matrix relative to the object's parent, or an object handle relative to whose reference frame we want the transformation matrix. If this handle is the handle of a joint, then the matrix relative to the joint's moving frame will be returned (unless objectHandle is combined with sim_handleflag_reljointbaseframe, in which case the matrix relative to the joint's base frame will be returned).
matrix: pointer to 12 simFloat values (the last row of the 4x4 matrix (0,0,0,1) is not needed)
The x-axis of the orientation component is (matrix[0],matrix[4],matrix[8])
The y-axis of the orientation component is (matrix[1],matrix[5],matrix[9])
The z-axis of the orientation component is (matrix[2],matrix[6],matrix[10])
The translation component is (matrix[3],matrix[7],matrix[11])</t>
<t tx="leo.20210528002346.1">-- Activate the suction pad:
sim.setScriptSimulationParameter(sim.getScriptAssociatedWithObject(suctionPad),'active','true')

-- Deactivate the suction pad:
sim.setScriptSimulationParameter(sim.getScriptAssociatedWithObject(suctionPad),'active','false')

</t>
</tnodes>
</leo_file>
