
function sysCall_threadmain()
    jointHandles={-1,-1,-1,-1,-1,-1}
    gripperHandle= sim.getObjectHandle('suctionPad')
    scriptHandle = sim.getScriptAssociatedWithObject(gripperHandle)
    for i=1,6,1 do
        jointHandles[i]=sim.getObjectHandle('UR3_joint'..i)
    end
    -- Set-up some of the RML vectors:
    vel=180
    accel=40
    jerk=80
    currentVel={0,0,0,0,0,0,0}
    currentAccel={0,0,0,0,0,0,0}
    maxVel={vel*math.pi/180,vel*math.pi/180,vel*math.pi/180,vel*math.pi/180,vel*math.pi/180,vel*math.pi/180}
    maxAccel={accel*math.pi/180,accel*math.pi/180,accel*math.pi/180,accel*math.pi/180,accel*math.pi/180,accel*math.pi/180}
    maxJerk={jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180}
    targetVel={0,0,0,0,0,0}
    targetPos1={0,60*math.pi/180,30*math.pi/180,0,-90*math.pi/180,0}
    targetPos2={0,0,0,0,0,0}
    targetPos3={-90*math.pi/180,60*math.pi/180,30*math.pi/180,0,-90*math.pi/180,0}
    targetPos4={0,92*math.pi/180,0,0,-90*math.pi/180,0}
    targetPos5={180*math.pi/180,90*math.pi/180,0,0,-90*math.pi/180,0*math.pi/180}
    dist = 99
    while dist > 0.5 do
        dist = sim.getFloatSignal("CarDistanceData")
    end
    sim.rmlMoveToJointPositions(jointHandles,-1,currentVel,currentAccel,maxVel,maxAccel,maxJerk,targetPos1,targetVel)
    sim.rmlMoveToJointPositions(jointHandles,-1,currentVel,currentAccel,maxVel,maxAccel,maxJerk,targetPos2,targetVel)
    sim.rmlMoveToJointPositions(jointHandles,-1,currentVel,currentAccel,maxVel,maxAccel,maxJerk,targetPos3,targetVel)
    sim.setScriptSimulationParameter(scriptHandle, 'active', 'false')
    sim.rmlMoveToJointPositions(jointHandles,-1,currentVel,currentAccel,maxVel,maxAccel,maxJerk,targetPos2,targetVel)
    sim.setScriptSimulationParameter(scriptHandle, 'active', 'true')
    --sim.rmlMoveToJointPositions(jointHandles,-1,currentVel,currentAccel,maxVel,maxAccel,maxJerk,targetPos1,targetVel)
    sim.rmlMoveToJointPositions(jointHandles,-1,currentVel,currentAccel,maxVel,maxAccel,maxJerk,targetPos4,targetVel)
    sim.rmlMoveToJointPositions(jointHandles,-1,currentVel,currentAccel,maxVel,maxAccel,maxJerk,targetPos2,targetVel)
    sim.rmlMoveToJointPositions(jointHandles,-1,currentVel,currentAccel,maxVel,maxAccel,maxJerk,targetPos5,targetVel)
    sim.setScriptSimulationParameter(scriptHandle, 'active', 'false')
    sim.rmlMoveToJointPositions(jointHandles,-1,currentVel,currentAccel,maxVel,maxAccel,maxJerk,targetPos2,targetVel)
end
