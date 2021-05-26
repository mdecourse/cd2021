sim.setThreadAutomaticSwitch(false)
sim.switchThread()

threadFunction=function()
    while sim.getSimulationState()~=sim.simulation_advancing_abouttostop do
        sim.wait(Time)
        sim.setJointTargetPosition(gripper2,gripperOpen2)
        sim.followPath(target2,Path2,1,0,manipVelocity2*0.2)
        sim.setJointTargetPosition(gripper2,gripperClose)
        sim.wait(gripperActionTime)
        sim.followPath(target2,Path3,1,0,manipVelocity2) 
        sim.setJointTargetPosition(gripper2,gripperOpen2)
        sim.wait(gripperActionTime)
        sim.followPath(target2,Path4,1,0,manipVelocity2*0.2)
        sim.wait(Time)
        sim.followPath(target2,Path8,1,0,manipVelocity2*0.2)
        sim.setJointTargetPosition(gripper2,gripperClose)
        sim.wait(gripperActionTime)
        sim.followPath(target2,Path9,1,0,manipVelocity2) 
        sim.setJointTargetPosition(gripper2,gripperOpen2)
        sim.wait(gripperActionTime)
        sim.followPath(target2,Path10,1,0,manipVelocity2*0.2)
        sim.wait(Time)
        sim.followPath(target2,Path14,1,0,manipVelocity2*0.2)
        sim.setJointTargetPosition(gripper2,gripperClose)
        sim.wait(gripperActionTime)
        sim.followPath(target2,Path15,1,0,manipVelocity2) 
        sim.setJointTargetPosition(gripper2,gripperOpen2)
        sim.wait(gripperActionTime)
        sim.followPath(target2,Path16,1,0,manipVelocity2*0.2)
        sim.wait(stopTime)
        --sim.stopSimulation()
    end
end

Path2=sim.getObjectHandle("Path2")
Path3=sim.getObjectHandle("Path3")
Path4=sim.getObjectHandle("Path7")
Path8=sim.getObjectHandle("Path9")
Path9=sim.getObjectHandle("Path8")
Path10=sim.getObjectHandle("Path10")
Path14=sim.getObjectHandle("Path14")
Path15=sim.getObjectHandle("Path15")
Path16=sim.getObjectHandle("Path16")
target2=sim.getObjectHandle("Scara_target2")
gripper2=sim.getObjectHandle("Gripper_J0")
manipVelocity2=1
gripperOpen2=0.04
gripperClose=0
gripperActionTime=1
stopTime=15
Time=10
defaultPosition=sim.getObjectPosition(target2,-1)
defaultOrientation=sim.getObjectOrientation(target2,-1)

res,err=xpcall(threadFunction,function(err) return debug.traceback(err) end)
if not res then
    sim.addStatusbarMessage('Lua runtime error: '..err)
endssage('Lua runtime error: '..err)
end
