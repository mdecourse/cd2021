function sysCall_init()
    -- sim.handle_self is the handle of the object associated with the script currently executing
    h=sim.getObjectHandle(sim.handle_self)
    initM=sim.getObjectMatrix(h,-1)
end

function sysCall_actuation()
    local t=sim.getSimulationTime()
    local p={0.11*math.sin(t*1),0.07*math.sin(t*1.2),0.05*math.sin(t*1.6)}
    local e={0.1*math.sin(t*0.5),0.05*math.sin(t*0.3),0.025*math.sin(t)}
    local m=sim.buildMatrix(p,e)
    m=sim.multiplyMatrices(initM,m)
    sim.setObjectMatrix(h,-1,m)
end
