<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2"/>
<globals/>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="leo.20210522214552.1"><vh>@settings</vh>
<v t="leo.20210522214552.2"><vh>@data qt-gui-plugin-style-sheet</vh></v>
<v t="leo.20210522214552.3"><vh>@string initial_split_orientation = horizontal</vh></v>
</v>
<v t="leo.20210522214903.1"><vh>recursive importer</vh></v>
<v t="leo.20210522215527.1"><vh>imported files</vh>
<v t="leo.20210522215527.2"><vh>@path ./</vh>
<v t="leo.20210522215527.5"><vh>@clean base.lua</vh>
<v t="leo.20210522215527.6"><vh>signal_on (base.lua)</vh></v>
<v t="leo.20210522215527.7"><vh>signal_1 (base.lua)</vh></v>
<v t="leo.20210522215527.8"><vh>signal_2 (base.lua)</vh></v>
<v t="leo.20210522215527.9"><vh>signal_3 (base.lua)</vh></v>
<v t="leo.20210522215527.10"><vh>signal_4 (base.lua)</vh></v>
<v t="leo.20210522215527.11"><vh>signal_5 (base.lua)</vh></v>
<v t="leo.20210522215527.12"><vh>signal_6 (base.lua)</vh></v>
<v t="leo.20210522215527.13"><vh>sysCall_threadmain (base.lua)</vh></v>
<v t="leo.20210522215527.14"><vh>sysCall_cleanup (base.lua)</vh></v>
</v>
<v t="leo.20210522215527.15"><vh>@clean rotate.lua</vh>
<v t="leo.20210522215527.16"><vh>sysCall_init (rotate.lua)</vh></v>
<v t="leo.20210522215527.17"><vh>sysCall_actuation (rotate.lua)</vh></v>
<v t="leo.20210522215527.18"><vh>sysCall_sensing (rotate.lua)</vh></v>
<v t="leo.20210522215527.19"><vh>sysCall_cleanup (rotate.lua)</vh></v>
</v>
<v t="leo.20210522215527.20"><vh>@clean suctionpad.lua</vh>
<v t="leo.20210522215527.21"><vh>sysCall_init (suctionpad.lua)</vh></v>
<v t="leo.20210522215527.22"><vh>sysCall_cleanup (suctionpad.lua)</vh></v>
<v t="leo.20210522215527.23"><vh>sysCall_sensing (suctionpad.lua)</vh></v>
</v>
<v t="leo.20210522215527.24"><vh>@clean suctionpad0.lua</vh>
<v t="leo.20210522215527.25"><vh>sysCall_init (suctionpad0.lua)</vh></v>
<v t="leo.20210522215527.26"><vh>sysCall_cleanup (suctionpad0.lua)</vh></v>
<v t="leo.20210522215527.27"><vh>sysCall_sensing (suctionpad0.lua)</vh></v>
</v>
<v t="leo.20210522215527.28"><vh>@clean suctionpad1.lua</vh>
<v t="leo.20210522215527.29"><vh>sysCall_init (suctionpad1.lua)</vh></v>
<v t="leo.20210522215527.30"><vh>sysCall_cleanup (suctionpad1.lua)</vh></v>
<v t="leo.20210522215527.31"><vh>sysCall_sensing (suctionpad1.lua)</vh></v>
</v>
<v t="leo.20210522215527.32"><vh>@clean suctionpad2.lua</vh>
<v t="leo.20210522215527.33"><vh>sysCall_init (suctionpad2.lua)</vh></v>
<v t="leo.20210522215527.34"><vh>sysCall_cleanup (suctionpad2.lua)</vh></v>
<v t="leo.20210522215527.35"><vh>sysCall_sensing (suctionpad2.lua)</vh></v>
</v>
<v t="leo.20210522215527.36"><vh>@clean suctionpad3.lua</vh>
<v t="leo.20210522215527.37"><vh>sysCall_init (suctionpad3.lua)</vh></v>
<v t="leo.20210522215527.38"><vh>sysCall_cleanup (suctionpad3.lua)</vh></v>
<v t="leo.20210522215527.39"><vh>sysCall_sensing (suctionpad3.lua)</vh></v>
</v>
<v t="leo.20210522215527.40"><vh>@clean suctionpad4.lua</vh>
<v t="leo.20210522215527.41"><vh>sysCall_init (suctionpad4.lua)</vh></v>
<v t="leo.20210522215527.42"><vh>sysCall_cleanup (suctionpad4.lua)</vh></v>
<v t="leo.20210522215527.43"><vh>sysCall_sensing (suctionpad4.lua)</vh></v>
</v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="leo.20210522214552.1"></t>
<t tx="leo.20210522214552.2">QTreeWidget {
    /* These apply to the selected item, but not to editing items.*/
    background-color: #ffffec; /* Leo's traditional tree color */
    selection-color: black; /* was white */
    selection-background-color: lightgrey;
    /* font-family: SansSerif; */
    /*font-family: DejaVu Sans Mono;*/
    font-family:YaHei Mono;
    /* 標題字型大小設定 */
    font-size: 20px;
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
    font-size: 20px;
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
    font-size: 20px;
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
    font-size: 20px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

QLabel {
    font-family:YaHei Mono;'CherryPy', 'pytz', 'mako', 'beautifulsoup4', 'pymysql', 'peewee'
    /* 下方的 Minibuffer 標題字型大小 */
    font-size: 20px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

/* Editor labels */
QLineEdit#editorLabel {
    background-color: #ffffec;
    font-family:YaHei Mono;
    /* 沒有直接對應字型大小 */
    font-size: 20px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
    border: 2px;
    margin: 2px;
}</t>
<t tx="leo.20210522214552.3">horizontal: body pane to the left
vertical: body pane on the botton</t>
<t tx="leo.20210522214903.1">'''Recursively import all python files in a directory and clean the result.'''
# ctrl + b to execute

c.recursiveImport(
    dir_ = r'./',
    kind = '@clean', # The new best practice.
    safe_at_file = False,
    theTypes = ['.lua'] 
)</t>
<t tx="leo.20210522215527.1"></t>
<t tx="leo.20210522215527.10">function signal_4(enable)
    modelBase4=sim.getObjectHandle(sim.handle_self)
    modelName4=sim.getObjectName(modelBase4)
    if enable then
        sim.setIntegerSignal(modelName4 .."call_4",1)
    else
        sim.setIntegerSignal(modelName4 .."call_4",0)
    end
end

</t>
<t tx="leo.20210522215527.11">function signal_5(enable)
    modelBase5=sim.getObjectHandle(sim.handle_self)
    modelName5=sim.getObjectName(modelBase5)
    if enable then
        sim.setIntegerSignal(modelName5 .."call_5",1)
    else
        sim.setIntegerSignal(modelName5 .."call_5",0)
    end
end

</t>
<t tx="leo.20210522215527.12">function signal_6(enable)


    modelBase6=sim.getObjectHandle(sim.handle_self)
    modelName6=sim.getObjectName(modelBase6)
    if enable then
        sim.setIntegerSignal(modelName6 .."call_6",1)
    else
        sim.setIntegerSignal(modelName6 .."call_6",0)
    end
end


</t>
<t tx="leo.20210522215527.13">function sysCall_threadmain()
    on=true
    joint01=sim.getObjectHandle('X')
    joint02=sim.getObjectHandle('Y')
    joint03=sim.getObjectHandle('Z')
    jointr=sim.getObjectHandle('Rotate')
    tt=1.2
    long_t=1.7
    long_long_t=3.2
    aty=0
    setx=0.5
    setpx=-0.5
    sety=-0.16
    setpy=-0.16
    pick_h1=0.0645
    pick_h2=0.134
    pick_h3=0.2025
    pick_h4=0.2768
    fall_h4=0.26
    fall_h3=0.18
    fall_h2=0.12
    fall_h1=0.05
    fall_h4_up=0.12
    fall_h3_up=0.05
    while (on==true) do
        signal_1(true)
        sim.setJointTargetPosition(joint01,setx) --pick_1
        sim.setJointTargetPosition(joint02,sety)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h1)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,60*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx+0.05) --pick_2 h2-h2-
        sim.setJointTargetPosition(joint02,sety-0.05)
        sim.wait(tt)
        signal_2(true)
        sim.setJointTargetPosition(joint03,aty-pick_h2)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,120*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx+0.05) --pick_3
        sim.setJointTargetPosition(joint02,sety+0.05)
        sim.wait(tt)
        signal_3(true)
        sim.setJointTargetPosition(joint03,aty-pick_h2)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,180*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx-0.05) --pick_4
        sim.setJointTargetPosition(joint02,sety+0.05)
        sim.wait(tt)
        signal_4(true)
        sim.setJointTargetPosition(joint03,aty-pick_h2)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,240*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx-0.05) --pick_5
        sim.setJointTargetPosition(joint02,sety-0.05)
        sim.wait(tt)
        signal_5(true)
        sim.setJointTargetPosition(joint03,aty-pick_h2)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,300*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx+0.1) --pick_6 h3-h3
        sim.setJointTargetPosition(joint02,sety+0.1)
        sim.wait(tt)
        signal_6(true)
        sim.setJointTargetPosition(joint03,aty-pick_h3)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,0)
        sim.wait(long_t)
        -----------------------------------------------------------
        sim.setJointTargetPosition(joint01,setpx-0.15)--fall 1
        sim.wait(long_long_t)
        sim.setJointTargetPosition(joint02,setpy+0.15)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_1(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,60*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx-0.15)--fall 2
        sim.setJointTargetPosition(joint02,setpy+0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_2(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,120*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx-0.15)--fall 3
        sim.setJointTargetPosition(joint02,setpy-0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_3(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,180*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx-0.15)--fall 4
        sim.setJointTargetPosition(joint02,setpy-0.15)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_4(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,240*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx-0.05)--fall 5
        sim.setJointTargetPosition(joint02,setpy-0.15)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_5(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,300*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx-0.05)--fall 6
        sim.setJointTargetPosition(joint02,setpy-0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_6(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx) 
        sim.setJointTargetPosition(joint02,sety)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,0)
        -----------------------------------------------------------
        sim.setJointTargetPosition(joint01,setx+0.1) --pick_7
        sim.setJointTargetPosition(joint02,sety)
        signal_1(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h3)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,60*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx+0.1) --pick_8
        sim.setJointTargetPosition(joint02,sety-0.1)
        signal_2(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h3)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,120*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx) --pick_9
        sim.setJointTargetPosition(joint02,sety-0.1)
        signal_3(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h3)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,180*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx) --pick_10
        sim.setJointTargetPosition(joint02,sety)
        signal_4(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h3)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,240*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx) --pick_11
        sim.setJointTargetPosition(joint02,sety+0.1)
        signal_5(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h3)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,300*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx-0.1) --pick_12
        sim.setJointTargetPosition(joint02,sety+0.1)
        signal_6(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h3)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,0)
        sim.wait(long_t)
         -----------------------------------------------------------
        sim.setJointTargetPosition(joint01,setpx-0.05)--fall 7
        sim.wait(tt)
        sim.setJointTargetPosition(joint02,setpy+0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_1(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,60*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx-0.05)--fall 8
        sim.setJointTargetPosition(joint02,setpy+0.15)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_2(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-0.12)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,120*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx+0.05)--fall 9
        sim.setJointTargetPosition(joint02,setpy+0.15)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_3(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,180*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx+0.05)--fall 10
        sim.setJointTargetPosition(joint02,setpy+0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_4(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,240*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx+0.05)--fall 11
        sim.setJointTargetPosition(joint02,setpy-0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_5(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,300*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx+0.05)--fall 12
        sim.setJointTargetPosition(joint02,setpy-0.15)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_6(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx) 
        sim.setJointTargetPosition(joint02,sety)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,0)
        -----------------------------------------------------------
        sim.setJointTargetPosition(joint01,setx-0.1) --pick_13
        sim.setJointTargetPosition(joint02,sety)
        signal_1(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h3)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,60*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx-0.1) --pick_14 
        sim.setJointTargetPosition(joint02,sety-0.1)
        signal_2(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h3)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,120*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx-0.15) --pick_15 --h4-h4
        sim.setJointTargetPosition(joint02,sety+0.15)
        signal_3(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,180*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx-0.15) --pick_16
        sim.setJointTargetPosition(joint02,sety+0.05)
        signal_4(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,240*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx-0.15) --pick_17
        sim.setJointTargetPosition(joint02,sety-0.05)
        signal_5(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,300*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx-0.15) --pick_18
        sim.setJointTargetPosition(joint02,sety-0.15)
        signal_6(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,0)
        sim.wait(tt)
        sim.wait(long_t)
         -----------------------------------------------------------
        sim.setJointTargetPosition(joint01,setpx+0.15)--fall 13
        sim.wait(tt)
        sim.setJointTargetPosition(joint02,setpy-0.15)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_1(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,60*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx+0.15)--fall 14
        sim.setJointTargetPosition(joint02,setpy-0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_2(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,120*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx+0.15)--fall 15
        sim.setJointTargetPosition(joint02,setpy+0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_3(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,180*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx+0.15)--fall 16
        sim.setJointTargetPosition(joint02,setpy+0.15)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_4(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,240*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx+0.1)--fall 17 h3--h3
        sim.setJointTargetPosition(joint02,setpy-0.1)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3)
        sim.wait(tt)
        signal_5(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,300*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx+0.1)--fall 18
        sim.setJointTargetPosition(joint02,setpy-0)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3)
        sim.wait(tt)
        signal_6(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx) 
        sim.setJointTargetPosition(joint02,sety)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,0)
        sim.wait(tt)
        -----------------------------------------------------------
        sim.setJointTargetPosition(joint01,setx-0.05) --pick_19
        sim.setJointTargetPosition(joint02,sety-0.15)
        signal_1(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,60*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx-0.05) --pick_20 
        sim.setJointTargetPosition(joint02,sety-0.05)
        signal_2(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,120*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx-0.05) --pick_21
        sim.setJointTargetPosition(joint02,sety+0.05)
        signal_3(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,180*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx-0.05) --pick_22
        sim.setJointTargetPosition(joint02,sety+0.15)
        signal_4(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,240*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx+0.05) --pick_23
        sim.setJointTargetPosition(joint02,sety+0.15)
        signal_5(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,300*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx+0.05) --pick_24
        sim.setJointTargetPosition(joint02,sety+0.05)
        signal_6(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,0*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,0*math.pi/180)
        sim.wait(long_t)
         -----------------------------------------------------------
        sim.setJointTargetPosition(joint01,setpx+0.1)--fall 19
        sim.wait(tt)
        sim.setJointTargetPosition(joint02,setpy+0.1)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3)
        sim.wait(tt)
        signal_1(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,60*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx)--fall 20
        sim.setJointTargetPosition(joint02,setpy+0.1)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3)
        sim.wait(tt)
        signal_2(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,120*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx)--fall 21
        sim.setJointTargetPosition(joint02,setpy)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3)
        sim.wait(tt)
        signal_3(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,180*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx)--fall 22
        sim.setJointTargetPosition(joint02,setpy-0.1)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3)
        sim.wait(tt)
        signal_4(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,240*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx-0.1)--fall 23
        sim.setJointTargetPosition(joint02,setpy-0.1)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3)
        sim.wait(tt)
        signal_5(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,300*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx-0.1)--fall 24
        sim.setJointTargetPosition(joint02,setpy-0)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3)
        sim.wait(tt)
        signal_6(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx) 
        sim.setJointTargetPosition(joint02,sety)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,0*math.pi/180)
        -----------------------------------------------------------
        sim.setJointTargetPosition(joint01,setx+0.05) --pick_25
        sim.setJointTargetPosition(joint02,sety-0.05)
        signal_1(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,60*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx+0.05) --pick_26 
        sim.setJointTargetPosition(joint02,sety-0.15)
        signal_2(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,120*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx+0.15) --pick_27
        sim.setJointTargetPosition(joint02,sety-0.15)
        signal_3(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,180*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx+0.15) --pick_28
        sim.setJointTargetPosition(joint02,sety-0.05)
        signal_4(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,240*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx+0.15) --pick_29
        sim.setJointTargetPosition(joint02,sety+0.05)
        signal_5(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,300*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx+0.15) --pick_30
        sim.setJointTargetPosition(joint02,sety+0.15)
        signal_6(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,0*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,0*math.pi/180)
        sim.wait(long_long_t)
         -----------------------------------------------------------
        sim.setJointTargetPosition(joint01,setpx-0.1)--fall 25
        sim.wait(long_long_t)
        sim.setJointTargetPosition(joint02,setpy+0.1)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3)
        sim.wait(tt)
        signal_1(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,60*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx-0.05)--fall 26
        sim.setJointTargetPosition(joint02,setpy+0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h2)
        sim.wait(tt)
        signal_2(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,120*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx-0.05)--fall 27
        sim.setJointTargetPosition(joint02,setpy-0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h2)
        sim.wait(tt)
        signal_3(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,180*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx+0.05)--fall 28
        sim.setJointTargetPosition(joint02,setpy-0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h2)
        sim.wait(tt)
        signal_4(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,240*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx+0.05)--fall 29
        sim.setJointTargetPosition(joint02,setpy+0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h2)
        sim.wait(tt)
        signal_5(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,300*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx)--fall 30
        sim.setJointTargetPosition(joint02,setpy)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h1)
        sim.wait(tt)
        signal_6(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        ----------------------------------------------
        sim.setJointTargetPosition(joint01,0) 
        sim.setJointTargetPosition(joint02,0)
        sim.wait(long_long_t)
        sim.setJointTargetPosition(jointr,0)
        sim.wait(long_long_t)
        -----------------------------------------------------------
        -----------------------------------------------------------
        pick_h1=0.07
        pick_h2=0.138
        pick_h3=0.2085
        pick_h4=0.2801
        setx=-0.5
        setpx=0.5
        signal_1(true)
        sim.setJointTargetPosition(joint01,setx) --pick_1
        sim.setJointTargetPosition(joint02,sety)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h1)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,60*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx+0.05) --pick_2 h2-h2-
        sim.setJointTargetPosition(joint02,sety-0.05)
        sim.wait(tt)
        signal_2(true)
        sim.setJointTargetPosition(joint03,aty-pick_h2)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,120*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx+0.05) --pick_3
        sim.setJointTargetPosition(joint02,sety+0.05)
        sim.wait(tt)
        signal_3(true)
        sim.setJointTargetPosition(joint03,aty-pick_h2)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,180*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx-0.05) --pick_4
        sim.setJointTargetPosition(joint02,sety+0.05)
        sim.wait(tt)
        signal_4(true)
        sim.setJointTargetPosition(joint03,aty-pick_h2)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,240*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx-0.05) --pick_5
        sim.setJointTargetPosition(joint02,sety-0.05)
        sim.wait(tt)
        signal_5(true)
        sim.setJointTargetPosition(joint03,aty-pick_h2)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,300*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx+0.1) --pick_6 h3-h3
        sim.setJointTargetPosition(joint02,sety+0.1)
        sim.wait(tt)
        signal_6(true)
        sim.setJointTargetPosition(joint03,aty-pick_h3)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,0)
        sim.wait(long_t)
        -----------------------------------------------------------
        sim.setJointTargetPosition(joint01,setpx-0.15)--fall 1
        sim.wait(tt)
        sim.setJointTargetPosition(joint02,setpy+0.15)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_1(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,60*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx-0.15)--fall 2
        sim.setJointTargetPosition(joint02,setpy+0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_2(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,120*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx-0.15)--fall 3
        sim.setJointTargetPosition(joint02,setpy-0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_3(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,180*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx-0.15)--fall 4
        sim.setJointTargetPosition(joint02,setpy-0.15)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_4(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,240*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx-0.05)--fall 5
        sim.setJointTargetPosition(joint02,setpy-0.15)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_5(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,300*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx-0.05)--fall 6
        sim.setJointTargetPosition(joint02,setpy-0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_6(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx) 
        sim.setJointTargetPosition(joint02,sety)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,0*math.pi/180)
        -----------------------------------------------------------
        sim.setJointTargetPosition(joint01,setx+0.1) --pick_7
        sim.setJointTargetPosition(joint02,sety)
        signal_1(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h3)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,60*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx+0.1) --pick_8
        sim.setJointTargetPosition(joint02,sety-0.1)
        signal_2(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h3)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,120*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx) --pick_9
        sim.setJointTargetPosition(joint02,sety-0.1)
        signal_3(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h3)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,180*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx) --pick_10
        sim.setJointTargetPosition(joint02,sety)
        signal_4(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h3)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,240*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx) --pick_11
        sim.setJointTargetPosition(joint02,sety+0.1)
        signal_5(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h3)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,300*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx-0.1) --pick_12
        sim.setJointTargetPosition(joint02,sety+0.1)
        signal_6(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h3)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,0)
        sim.wait(long_t)
         -----------------------------------------------------------
        sim.setJointTargetPosition(joint01,setpx-0.05)--fall 7
        sim.wait(tt)
        sim.setJointTargetPosition(joint02,setpy+0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_1(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,60*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx-0.05)--fall 8
        sim.setJointTargetPosition(joint02,setpy+0.15)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_2(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-0.12)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,120*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx+0.05)--fall 9
        sim.setJointTargetPosition(joint02,setpy+0.15)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_3(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,180*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx+0.05)--fall 10
        sim.setJointTargetPosition(joint02,setpy+0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_4(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,240*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx+0.05)--fall 11
        sim.setJointTargetPosition(joint02,setpy-0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_5(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,300*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx+0.05)--fall 12
        sim.setJointTargetPosition(joint02,setpy-0.15)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_6(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx) 
        sim.setJointTargetPosition(joint02,sety)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,0)
        -----------------------------------------------------------
        sim.setJointTargetPosition(joint01,setx-0.1) --pick_13
        sim.setJointTargetPosition(joint02,sety)
        signal_1(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h3)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,60*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx-0.1) --pick_14 
        sim.setJointTargetPosition(joint02,sety-0.1)
        signal_2(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h3)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,120*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx-0.15) --pick_15 --h4-h4
        sim.setJointTargetPosition(joint02,sety+0.15)
        signal_3(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,180*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx-0.15) --pick_16
        sim.setJointTargetPosition(joint02,sety+0.05)
        signal_4(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,240*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx-0.15) --pick_17
        sim.setJointTargetPosition(joint02,sety-0.05)
        signal_5(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,300*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx-0.15) --pick_18
        sim.setJointTargetPosition(joint02,sety-0.15)
        signal_6(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,0)
        sim.wait(long_long_t)
        
         -----------------------------------------------------------
        sim.setJointTargetPosition(joint01,setpx+0.15)--fall 13
        sim.wait(long_long_t)
        sim.setJointTargetPosition(joint02,setpy-0.15)
        sim.wait(long_long_t)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_1(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,60*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx+0.15)--fall 14
        sim.setJointTargetPosition(joint02,setpy-0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_2(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,120*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx+0.15)--fall 15
        sim.setJointTargetPosition(joint02,setpy+0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_3(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,180*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx+0.15)--fall 16
        sim.setJointTargetPosition(joint02,setpy+0.15)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4)
        sim.wait(tt)
        signal_4(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h4_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,240*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx+0.1)--fall 17 h3--h3
        sim.setJointTargetPosition(joint02,setpy-0.1)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3)
        sim.wait(tt)
        signal_5(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,300*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx+0.1)--fall 18
        sim.setJointTargetPosition(joint02,setpy-0)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3)
        sim.wait(tt)
        signal_6(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx) 
        sim.setJointTargetPosition(joint02,sety)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,0)
        -----------------------------------------------------------
        sim.setJointTargetPosition(joint01,setx-0.05) --pick_19
        sim.setJointTargetPosition(joint02,sety-0.15)
        signal_1(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,60*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx-0.05) --pick_20 
        sim.setJointTargetPosition(joint02,sety-0.05)
        signal_2(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,120*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx-0.05) --pick_21
        sim.setJointTargetPosition(joint02,sety+0.05)
        signal_3(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,180*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx-0.05) --pick_22
        sim.setJointTargetPosition(joint02,sety+0.15)
        signal_4(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,240*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx+0.05) --pick_23
        sim.setJointTargetPosition(joint02,sety+0.15)
        signal_5(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,300*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx+0.05) --pick_24
        sim.setJointTargetPosition(joint02,sety+0.05)
        signal_6(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,0)
        sim.wait(tt)
        sim.wait(long_t)
         -----------------------------------------------------------
        sim.setJointTargetPosition(joint01,setpx+0.1)--fall 19
        sim.wait(tt)
        sim.setJointTargetPosition(joint02,setpy+0.1)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3)
        sim.wait(tt)
        signal_1(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,60*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx)--fall 20
        sim.setJointTargetPosition(joint02,setpy+0.1)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3)
        sim.wait(tt)
        signal_2(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,120*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx)--fall 21
        sim.setJointTargetPosition(joint02,setpy)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3)
        sim.wait(tt)
        signal_3(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,180*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx)--fall 22
        sim.setJointTargetPosition(joint02,setpy-0.1)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3)
        sim.wait(tt)
        signal_4(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,240*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx-0.1)--fall 23
        sim.setJointTargetPosition(joint02,setpy-0.1)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3)
        sim.wait(tt)
        signal_5(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,300*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx-0.1)--fall 24
        sim.setJointTargetPosition(joint02,setpy-0)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3)
        sim.wait(tt)
        signal_6(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx) 
        sim.setJointTargetPosition(joint02,sety)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,0)
        -----------------------------------------------------------
        sim.setJointTargetPosition(joint01,setx+0.05) --pick_25
        sim.setJointTargetPosition(joint02,sety-0.05)
        signal_1(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,60*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx+0.05) --pick_26 
        sim.setJointTargetPosition(joint02,sety-0.15)
        signal_2(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,120*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx+0.15) --pick_27
        sim.setJointTargetPosition(joint02,sety-0.15)
        signal_3(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,180*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx+0.15) --pick_28
        sim.setJointTargetPosition(joint02,sety-0.05)
        signal_4(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,240*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx+0.15) --pick_29
        sim.setJointTargetPosition(joint02,sety+0.05)
        signal_5(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,300*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setx+0.15) --pick_30
        sim.setJointTargetPosition(joint02,sety+0.15)
        signal_6(true)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-pick_h4)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,0*math.pi/180)
        sim.wait(tt)
        sim.wait(long_long_t)
         -----------------------------------------------------------
        sim.setJointTargetPosition(joint01,setpx-0.1)--fall 25
        sim.wait(long_long_t)
        sim.setJointTargetPosition(joint02,setpy+0.1)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3)
        sim.wait(tt)
        signal_1(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h3_up)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,60*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx-0.05)--fall 26
        sim.setJointTargetPosition(joint02,setpy+0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h2)
        sim.wait(tt)
        signal_2(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,120*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx-0.05)--fall 27
        sim.setJointTargetPosition(joint02,setpy-0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h2)
        sim.wait(tt)
        signal_3(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,180*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx+0.05)--fall 28
        sim.setJointTargetPosition(joint02,setpy-0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h2)
        sim.wait(tt)
        signal_4(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,240*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx+0.05)--fall 29
        sim.setJointTargetPosition(joint02,setpy+0.05)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h2)
        sim.wait(tt)
        signal_5(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        sim.setJointTargetPosition(jointr,300*math.pi/180)
        sim.wait(tt)
        sim.setJointTargetPosition(joint01,setpx)--fall 30
        sim.setJointTargetPosition(joint02,setpy)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty-fall_h1)
        sim.wait(tt)
        signal_6(false)
        sim.wait(tt)
        sim.setJointTargetPosition(joint03,aty)
        sim.wait(tt)
        ----------------------------------------------
        sim.setJointTargetPosition(joint01,0) 
        sim.setJointTargetPosition(joint02,0)
        setx=0.485
        setpx=-0.515
        pick_h1=0.07
        pick_h2=0.139
        pick_h3=0.207
        pick_h4=0.2772
        sim.wait(long_long_t)
        sim.setJointTargetPosition(jointr,0*math.pi/180)
        sim.wait(long_long_t)
    -----------------------------------------------------------
    end
end

</t>
<t tx="leo.20210522215527.14">function sysCall_cleanup()
    -- Put some clean-up code here
end
</t>
<t tx="leo.20210522215527.15">@path ./
@others
-- See the user manual or the available code snippets for additional callback functions and details
@language lua
@tabwidth -4
</t>
<t tx="leo.20210522215527.16">function sysCall_init()
    -- do some initialization here
    jointr=sim.getObjectHandle('Rotate')
end

</t>
<t tx="leo.20210522215527.17">function sysCall_actuation()
    -- put your actuation code here
end

</t>
<t tx="leo.20210522215527.18">function sysCall_sensing()
    aa=(sim.getJointPosition(jointr)*180/math.pi)
    print(math.floor(aa))
end

</t>
<t tx="leo.20210522215527.19">function sysCall_cleanup()
    -- do some clean-up here
end

</t>
<t tx="leo.20210522215527.2"></t>
<t tx="leo.20210522215527.20">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210522215527.21">function sysCall_init() 
    modelBase1=sim.getObjectHandle(sim.handle_self)
    robotBase1=modelBase1
    while true do
        robotBase1=sim.getObjectParent(robotBase1)
        if robotBase1==-1 then
            robotName1='Base'
            break
        end
        robotName1=sim.getObjectName(robotBase1)
        suffix,suffixlessName=sim.getNameSuffix(robotName1)
        if suffixlessName=='Base' then
            break
        end
    end
    sa=sim.getObjectHandle('suctionPadSensor')
    la=sim.getObjectHandle('suctionPadLoopClosureDummy1')
    l2a=sim.getObjectHandle('suctionPadLoopClosureDummy2')
    ba=sim.getObjectHandle('suctionPad')
    suctionPadLink=sim.getObjectHandle('suctionPadLink')
    local gripperBase=sim.getObjectHandle(sim.handle_self)

    infiniteStrength=sim.getScriptSimulationParameter(sim.handle_self,'infiniteStrength')
    maxPullForce=sim.getScriptSimulationParameter(sim.handle_self,'maxPullForce')
    maxShearForce=sim.getScriptSimulationParameter(sim.handle_self,'maxShearForce')
    maxPeelTorque=sim.getScriptSimulationParameter(sim.handle_self,'maxPeelTorque')

    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end


</t>
<t tx="leo.20210522215527.22">function sysCall_cleanup() 
    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end 

</t>
<t tx="leo.20210522215527.23">function sysCall_sensing() 
    parent=sim.getObjectParent(la)
    local sig=sim.getIntegerSignal(robotName1 .."call_1")
    if (not sig) or (sig==0) then
        if (parent~=ba) then
            sim.setLinkDummy(la,-1)
            sim.setObjectParent(la,ba,true)
            ma=sim.getObjectMatrix(l2a,-1)
            sim.setObjectMatrix(la,-1,ma)
        end
    else
        if (parent==ba) then
            -- Here we want to detect a respondable shape, and then connect to it with a force sensor (via a loop closure dummy dummy link)
            -- However most respondable shapes are set to "non-detectable", so "sim.readProximitySensor" or similar will not work.
            -- But "sim.checkProximitySensor" or similar will work (they don't check the "detectable" flags), but we have to go through all shape objects!
            index=0
            while true do
                shape=sim.getObjects(index,sim.object_shape_type)
                if (shape==-1) then
                    break
                end
                if (shape~=ba) and (sim.getObjectInt32Parameter(shape,sim.shapeintparam_respondable)~=0) and (sim.checkProximitySensor(sa,shape)==1) then
                    -- Ok, we found a respondable shape that was detected
                    -- We connect to that shape:
                    -- Make sure the two dummies are initially coincident:
                    sim.setObjectParent(la,ba,true)
                    ma=sim.getObjectMatrix(l2a,-1)
                    sim.setObjectMatrix(la,-1,ma)
                    -- Do the connection:
                    sim.setObjectParent(la,shape,true)
                    sim.setLinkDummy(la,l2a)
                    break
                end
                index=index+1
            end
        else
            -- Here we have an object attached
            if (infiniteStrength==false) then
                -- We might have to conditionally beak it apart!
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
                        sim.setLinkDummy(la,-1)
                        sim.setObjectParent(la,ba,true)
                        ma=sim.getObjectMatrix(l2a,-1)
                        sim.setObjectMatrix(la,-1,ma)
                    end
                    
                end
            end
        end
    end
end 
</t>
<t tx="leo.20210522215527.24">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210522215527.25">function sysCall_init() 
    modelBase2=sim.getObjectHandle(sim.handle_self)
    robotBase2=modelBase2
    while true do
        robotBase2=sim.getObjectParent(robotBase2)
        if robotBase2==-1 then
            robotName2='Base'
            break
        end
        robotName2=sim.getObjectName(robotBase2)
        suffix,suffixlessName=sim.getNameSuffix(robotName2)
        if suffixlessName=='Base' then
            break
        end
    end
    sa=sim.getObjectHandle('suctionPadSensor#0')
    la=sim.getObjectHandle('suctionPadLoopClosureDummy1#0')
    l2a=sim.getObjectHandle('suctionPadLoopClosureDummy2#0')
    ba=sim.getObjectHandle('suctionPad#0')
    suctionPadLink=sim.getObjectHandle('suctionPadLink#0')
    local gripperBase=sim.getObjectHandle(sim.handle_self)

    infiniteStrength=sim.getScriptSimulationParameter(sim.handle_self,'infiniteStrength')
    maxPullForce=sim.getScriptSimulationParameter(sim.handle_self,'maxPullForce')
    maxShearForce=sim.getScriptSimulationParameter(sim.handle_self,'maxShearForce')
    maxPeelTorque=sim.getScriptSimulationParameter(sim.handle_self,'maxPeelTorque')

    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end


</t>
<t tx="leo.20210522215527.26">function sysCall_cleanup() 
    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end 

</t>
<t tx="leo.20210522215527.27">function sysCall_sensing() 
    parent=sim.getObjectParent(la)
    local sig=sim.getIntegerSignal(robotName2 .."call_2")
    if (not sig) or (sig==0) then
        if (parent~=ba) then
            sim.setLinkDummy(la,-1)
            sim.setObjectParent(la,ba,true)
            ma=sim.getObjectMatrix(l2a,-1)
            sim.setObjectMatrix(la,-1,ma)
        end
    else
        if (parent==ba) then
            -- Here we want to detect a respondable shape, and then connect to it with a force sensor (via a loop closure dummy dummy link)
            -- However most respondable shapes are set to "non-detectable", so "sim.readProximitySensor" or similar will not work.
            -- But "sim.checkProximitySensor" or similar will work (they don't check the "detectable" flags), but we have to go through all shape objects!
            index=0
            while true do
                shape=sim.getObjects(index,sim.object_shape_type)
                if (shape==-1) then
                    break
                end
                if (shape~=ba) and (sim.getObjectInt32Parameter(shape,sim.shapeintparam_respondable)~=0) and (sim.checkProximitySensor(sa,shape)==1) then
                    -- Ok, we found a respondable shape that was detected
                    -- We connect to that shape:
                    -- Make sure the two dummies are initially coincident:
                    sim.setObjectParent(la,ba,true)
                    ma=sim.getObjectMatrix(l2a,-1)
                    sim.setObjectMatrix(la,-1,ma)
                    -- Do the connection:
                    sim.setObjectParent(la,shape,true)
                    sim.setLinkDummy(la,l2a)
                    break
                end
                index=index+1
            end
        else
            -- Here we have an object attached
            if (infiniteStrength==false) then
                -- We might have to conditionally beak it apart!
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
                        sim.setLinkDummy(la,-1)
                        sim.setObjectParent(la,ba,true)
                        ma=sim.getObjectMatrix(l2a,-1)
                        sim.setObjectMatrix(la,-1,ma)
                    end
                    
                end
            end
        end
    end
end 
</t>
<t tx="leo.20210522215527.28">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210522215527.29">
function sysCall_init() 
    modelBase3=sim.getObjectHandle(sim.handle_self)
    robotBase3=modelBase3
    while true do
        robotBase3=sim.getObjectParent(robotBase3)
        if robotBase3==-1 then
            robotName3='Base'
            break
        end
        robotName3=sim.getObjectName(robotBase3)
        suffix,suffixlessName=sim.getNameSuffix(robotName3)
        if suffixlessName=='Base' then
            break
        end
    end
    sa=sim.getObjectHandle('suctionPadSensor')
    la=sim.getObjectHandle('suctionPadLoopClosureDummy1')
    l2a=sim.getObjectHandle('suctionPadLoopClosureDummy2')
    ba=sim.getObjectHandle('suctionPad')
    suctionPadLink=sim.getObjectHandle('suctionPadLink')
    local gripperBase=sim.getObjectHandle(sim.handle_self)

    infiniteStrength=sim.getScriptSimulationParameter(sim.handle_self,'infiniteStrength')
    maxPullForce=sim.getScriptSimulationParameter(sim.handle_self,'maxPullForce')
    maxShearForce=sim.getScriptSimulationParameter(sim.handle_self,'maxShearForce')
    maxPeelTorque=sim.getScriptSimulationParameter(sim.handle_self,'maxPeelTorque')

    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end


</t>
<t tx="leo.20210522215527.30">function sysCall_cleanup() 
    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end 

</t>
<t tx="leo.20210522215527.31">function sysCall_sensing() 
    parent=sim.getObjectParent(la)
    local sig=sim.getIntegerSignal(robotName3 .."call_3")
    if (not sig) or (sig==0) then
        if (parent~=ba) then
            sim.setLinkDummy(la,-1)
            sim.setObjectParent(la,ba,true)
            ma=sim.getObjectMatrix(l2a,-1)
            sim.setObjectMatrix(la,-1,ma)
        end
    else
        if (parent==ba) then
            -- Here we want to detect a respondable shape, and then connect to it with a force sensor (via a loop closure dummy dummy link)
            -- However most respondable shapes are set to "non-detectable", so "sim.readProximitySensor" or similar will not work.
            -- But "sim.checkProximitySensor" or similar will work (they don't check the "detectable" flags), but we have to go through all shape objects!
            index=0
            while true do
                shape=sim.getObjects(index,sim.object_shape_type)
                if (shape==-1) then
                    break
                end
                if (shape~=ba) and (sim.getObjectInt32Parameter(shape,sim.shapeintparam_respondable)~=0) and (sim.checkProximitySensor(sa,shape)==1) then
                    -- Ok, we found a respondable shape that was detected
                    -- We connect to that shape:
                    -- Make sure the two dummies are initially coincident:
                    sim.setObjectParent(la,ba,true)
                    ma=sim.getObjectMatrix(l2a,-1)
                    sim.setObjectMatrix(la,-1,ma)
                    -- Do the connection:
                    sim.setObjectParent(la,shape,true)
                    sim.setLinkDummy(la,l2a)
                    break
                end
                index=index+1
            end
        else
            -- Here we have an object attached
            if (infiniteStrength==false) then
                -- We might have to conditionally beak it apart!
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
                        sim.setLinkDummy(la,-1)
                        sim.setObjectParent(la,ba,true)
                        ma=sim.getObjectMatrix(l2a,-1)
                        sim.setObjectMatrix(la,-1,ma)
                    end
                    
                end
            end
        end
    end
end 
</t>
<t tx="leo.20210522215527.32">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210522215527.33">function sysCall_init() 
    modelBase4=sim.getObjectHandle(sim.handle_self)
    robotBase4=modelBase4
    while true do
        robotBase4=sim.getObjectParent(robotBase4)
        if robotBase4==-1 then
            robotName4='Base'
            break
        end
        robotName4=sim.getObjectName(robotBase4)
        suffix,suffixlessName=sim.getNameSuffix(robotName4)
        if suffixlessName=='Base' then
            break
        end
    end
    sa=sim.getObjectHandle('suctionPadSensor#2')
    la=sim.getObjectHandle('suctionPadLoopClosureDummy1#2')
    l2a=sim.getObjectHandle('suctionPadLoopClosureDummy2#2')
    ba=sim.getObjectHandle('suctionPad')
    suctionPadLink=sim.getObjectHandle('suctionPadLink#2')
    local gripperBase=sim.getObjectHandle(sim.handle_self)

    infiniteStrength=sim.getScriptSimulationParameter(sim.handle_self,'infiniteStrength')
    maxPullForce=sim.getScriptSimulationParameter(sim.handle_self,'maxPullForce')
    maxShearForce=sim.getScriptSimulationParameter(sim.handle_self,'maxShearForce')
    maxPeelTorque=sim.getScriptSimulationParameter(sim.handle_self,'maxPeelTorque')

    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end


</t>
<t tx="leo.20210522215527.34">function sysCall_cleanup() 
    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end 

</t>
<t tx="leo.20210522215527.35">function sysCall_sensing() 
    parent=sim.getObjectParent(la)
    local sig=sim.getIntegerSignal(robotName4 .."call_4")
    if (not sig) or (sig==0) then
        if (parent~=ba) then
            sim.setLinkDummy(la,-1)
            sim.setObjectParent(la,ba,true)
            ma=sim.getObjectMatrix(l2a,-1)
            sim.setObjectMatrix(la,-1,ma)
        end
    else
        if (parent==ba) then
            -- Here we want to detect a respondable shape, and then connect to it with a force sensor (via a loop closure dummy dummy link)
            -- However most respondable shapes are set to "non-detectable", so "sim.readProximitySensor" or similar will not work.
            -- But "sim.checkProximitySensor" or similar will work (they don't check the "detectable" flags), but we have to go through all shape objects!
            index=0
            while true do
                shape=sim.getObjects(index,sim.object_shape_type)
                if (shape==-1) then
                    break
                end
                if (shape~=ba) and (sim.getObjectInt32Parameter(shape,sim.shapeintparam_respondable)~=0) and (sim.checkProximitySensor(sa,shape)==1) then
                    -- Ok, we found a respondable shape that was detected
                    -- We connect to that shape:
                    -- Make sure the two dummies are initially coincident:
                    sim.setObjectParent(la,ba,true)
                    ma=sim.getObjectMatrix(l2a,-1)
                    sim.setObjectMatrix(la,-1,ma)
                    -- Do the connection:
                    sim.setObjectParent(la,shape,true)
                    sim.setLinkDummy(la,l2a)
                    break
                end
                index=index+1
            end
        else
            -- Here we have an object attached
            if (infiniteStrength==false) then
                -- We might have to conditionally beak it apart!
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
                        sim.setLinkDummy(la,-1)
                        sim.setObjectParent(la,ba,true)
                        ma=sim.getObjectMatrix(l2a,-1)
                        sim.setObjectMatrix(la,-1,ma)
                    end
                    
                end
            end
        end
    end
end 
</t>
<t tx="leo.20210522215527.36">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210522215527.37">function sysCall_init() 
    modelBase5=sim.getObjectHandle(sim.handle_self)
    robotBase5=modelBase5
    while true do
        robotBase5=sim.getObjectParent(robotBase5)
        if robotBase5==-1 then
            robotName5='Base'

            break
        end
        robotName5=sim.getObjectName(robotBase5)
        suffix,suffixlessName=sim.getNameSuffix(robotName5)
        if suffixlessName=='Base' then

            break
        end
    end
    sa=sim.getObjectHandle('suctionPadSensor#3')
    la=sim.getObjectHandle('suctionPadLoopClosureDummy1#3')
    l2a=sim.getObjectHandle('suctionPadLoopClosureDummy2#3')
    ba=sim.getObjectHandle('suctionPad')
    suctionPadLink=sim.getObjectHandle('suctionPadLink#3')
    local gripperBase=sim.getObjectHandle(sim.handle_self)

    infiniteStrength=sim.getScriptSimulationParameter(sim.handle_self,'infiniteStrength')
    maxPullForce=sim.getScriptSimulationParameter(sim.handle_self,'maxPullForce')
    maxShearForce=sim.getScriptSimulationParameter(sim.handle_self,'maxShearForce')
    maxPeelTorque=sim.getScriptSimulationParameter(sim.handle_self,'maxPeelTorque')

    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end


</t>
<t tx="leo.20210522215527.38">function sysCall_cleanup() 
    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end 

</t>
<t tx="leo.20210522215527.39">function sysCall_sensing() 
    parent=sim.getObjectParent(la)
    local sig=sim.getIntegerSignal(robotName5 .."call_5")
    if (not sig) or (sig==0) then
        if (parent~=ba) then
            sim.setLinkDummy(la,-1)
            sim.setObjectParent(la,ba,true)
            ma=sim.getObjectMatrix(l2a,-1)
            sim.setObjectMatrix(la,-1,ma)
        end
    else
        if (parent==ba) then
            -- Here we want to detect a respondable shape, and then connect to it with a force sensor (via a loop closure dummy dummy link)
            -- However most respondable shapes are set to "non-detectable", so "sim.readProximitySensor" or similar will not work.
            -- But "sim.checkProximitySensor" or similar will work (they don't check the "detectable" flags), but we have to go through all shape objects!
            index=0
            while true do
                shape=sim.getObjects(index,sim.object_shape_type)
                if (shape==-1) then
                    break
                end
                if (shape~=ba) and (sim.getObjectInt32Parameter(shape,sim.shapeintparam_respondable)~=0) and (sim.checkProximitySensor(sa,shape)==1) then
                    -- Ok, we found a respondable shape that was detected
                    -- We connect to that shape:
                    -- Make sure the two dummies are initially coincident:
                    sim.setObjectParent(la,ba,true)
                    ma=sim.getObjectMatrix(l2a,-1)
                    sim.setObjectMatrix(la,-1,ma)
                    -- Do the connection:
                    sim.setObjectParent(la,shape,true)
                    sim.setLinkDummy(la,l2a)
                    break
                end
                index=index+1
            end
        else
            -- Here we have an object attached
            if (infiniteStrength==false) then
                -- We might have to conditionally beak it apart!
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
                        sim.setLinkDummy(la,-1)
                        sim.setObjectParent(la,ba,true)
                        ma=sim.getObjectMatrix(l2a,-1)
                        sim.setObjectMatrix(la,-1,ma)
                    end
                    
                end
            end
        end
    end
end 
</t>
<t tx="leo.20210522215527.40">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210522215527.41">function sysCall_init() 
    modelBase6=sim.getObjectHandle(sim.handle_self)
    robotBase6=modelBase6
    while true do
        robotBase6=sim.getObjectParent(robotBase6)
        if robotBase6==-1 then
            robotName6='Base'
            break
        end
        robotName6=sim.getObjectName(robotBase6)
        suffix,suffixlessName=sim.getNameSuffix(robotName6)
        if suffixlessName=='Base' then
            break
        end
    end
    sa=sim.getObjectHandle('suctionPadSensor#4')
    la=sim.getObjectHandle('suctionPadLoopClosureDummy1#4')
    l2a=sim.getObjectHandle('suctionPadLoopClosureDummy2#4')
    ba=sim.getObjectHandle('suctionPad#4')
    suctionPadLink=sim.getObjectHandle('suctionPadLink#4')
    local gripperBase=sim.getObjectHandle(sim.handle_self)

    infiniteStrength=sim.getScriptSimulationParameter(sim.handle_self,'infiniteStrength')
    maxPullForce=sim.getScriptSimulationParameter(sim.handle_self,'maxPullForce')
    maxShearForce=sim.getScriptSimulationParameter(sim.handle_self,'maxShearForce')
    maxPeelTorque=sim.getScriptSimulationParameter(sim.handle_self,'maxPeelTorque')

    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end


</t>
<t tx="leo.20210522215527.42">function sysCall_cleanup() 
    sim.setLinkDummy(la,-1)
    sim.setObjectParent(la,ba,true)
    ma=sim.getObjectMatrix(l2a,-1)
    sim.setObjectMatrix(la,-1,ma)
end 

</t>
<t tx="leo.20210522215527.43">function sysCall_sensing() 
    parent=sim.getObjectParent(la)
    local sig=sim.getIntegerSignal(robotName6 .."call_6")
    if (not sig) or (sig==0) then
        if (parent~=ba) then
            sim.setLinkDummy(la,-1)
            sim.setObjectParent(la,ba,true)
            ma=sim.getObjectMatrix(l2a,-1)
            sim.setObjectMatrix(la,-1,ma)
        end
    else
        if (parent==ba) then
            -- Here we want to detect a respondable shape, and then connect to it with a force sensor (via a loop closure dummy dummy link)
            -- However most respondable shapes are set to "non-detectable", so "sim.readProximitySensor" or similar will not work.
            -- But "sim.checkProximitySensor" or similar will work (they don't check the "detectable" flags), but we have to go through all shape objects!
            index=0
            while true do
                shape=sim.getObjects(index,sim.object_shape_type)
                if (shape==-1) then
                    break
                end
                if (shape~=ba) and (sim.getObjectInt32Parameter(shape,sim.shapeintparam_respondable)~=0) and (sim.checkProximitySensor(sa,shape)==1) then
                    -- Ok, we found a respondable shape that was detected
                    -- We connect to that shape:
                    -- Make sure the two dummies are initially coincident:
                    sim.setObjectParent(la,ba,true)
                    ma=sim.getObjectMatrix(l2a,-1)
                    sim.setObjectMatrix(la,-1,ma)
                    -- Do the connection:
                    sim.setObjectParent(la,shape,true)
                    sim.setLinkDummy(la,l2a)
                    break
                end
                index=index+1
            end
        else
            -- Here we have an object attached
            if (infiniteStrength==false) then
                -- We might have to conditionally beak it apart!
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
                        sim.setLinkDummy(la,-1)
                        sim.setObjectParent(la,ba,true)
                        ma=sim.getObjectMatrix(l2a,-1)
                        sim.setObjectMatrix(la,-1,ma)
                    end
                    
                end
            end
        end
    end
end 
</t>
<t tx="leo.20210522215527.5">@path ./
@others
@language lua
@tabwidth -4
</t>
<t tx="leo.20210522215527.6">function signal_on()
    signal_1(true)
    signal_2(true)
    signal_3(true)
    signal_4(true)
    signal_5(true)
    signal_6(true)
end

</t>
<t tx="leo.20210522215527.7">function signal_1(enable)
    modelBase1=sim.getObjectHandle(sim.handle_self)
    modelName1=sim.getObjectName(modelBase1)
    if enable then
        sim.setIntegerSignal(modelName1 .."call_1",1)
    else
        sim.setIntegerSignal(modelName1 .."call_1",0)
    end
end

</t>
<t tx="leo.20210522215527.8">function signal_2(enable)
    modelBase2=sim.getObjectHandle(sim.handle_self)
    modelName2=sim.getObjectName(modelBase2)
    if enable then
        sim.setIntegerSignal(modelName2 .."call_2",1)
    else
        sim.setIntegerSignal(modelName2 .."call_2",0)
    end
end

</t>
<t tx="leo.20210522215527.9">function signal_3(enable)
    modelBase3=sim.getObjectHandle(sim.handle_self)
    modelName3=sim.getObjectName(modelBase3)
    if enable then
        sim.setIntegerSignal(modelName3 .."call_3",1)
    else
        sim.setIntegerSignal(modelName3 .."call_3",0)
    end
end

</t>
</tnodes>
</leo_file>
