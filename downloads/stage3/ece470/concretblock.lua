function sysCall_init()
    
    h=sim.getObjectAssociatedWithScript(sim.handle_self)
    ui=simGetUIHandle('ConcretBlock')

    local p=simGetUIProperty(ui)
    p=sim.boolOr32(p,sim_ui_property_visible)
    simSetUIProperty(ui,p-sim_ui_property_visible)    
end

function sysCall_nonSimulation()
    local selectedObjects=sim.getObjectSelection()
    if selectedObjects and (#selectedObjects==1) and (selectedObjects[1]==h) then
        local p=simGetUIProperty(ui)
        p=sim.boolOr32(p,sim_ui_property_visible)
        simSetUIProperty(ui,p)
        buttonID=simGetUIEventButton(ui)
        if (buttonID~=-1) then
            isStatic=(sim.boolAnd32(simGetUIButtonProperty(ui,14),sim.buttonproperty_isdown)~=0)
            xs=simGetUISlider(ui,7)/1000
            ys=simGetUISlider(ui,8)/1000
            zs=simGetUISlider(ui,9)/1000
            ds=simGetUISlider(ui,10)/1000

            dxs=5*0.1^((1-xs)*2)
            dys=5*0.1^((1-ys)*2)
            dzs=5*0.1^((1-zs)*2)
            dds=10000*0.1^((1-ds)*2)

            sizeVals=sim.getObjectSizeValues(h)
            sizeVals[1]=sizeVals[1]*0.5
            sizeVals[2]=sizeVals[2]*0.5
            sizeVals[3]=sizeVals[3]*0.5
                
            sim.scaleObject(h,dxs/sizeVals[1],dys/sizeVals[2],dzs/sizeVals[3])

            p=sim.getObjectPosition(h,-1)
            sim.setObjectPosition(h,-1,{p[1],p[2],p[3]+sizeVals[3]*(dzs/sizeVals[3]-1)*0.5})

            sizeVals=sim.getObjectSizeValues(h)
            sizeVals[1]=sizeVals[1]*0.5
            sizeVals[2]=sizeVals[2]*0.5
            sizeVals[3]=sizeVals[3]*0.5
            mass=sizeVals[1]*sizeVals[2]*sizeVals[3]*dds
            sim.setObjectFloatParameter(h,sim.shapefloatparam_mass,mass)

            if (isStatic) then
                sim.setObjectInt32Parameter(h,sim.shapeintparam_static,1)
            else
                sim.setObjectInt32Parameter(h,sim.shapeintparam_static,0)
            end
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
