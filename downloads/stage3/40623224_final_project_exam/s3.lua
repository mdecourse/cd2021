threadFunction=function()
    while sim.getSimulationState()~=sim.simulation_advancing_abouttostop do
        -- Read the keyboard messages (make sure the focus is on the main window, scene view):
message,auxiliaryData=sim.getSimulatorMessage()
        while message~=-1 do
key=auxiliaryData[1]
sim.addStatusbarMessage('key:'..key)
            if (message==sim.message_keypress) then
                if (auxiliaryData[1]==2010) then
                    --  catch key 
                    if(sliding >=0.25) then
                    else sliding = sliding + 0.05
sim.addStatusbarMessage('sliding:'..sliding)
                    end
                end
                if (auxiliaryData[1]==2009) then
                    --  place key 
                    if(sliding <= -0.25) then
                    else sliding = sliding - 0.05
sim.addStatusbarMessage('sliding:'..sliding)
                    end
                end
            end
message,auxiliaryData=sim.getSimulatorMessage()
        end
 

        sim.setJointTargetPosition(slider, sliding)

        -- Since this script is threaded, don't waste time here:
        sim.switchThread() -- Resume the script at next simulation loop start
    end
end
-- Put some initialization code here:
-- Retrieving of some handles and setting of some initial values:
slider=sim.getObjectHandle("S4")
sliding = 0
-- Here we execute the regular thread code:
res,err=xpcall(threadFunction,function(err) return debug.traceback(err) end)
if not res then
    sim.addStatusbarMessage('Lua runtime error: '..err)
end
 
-- Put some clean-up code here: