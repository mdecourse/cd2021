function sysCall_init()
         
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
-- We handle inverse kinematics explicitely in this script, so that we can control
-- what happens if an IK task fails

function sysCall_cleanup() 
 
end 

function sysCall_sensing() 
     
end 

function sysCall_actuation() 
    
    
    -- Now save the robot joint configuration in case IK fails at the next stage.
    -- We have to explore the tree structure of the model:
    toExplore={baseObjectHandle}
    jointsAndTheirPositions={}
    while (#toExplore>0) do
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

