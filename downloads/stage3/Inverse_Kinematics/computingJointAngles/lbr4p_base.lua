function sysCall_init()
        
    jh={-1,-1,-1,-1,-1,-1,-1}
    for i=1,7,1 do
        jh[i]=sim.getObjectHandle('j'..i)
    end
    ikGroup=sim.getIkGroupHandle('ik')
    ikTarget=sim.getObjectHandle('target')
    targets={sim.getObjectHandle('testTarget5'),sim.getObjectHandle('testTarget6'),sim.getObjectHandle('testTarget7'),sim.getObjectHandle('testTarget8')}
    cnt1=0
    cnt2=0
    
end
applyJoints=function(jointHandles,joints)
    for i=1,#jointHandles,1 do
        sim.setJointPosition(jointHandles[i],joints[i])
    end
end


function sysCall_actuation()
    local dummyHandle=targets[cnt1+1]
    local m=sim.getObjectMatrix(dummyHandle,-1)
    sim.setObjectMatrix(ikTarget,-1,m)
    state=sim.getConfigForTipPose(ikGroup,jh,0.5,100)
    if state then
        applyJoints(jh,state)
    end
    cnt2=cnt2+1
    if cnt2>9 then
        cnt2=0
        cnt1=cnt1+1
        if cnt1>3 then
            cnt1=0
        end
    end
end

