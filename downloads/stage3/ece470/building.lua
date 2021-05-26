function __setObjectPosition__(a,b,c)
    -- compatibility routine, wrong results could be returned in some situations, in CoppeliaSim <4.0.1
    if b==sim.handle_parent then
        b=sim.getObjectParent(a)
    end
    if (b~=-1) and (sim.getObjectType(b)==sim.object_joint_type) and (sim.getInt32Parameter(sim.intparam_program_version)>=40001) then
        a=a+sim.handleflag_reljointbaseframe
    end
    return sim.setObjectPosition(a,b,c)
end
function __setObjectOrientation__(a,b,c)
    -- compatibility routine, wrong results could be returned in some situations, in CoppeliaSim <4.0.1
    if b==sim.handle_parent then
        b=sim.getObjectParent(a)
    end
    if (b~=-1) and (sim.getObjectType(b)==sim.object_joint_type) and (sim.getInt32Parameter(sim.intparam_program_version)>=40001) then
        a=a+sim.handleflag_reljointbaseframe
    end
    return sim.setObjectOrientation(a,b,c)
end
function sysCall_init()
    
    h=sim.getObjectAssociatedWithScript(sim.handle_self)
    windowElement=sim.getObjectHandle('building_windowElement')
    windows=sim.getObjectHandle('building_windows')
    body=sim.getObjectHandle('building_body')
    ui=simGetUIHandle('building')

    local p=simGetUIProperty(ui)
    p=sim.boolOr32(p,sim_ui_property_visible)
    simSetUIProperty(ui,p-sim_ui_property_visible)    
end
------------------------------------------------------------------------------ 
-- Following few lines automatically added by V-REP to guarantee compatibility 
-- with V-REP 3.1.3 and earlier: 
colorCorrectionFunction=function(_aShapeHandle_) 
    local version=sim.getInt32Parameter(sim.intparam_program_version) 
    local revision=sim.getInt32Parameter(sim.intparam_program_revision) 
    if (version<30104)and(revision<3) then 
        return _aShapeHandle_ 
    end 
    return '@backCompatibility1:'.._aShapeHandle_ 
end 
------------------------------------------------------------------------------ 
 
 
_hueToRgb=function(m1,m2,h)
    if h<0 then 
        h=h+1
    end
    if h>1 then 
        h=h-1
    end
    if 6*h<1 then
        return(m1+(m2-m1)*h*6)
    end
    if 2*h<1 then
        return(m2)
    end
    if 3*h<2 then
        return(m1+(m2-m1)*((2/3)-h)*6)
    end
    return(m1)
end

hslToRgb=function(hsl)
    local h=hsl[1]
    local s=hsl[2]
    local l=hsl[3]
    local m1,m2
    local rgb={0,0,0}

    if s==0 then
        rgb[1]=l
        rgb[2]=l
        rgb[3]=l
    else 
        if l<=0.5 then
            m2=l*(1+s)
        else
            m2=l+s-l*s
        end
        m1=2*l-m2
        rgb[1]=_hueToRgb(m1,m2,h+1/3)
        rgb[2]=_hueToRgb(m1,m2,h)
        rgb[3]=_hueToRgb(m1,m2,h-1/3)
    end
    return(rgb)
end


function sysCall_nonSimulation()
    local selectedObjects=sim.getObjectSelection()
    if selectedObjects and (#selectedObjects==1) and (selectedObjects[1]==h) then
        local p=simGetUIProperty(ui)
        p=sim.boolOr32(p,sim_ui_property_visible)
        simSetUIProperty(ui,p)
        buttonID=simGetUIEventButton(ui)
        if ((buttonID==7)or(buttonID==8)or(buttonID==9)) then
            sizeFact=sim.getObjectSizeFactor(h)
            local xCnt=math.floor(17.5*simGetUISlider(ui,7)/1000)+3
            local yCnt=math.floor(17.5*simGetUISlider(ui,8)/1000)+3
            local zCnt=math.floor(19.5*simGetUISlider(ui,9)/1000)+1
            local sx=2.9*xCnt
            local sy=2.9*yCnt
            local sz=2.6*zCnt

            dat=sim.readCustomDataBlock(h,'buildingSizes')
            if (dat) then
                dat=sim.unpackInt32Table(dat)
            end
            if (not dat)or(dat[1]~=xCnt)or(dat[2]~=yCnt)or(dat[3]~=zCnt) then
                sim.writeCustomDataBlock(h,'buildingSizes',sim.packInt32Table({xCnt,yCnt,zCnt}))
                simSetUIButtonLabel(ui,3,'X-size: '..(sx*sizeFact)..'m')
                simSetUIButtonLabel(ui,4,'Y-size: '..(sy*sizeFact)..'m')
                simSetUIButtonLabel(ui,5,'Z-size: '..(sz*sizeFact)..'m')
                local bodyName=sim.getObjectName(body)
                sim.removeObject(body)
                local windowsName=sim.getObjectName(windows)
                sim.removeObject(windows)
                body=sim.createPureShape(0,1+2+8+16,{sx*sizeFact,sy*sizeFact,sz*sizeFact},1000)
                adjustColor=true    
                sim.setObjectName(body,bodyName)
                sim.setObjectParent(body,h,true)
                __setObjectPosition__(body,h,{0,0,sz*sizeFact*0.5})
                __setObjectOrientation__(body,h,{0,0,0})
                sim.setObjectInt32Parameter(body,sim.objintparam_visibility_layer,1+256)
                local p=sim.getObjectProperty(body)
                sim.setObjectProperty(body,p+sim.objectproperty_selectmodelbaseinstead)
                p=sim.getObjectSpecialProperty(body)
                sim.setObjectSpecialProperty(body,sim.boolOr32(p,sim.objectspecialproperty_collidable+sim.objectspecialproperty_measurable+sim.objectspecialproperty_detectable_all+sim.objectspecialproperty_renderable))
                selection=sim.getObjectSelection()
                -- Now the windows:
                local allWindows={}
                for i=1,xCnt-1,1 do
                    for k=1,zCnt,1 do
                        local c=sim.copyPasteObjects({windowElement},0)
                        local window=c[1]
                        allWindows[#allWindows+1]=window
                        __setObjectPosition__(window,h,{(-(xCnt-2)*0.5*2.9+(i-1)*2.9)*sizeFact,-sy*0.5*sizeFact,(1.4+(k-1)*2.6)*sizeFact})
                        c=sim.copyPasteObjects({windowElement},0)
                        window=c[1]
                        allWindows[#allWindows+1]=window
                        __setObjectPosition__(window,h,{(-(xCnt-2)*0.5*2.9+(i-1)*2.9)*sizeFact,sy*0.5*sizeFact,(1.4+(k-1)*2.6)*sizeFact})
                        __setObjectOrientation__(window,h,{0,0,math.pi})
                    end
                end
                for i=1,yCnt-1,1 do
                    for k=1,zCnt,1 do
                        local c=sim.copyPasteObjects({windowElement},0)
                        local window=c[1]
                        allWindows[#allWindows+1]=window
                        __setObjectPosition__(window,h,{-sx*0.5*sizeFact,(-(yCnt-2)*0.5*2.9+(i-1)*2.9)*sizeFact,(1.4+(k-1)*2.6)*sizeFact})
                        __setObjectOrientation__(window,h,{0,0,-math.pi*0.5})
                        c=sim.copyPasteObjects({windowElement},0)
                        window=c[1]
                        allWindows[#allWindows+1]=window
                        __setObjectPosition__(window,h,{sx*0.5*sizeFact,(-(yCnt-2)*0.5*2.9+(i-1)*2.9)*sizeFact,(1.4+(k-1)*2.6)*sizeFact})
                        __setObjectOrientation__(window,h,{0,0,math.pi*0.5})
                    end
                end
                -- Now group all the windows:
                windows=sim.groupShapes(allWindows)
                sim.setObjectName(windows,windowsName)
                sim.setObjectParent(windows,h,true)
                p=sim.getObjectProperty(windows)
                sim.setObjectProperty(windows,p+sim.objectproperty_selectmodelbaseinstead+sim.objectproperty_dontshowasinsidemodel)
                sim.setObjectInt32Parameter(windows,sim.objintparam_visibility_layer,1)
                sim.removeObjectFromSelection(sim.handle_all,-1)
                sim.addObjectToSelection(selection)
            end
        end
        if (buttonID==10) or adjustColor then
            local specialHue=simGetUISlider(ui,10)/1000
            if specialHue<0.1 then
                rgb={0.7,0.7,0.7}
            else
                hsl={(specialHue-0.1)/0.9,0.3,0.7}
                rgb=hslToRgb(hsl)
            end
            sim.setShapeColor(colorCorrectionFunction(body),nil,0,rgb)
            adjustColor=false
        end

        if (buttonID==2) then
            simRemoveUI(ui)
            sim.removeScript(sim.handle_self)
        end
    else
        local p=simGetUIProperty(ui)
        p=sim.boolOr32(p,sim_ui_property_visible)
        simSetUIProperty(ui,p-sim_ui_property_visible)
    end
end

function sysCall_beforeSimulation()
    local p=simGetUIProperty(ui)
    p=sim.boolOr32(p,sim_ui_property_visible)
    simSetUIProperty(ui,p-sim_ui_property_visible)
end
