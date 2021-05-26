function sysCall_init()
    
    h=sim.getObjectAssociatedWithScript(sim.handle_self)
    ui=simGetUIHandle('Tree')
    local randomCols=(sim.boolAnd32(simGetUIButtonProperty(ui,6),sim.buttonproperty_isdown)~=0)
    setColors(randomCols)

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
 
 
setColors=function(randomCols)
    local green={0.23,0.32,0.23}
    local brown={0.49,0.41,0.29}
    if (randomCols) then
        math.randomseed(sim.getFloatParameter(sim.floatparam_rand)*10000)
        green[1]=0.17+math.random()*0.16
        green[3]=0.11+math.random()*0.12
        brown[1]=0.45+math.random()*0.04
        brown[2]=0.36+math.random()*0.05
        brown[3]=0.29+math.random()*0.07
    end
    sim.setShapeColor(colorCorrectionFunction(h),'TREE_GREEN',0,green)
    sim.setShapeColor(colorCorrectionFunction(h),'TREE_BROWN',0,brown)
end


function sysCall_nonSimulation()
    local selectedObjects=sim.getObjectSelection()
    if selectedObjects and (#selectedObjects==1) and (selectedObjects[1]==h) then
        local p=simGetUIProperty(ui)
        p=sim.boolOr32(p,sim_ui_property_visible)
        simSetUIProperty(ui,p)
        buttonID=simGetUIEventButton(ui)
        if (buttonID==7) then
            local s=simGetUISlider(ui,7)/1000
            local ds=10*0.1^((1-s)*2)
            local sf=sim.getObjectSizeFactor(h)
            local scale=ds/sf
            sim.scaleObject(h,scale,scale,scale)
            p=sim.getObjectPosition(h,-1)
            sim.setObjectPosition(h,-1,{p[1],p[2],p[3]*scale})
        end
        if (buttonID==5) then
            local respondable=(sim.boolAnd32(simGetUIButtonProperty(ui,5),sim.buttonproperty_isdown)~=0)
            local p=sim.getModelProperty(h)
            p=sim.boolOr32(p,sim.modelproperty_not_respondable)
            if (respondable) then
                p=p-sim.modelproperty_not_respondable
            end
            sim.setModelProperty(h,p)
        end
        if (buttonID==6) then
            local randomCols=(sim.boolAnd32(simGetUIButtonProperty(ui,6),sim.buttonproperty_isdown)~=0)
            setColors(randomCols)
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
