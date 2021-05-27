function sysCall_init()
        
    sensor=sim.getObjectHandle('deletionBox_sensor')
    uiH=simGetUIHandle('sinkCounter')
    destroyedCount=0
    updateUI(uiH,destroyedCount)
    
end
updateUI=function(uiHandle,number)
    if (previousCounter~=number) then
        activeCol={1.0,0.1,0.1}
        passiveCol={0.1,0.1,0.1}
        c=math.fmod(number,1000)
        for i=0,2,1 do
            d=math.floor(c/(10^(2-i)))
            b=100+i*10
            if (d==0) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,activeCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,passiveCol)
                simSetUIButtonColor(uiHandle,b+4,activeCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,activeCol)
            end
            if (d==1) then
                simSetUIButtonColor(uiHandle,b+0,passiveCol)
                simSetUIButtonColor(uiHandle,b+1,passiveCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,passiveCol)
                simSetUIButtonColor(uiHandle,b+4,passiveCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,passiveCol)
            end
            if (d==2) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,passiveCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,activeCol)
                simSetUIButtonColor(uiHandle,b+4,activeCol)
                simSetUIButtonColor(uiHandle,b+5,passiveCol)
                simSetUIButtonColor(uiHandle,b+6,activeCol)
            end
            if (d==3) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,passiveCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,activeCol)
                simSetUIButtonColor(uiHandle,b+4,passiveCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,activeCol)
            end
            if (d==4) then
                simSetUIButtonColor(uiHandle,b+0,passiveCol)
                simSetUIButtonColor(uiHandle,b+1,activeCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,activeCol)
                simSetUIButtonColor(uiHandle,b+4,passiveCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,passiveCol)
            end
            if (d==5) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,activeCol)
                simSetUIButtonColor(uiHandle,b+2,passiveCol)
                simSetUIButtonColor(uiHandle,b+3,activeCol)
                simSetUIButtonColor(uiHandle,b+4,passiveCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,activeCol)
            end
            if (d==6) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,activeCol)
                simSetUIButtonColor(uiHandle,b+2,passiveCol)
                simSetUIButtonColor(uiHandle,b+3,activeCol)
                simSetUIButtonColor(uiHandle,b+4,activeCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,activeCol)
            end
            if (d==7) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,passiveCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,passiveCol)
                simSetUIButtonColor(uiHandle,b+4,passiveCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,passiveCol)
            end
            if (d==8) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,activeCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,activeCol)
                simSetUIButtonColor(uiHandle,b+4,activeCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,activeCol)
            end
            if (d==9) then
                simSetUIButtonColor(uiHandle,b+0,activeCol)
                simSetUIButtonColor(uiHandle,b+1,activeCol)
                simSetUIButtonColor(uiHandle,b+2,activeCol)
                simSetUIButtonColor(uiHandle,b+3,activeCol)
                simSetUIButtonColor(uiHandle,b+4,passiveCol)
                simSetUIButtonColor(uiHandle,b+5,activeCol)
                simSetUIButtonColor(uiHandle,b+6,activeCol)
            end
            c=c-d*(10^(2-i))
        end
    end
    previousCounter=number
end


function sysCall_sensing()
    local res,dist,pt,objHandle=sim.readProximitySensor(sensor)
    if res>0 then
        local p=sim.getModelProperty(objHandle)
        if sim.boolAnd32(p,sim.modelproperty_not_model)~=0 then
            objHandle=sim.getObjectParent(objHandle)
        end
        sim.removeModel(objHandle)
        destroyedCount=destroyedCount+1
        updateUI(uiH,destroyedCount)
    end
end

