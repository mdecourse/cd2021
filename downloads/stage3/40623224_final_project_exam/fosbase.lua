function sysCall_init() 
    velocity=0
    velocity2=0
    velocity3=0
    velocity4=0
    velocity5=0
    velocity6=0
    velocity7=0
    velocity8=0
-----------
    sliding_b = 0
    sliding_r = 0
-----------
    left_joint_b1=sim.getObjectHandle('left_R1')
    left_joint_b2=sim.getObjectHandle('left_R2')
    left_joint_b3=sim.getObjectHandle('left_R3')
    left_joint_b4=sim.getObjectHandle('left_R4')

    left_slider_b1=sim.getObjectHandle('left_S1')
    left_slider_b2=sim.getObjectHandle('left_S2')
    left_slider_b3=sim.getObjectHandle('left_S3')
    left_slider_b4=sim.getObjectHandle('left_S4')
-----------

    right_joint_r1=sim.getObjectHandle('right_R1')
    right_joint_r2=sim.getObjectHandle('right_R2')
    right_joint_r3=sim.getObjectHandle('right_R3')
    right_joint_r4=sim.getObjectHandle('right_R4')

    right_slider_r1=sim.getObjectHandle('right_S1')
    right_slider_r2=sim.getObjectHandle('right_S2')
    right_slider_r3=sim.getObjectHandle('right_S3')
    right_slider_r4=sim.getObjectHandle('right_S4')
end

function sysCall_actuation()
        sim.setJointTargetPosition(left_joint_b1,velocity)
        sim.setJointTargetPosition(left_joint_b2,velocity2)
        sim.setJointTargetPosition(left_joint_b3,velocity3)
        sim.setJointTargetPosition(left_joint_b4,velocity4)
        sim.setJointTargetPosition(right_joint_r1,velocity5)
        sim.setJointTargetPosition(right_joint_r2,velocity6)
        sim.setJointTargetPosition(right_joint_r3,velocity7)
        sim.setJointTargetPosition(right_joint_r4,velocity8)
---------------------
        sim.setJointTargetPosition(left_slider_b1,sliding_b)
        sim.setJointTargetPosition(left_slider_b2,sliding_b)
        sim.setJointTargetPosition(left_slider_b3,sliding_b)
        sim.setJointTargetPosition(left_slider_b4,sliding_b)
        sim.setJointTargetPosition(right_slider_r1,sliding_r)
        sim.setJointTargetPosition(right_slider_r2,sliding_r)
        sim.setJointTargetPosition(right_slider_r3,sliding_r)
        sim.setJointTargetPosition(right_slider_r4,sliding_r)
    message,auxiliaryData=sim.getSimulatorMessage()
        while message ~= -1 do
key=auxiliaryData[1]
sim.addStatusbarMessage('key:'..key)
            if (message==sim.message_keypress) then
-----------------player_B
                if (auxiliaryData[1]==119)then --w
                    velocity=100
                    velocity2=100
                    velocity3=100
                    velocity4=100
                end
                if (auxiliaryData[1]==103) then --g
                    -- goalkeeper kick keypress(g)
                     velocity = -100 
                end
                if (auxiliaryData[1]==104) then
                    -- guard kick keypress(h) 
                     velocity2 = -100 
                end
                if (auxiliaryData[1]==106) then
                    -- midfield kick keypress(j) 
                     velocity3 = -100 
                end
                if (auxiliaryData[1]==107) then
                    -- forward kick keypress(k)
                     velocity4 = -100 
                end
                if (auxiliaryData[1]==97) then
                    -- left key
                    if (sliding_b >= 0.05) then 
                    else sliding_b = sliding_b + 0.01
sim.addStatusbarMessage('sliding_b:'..sliding_b)
                    end
                end
                if (auxiliaryData[1]==100) then
                    -- right key
                    if (sliding_b <= -0.05) then 
                    else sliding_b = sliding_b - 0.01
sim.addStatusbarMessage('sliding_b:'..sliding_b)
                    end
                end
-------------------player_R
                if (auxiliaryData[1]==2007)then
                    velocity5=100
                    velocity6=100
                    velocity7=100
                    velocity8=100
                end
                if (auxiliaryData[1]==49) then
                    -- goalkeeper kick keypress(1)
                     velocity5 = -100 
                end
                if (auxiliaryData[1]==50) then
                    -- guard kick keypress(2)
                     velocity6 = -100 
                end
                if (auxiliaryData[1]==51) then
                    -- midfield kick keypress(3)
                     velocity7 = -100 
                end
                if (auxiliaryData[1]==2001) then
                    -- forward kick keypress(enter)
                     velocity8 = -100 
                end
                if (auxiliaryData[1]==2009) then
                    -- left key
                    if (sliding_r >= 0.05) then 
                    else sliding_r = sliding_r + 0.01
sim.addStatusbarMessage('sliding_r:'..sliding_r)
                    end
                end
                if (auxiliaryData[1]==2010) then
                    -- right key
                    if (sliding_r <= -0.05) then 
                    else sliding_r = sliding_r - 0.01
sim.addStatusbarMessage('sliding_r:'..sliding_r)
                    end
                end
            end
            message,auxiliaryData=sim.getSimulatorMessage()
        end
----
end