function sysCall_init() 
    modelBase=sim.getObjectHandle('LaserPointer')
    sensor=sim.getObjectHandle('LaserPointer_sensor')
    ui=simGetUIHandle('LaserPointer_UI')
    simSetUIButtonLabel(ui,0,sim.getObjectName(modelBase))
    local color={1,0,0}
    pointContainer=sim.addDrawingObject(sim.drawing_cyclic+sim.drawing_painttag+sim.drawing_points,4,0,-1,1,color)
    lineContainer=sim.addDrawingObject(sim.drawing_cyclic+sim.drawing_painttag+sim.drawing_lines,2,0,-1,1,color)
    communicationTube=sim.tubeOpen(0,'laserPointerData'..sim.getNameSuffix(nil),1)
end
-- Check the end of the script for some explanations!
function sysCall_cleanup() 
end 
function sysCall_sensing() 
    res,dist,pt=sim.handleProximitySensor(sensor)
    m=sim.getObjectMatrix(sensor,-1)
    pt1=sim.multiplyVector(m,{0,0,0})
    pt2={0,0,100}
    if (res>0) then
        pt2=pt
    end
    pt2=sim.multiplyVector(m,pt2)
    sim.addDrawingObjectItem(lineContainer,nil)
    sim.addDrawingObjectItem(pointContainer,nil)
    if (sim.getScriptSimulationParameter(sim.handle_self,'showLaserRay')) then
        sim.addDrawingObjectItem(lineContainer,{pt1[1],pt1[2],pt1[3],pt2[1],pt2[2],pt2[3]})
    end
    if (res>0) then
        if (sim.getScriptSimulationParameter(sim.handle_self,'showLaserPoint')) then
            sim.addDrawingObjectItem(pointContainer,pt2)
        end
        simSetUIButtonLabel(ui,2,string.format("Distance: %.4f meters",dist))
        sim.tubeWrite(communicationTube,sim.packFloatTable({dist}))
        sim.setFloatSignal('laserPointerData',dist)
    else
        simSetUIButtonLabel(ui,2,'Distance: -')
        sim.tubeWrite(communicationTube,sim.packFloatTable({-1}))
        sim.setFloatSignal('laserPointerData',99)
    end
    -- To read data from this laser range finder in another script, use following code:
    --
    -- communicationTube=sim.tubeOpen(0,'laserPointerData'..sim.getNameSuffix(nil),1) -- put this in the initialization phase
    -- data=sim.tubeRead(communicationTube)
    -- if (data) then
    --     distance=sim.unpackFloatTable(data)[1]
    -- end
    --
    -- If the script in which you read the laser pointer has a different suffix than the laser pointer suffix,
    -- then you will have to slightly adjust the code, e.g.:
    -- communicationTube=sim.tubeOpen(0,'laserPointerData#') -- if the laser pointer script has no suffix
    -- or
    -- communicationTube=sim.tubeOpen(0,'laserPointerData#0') -- if the laser pointer script has a suffix 0
    -- or
    -- communicationTube=sim.tubeOpen(0,'laserPointerData#1') -- if the laser pointer script has a suffix 1
    -- etc.
    --
    --
    -- You can of course also use global variables (not elegant and not scalable), e.g.:
    -- In the laser pointer script:
    -- sim.setFloatSignal('laserPointerData',dist)
    --
    -- And in the script that needs the data:
    -- dist=sim.getFloatSignal('laserPointerData')
    --
    -- In addition to that, there are many other ways to have 2 scripts exchange data. Check the documentation for more details
end 
