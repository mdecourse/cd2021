<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2"/>
<globals/>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="leo.20190603200714.1"><vh>@settings</vh>
<v t="leo.20190603200714.2"><vh>@data qt-gui-plugin-style-sheet</vh></v>
<v t="leo.20190603200714.3"><vh>@string initial_split_orientation = horizontal</vh></v>
</v>
<v t="leo.20190603200945.1"><vh>pelican settings</vh>
<v t="leo.20190603201004.1"><vh>@clean pelicanconf.py</vh>
<v t="leo.20190603201017.1"><vh>Declarations (pelicanconf.py)</vh></v>
</v>
<v t="leo.20190603201019.1"><vh>@clean publishconf.py</vh>
<v t="leo.20190603201038.1"><vh>Declarations (publishconf.py)</vh></v>
</v>
</v>
<v t="leo.20190603200826.1"><vh>@clean init.py</vh>
<v t="leo.20190603200835.1"><vh>Declarations (init.py)</vh></v>
<v t="leo.20190603200835.2"><vh>class Init(object)</vh>
<v t="leo.20190603200835.3"><vh>Init(object).__init__</vh></v>
</v>
</v>
<v t="leo.20190603200909.1"><vh>@clean http-server.py</vh>
<v t="leo.20190603200921.1"><vh>Declarations (http-server.py)</vh></v>
<v t="leo.20190603200921.2"><vh>domake (http-server.py)</vh></v>
</v>
<v t="leo.20190603200703.2"><vh>@clean user.py</vh>
<v t="leo.20190603200801.1"><vh>Declarations (user.py)</vh></v>
<v t="leo.20190603200801.2"><vh>index (user.py)</vh></v>
<v t="leo.20190603200801.3"><vh>threegear (user.py)</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="leo.20190603200703.2">@others
@language python
@tabwidth -4
</t>
<t tx="leo.20190603200714.1"></t>
<t tx="leo.20190603200714.2">QSplitter::handle {
    background-color: #CAE1FF; /* lightSteelBlue1 */
}

QStackedWidget {
    /* background-color:lightpink; */
    border-color: red;
    padding: 0px;
    /* border-width: 0px; */
    /* background-color: yellow; */
}

QSplitter {
    border-color: white;
    background-color: white;
    border-style: solid;
}

QTreeWidget {
    /* These apply to the selected item, but not to editing items.*/
    background-color: #ffffec; /* Leo's traditional tree color */
    selection-color: black; /* was white */
    selection-background-color: lightgrey;
    /* font-family: SansSerif; */
    /*font-family: DejaVu Sans Mono;*/
    font-family:YaHei Mono;
    /* 標題字型大小設定 */
    font-size: 22px;
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
    font-size: 22px;
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
    font-size: 22px;
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
    font-size: 22px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

QLabel {
    font-family:YaHei Mono;
    /* 下方的 Minibuffer 標題字型大小 */
    font-size: 22px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

/* Editor labels */
QLineEdit#editorLabel {
    background-color: #ffffec;
    font-family:YaHei Mono;
    /* 沒有直接對應字型大小 */
    font-size: 22px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
    border: 2px;
    margin: 2px;
}</t>
<t tx="leo.20190603200714.3">horizontal: body pane to the left
vertical: body pane on the botton</t>
<t tx="leo.20190603200801.1">from flask import Blueprint, render_template, current_app, \
    send_from_directory, session, redirect, url_for
import os

userapp = Blueprint('user', __name__, url_prefix='/user', template_folder='templates')




</t>
<t tx="leo.20190603200801.2">@userapp.route('/')
def index():
    user = "Yen"
    # 若 template 檔案名稱與位於外部 templates 目錄中的檔案同名, 則取外部的 template
    return render_template('index.html', user=user)
</t>
<t tx="leo.20190603200801.3">@userapp.route('/threegear', defaults={'n1':15,'n2':20,'n3':18})
@userapp.route('/threegear/&lt;n1&gt;/&lt;n2&gt;/&lt;n3&gt;')
def threegear(n1, n2, n3):
    # 真正最後的架構應該要在函式中準備繪圖所需的資料, 然後用 template 呈現內容
    title = "網際 2D 繪圖"
    head = '''
&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;'''+ title +'''&lt;/title&gt;
    &lt;!-- IE 9: display inline SVG --&gt;
    &lt;meta http-equiv="X-UA-Compatible" content="IE=9"&gt;
'''
    script = '''
&lt;script type="text/javascript" src="https://brython.info/src/brython_dist.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript" src="https://2015fallhw.github.io/cptocadp/static/Cango-8v03.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript" src="https://2015fallhw.github.io/cptocadp/static/Cango2D-7v01-min.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript" src="https://2015fallhw.github.io/cptocadp/static/gearUtils-05.js"&gt;&lt;/script&gt;
 
&lt;script&gt;
window.onload=function(){
brython(1);
}
&lt;/script&gt;
'''
    headstring = head + script + "&lt;/head&gt;"
    # 能否根據 n1, n2, n3 與 width, 算出合理的 height
    # 模數計算 m = canvas.width*0.8/(n1+n2+n3)
    # max([int(n1), int(n2), int(n3)])
    # 所以 height = 1.2*800*0.8/(int(n1)+int(n2)+int(n3))*max([int(n1), int(n2), int(n3)])
    height = 1.2*800*0.8/(int(n1)+int(n2)+int(n3))*max([int(n1), int(n2), int(n3)])
    body = '''
    
延伸應用:&lt;br /&gt;

軸孔加入 keyway &lt;br /&gt;
與 3D 零件設計繪圖對應 &lt;br/&gt;
與 2D/3D 軸的設計與繪圖對應&lt;br /&gt;&lt;br /&gt;
&lt;canvas id='gear1' width='800' height="'''+str(int(height))+'''"&gt;&lt;/canvas&gt;
 
&lt;script type="text/python"&gt;
# 將 導入的 document 設為 doc 主要原因在於與舊程式碼相容
from browser import document as doc
# 由於 Python3 與 Javascript 程式碼已經不再混用, 因此來自 Javascript 的變數, 必須居中透過 window 物件轉換
from browser import window
# 針對 Javascript 既有的物件, 則必須透過 JSConstructor 轉換
from javascript import JSConstructor
import math
 
# 主要用來取得畫布大小
canvas = doc["gear1"]
# 此程式採用 Cango Javascript 程式庫繪圖, 因此無需 ctx
#ctx = canvas.getContext("2d")
# 針對類別的轉換, 將 Cango.js 中的 Cango 物件轉為 Python cango 物件
cango = JSConstructor(window.Cango)
# 針對變數的轉換, shapeDefs 在 Cango 中資料型別為變數, 可以透過 window 轉換
shapedefs = window.shapeDefs
# 目前 Cango 結合 Animation 在 Brython 尚無法運作, 此刻只能繪製靜態圖形
# in CangoAnimation.js
#interpolate1 = window.interpolate
# Cobi 與 createGearTooth 都是 Cango Javascript 程式庫中的物件
cobj = JSConstructor(window.Cobj)
creategeartooth = JSConstructor(window.createGearTooth)
 
# 經由 Cango 轉換成 Brython 的 cango, 指定將圖畫在 id="plotarea" 的 canvas 上
cgo = cango("gear1")
 
######################################
# 畫正齒輪輪廓
#####################################
def spur(cx, cy, m, n, pa, theta):
    # n 為齒數
    #n = 17
    # pa 為壓力角
    #pa = 25
    # m 為模數, 根據畫布的寬度, 計算適合的模數大小
    # Module = mm of pitch diameter per tooth
    #m = 0.8*canvas.width/n
    # pr 為節圓半徑
    pr = n*m/2 # gear Pitch radius
    # generate gear
    data = creategeartooth(m, n, pa)
    # Brython 程式中的 print 會將資料印在 Browser 的 console 區
    #print(data)
 
    gearTooth = cobj(data, "SHAPE", {
            "fillColor":"#ddd0dd",
            "border": True,
            "strokeColor": "#606060" })
    #gearTooth.rotate(180/n) # rotate gear 1/2 tooth to mesh, 請注意 rotate 角度為 degree
    # theta 為角度
    gearTooth.rotate(theta) 
    # 單齒的齒形資料經過旋轉後, 將資料複製到 gear 物件中
    gear = gearTooth.dup()
    # gear 為單一齒的輪廓資料
    #cgo.render(gearTooth)
 
    # 利用單齒輪廓旋轉, 產生整個正齒輪外形
    for i in range(1, n):
        # 將 gearTooth 中的資料複製到 newTooth
        newTooth = gearTooth.dup()
        # 配合迴圈, newTooth 的齒形資料進行旋轉, 然後利用 appendPath 方法, 將資料併入 gear
        newTooth.rotate(360*i/n)
        # appendPath 為 Cango 程式庫中的方法, 第二個變數為 True, 表示要刪除最前頭的 Move to SVG Path 標註符號
        gear.appendPath(newTooth, True) # trim move command = True
 
    # 建立軸孔
    # add axle hole, hr 為 hole radius
    hr = 0.6*pr # diameter of gear shaft
    shaft = cobj(shapedefs.circle(hr), "PATH")
    shaft.revWinding()
    gear.appendPath(shaft) # retain the 'moveTo' command for shaft sub path
    gear.translate(cx, cy)
    # render 繪出靜態正齒輪輪廓
    cgo.render(gear)
    # 接著繪製齒輪的基準線
    deg = math.pi/180
    Line = cobj(['M', cx, cy, 'L', cx+pr*math.cos(theta*deg), cy+pr*math.sin(theta*deg)], "PATH", {
          'strokeColor':'blue', 'lineWidth': 1})
    cgo.render(Line)
 
# 3個齒輪的齒數
n1 = '''+str(n1)+'''
n2 = '''+str(n2)+'''
n3 = '''+str(n3)+'''
 
# m 為模數, 根據畫布的寬度, 計算適合的模數大小
# Module = mm of pitch diameter per tooth
# 利用 80% 的畫布寬度進行繪圖
# 計算模數的對應尺寸
m = canvas.width*0.8/(n1+n2+n3)
 
# 根據齒數與模組計算各齒輪的節圓半徑
pr1 = n1*m/2
pr2 = n2*m/2
pr3 = n3*m/2
 
# 畫布左右兩側都保留畫布寬度的 10%
# 依此計算對應的最左邊齒輪的軸心座標
cx = canvas.width*0.1+pr1
cy = canvas.height/2
 
# pa 為壓力角
pa = 25
 
# 畫最左邊齒輪, 定位線旋轉角為 0, 軸心座標 (cx, cy)
spur(cx, cy, m, n1, pa, 0)
# 第2個齒輪將原始的定位線逆時鐘轉 180 度後, 與第1個齒輪正好齒頂與齒頂對齊
# 只要第2個齒輪再逆時鐘或順時鐘轉動半齒的角度, 即可完成囓合
# 每一個齒分別包括從齒根到齒頂的範圍, 涵蓋角度為 360/n, 因此所謂的半齒角度為 180/n
spur(cx+pr1+pr2, cy, m, n2, pa, 180-180/n2)
# 第2齒與第3齒的囓合, 首先假定第2齒的定位線在 theta 角為 0 的原始位置
# 如此, 第3齒只要逆時鐘旋轉 180 度後, 再逆時鐘或順時鐘轉動半齒的角度, 即可與第2齒囓合
# 但是第2齒為了與第一齒囓合時, 已經從原始定位線轉了 180-180/n2 度
# 而當第2齒從與第3齒囓合的定位線, 逆時鐘旋轉 180-180/n2 角度後, 原先囓合的第3齒必須要再配合旋轉 (180-180/n2 )*n2/n3
spur(cx+pr1+pr2+pr2+pr3, cy, m, n3, pa, 180-180/n3+(180-180/n2)*n2/n3)
&lt;/script&gt;
'''
    bodystring = "&lt;body&gt;" + body+"&lt;/body&gt;"
    endstring = "&lt;/html&gt;"
    outstring = headstring + bodystring + endstring
    return outstring
    # 若 template 檔案名稱與位於外部 templates 目錄中的檔案同名, 則取外部的 template
   # return render_template('g1index.html', user=user)
</t>
<t tx="leo.20190603200826.1">@others
@language python
@tabwidth -4
</t>
<t tx="leo.20190603200835.1">import os

"""CMSimfly 程式起始設定
"""

# 確定程式檔案所在目錄, 在 Windows 有最後的反斜線
_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__))
# 設定在 uwsgi 與近端的資料儲存目錄
config_dir = _curdir + "/config/"
</t>
<t tx="leo.20190603200835.2">class Init(object):
    # uwsgi as static class variable, can be accessed by Init.uwsgi
    uwsgi = False
    site_title = "CMSiMDE"
    @others
</t>
<t tx="leo.20190603200835.3">def __init__(self):
    # hope to create downloads and images directories　
    if not os.path.isdir(_curdir + "/downloads"):
        try:
            os.makedirs(_curdir + "/downloads")
        except:
            print("mkdir error")
    if not os.path.isdir(_curdir + "/images"):
        try:
            os.makedirs(_curdir + "/images")
        except:
            print("mkdir error")


</t>
<t tx="leo.20190603200909.1">@others
@language python
@tabwidth -4
</t>
<t tx="leo.20190603200921.1">import os
import subprocess
import threading
import http.server, ssl

</t>
<t tx="leo.20190603200921.2">def domake():
    # build directory
    #os.chdir("./../")
    server_address = ('localhost', 8444)
    httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   server_side=True,
                                   certfile='./cmsimde/localhost.crt',
                                   keyfile='./cmsimde/localhost.key',
                                   ssl_version=ssl.PROTOCOL_TLSv1)
    print(os.getcwd())
    print("8444 https server started")
    httpd.serve_forever()

# 利用執行緒執行 https 伺服器
make = threading.Thread(target=domake)
make.start()
</t>
<t tx="leo.20190603200945.1"></t>
<t tx="leo.20190603201004.1">#!/usr/bin/env python
# -*- coding: utf-8 -*- #
@others
@language python
@tabwidth -4
</t>
<t tx="leo.20190603201017.1">from __future__ import unicode_literals

AUTHOR = 'KMOL'
SITENAME = 'CMSimfly 網際內容管理'
# 不要用文章所在目錄作為類別
USE_FOLDER_AS_CATEGORY = False

#PATH = 'markdown'

#OUTPUT_PATH = 'blog'

TIMEZONE = 'Asia/Taipei'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Nature', 'https://www.nature.com/'),
        ('Science', 'http://www.sciencemag.org/'),
        ('Sam Harris', 'https://www.samharris.org/'),
        ('Andreas Wagner', 'http://www.ieu.uzh.ch/wagner/'),
        ('American Scientist', 'https://www.americanscientist.org/'),
        ('Scientific American', 'https://www.scientificamerican.com/'),)

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# 必須絕對目錄或相對於設定檔案所在目錄
PLUGIN_PATHS = ['plugin']
PLUGINS = ['summary', 'tipue_search', 'sitemap', 'neighbors']

# for sitemap plugin
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

# search is for Tipue search
DIRECT_TEMPLATES = (('index', 'tags', 'categories', 'authors', 'archives', 'search'))

# for pelican-bootstrap3 theme settings
#TAG_CLOUD_MAX_ITEMS = 50
DISPLAY_CATEGORIES_ON_SIDEBAR = True
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
DISPLAY_TAGS_ON_SIDEBAR = True
DISPLAY_TAGS_INLINE = True
TAGS_URL = "tags.html"
CATEGORIES_URL = "categories.html"
#MENUITEMS = [('About', '/blog/pages/about/index.html')]
#SHOW_ARTICLE_AUTHOR = True

#MENUITEMS = [('Home', '/'), ('Archives', '/archives.html'), ('Search', '/search.html')]
</t>
<t tx="leo.20190603201019.1">#!/usr/bin/env python
# -*- coding: utf-8 -*- #
@others
@language python
@tabwidth -4
</t>
<t tx="leo.20190603201038.1">from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# 因為 publishconf.py 在 pelicanconf.py 之後, 因此若兩處有相同變數的設定, 將以較後讀入的 publishconf.py 中的設定為主.

# 將所有靜態 html 檔案移到 blog 子目錄
SITEURL = 'https://chiamingyen.github.io/cmsimfly/blog'
# 此設定用於將資料送到 gh-pages, 因此使用絕對 URL 設定
RELATIVE_URLS = False

THEME = 'theme/attila'
BOOTSTRAP_THEME = 'united'
COLOR_SCHEME_CSS = 'tomorrow_night.css'


FEED_ALL_ATOM = 'feeds/all.atom.xml'
#CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

DISQUS_SITENAME = "kmolab-github"
DISQUS_DISPLAY_COUNTS = False
#GOOGLE_ANALYTICS = ""

# 設定網誌以 md 檔案建立的 file system date 為準, 無需自行設定
DEFAULT_DATE = 'fs'

# 遠端的 code hightlight
#MD_EXTENSIONS = ['fenced_code', 'extra', 'codehilite(linenums=True)']
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}

# 若要依照日期存檔呼叫
#ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
#ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'
SHOW_ARTICLE_AUTHOR = True
</t>
</tnodes>
</leo_file>
