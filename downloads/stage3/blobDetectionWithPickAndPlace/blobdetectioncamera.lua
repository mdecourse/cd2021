function sysCall_init()
         
    camera=sim.getObjectHandle('blobDetectionCamera_camera')
    baseObject=sim.getObjectAssociatedWithScript(sim.handle_self)
    conveyor=sim.getObjectHandle('whiteConveyor')
    res=sim.getVisionSensorResolution(camera)
    lastImageAnalysisTime=0
    lastLowestBlobDetectionPositionY=100
    lastLowestBlobDetectionTime=0
    
end

function sysCall_cleanup() 
 
end 

function sysCall_actuation() 
    t=sim.getSimulationTime()
    camPos=sim.getObjectPosition(camera,-1)
    imageAnalysisFrequency=sim.getScriptSimulationParameter(sim.getScriptAssociatedWithObject(baseObject),'imageAnalysisFrequency')
    
    if (t-lastImageAnalysisTime>1/imageAnalysisFrequency) then
        cv=sim.getScriptSimulationParameter(sim.getScriptAssociatedWithObject(conveyor),'conveyorBeltVelocity')
        lastImageAnalysisTime=t
        sim.handleVisionSensor(camera) -- the image processing camera is handled explicitely, since we do not need to execute that command at each simulation pass
        result,t0,t1=sim.readVisionSensor(camera) -- Here we read the image processing camera!
        if (t1) then -- in t1 we should have the blob information if the camera was set-up correctly
            blobCount=t1[1]
            dataSizePerBlob=t1[2]
            lowestYofDetection=100
            -- Now we go through all blobs:
            for i=1,blobCount,1 do
                blobSize=t1[2+(i-1)*dataSizePerBlob+1]
                blobOrientation=t1[2+(i-1)*dataSizePerBlob+2]
                blobPos={t1[2+(i-1)*dataSizePerBlob+3],t1[2+(i-1)*dataSizePerBlob+4]}
                blobBoxDimensions={t1[2+(i-1)*dataSizePerBlob+5],t1[2+(i-1)*dataSizePerBlob+6]}
    
                if (blobBoxDimensions[1]>blobBoxDimensions[2]) then
                    tmp=blobBoxDimensions[1]
                    blobBoxDimensions[1]=blobBoxDimensions[2]
                    blobBoxDimensions[2]=tmp
                    blobOrientation=blobOrientation+math.pi/2
                end
    
    
                if (blobSize>0.01)and(blobPos[2]>0.2)and(blobPos[2]<0.8) then
    
                    blobCol=sim.getVisionSensorImage(camera,res[1]*blobPos[1],res[2]*blobPos[2],1,1)
                    if (blobCol[1]>blobCol[2])and(blobCol[1]>blobCol[3]) then
                        colorCode=1
                    end
                    if (blobCol[2]>blobCol[1])and(blobCol[2]>blobCol[3]) then
                        colorCode=2
                    end
                    if (blobCol[3]>blobCol[1])and(blobCol[3]>blobCol[2]) then
                        colorCode=3
                    end
                    if (blobSize>0.02) then
                        blobColIntensity=(blobCol[1]+blobCol[2]+blobCol[3])/3
                        shapeType=2 -- T
                        -- Now check the orientation of the T (up or down). We test a point that is supposed to be in the left or right T wings:
                        coord={0,0}
                        coord[1]=blobPos[1]+blobBoxDimensions[1]*0.37*math.cos(blobOrientation)-blobBoxDimensions[2]*0.45*math.sin(blobOrientation)
                        coord[2]=blobPos[2]+blobBoxDimensions[1]*0.37*math.sin(blobOrientation)+blobBoxDimensions[2]*0.45*math.cos(blobOrientation)
                        blobCol=sim.getVisionSensorImage(camera,res[1]*coord[1],res[2]*coord[2],1,1)
                        pointIntensity=(blobCol[1]+blobCol[2]+blobCol[3])/3
                        if (math.abs(pointIntensity-blobColIntensity)>0.1) then
                            blobOrientation=blobOrientation+math.pi
                        end
                    else
                        shapeType=1 -- I
                    end
                    absPosX=camPos[1]+(0.5-blobPos[1])*0.55 -- 0.55 is to have a match between camera coordinates and space coordinates
                    absPosY=camPos[2]+(0.5-blobPos[2])*0.55
                    -- Following condition is so that we don't detect two same blobs that were detected at different times:
                    if (absPosY<(lastLowestBlobDetectionPositionY+cv*(t-lastLowestBlobDetectionTime)-0.05)) then
                        packedBlobData=sim.packInt32Table({shapeType,colorCode})..sim.packFloatTable({absPosX,absPosY,t,blobOrientation})
                        info=sim.getStringSignal('shapeInfos')
                        if (not info) then
                            info=packedBlobData
                        else
                            info=packedBlobData..info
                        end
                        sim.setStringSignal('shapeInfos',info) -- this string signal is available to the two robots
                    end
                    if (absPosY<lowestYofDetection) then
                        lowestYofDetection=absPosY
                    end
                end
            end
            lastLowestBlobDetectionPositionY=lowestYofDetection
            lastLowestBlobDetectionTime=t
        end
    end
end 

