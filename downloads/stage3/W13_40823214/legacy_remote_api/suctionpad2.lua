function sysCall_init() 
    modelBase4=sim.getObjectAssociatedWithScript(sim.handle_self)
    robotBase4=modelBase4
    while true do
        robotBase4=sim.getObjectParent(robotBase4)
        if robotBase4==-1 then
            robotName4='Base'
            break
        end
        robotName4=sim.getObjectName(robotBase4)
        suffix,suffixlessName=sim.getNameSuffix(robotName4)
        if suffixlessName=='Base' then
            break
        end
    end
    sa=sim.getObjectHandle('suctionPadSensor#2')
    la=sim.getObjectHandle('suctionPadLoopClosureDummy1#2')
    l2a=sim.getObjectHandle('suctionPadLoopClosureDummy2#2')
    ba=sim.getObjectHandle('suctionPad')
    suctionPadLink=sim.getObjectHandle('suctionPadLink#2')
    local gripperBase=sim.getObjectAssociatedWithScript(sim.handle_self)

    infiniteStrength=sim.getScriptSimulationParameter(sim.handle_self,'infiniteStrength')
    maxPullForce=sim.getScriptSimulationParameter(sim.handle_self,'maxPullForce')
    maxShearForce=sim.getScriptSimulationParameter(sim.handle_self,'maxShearForce')
    maxPeelTorque=sim.getScriptSimulationParameter(sim.handle_self,'maxPeelTorque')

    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end


function sysCall_cleanup() 
    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end 

function sysCall_sensing() 
    parent=sim.getObjectParent(la)
    local sig=sim.getIntegerSignal("call_4")
    if (not sig) or (sig==0) then
        if (parent~=ba) then
            sim.setLinkDummy(la,-1)
            sim.setObjectParent(la,ba,true)
            ma=sim.getObjectMatrix(l2a,-1)
            sim.setObjectMatrix(la,-1,ma)
        end
    else
        if (parent==ba) then
            -- Here we want to detect a respondable shape, and then connect to it with a force sensor (via a loop closure dummy dummy link)
            -- However most respondable shapes are set to "non-detectable", so "sim.readProximitySensor" or similar will not work.
            -- But "sim.checkProximitySensor" or similar will work (they don't check the "detectable" flags), but we have to go through all shape objects!
            index=0
            while true do
                shape=sim.getObjects(index,sim.object_shape_type)
                if (shape==-1) then
                    break
                end
                if (shape~=ba) and (sim.getObjectInt32Parameter(shape,sim.shapeintparam_respondable)~=0) and (sim.checkProximitySensor(sa,shape)==1) then
                    -- Ok, we found a respondable shape that was detected
                    -- We connect to that shape:
                    -- Make sure the two dummies are initially coincident:
                    sim.setObjectParent(la,ba,true)
                    ma=sim.getObjectMatrix(l2a,-1)
                    sim.setObjectMatrix(la,-1,ma)
                    -- Do the connection:
                    sim.setObjectParent(la,shape,true)
                    sim.setLinkDummy(la,l2a)
                    break
                end
                index=index+1
            end
        else
            -- Here we have an object attached
            if (infiniteStrength==false) then
                -- We might have to conditionally beak it apart!
                result,force,torque=sim.readForceSensor(suctionPadLink) -- Here we read the median value out of 5 values (check the force sensor prop. dialog)
                if (result>0) then
                    breakIt=false
                    if (force[3]>maxPullForce) then breakIt=true end
                    sf=math.sqrt(force[1]*force[1]+force[2]*force[2])
                    if (sf>maxShearForce) then breakIt=true end
                    if (torque[1]>maxPeelTorque) then breakIt=true end
                    if (torque[2]>maxPeelTorque) then breakIt=true end
                    if (breakIt) then
                        -- We break the link:
                        sim.setLinkDummy(la,-1)
                        sim.setObjectParent(la,ba,true)
                        ma=sim.getObjectMatrix(l2a,-1)
                        sim.setObjectMatrix(la,-1,ma)
                    end
                    
                end
            end
        end
    end
end 
