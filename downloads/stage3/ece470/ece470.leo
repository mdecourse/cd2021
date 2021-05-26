<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2"/>
<globals/>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="leo.20210526093155.1"><vh>@settings</vh>
<v t="leo.20210526093155.2"><vh>@data qt-gui-plugin-style-sheet</vh></v>
<v t="leo.20210526093155.3"><vh>@string initial_split_orientation = horizontal</vh></v>
</v>
<v t="leo.20210526142340.1"><vh>Scripts</vh></v>
<v t="leo.20210526101725.1"><vh>Customization Scripts</vh></v>
<v t="leo.20210526102644.1"><vh>Child Scripts</vh></v>
<v t="leo.20210526095443.1"><vh>@clean ur3.lua</vh>
<v t="leo.20210526095454.1"><vh>sysCall_threadmain (ur3.lua)</vh></v>
</v>
<v t="leo.20210526100006.1"><vh>@clean suctionpad.lua</vh>
<v t="leo.20210526100025.1"><vh>sysCall_init (suctionpad.lua)</vh></v>
<v t="leo.20210526100025.2"><vh>sysCall_cleanup (suctionpad.lua)</vh></v>
<v t="leo.20210526100025.3"><vh>sysCall_sensing (suctionpad.lua)</vh></v>
</v>
<v t="leo.20210526093137.2"><vh>@clean tree.lua</vh>
<v t="leo.20210526093514.1"><vh>sysCall_init (tree.lua)</vh></v>
<v t="leo.20210526093514.2"><vh>sysCall_nonSimulation (tree.lua)</vh></v>
<v t="leo.20210526093514.3"><vh>sysCall_beforeSimulation (tree.lua)</vh></v>
</v>
<v t="leo.20210526100801.1"><vh>@clean bill.lua</vh>
<v t="leo.20210526100811.1"><vh>sysCall_init (bill.lua)</vh></v>
<v t="leo.20210526100811.2"><vh>sysCall_cleanup (bill.lua)</vh></v>
</v>
<v t="leo.20210526093824.1"><vh>@clean building.lua</vh>
<v t="leo.20210526093835.1"><vh>__setObjectPosition__ (building.lua)</vh></v>
<v t="leo.20210526093835.2"><vh>__setObjectOrientation__ (building.lua)</vh></v>
<v t="leo.20210526093835.3"><vh>sysCall_init (building.lua)</vh></v>
<v t="leo.20210526093835.4"><vh>sysCall_nonSimulation (building.lua)</vh></v>
<v t="leo.20210526093835.5"><vh>sysCall_beforeSimulation (building.lua)</vh></v>
</v>
<v t="leo.20210526094112.1"><vh>@clean laserpointer.lua</vh>
<v t="leo.20210526094124.1"><vh>sysCall_init (laserpointer.lua)</vh></v>
<v t="leo.20210526094124.2"><vh>sysCall_cleanup (laserpointer.lua)</vh></v>
<v t="leo.20210526094124.3"><vh>sysCall_sensing (laserpointer.lua)</vh></v>
</v>
<v t="leo.20210526095326.1"><vh>@clean laserpointer4car.lua</vh>
<v t="leo.20210526095341.1"><vh>sysCall_init (laserpointer4car.lua)</vh></v>
<v t="leo.20210526095341.2"><vh>sysCall_cleanup (laserpointer4car.lua)</vh></v>
<v t="leo.20210526095341.3"><vh>sysCall_sensing (laserpointer4car.lua)</vh></v>
</v>
<v t="leo.20210526101155.1"><vh>@clean main.lua</vh>
<v t="leo.20210526101204.1"><vh>sysCall_init (main.lua)</vh></v>
<v t="leo.20210526101204.2"><vh>sysCall_actuation (main.lua)</vh></v>
<v t="leo.20210526101204.3"><vh>sysCall_sensing (main.lua)</vh></v>
<v t="leo.20210526101204.4"><vh>sysCall_cleanup (main.lua)</vh></v>
<v t="leo.20210526101204.5"><vh>sysCall_suspend (main.lua)</vh></v>
<v t="leo.20210526101204.6"><vh>sysCall_suspended (main.lua)</vh></v>
<v t="leo.20210526101204.7"><vh>sysCall_resume (main.lua)</vh></v>
</v>
<v t="leo.20210526101316.1"><vh>@clean concretblock.lua</vh>
<v t="leo.20210526101329.1"><vh>sysCall_init (concretblock.lua)</vh></v>
<v t="leo.20210526101329.2"><vh>sysCall_nonSimulation (concretblock.lua)</vh></v>
<v t="leo.20210526101329.3"><vh>sysCall_beforeSimulation (concretblock.lua)</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="leo.20210526093137.2">@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210526093155.1"></t>
<t tx="leo.20210526093155.2">QTreeWidget {
    /* These apply to the selected item, but not to editing items.*/
    background-color: #ffffec; /* Leo's traditional tree color */
    selection-color: black; /* was white */
    selection-background-color: lightgrey;
    /* font-family: SansSerif; */
    /*font-family: DejaVu Sans Mono;*/
    font-family:YaHei Mono;
    /* 標題字型大小設定 */
    font-size: 30px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal, italic,oblique */
 }

/* Headline edit widgets */
QTreeWidget QLineEdit {
    background-color: cornsilk;
    selection-color: white;
    selection-background-color: blue;
    /*font-family: DejaVu Sans Mono;*/    
    font-family:YaHei Mono;
    /* 沒有特別對應字型大小 */
    font-size: 30px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal, italic,oblique */
}

/* The log panes */
QTextEdit {
    background-color: #f2fdff;
    selection-color: red;
    selection-background-color: blue;
    /* font-family: Courier New; */
    font-family:YaHei Mono;
    /* log font 大小 */
    font-size: 30px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal, italic,oblique */
}

/* The body pane */
QTextEdit#richTextEdit {
    background-color: #fdf5f5; /* A kind of pink. */
    selection-color: white;
    selection-background-color: red;
    /*font-family: DejaVu Sans Mono;*/
    /* font-family: Courier New; */
    font-family:YaHei Mono;
    /* 內文字型大小 */
    font-size: 30px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

QLabel {
    font-family:YaHei Mono;'CherryPy', 'pytz', 'mako', 'beautifulsoup4', 'pymysql', 'peewee'
    /* 下方的 Minibuffer 標題字型大小 */
    font-size: 30px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

/* Editor labels */
QLineEdit#editorLabel {
    background-color: #ffffec;
    font-family:YaHei Mono;
    /* 沒有直接對應字型大小 */
    font-size: 30px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
    border: 2px;
    margin: 2px;
}</t>
<t tx="leo.20210526093155.3">horizontal: body pane to the left
vertical: body pane on the botton</t>
<t tx="leo.20210526093514.1">function sysCall_init()
    
    h=sim.getObjectAssociatedWithScript(sim.handle_self)
    ui=simGetUIHandle('Tree')
    local randomCols=(sim.boolAnd32(simGetUIButtonProperty(ui,6),sim.buttonproperty_isdown)~=0)
    setColors(randomCols)

    local p=simGetUIProperty(ui)
    p=sim.boolOr32(p,sim_ui_property_visible)
    simSetUIProperty(ui,p-sim_ui_property_visible)    
end
</t>
<t tx="leo.20210526093514.2">------------------------------------------------------------------------------ 
-- Following few lines automatically added by V-REP to guarantee compatibility 
-- with V-REP 3.1.3 and earlier: 
colorCorrectionFunction=function(_aShapeHandle_) 
  local version=sim.getInt32Parameter(sim.intparam_program_version) 
  local revision=sim.getInt32Parameter(sim.intparam_program_revision) 
  if (version&lt;30104)and(revision&lt;3) then 
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

</t>
<t tx="leo.20210526093514.3">function sysCall_beforeSimulation()
    local p=simGetUIProperty(ui)
    p=sim.boolOr32(p,sim_ui_property_visible)
    simSetUIProperty(ui,p-sim_ui_property_visible)
end
</t>
<t tx="leo.20210526093824.1">@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210526093835.1">function __setObjectPosition__(a,b,c)
    -- compatibility routine, wrong results could be returned in some situations, in CoppeliaSim &lt;4.0.1
    if b==sim.handle_parent then
        b=sim.getObjectParent(a)
    end
    if (b~=-1) and (sim.getObjectType(b)==sim.object_joint_type) and (sim.getInt32Parameter(sim.intparam_program_version)&gt;=40001) then
        a=a+sim.handleflag_reljointbaseframe
    end
    return sim.setObjectPosition(a,b,c)
end
</t>
<t tx="leo.20210526093835.2">function __setObjectOrientation__(a,b,c)
    -- compatibility routine, wrong results could be returned in some situations, in CoppeliaSim &lt;4.0.1
    if b==sim.handle_parent then
        b=sim.getObjectParent(a)
    end
    if (b~=-1) and (sim.getObjectType(b)==sim.object_joint_type) and (sim.getInt32Parameter(sim.intparam_program_version)&gt;=40001) then
        a=a+sim.handleflag_reljointbaseframe
    end
    return sim.setObjectOrientation(a,b,c)
end
</t>
<t tx="leo.20210526093835.3">function sysCall_init()
    
    h=sim.getObjectAssociatedWithScript(sim.handle_self)
    windowElement=sim.getObjectHandle('building_windowElement')
    windows=sim.getObjectHandle('building_windows')
    body=sim.getObjectHandle('building_body')
    ui=simGetUIHandle('building')

    local p=simGetUIProperty(ui)
    p=sim.boolOr32(p,sim_ui_property_visible)
    simSetUIProperty(ui,p-sim_ui_property_visible)    
end
</t>
<t tx="leo.20210526093835.4">------------------------------------------------------------------------------ 
-- Following few lines automatically added by V-REP to guarantee compatibility 
-- with V-REP 3.1.3 and earlier: 
colorCorrectionFunction=function(_aShapeHandle_) 
    local version=sim.getInt32Parameter(sim.intparam_program_version) 
    local revision=sim.getInt32Parameter(sim.intparam_program_revision) 
    if (version&lt;30104)and(revision&lt;3) then 
        return _aShapeHandle_ 
    end 
    return '@backCompatibility1:'.._aShapeHandle_ 
end 
------------------------------------------------------------------------------ 
 
 
_hueToRgb=function(m1,m2,h)
    if h&lt;0 then 
        h=h+1
    end
    if h&gt;1 then 
        h=h-1
    end
    if 6*h&lt;1 then
        return(m1+(m2-m1)*h*6)
    end
    if 2*h&lt;1 then
        return(m2)
    end
    if 3*h&lt;2 then
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
        if l&lt;=0.5 then
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
            if specialHue&lt;0.1 then
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

</t>
<t tx="leo.20210526093835.5">function sysCall_beforeSimulation()
    local p=simGetUIProperty(ui)
    p=sim.boolOr32(p,sim_ui_property_visible)
    simSetUIProperty(ui,p-sim_ui_property_visible)
end
</t>
<t tx="leo.20210526094112.1">@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210526094124.1">function sysCall_init() 
    modelBase=sim.getObjectHandle('LaserPointer')
    sensor=sim.getObjectHandle('LaserPointer_sensor')
    ui=simGetUIHandle('LaserPointer_UI')
    simSetUIButtonLabel(ui,0,sim.getObjectName(modelBase))
    local color={1,0,0}
    pointContainer=sim.addDrawingObject(sim.drawing_cyclic+sim.drawing_painttag+sim.drawing_points,4,0,-1,1,color)
    lineContainer=sim.addDrawingObject(sim.drawing_cyclic+sim.drawing_painttag+sim.drawing_lines,2,0,-1,1,color)
    communicationTube=sim.tubeOpen(0,'laserPointerData'..sim.getNameSuffix(nil),1)
end
</t>
<t tx="leo.20210526094124.2">-- Check the end of the script for some explanations!
function sysCall_cleanup() 
end 
</t>
<t tx="leo.20210526094124.3">function sysCall_sensing() 
    res,dist,pt=sim.handleProximitySensor(sensor)
    m=sim.getObjectMatrix(sensor,-1)
    pt1=sim.multiplyVector(m,{0,0,0})
    pt2={0,0,100}
    if (res&gt;0) then
        pt2=pt
    end
    pt2=sim.multiplyVector(m,pt2)
    sim.addDrawingObjectItem(lineContainer,nil)
    sim.addDrawingObjectItem(pointContainer,nil)
    if (sim.getScriptSimulationParameter(sim.handle_self,'showLaserRay')) then
        sim.addDrawingObjectItem(lineContainer,{pt1[1],pt1[2],pt1[3],pt2[1],pt2[2],pt2[3]})
    end
    if (res&gt;0) then
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
</t>
<t tx="leo.20210526095326.1">@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210526095341.1">function sysCall_init() 
    modelBase=sim.getObjectHandle('LaserPointer4Car')
    sensor=sim.getObjectHandle('LaserPointer_sensor#0')
    ui=simGetUIHandle('LaserPointer_UI#0')
    simSetUIButtonLabel(ui,0,sim.getObjectName(modelBase))
    local color={0,0,1}
    pointContainer=sim.addDrawingObject(sim.drawing_cyclic+sim.drawing_painttag+sim.drawing_points,4,0,-1,1,color)
    lineContainer=sim.addDrawingObject(sim.drawing_cyclic+sim.drawing_painttag+sim.drawing_lines,2,0,-1,1,color)
    communicationTube=sim.tubeOpen(0,'CarDistanceData'..sim.getNameSuffix(nil),1)
end
</t>
<t tx="leo.20210526095341.2">-- Check the end of the script for some explanations!


function sysCall_cleanup() 
 
end 

</t>
<t tx="leo.20210526095341.3">function sysCall_sensing() 
    res,dist,pt=sim.handleProximitySensor(sensor)
    m=sim.getObjectMatrix(sensor,-1)
    pt1=sim.multiplyVector(m,{0,0,0})
    pt2={0,0,100}
    if (res&gt;0) then
        pt2=pt
    end
    pt2=sim.multiplyVector(m,pt2)
    
    sim.addDrawingObjectItem(lineContainer,nil)
    sim.addDrawingObjectItem(pointContainer,nil)
    
    if (sim.getScriptSimulationParameter(sim.handle_self,'showLaserRay')) then
        sim.addDrawingObjectItem(lineContainer,{pt1[1],pt1[2],pt1[3],pt2[1],pt2[2],pt2[3]})
    end
    
    if (res&gt;0) then
        if (sim.getScriptSimulationParameter(sim.handle_self,'showLaserPoint')) then
            sim.addDrawingObjectItem(pointContainer,pt2)
        end
        simSetUIButtonLabel(ui,2,string.format("Distance: %.4f meters",dist))
        sim.tubeWrite(communicationTube,sim.packFloatTable({dist}))
        sim.setFloatSignal('CarDistanceData',dist)
    else
        simSetUIButtonLabel(ui,2,'Distance: -')
        sim.tubeWrite(communicationTube,sim.packFloatTable({-1}))
        sim.setFloatSignal('CarDistanceData',99)
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
</t>
<t tx="leo.20210526095443.1">@language lua
@tabwidth -4

@others
</t>
<t tx="leo.20210526095454.1">function sysCall_threadmain()
    jointHandles={-1,-1,-1,-1,-1,-1}
    
    gripperHandle= sim.getObjectHandle('suctionPad')
    scriptHandle = sim.getScriptAssociatedWithObject(gripperHandle)
    
    for i=1,6,1 do
        jointHandles[i]=sim.getObjectHandle('UR3_joint'..i)
    end
    -- Set-up some of the RML vectors:
    vel=180
    accel=40
    jerk=80
    currentVel={0,0,0,0,0,0,0}
    currentAccel={0,0,0,0,0,0,0}
    deg = math.pi/180
    maxVel={vel*deg,vel*deg,vel*deg,vel*deg,vel*deg,vel*deg}
    maxAccel={accel*deg,accel*deg,accel*deg,accel*deg,accel*deg,accel*deg}
    maxJerk={jerk*deg,jerk*deg,jerk*deg,jerk*deg,jerk*deg,jerk*deg}
    targetVel={0,0,0,0,0,0}
    targetPos1={0,60*deg,30*deg,0,-90*deg,0}
    targetPos2={0,0,0,0,0,0}
    targetPos3={-90*deg,60*deg,30*deg,0,-90*deg,0}
    targetPos4={0,92*deg,0,0,-90*deg,0}
    targetPos5={180*deg,90*deg,0,0,-90*deg,0*deg}
    dist = 99
    while dist &gt; 0.5 do
        dist = sim.getFloatSignal("CarDistanceData")
    end
    sim.rmlMoveToJointPositions(jointHandles,-1,currentVel,currentAccel,maxVel,maxAccel,maxJerk,targetPos1,targetVel)
    sim.rmlMoveToJointPositions(jointHandles,-1,currentVel,currentAccel,maxVel,maxAccel,maxJerk,targetPos2,targetVel)
    sim.rmlMoveToJointPositions(jointHandles,-1,currentVel,currentAccel,maxVel,maxAccel,maxJerk,targetPos3,targetVel)
    
    sim.setScriptSimulationParameter(scriptHandle, 'active', 'false')
    
    sim.rmlMoveToJointPositions(jointHandles,-1,currentVel,currentAccel,maxVel,maxAccel,maxJerk,targetPos2,targetVel)
    
    sim.setScriptSimulationParameter(scriptHandle, 'active', 'true')
    --sim.rmlMoveToJointPositions(jointHandles,-1,currentVel,currentAccel,maxVel,maxAccel,maxJerk,targetPos1,targetVel)
    sim.rmlMoveToJointPositions(jointHandles,-1,currentVel,currentAccel,maxVel,maxAccel,maxJerk,targetPos4,targetVel)
    sim.rmlMoveToJointPositions(jointHandles,-1,currentVel,currentAccel,maxVel,maxAccel,maxJerk,targetPos2,targetVel)
    sim.rmlMoveToJointPositions(jointHandles,-1,currentVel,currentAccel,maxVel,maxAccel,maxJerk,targetPos5,targetVel)
    sim.setScriptSimulationParameter(scriptHandle, 'active', 'false')
    sim.rmlMoveToJointPositions(jointHandles,-1,currentVel,currentAccel,maxVel,maxAccel,maxJerk,targetPos2,targetVel)
end
</t>
<t tx="leo.20210526100006.1">@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210526100025.1">function sysCall_init() 
    s=sim.getObjectHandle('suctionPadSensor')
    
    l=sim.getObjectHandle('suctionPadLoopClosureDummy1')
    l2=sim.getObjectHandle('suctionPadLoopClosureDummy2')
    
    b=sim.getObjectHandle('suctionPad')
    suctionPadLink=sim.getObjectHandle('suctionPadLink')

    infiniteStrength=sim.getScriptSimulationParameter(sim.handle_self,'infiniteStrength')
    maxPullForce=sim.getScriptSimulationParameter(sim.handle_self,'maxPullForce')
    maxShearForce=sim.getScriptSimulationParameter(sim.handle_self,'maxShearForce')
    maxPeelTorque=sim.getScriptSimulationParameter(sim.handle_self,'maxPeelTorque')
    -- set l to -1 to unlink the dummy-dummy link pair
    --[[
    https://www.coppeliarobotics.com/helpFiles/en/dummies.htm
     they are also used in pairs to specify loop closures or tip-target relationships for dynamics or kinematics calculations
    ]]--
    sim.setLinkDummy(l,-1)
    -- https://www.coppeliarobotics.com/helpFiles/en/regularApi/simSetObjectParent.htm
    sim.setObjectParent(l,b,true)
    -- https://www.coppeliarobotics.com/helpFiles/en/regularApi/simGetObjectMatrix.htm
    m=sim.getObjectMatrix(l2,-1)
    sim.setObjectMatrix(l,-1,m)
end

</t>
<t tx="leo.20210526100025.2">function sysCall_cleanup() 
    sim.setLinkDummy(l,-1)
    sim.setObjectParent(l,b,true)
    m=sim.getObjectMatrix(l2,-1)
    sim.setObjectMatrix(l,-1,m)
end 

</t>
<t tx="leo.20210526100025.3">function sysCall_sensing() 
    parent=sim.getObjectParent(l)
    if (sim.getScriptSimulationParameter(sim.handle_self,'active')==false) then
        if (parent~=b) then
            sim.setLinkDummy(l,-1)
            sim.setObjectParent(l,b,true)
            m=sim.getObjectMatrix(l2,-1)
            sim.setObjectMatrix(l,-1,m)
        end
    else
        if (parent==b) then
            -- Here we want to detect a respondable shape, and then connect to it with a force sensor (via a loop closure dummy dummy link)
            -- However most respondable shapes are set to "non-detectable", so "sim.readProximitySensor" or similar will not work.
            -- But "sim.checkProximitySensor" or similar will work (they don't check the "detectable" flags), but we have to go through all shape objects!
            index=0
            while true do
                shape=sim.getObjects(index,sim.object_shape_type)
                if (shape==-1) then
                    break
                end
                if (shape~=b) and (sim.getObjectInt32Parameter(shape,sim.shapeintparam_respondable)~=0) and (sim.checkProximitySensor(s,shape)==1) then
                    -- Ok, we found a respondable shape that was detected
                    -- We connect to that shape:
                    -- Make sure the two dummies are initially coincident:
                    sim.setObjectParent(l,b,true)
                    m=sim.getObjectMatrix(l2,-1)
                    sim.setObjectMatrix(l,-1,m)
                    -- Do the connection:
                    sim.setObjectParent(l,shape,true)
                    sim.setLinkDummy(l,l2)
                    break
                end
                index=index+1
            end
        else
            -- Here we have an object attached
            if (infiniteStrength==false) then
                -- We might have to conditionally beak it apart!
                -- https://www.coppeliarobotics.com/helpFiles/en/forceSensors.htm
                --[[
                A force sensor is only operational during simulation if it is dynamically enabled. 
                ]]--
                result,force,torque=sim.readForceSensor(suctionPadLink) -- Here we read the median value out of 5 values (check the force sensor prop. dialog)
                if (result&gt;0) then
                    breakIt=false
                    if (force[3]&gt;maxPullForce) then breakIt=true end
                    sf=math.sqrt(force[1]*force[1]+force[2]*force[2])
                    if (sf&gt;maxShearForce) then breakIt=true end
                    if (torque[1]&gt;maxPeelTorque) then breakIt=true end
                    if (torque[2]&gt;maxPeelTorque) then breakIt=true end
                    if (breakIt) then
                        -- We break the link:
                        sim.setLinkDummy(l,-1)
                        sim.setObjectParent(l,b,true)
                        m=sim.getObjectMatrix(l2,-1)
                        sim.setObjectMatrix(l,-1,m)
                    end
                end
            end
        end
    end
end 
</t>
<t tx="leo.20210526100801.1">@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210526100811.1">function sysCall_init() 
    modelHandle=sim.getObjectAssociatedWithScript(sim.handle_self)
    randomColors=sim.getScriptSimulationParameter(sim.handle_self,'randomColors')
    HairColors={4,{0.30,0.22,0.14},{0.75,0.75,0.75},{0.075,0.075,0.075},{0.75,0.68,0.23}}
    skinColors={2,{0.61,0.54,0.45},{0.52,0.45,0.35}}
    shirtColors={5,{0.27,0.36,0.54},{0.54,0.27,0.27},{0.31,0.51,0.33},{0.46,0.46,0.46},{0.18,0.18,0.18}}
    trouserColors={2,{0.4,0.34,0.2},{0.12,0.12,0.12}}
    shoeColors={2,{0.12,0.12,0.12},{0.25,0.12,0.045}}
    -- Initialize to random colors if desired:
    if (randomColors) then
        -- First we just retrieve all objects in the model:
        previousSelection=sim.getObjectSelection()
        sim.removeObjectFromSelection(sim.handle_all,-1)
        sim.addObjectToSelection(sim.handle_tree,modelHandle)
        modelObjects=sim.getObjectSelection()
        sim.removeObjectFromSelection(sim.handle_all,-1)
        sim.addObjectToSelection(previousSelection)
        -- Now we set random colors:
        math.randomseed(sim.getFloatParameter(sim.floatparam_rand)*10000) -- each lua instance should start with a different and 'good' seed
        setColor(modelObjects,'HAIR',HairColors[1+math.random(HairColors[1])])
        setColor(modelObjects,'SKIN',skinColors[1+math.random(skinColors[1])])
        setColor(modelObjects,'SHIRT',shirtColors[1+math.random(shirtColors[1])])
        setColor(modelObjects,'TROUSERS',trouserColors[1+math.random(trouserColors[1])])
        setColor(modelObjects,'SHOE',shoeColors[1+math.random(shoeColors[1])])
    end
end
</t>
<t tx="leo.20210526100811.2">------------------------------------------------------------------------------ 
-- Following few lines automatically added by V-REP to guarantee compatibility 
-- with V-REP 3.1.3 and earlier: 
colorCorrectionFunction=function(_aShapeHandle_) 
  local version=sim.getInt32Parameter(sim.intparam_program_version) 
  local revision=sim.getInt32Parameter(sim.intparam_program_revision) 
  if (version&lt;30104)and(revision&lt;3) then 
      return _aShapeHandle_ 
  end 
  return '@backCompatibility1:'.._aShapeHandle_ 
end 
------------------------------------------------------------------------------ 
 
 
setColor=function(objectTable,colorName,color)
    for i=1,#objectTable,1 do
        if (sim.getObjectType(objectTable[i])==sim.object_shape_type) then
            sim.setShapeColor(colorCorrectionFunction(objectTable[i]),colorName,0,color)
        end
    end
end


function sysCall_cleanup() 
    -- Restore to initial colors:
    if (randomColors) then
        previousSelection=sim.getObjectSelection()
        sim.removeObjectFromSelection(sim.handle_all,-1)
        sim.addObjectToSelection(sim.handle_tree,modelHandle)
        modelObjects=sim.getObjectSelection()
        sim.removeObjectFromSelection(sim.handle_all,-1)
        sim.addObjectToSelection(previousSelection)
        setColor(modelObjects,'HAIR',HairColors[2])
        setColor(modelObjects,'SKIN',skinColors[2])
        setColor(modelObjects,'SHIRT',shirtColors[2])
        setColor(modelObjects,'TROUSERS',trouserColors[2])
        setColor(modelObjects,'SHOE',shoeColors[2])
    end
end 
</t>
<t tx="leo.20210526101155.1">-- This is the main script. The main script is not supposed to be modified,
-- unless there is a very good reason to do it.
-- Without main script,
-- there is no real simulation (child scripts are not called either in that case).
-- A main script marked as "default" (this is the default case) will use the
-- content of following file: system/dltmscpt.txt. This allows your old simulation
-- scenes to be automatically also using newer features, without explicitely coding
-- them. If you modify the main script, it will be marked as "customized", and you
-- won't benefit of that automatic forward compatibility mechanism. 

@others
-- By default threaded child scripts switch back to the main thread after 2 ms. The main
-- thread switches back to a threaded child script at one of above's "sim.resumeThreads"
-- location

-- You can define additional system calls here:
--[[
function sysCall_beforeCopy(inData)
    for key,value in pairs(inData.objectHandles) do
        print("Object with handle "..key.." will be copied")
    end
end

function sysCall_afterCopy(inData)
    for key,value in pairs(inData.objectHandles) do
        print("Object with handle "..key.." was copied")
    end
end

function sysCall_beforeDelete(inData)
    for key,value in pairs(inData.objectHandles) do
        print("Object with handle "..key.." will be deleted")
    end
    -- inData.allObjects indicates if all objects in the scene will be deleted
end

function sysCall_afterDelete(inData)
    for key,value in pairs(inData.objectHandles) do
        print("Object with handle "..key.." was deleted")
    end
    -- inData.allObjects indicates if all objects in the scene were deleted
end
--]]
@language lua
@tabwidth -4
</t>
<t tx="leo.20210526101204.1">function sysCall_init()
    sim.handleSimulationStart()
    sim.openModule(sim.handle_all)
    sim.handleGraph(sim.handle_all_except_explicit,0)
end

</t>
<t tx="leo.20210526101204.2">function sysCall_actuation()
    sim.resumeThreads(sim.scriptthreadresume_default)
    sim.resumeThreads(sim.scriptthreadresume_actuation_first)
    sim.launchThreadedChildScripts()
    sim.handleChildScripts(sim.syscb_actuation)
    sim.resumeThreads(sim.scriptthreadresume_actuation_last)
    sim.handleCustomizationScripts(sim.syscb_actuation)
    sim.handleAddOnScripts(sim.syscb_actuation)
    sim.handleSandboxScript(sim.syscb_actuation)
    sim.handleModule(sim.handle_all,false)
    simHandleJoint(sim.handle_all_except_explicit,sim.getSimulationTimeStep()) -- DEPRECATED
    simHandlePath(sim.handle_all_except_explicit,sim.getSimulationTimeStep()) -- DEPRECATED
    sim.handleMechanism(sim.handle_all_except_explicit)
    sim.handleIkGroup(sim.handle_all_except_explicit)
    sim.handleDynamics(sim.getSimulationTimeStep())
    sim.handleMill(sim.handle_all_except_explicit)
end

</t>
<t tx="leo.20210526101204.3">function sysCall_sensing()
    -- put your sensing code here
    sim.handleSensingStart()
    sim.handleCollision(sim.handle_all_except_explicit)
    sim.handleDistance(sim.handle_all_except_explicit)
    sim.handleProximitySensor(sim.handle_all_except_explicit)
    sim.handleVisionSensor(sim.handle_all_except_explicit)
    sim.resumeThreads(sim.scriptthreadresume_sensing_first)
    sim.handleChildScripts(sim.syscb_sensing)
    sim.resumeThreads(sim.scriptthreadresume_sensing_last)
    sim.handleCustomizationScripts(sim.syscb_sensing)
    sim.handleAddOnScripts(sim.syscb_sensing)
    sim.handleSandboxScript(sim.syscb_sensing)
    sim.handleModule(sim.handle_all,true)
    sim.resumeThreads(sim.scriptthreadresume_allnotyetresumed)
    sim.handleGraph(sim.handle_all_except_explicit,sim.getSimulationTime()+sim.getSimulationTimeStep())
end

</t>
<t tx="leo.20210526101204.4">function sysCall_cleanup()
    sim.resetMilling(sim.handle_all)
    sim.resetMill(sim.handle_all_except_explicit)
    sim.resetCollision(sim.handle_all_except_explicit)
    sim.resetDistance(sim.handle_all_except_explicit)
    sim.resetProximitySensor(sim.handle_all_except_explicit)
    sim.resetVisionSensor(sim.handle_all_except_explicit)
    sim.closeModule(sim.handle_all)
end

</t>
<t tx="leo.20210526101204.5">function sysCall_suspend()
    sim.handleChildScripts(sim.syscb_suspend)
    sim.handleCustomizationScripts(sim.syscb_suspend)
    sim.handleAddOnScripts(sim.syscb_suspend)
    sim.handleSandboxScript(sim.syscb_suspend)
end

</t>
<t tx="leo.20210526101204.6">function sysCall_suspended()
    sim.handleCustomizationScripts(sim.syscb_suspended)
    sim.handleAddOnScripts(sim.syscb_suspended)
    sim.handleSandboxScript(sim.syscb_suspended)
end

</t>
<t tx="leo.20210526101204.7">function sysCall_resume()
    sim.handleChildScripts(sim.syscb_resume)
    sim.handleCustomizationScripts(sim.syscb_resume)
    sim.handleAddOnScripts(sim.syscb_resume)
    sim.handleSandboxScript(sim.syscb_resume)
end

</t>
<t tx="leo.20210526101316.1">@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210526101329.1">function sysCall_init()
    
    h=sim.getObjectAssociatedWithScript(sim.handle_self)
    ui=simGetUIHandle('ConcretBlock')

    local p=simGetUIProperty(ui)
    p=sim.boolOr32(p,sim_ui_property_visible)
    simSetUIProperty(ui,p-sim_ui_property_visible)    
end

</t>
<t tx="leo.20210526101329.2">function sysCall_nonSimulation()
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

</t>
<t tx="leo.20210526101329.3">function sysCall_beforeSimulation()
    local p=simGetUIProperty(ui)
    p=sim.boolOr32(p,sim_ui_property_visible)
    simSetUIProperty(ui,p-sim_ui_property_visible)
end
</t>
<t tx="leo.20210526101725.1">https://www.coppeliarobotics.com/helpFiles/en/customizationScripts.htm

Customization scripts

Customization scripts are embedded scripts that can be used to customize a simulation scene to a great extent. They are attached to (or associated with) scene objects, and they can be easily recognized from their dark script icon in the scene hierarchy:

Double-clicking the script icon allows opening the script editor. You can change properties of a given script, or associate it with another object via the script dialog. You can attach a new customization script to an object by selecting the object, then navigating to [menu bar --&gt; Add --&gt; Associated customization script].

Following are customization script's main properties:

they are executed all the time (within a same scene): when simulation is running, as well as when simulation is not running.
they are attached to (or associated with) scene objects (i.e. they are associated scripts). Associated scripts form the basis of CoppeliaSim's distributed control architecture, and share the convenient property to be automatically duplicated if their associated object is duplicated.

Above properties allow customization scripts to share some of the best features of add-ons and child scripts. Customization scripts allow the creation of customizable models for instance: imagine a model that was dropped into a scene, and that is able to configure or adapt itself, even when simulation is not running. This could be a robot where the user can adjust the various link lengths with a single slider repositioning.

Customization scripts should contain a collection of callback functions. Those should not be blocking. This means that every time they are called, they should perform some task and then return control. If control is not returned, then the whole application halts. Customization script functions are called by the system often, but also by the main script, and follow a precise execution order in relation with other script types.

A customization script can run threaded or non-threaded, and should be segmented in several system callback functions. If possible, do not use customization scripts to run simulation code, which is anyway best handled via child scripts.


</t>
<t tx="leo.20210526102644.1">https://www.coppeliarobotics.com/helpFiles/en/childScripts.htm

Child scripts

A child script is a simulation script. CoppeliaSim supports an unlimited number of child scripts per scene. Each child script represents a small collection of routines written in Lua allowing handling a particular function in a simulation. Child scripts are attached to (or associated with) scene objects, and they can be easily recognized from their script icon in the scene hierarchy:


Double-clicking the script icon allows opening the script editor. You can change properties of a given script, or associate it with another object via the script dialog. You can attach a new child script to an object by selecting the object, then navigating to [menu bar --&gt; Add --&gt; Associated child script].

A child script's association with a scene object has important and positive consequences:

Very good portability: child scripts will be saved/loaded together with their associated object. Using child scripts, you are able to create extremely portable code and simulation models that do not need to rely on any system specific plugin. A fully functional model can be contained in a single file (usable without modification across various platforms), which is not the case when relying on plugins for model control. Additionally, and for the same reason, models relying on child scripts require no maintenance over time (e.g. a new OS version will not require you to adjust portions of code or recompilation, as you might have to do when using plugins).

Inherent scalability: if an object that has an attached child script is duplicated, its child script will also be duplicated. The duplicated child script's content will be identical to the original child script's content, however, the duplicated child script will know that is was duplicated and redirect object access correctly (e.g. if the original child script is accessing robot, then the duplicated child script will automatically append a name index to robot in order to access the duplicated robot and not the original one). Refer to the section on accessing general-type objects programmatically for more details. The automatic name index adjustment allows duplicating objects and behavior without having to rewrite / adjust any code.

No conflict between different model versions: if you modify the child script of a given model (e.g. to customize it to your needs), this will have no consequence on other similar models. This is a much more critical aspect when relying on plugins instead of child scripts for model control: indeed, with plugins you always run the risk of having conflicts with previous plugin versions.

Very easy synchronization with the simulation loop: child scripts can run threaded or non-threaded, and can be easily synchronized with the simulation loop, which represents a powerful feature.

Child scripts can run threaded or non-threaded code. Since they only run when simulation is running, they should exclusively be used to handle simulation-time tasks.

As do other script types, child scripts should mainly contain a collection of functions. The entrance functions are callback functions. Functions that are not running threaded (i.e. that are not running in a coroutine) should not be blocking. This means that every time they are called, they should perform some task and then return control. If control is not returned, then the whole simulation halts. Child script functions are called by the main script at least twice per simulation step from the main script's actuation and sensing functions. The system will also call other system callback functions where appropriate (e.g. during child script initialization, clean-up, etc).

Child scripts also follow a precise calling or execution order: by default, child scripts are called starting with leaf objects (or childless objects), and ending with root objects (or parentless objects). A child script is typically segmented into a collection of system callback functions, the most important ones are:

the initialization function: sysCall_init. This system callback function is the only one that is not optional. It will be executed just one time (the first time the child script is called). This can be at the beginning of a simulation, but also in the middle of a simulation: remember that objects associated with child scripts can be copy/pasted into a scene at any time, also when a simulation is running. Usually you would put some initialization code as well as handle retrieval in this part. Or, if your code is meant to run threaded, then you would prepare one or several coroutines in that part.

the actuation function: sysCall_actuation. This part will be executed in each simulation step, during the actuation phase of a simulation step. Refer to the main script default code for more details about the actuation phase, but typically, you would do some actuation in this part (no sensing). Or, if an actuation function is meant to run threaded, then you would resume the coroutine of that function in that part.

the sensing function: sysCall_sensing. This part will be executed in each simulation step, during the sensing phase of a simulation step. Refer to the main script default code for more details about the sensing phase, but typically, you would only do sensing in this part (no actuation). Or, if a sensing function is meant to run threaded, then you would resume the coroutine of that function in that part.

the restoration function: sysCall_cleanup. This part will be executed one time just before a simulation ends, or before the script is destroyed.


</t>
<t tx="leo.20210526142340.1">https://www.coppeliarobotics.com/helpFiles/en/scripts.htm</t>
</tnodes>
</leo_file>
