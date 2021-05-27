function signal_switch(singal,enable)
    
    if singal==1 or singal==12 then
        sim.setIntegerSignal("call_1",enable)
    end
    if singal==2 or singal==11 then
        sim.setIntegerSignal("call_2",enable)
    end
    if singal==3 or singal==10 then
        sim.setIntegerSignal("call_3",enable)
    end
    if singal==4 or singal==9 then
        sim.setIntegerSignal("call_4",enable)
    end
    if singal==5 or singal==8 then
        sim.setIntegerSignal("call_5",enable)
    end
    if singal==6 or singal==7 then
        sim.setIntegerSignal("call_6",enable)
    end
end

function sysCall_threadmain()
    joint01=sim.getObjectHandle('X')
    joint02=sim.getObjectHandle('Y')
    joint03=sim.getObjectHandle('Z')
    jointr=sim.getObjectHandle('Rotate')
    tt=1
    long_t=1.5
    long_long_t=3 --time set
    rotate_deg=0 --pad rotate
    atz=0  --altitude set
    setx=0.5
    setpx=-0.5 --center pick set
    sety=-0.16
    setpy=-0.16 --center fall set
    local pick_high={"0.0645","0.134","0.2025","0.2768"} --pick up high set
    local fall_high={"0.05","0.12","0.18","0.26"} --fall high set
    local high_up={"0","0","0.05","0.12"}
    cube=1              -- set cube
    ball_pick_time=0    --total ball we pick
    ball_put_time=31     --total ball we put
    while (ball_pick_time<60) do
        for ball=1,6,1 do    --pick the ball
            ball_pick_time=ball_pick_time+1 --total time we pick
            i=1
            unit=0
            level=0
            while level < ball_pick_time do  --find which level and place should be of the xy coordinates
                unit=unit+1
                level=level+unit^2
            end
            finding_XY=ball_pick_time   --this is the XY on that floor
            while(i<=unit-1) do            
                finding_XY=finding_XY-(i^2) 
                i=i+1
            end
            X_Pos=finding_XY%unit       -- the X and Y coordinates(by balls)
             if X_Pos==0 then
                X_Pos=unit
            end
            Y_Pos=(math.ceil(finding_XY/unit)) 
            BaseX=setx-((unit-1)*0.05)--now we need to find the 0 of the xy
            BaseY=sety-((unit-1)*0.05)
            sim.setJointTargetPosition(joint01,BaseX+(0.1*(X_Pos-1))) --move to Position
            sim.wait(tt)
            sim.setJointTargetPosition(joint02,BaseY+(0.1*(Y_Pos-1)))
            sim.wait(tt)
            signal_switch(ball,1) --switch pad on
            sim.setJointTargetPosition(joint03,-pick_high[unit])--pick the pall
            sim.wait(tt)
            sim.setJointTargetPosition(joint03,atz-high_up[unit]) --after pick up we dont need to go that high
            sim.wait(tt)
            rotate_deg=rotate_deg+60  --rotate the pad
            sim.setJointTargetPosition(jointr,rotate_deg*math.pi/180)
            sim.wait(tt)
            sim.wait(tt)
        end
        sim.wait(long_t)
        sim.setJointTargetPosition(joint01,0)
        sim.setJointTargetPosition(joint02,0)
        sim.setJointTargetPosition(joint03,0)
        sim.wait(long_t)
        for ball=1,6,1 do --put the ball
            ball_put_time=ball_put_time-1
            i=1
            unit=0
            level=0
            while level < ball_put_time do  --find which level and place should be of the xy coordinates
                unit=unit+1
                level=level+unit^2
            end
            finding_XY=ball_put_time   --this is the XY on that floor
            while(i<=unit-1) do            
                finding_XY=finding_XY-(i^2) 
                i=i+1
            end
            X_Pos=finding_XY%unit       -- the X and Y coordinates(by balls)
             if X_Pos==0 then
                X_Pos=unit
            end
            Y_Pos=(math.ceil(finding_XY/unit)) 
            BaseX=setpx-((unit-1)*0.05)--now we need to find the 0 of the xy
            BaseY=setpy-((unit-1)*0.05)
            rotate_deg=rotate_deg-60  --rotate the pad
            sim.setJointTargetPosition(jointr,rotate_deg*math.pi/180)
            sim.wait(tt)
            sim.setJointTargetPosition(joint01,BaseX+(0.1*(X_Pos-1))) --move to Position
            sim.wait(tt)
            sim.setJointTargetPosition(joint02,BaseY+(0.1*(Y_Pos-1)))
            sim.wait(tt)
            sim.setJointTargetPosition(joint03,-fall_high[unit])--pick the pall
            sim.wait(tt)
            signal_switch(ball+6,0) --switch pad off
            sim.wait(tt)
            sim.setJointTargetPosition(joint03,atz-high_up[unit]) --after pick up we dont need to go that high
            sim.wait(tt)
            sim.wait(tt)
        end
        sim.wait(long_t)
        sim.setJointTargetPosition(joint01,0)
        sim.setJointTargetPosition(joint02,0)
        sim.setJointTargetPosition(joint03,0)
        sim.wait(long_t)
        if ball_pick_time==30 then
            pick_high={"0.07","0.138","0.2085","0.28"}
            setx=-setx
            setpx=-setpx
            ball_pick_time=0
            ball_put_time=31
        end
    end
end