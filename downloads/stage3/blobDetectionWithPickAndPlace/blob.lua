function sysCall_init()
         
    -- Prepare a floating view with the camera views:
    cam=sim.getObjectAssociatedWithScript(sim.handle_self)
    view=sim.floatingViewAdd(0.9,0.9,0.2,0.2,0)
    sim.adjustView(view,cam,64)
    
end

function sysCall_cleanup() 
 
end 

