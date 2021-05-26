function sysCall_init() 
    -- Check if the required plugin (simExtMtb.dll) is there:
    -- ##################################################################
    moduleName=0
    moduleVersion=0
    index=0
    MTBModuleFound=false
    while moduleName do
        moduleName,moduleVersion=sim.getModuleName(index)
        if (moduleName=='Mtb') then
            MTBModuleFound=true
        end
        index=index+1
    end
    if (MTBModuleFound==false) then
        sim.displayDialog('Error','\'Mtb\' plugin was not found. (simExtMtb.dll, libsimExtMtb.dylib or libsimExtMtb.so)&&nSimulation will not run properly',sim.dlgstyle_ok,false,nil,{0.8,0,0,0,0,0},{0.5,0,0,1,1,1})
    end
    -- -----------------------------------------------------------------
    -- Get some object handles that are required later:
    -- ################################################
    robotHandle=sim.getObjectAssociatedWithScript(sim.handle_self)
    userInterfaceHandle=simGetUIHandle('MTB_userInterface')
    inOutDlgHandle=simGetUIHandle('MTB_IN_OUT_userInterface')
    collisionHandle=sim.getCollisionHandle('MTB_Collision')
    jointHandles={-1,-1,-1,-1}
    for i=1,4,1 do
        jointHandles[i]=sim.getObjectHandle('MTB_axis'..i)
    end
    robotName=sim.getObjectName(sim.getObjectAssociatedWithScript(sim.handle_self))
    simSetUIButtonLabel(userInterfaceHandle,0,robotName)
    simSetUIButtonLabel(inOutDlgHandle,0,robotName)
    collisionMessageID=-1
    compilErrorMessageID=-1
    dfltButProp=sim.buttonproperty_button+sim.buttonproperty_horizontallycentered+sim.buttonproperty_staydown+sim.buttonproperty_verticallycentered
    jointPositions={0,0,0,0}
    for i=1,4,1 do
        jointPositions[i]=sim.getJointPosition(jointHandles[i]) -- the initial joint positions
    end
    restarting=false
    cmdMessage=''
    robotProgramExecutionState=1 -- 0 is stopped, 1 is executing, 2 is paused
    -- ------------------------------------------------
    -- Now start the server:
    serverHandle=startRobotServer(robotHandle,program,{0,0,0,0},{0.1,0.4})
end
program=[[REM ************************************************
REM This is a very very simple robot language EXAMPLE!
REM Following commands are supported (one command per line):
REM -"REM" starts a comment line
REM -"SETROTVEL v": sets the revolute joint velocity for next movements (in degrees/s)
REM -"SETLINVEL v": sets the prismatic joint velocity for next movements (in meters/s)
REM -"MOVE p1 p2 p3 p4": moves to joint positions (p1;p2;p3;p4) (in degrees or meter)
REM -"WAIT x": waits x miliseconds
REM -"SETBIT y": sets the bit at pos y in the output buffer
REM -"CLEARBIT y": clears the bit at pos y in the output buffer
REM -"IFBITGOTO y label": jumps to "label" position if bit at pos y is set in the input buffer
REM -"IFNBITGOTO y label": jumps to "label" position if bit at pos y is not set in the input buffer
REM -"GOTO label": jumps to "label" position
REM any not recognized word is considered to be a label
REM ************************************************
SETROTVEL 45
SETLINVEL 0.1
MOVE 0 0 0 0
PROGRAM_BEGIN_LABEL
MOVE 0 0 0.03 0
IFBITGOTO 1 LABEL1
SETBIT 1
LABEL1
WAIT 500
MOVE 0 0 0 0
WAIT 250
MOVE -160 -43.5 0 203.5
WAIT 250
MOVE -160 -43.5 0.03 203.5
CLEARBIT 1
WAIT 500
MOVE -160 -43.5 0 203.5
WAIT 250
MOVE 160 43.5 0 -203.5
WAIT 250
MOVE 160 43.5  0.03 -203.5
IFBITGOTO 1 LABEL2
SETBIT 1
LABEL2
WAIT 500
MOVE 160 43.5  0 -203.5
GOTO LABEL1
]]
-- ***********************************************************************************************************************
-- ***********************************************************************************************************************
-- ***********************************************************************************************************************
-- This script makes the link between the MTB robot and the simExtMtb.dll plugin. This script could be much
-- shorter and simple, if everything was taken care of in the plugin. The advantage of handling many things here
-- is that if something needs to be changed, the plugin doesn't require to be recompiled
-- Following commands are registered by the MTB plugin:
--
-- number serverHandle,string msg=simMTB.startServer(string serverExecutable,number connectionPort,string programData,table_4 jointValues,table_2 initialJointVelocity)
-- Starts a robot server, and compiles the program. If result>=0, the call was successful. Otherwise msg contains a compilation error message
--
-- boolean result=simMTB.stopServer(number serverHandle)
-- Stops a robot server
--
-- number result,string info=simMTB.step(number serverHandle,number deltaTime)
-- runs the robot language interpreter for deltaTime. if result==0, the program is running, if result==1 the program ended. Any other value means an error
--
-- table_4 jointValues=simMTB.getJoints(number serverHandle)
-- returns the values of the robot's 4 axis
--
-- table_4 outputValues=simMTB.getOutput(number serverHandle)
-- returns the 32 bits (4*8) of the robot's outputs
--
-- table_4 inputValues=simMTB.getInput(number serverHandle)
-- returns the 32 bits (4*8) of the robot's inputs
--
-- number result=simMTB.setInput(number serverHandle,table_4 inputValues)
-- writes the 32 bits (4*8) of the robot's inputs
--
-- boolean result=simMTB.connectInput(number inputServerHandle,number inputBitNumber,number outputServerHandle,number outputBitNumber,number connectionType)
-- connects a robot's output bit to another robot's input bit. If connectionType~=0 the connection line invertes the bit state
--
-- boolean result=simMTB.disconnectInput(number inputServerHandle,number inputBitNumber)
-- disconnects a connection previously done with simMTB.connectInput
--
-- ***********************************************************************************************************************
-- ***********************************************************************************************************************
-- ***********************************************************************************************************************
startRobotServer=function(theRobotHandle,theProgram,initJoints,initVel)
    -- Find a (hopefully) free port:
    local portNb=sim.getInt32Parameter(sim.intparam_server_port_next)
    local portStart=sim.getInt32Parameter(sim.intparam_server_port_start)
    local portRange=sim.getInt32Parameter(sim.intparam_server_port_range)
    local newPortNb=portNb+1
    if (newPortNb>=portStart+portRange) then
        newPortNb=portStart
    end
    sim.setInt32Parameter(sim.intparam_server_port_next,newPortNb)
    -- Start the server:
    local serverHandle,errorMsg=simMTB.startServer('mtbServer',portNb,theProgram,initJoints,initVel)
    if serverHandle<0 then
        -- We have a problem. Display the message:
        sim.displayDialog('Compilation Error','Robot \''..robotName..'\' caused a program compilation error: '..errorMsg,sim.dlgstyle_ok,false,nil,{0,0,0,1,1,1},{1,0.74,0,0,0,0})
    end
    -- Now write the server handle to the robot object, so that other objects can access that handle too:
    sim.writeCustomDataBlock(theRobotHandle,'@tmpMTBSERVERHANDLE',sim.packInt32Table({serverHandle}))
    return serverHandle
end
function sysCall_cleanup()
    if serverHandle>=0 then
        simMTB.stopServer(serverHandle)
    end
end 
function sysCall_actuation() 
    -- React to "run", "pause" and "stop" presses:
    -- ###########################################
    buttonHandle=simGetUIEventButton(userInterfaceHandle)
    if (buttonHandle==99) then
        -- "Run" was pressed
        if (robotProgramExecutionState==0) then
            robotProgramExecutionState=1
        else
            if (robotProgramExecutionState==2) then robotProgramExecutionState=1 end
        end
    end
    if (buttonHandle==100) then
        -- "Pause" was pressed
        if (robotProgramExecutionState==1) then robotProgramExecutionState=2 end
    end
    if (buttonHandle==101) then
        -- "Stop" was pressed
        if (robotProgramExecutionState~=0) then
            robotProgramExecutionState=0
            restarting=true
            cmdMessage=''
        end
    end
    -- ------------------------------------------
    -- Following section is where the script is communicating with the extension module:
    -- #################################################################################
    if MTBModuleFound and serverHandle>=0 then
        if (robotProgramExecutionState>0) then
            dt=sim.getSimulationTimeStep()
            if (robotProgramExecutionState==2) then dt=0 end -- When pausing, we simply set dt to zero!
            if (restarting) then
                -- Reset the robot and interpreter:
                simMTB.stopServer(serverHandle)
                serverHandle=startRobotServer(robotHandle,program,{0,0,0,0},{0.1,0.4})
                restarting=false
            else
                -- Handle the robot program (simMTB.run is a custom Lua command defined in the simExtMtb.dll extension module):
                result,cmdMessage,newJointPositions=simMTB.step(serverHandle,dt)
                if (result~=-1) then
                    -- program executes fine
                    -- Read the joint values and the robot's output (simMTB.getJoints and simMTB.getOutput are custom Lua command defined in the simExtMtb.dll extension module):
                    jointPositions=simMTB.getJoints(serverHandle)
                    outputData=simMTB.getOutput(serverHandle)
                    if (result==1) then
                        -- program end
                        robotProgramExecutionState=0
                        restarting=true
                        cmdMessage=''
                    end
                end
            end
        end
        -- Read the robot's input (simMTB.getInput is a custom Lua command defined in the simExtMtb.dll extension module):
        inputData=simMTB.getInput(serverHandle)
    end
    -- ---------------------------------------------------------------------------------
    -- Report the new joint positions to the MTB robot:
    -- ################################################
    for i=1,4,1 do
        sim.setJointPosition(jointHandles[i],jointPositions[i])
    end
    -- ------------------------------------------------
    -- Update the main custom dialog:
    -- ##############################
    -- The "run" button:
    runP=0
    if (robotProgramExecutionState~=1) then 
        runP=sim.buttonproperty_enabled
    else
        runP=sim.buttonproperty_isdown
    end
    simSetUIButtonProperty(userInterfaceHandle,99,dfltButProp+runP)
    -- The "pause" button:
    pauseP=0
    if (robotProgramExecutionState==1) then pauseP=sim.buttonproperty_enabled end
    if (robotProgramExecutionState==2) then pauseP=pauseP+sim.buttonproperty_isdown end
    simSetUIButtonProperty(userInterfaceHandle,100,dfltButProp+pauseP)
    -- The "stop" button:
    stopP=0
    if (robotProgramExecutionState~=0) then stopP=sim.buttonproperty_enabled end
    simSetUIButtonProperty(userInterfaceHandle,101,dfltButProp+stopP)
    -- The command label:
    simSetUIButtonLabel(userInterfaceHandle,102,cmdMessage)
    -- The joint labels:
    simSetUIButtonLabel(userInterfaceHandle,103,string.format('%.2f',jointPositions[1]*180/math.pi))
    simSetUIButtonLabel(userInterfaceHandle,104,string.format('%.2f',jointPositions[2]*180/math.pi))
    simSetUIButtonLabel(userInterfaceHandle,105,string.format('%.4f',jointPositions[3]))
    simSetUIButtonLabel(userInterfaceHandle,106,string.format('%.2f',jointPositions[4]*180/math.pi))
    -- ------------------------------
    -- Display or hide the digital IN/OUT custom dialog:
    -- #################################################
    if (sim.boolAnd32(simGetUIButtonProperty(userInterfaceHandle,109),sim.buttonproperty_isdown)~=0) then
        simSetUIProperty(inOutDlgHandle,sim.boolOr32(simGetUIProperty(inOutDlgHandle),sim_ui_property_visible))
    else
        simSetUIProperty(inOutDlgHandle,sim.boolOr32(simGetUIProperty(inOutDlgHandle),sim_ui_property_visible)-sim_ui_property_visible)
    end
    -- ------------------------------------------------
    -- Update (read and write) the IN/OUT custom dialog:
    -- #################################################
    if (MTBModuleFound and (sim.boolAnd32(simGetUIProperty(inOutDlgHandle),sim_ui_property_visible)~=0) ) then
        buttonHandle=simGetUIEventButton(inOutDlgHandle)
        if (buttonHandle>=120)and(buttonHandle<=151) then -- React to button presses here:
            inputData[1+math.floor((buttonHandle-120)/8)]=sim.boolXor32(inputData[1+math.floor((buttonHandle-120)/8)],2^math.mod(buttonHandle-120,8))
        end
        -- Write the robot's input (simMTB.setInput is a custom Lua command defined in the simExtMtb.dll extension module):
        simMTB.setInput(serverHandle,inputData)
        for i=0,3,1 do
            for j=0,7,1 do
                if (sim.boolAnd32(inputData[1+i],2^j)~=0) then
                    simSetUIButtonProperty(inOutDlgHandle,120+j+i*8,dfltButProp+sim.buttonproperty_isdown+sim.buttonproperty_enabled)
                else
                    simSetUIButtonProperty(inOutDlgHandle,120+j+i*8,dfltButProp+sim.buttonproperty_enabled)
                end
            end
        end
        for i=0,3,1 do
            for j=0,7,1 do
                if (sim.boolAnd32(outputData[1+i],2^j)~=0) then
                    simSetUIButtonProperty(inOutDlgHandle,220+j+i*8,dfltButProp+sim.buttonproperty_isdown)
                else
                    simSetUIButtonProperty(inOutDlgHandle,220+j+i*8,dfltButProp)
                end
            end
        end
    end
    -- -------------------------------------------------
end
function sysCall_cleanup() 
    sim.writeCustomDataBlock(robotHandle,'@tmpMTBSERVERHANDLE',nil)
end 
