function sysCall_init()
        
    h=sim.getObjectAssociatedWithScript(sim.handle_self)
    amplitude=0.6
    speed=0.46
    
end

function sysCall_actuation()
    sim.setJointPosition(h,math.sin(sim.getSimulationTime()*speed)*amplitude)
end

