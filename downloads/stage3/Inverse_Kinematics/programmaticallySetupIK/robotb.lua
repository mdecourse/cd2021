-- use program to setup IK group
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

function sysCall_actuation()
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

function sysCall_cleanup() 
    simIK.eraseEnvironment(ikEnv) -- erase the IK environment
end 
