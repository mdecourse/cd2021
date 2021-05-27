function sysCall_init()
end

function sysCall_vision(inData)
    -- callback function automatically added for backward compatibility
    -- (vision sensor have no filters anymore, but rather a callback function where image processing can be performed)
    local retVal={}
    retVal.trigger=false
    retVal.packedPackets={}
    simVision.sensorImgToWorkImg(inData.handle)
    -- simVision.intensityScaleOnWorkImg(inData.handle,1.000000,0.000000,true)
    simVision.selectiveColorOnWorkImg(inData.handle,{0.500000,0.900000,0.500000},{0.500000,0.100000,0.400000},false,true,false)
    local trig,packedPacket=simVision.blobDetectionOnWorkImg(inData.handle,0.150000,0.000000,false) 
    if trig 
        then retVal.trigger=true 
    end 
    if packedPacket 
        then retVal.packedPackets[#retVal.packedPackets+1]=packedPacket 
    end
    simVision.sensorImgToWorkImg(inData.handle)
    simVision.workImgToSensorImg(inData.handle)
    return retVal
end

