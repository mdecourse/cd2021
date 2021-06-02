-- IK setup by using GUI method
function sysCall_init() 
    ik_undamped=sim.getIkGroupHandle('RobotA_undamped')
    ik_damped=sim.getIkGroupHandle('RobotA_damped')
end

function sysCall_cleanup() 
 
end 

function sysCall_actuation() 
    if sim.handleIkGroup(ik_undamped)==sim.ikresult_fail then
        -- the position/orientation could not be reached.
        sim.handleIkGroup(ik_damped) -- Apply a damped resolution method
        if not ikFailedReportHandle then -- We display a IK failure report message
            ikFailedReportHandle=sim.displayDialog("IK failure report","RobotA: IK solver failed.",sim.dlgstyle_message,false,"",nil,{1,0.7,0,0,0,0})
        end
    else
        if ikFailedReportHandle then
            sim.endDialog(ikFailedReportHandle) -- We close any report message about IK failure
            ikFailedReportHandle=nil
        end
    end
end 
