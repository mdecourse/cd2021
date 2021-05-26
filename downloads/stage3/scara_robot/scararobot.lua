sim.setThreadAutomaticSwitch(false)
sim.switchThread()

threadFunction=function()
    while sim.getSimulationState()~=sim.simulation_advancing_abouttostop do
        sim.setJointTargetPosition(gripper,gripperOpen)
        sim.followPath(target,Path,1,0,manipVelocity)
        sim.setJointTargetPosition(gripper,gripperClose)
        sim.wait(gripperActionTime)
        sim.followPath(target,Path0,1,0,manipVelocity) 
        sim.setJointTargetPosition(gripper,gripperOpen)
        sim.wait(gripperActionTime)
        sim.followPath(target,Path1,1,0,manipVelocity*0.2)
        sim.wait(stopTime)
        sim.followPath(target,Path4,1,0,manipVelocity)
        sim.setJointTargetPosition(gripper,gripperClose)
        sim.wait(gripperActionTime)
        sim.followPath(target,Path5,1,0,manipVelocity) 
        sim.setJointTargetPosition(gripper,gripperOpen)
        sim.wait(gripperActionTime)
        sim.followPath(target,Path6,1,0,manipVelocity*0.2)
        sim.wait(stopTime)
        sim.followPath(target,Path11,1,0,manipVelocity)
        sim.setJointTargetPosition(gripper,gripperClose)
        sim.wait(gripperActionTime)
        sim.followPath(target,Path12,1,0,manipVelocity) 
        sim.setJointTargetPosition(gripper,gripperOpen)
        sim.wait(gripperActionTime)
        sim.followPath(target,Path13,1,0,manipVelocity*0.2)
        sim.wait(stopTime)
        sim.followPath(target,Path17,1,0,manipVelocity)
        sim.setJointTargetPosition(gripper,gripperClose)
        sim.wait(gripperActionTime)
        sim.followPath(target,Path18,1,0,manipVelocity) 
        sim.setJointTargetPosition(gripper,gripperOpen)
        sim.wait(gripperActionTime)
        sim.followPath(target,Path19,1,0,manipVelocity*0.2)
        sim.wait(stopTime)
        sim.stopSimulation()
    end
end

Path=sim.getObjectHandle("Path")
Path0=sim.getObjectHandle("Path0")
Path1=sim.getObjectHandle("Path1")
Path4=sim.getObjectHandle("Path4")
Path5=sim.getObjectHandle("Path5")
Path6=sim.getObjectHandle("Path6")
Path11=sim.getObjectHandle("Path13")
Path12=sim.getObjectHandle("Path11")
Path13=sim.getObjectHandle("Path12")
Path17=sim.getObjectHandle("Path17")
Path18=sim.getObjectHandle("Path18")
Path19=sim.getObjectHandle("Path19")
target=sim.getObjectHandle("Scara_target")
gripper=sim.getObjectHandle("Gripper_J")
manipVelocity=1
gripperOpen=0.04
gripperClose=0
gripperActionTime=1
stopTime=10
defaultPosition=sim.getObjectPosition(target,-1)
defaultOrientation=sim.getObjectOrientation(target,-1)

res,err=xpcall(threadFunction,function(err) return debug.traceback(err) end)
if not res then
    sim.addStatusbarMessage('Lua runtime error: '..err)
end
