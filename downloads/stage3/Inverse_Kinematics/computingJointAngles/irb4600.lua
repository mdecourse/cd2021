function sysCall_init()
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

applyJoints=function(jointHandles,joints)
    for i=1,#jointHandles,1 do
        sim.setJointPosition(jointHandles[i],joints[i])
    end
end

function configurationValidationCallback(config)
    sim.addLog(sim.verbosity_scriptinfos,"Hello from validation callback")
    -- Here you could check for collisions, and other test. If the configuration is valid, return true
    return true
end

function sysCall_actuation()
    local dummyHandle=targets[cnt1+1]
    local m=sim.getObjectMatrix(dummyHandle,-1)
    simIK.setObjectMatrix(ikEnv,ikTarget,-1,m)
    
    -- Search for a configuration for a maximum of 100 ms:
    local startTime=sim.getSystemTimeInMs(-1)
    while sim.getSystemTimeInMs(startTime)<100 do
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
    if cnt2>20 then
        cnt2=0
        cnt1=cnt1+1
        if cnt1>3 then
            cnt1=0
        end
    end
end

function sysCall_cleanup()
    simIK.eraseEnvironment(ikEnv)
end