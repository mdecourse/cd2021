var tipuesearch = {"pages": [{'title': 'About', 'text': 'cd2021 course repository:  https://github.com/mdecourse/cd2021 \n cd2021 course discussion:  https://github.com/mdecourse/cd2021/discussions \n cd2021 gitter:\xa0 https://gitter.im/mdecourse/cd2021 \n 區網下載區:  http://a.kmol.info:88/  (for 機械設計工程系 IPv6 網路連線) \n GDrive 下載區:  for @gm users only \n 其他 KMOLab 課程:  http://mde.tw/ \n 分組專題: \n W2-W4 (3 Weeks): 二人一組 \n W5-W9 (5 Weeks): 四人一組 \n W10-W18 (9 Weeks): 八人一組 \n 評分: \n 出席 10% \n 個人倉儲與網頁 30% \n 每週網際 html 簡報與 Pdf 報告 60% (含 Youtube 操作影片) \n \n 電腦輔助設計室與協同設計室行事曆 \n 全頁檢視 \n \n', 'tags': '', 'url': 'About.html'}, {'title': 'Topics', 'text': '課程簡介 \n 從英文單字解釋了解何謂協同? 產品? 設計? 以及實習? \n \n 針對 Leo Editor 6.3 在 Windows 10 無法正確建立 home/.leo/.leoID.txt, 因此必須手動建立: \n \n 為了讓各階段分組協同產品設計實習過程, 可以利用網誌建立特定時間點的設計報告資料, 特別利用 Leo Editor 設定 CMSiMDE 中的 Pelican 網誌, 並以 button 指令對 Pelican Markdown 檔案轉檔, 並將網誌超文件存入 blog 目錄: \n \n \n \xa0為了因應協同設計過程, 特定檔案可能在 Leo Editor 以外的編輯流程中改版, 且該檔案並未導入 Leo Editor 中進行編輯, 則使用者可以透過 refresh from disk 的功能將外部檔案的內容導入: \n \n 為了順利完成 W2-W4 以自選組員方式進行分組協同產品開發實習, 必須在各班取得分組名單 (以學號為依據) 以及各班組序, 若採用 Ethercalc 網際共用表單, 讓各班以線上同步分式輸入各組名單並設法訂定組序, 則可以採用全人工輸入與排序方式或人工輸入且程式自動排序方式進行, 以下嘗試透過  https://pypi.org/project/ethercalc-python/  讀取 Ethercalc 表單中的資料, 並設法進行排序, 且期望能自動產生可直接輸入 CMSiMDE 網頁的方式進行: \n \n 根據第一階段的分組要求, 嘗試採電腦程式執行的方式完成分組與排序, 目前結果如下: \n 討論: \n 在無其他同步或非同步網際程式工具輔助下, 若採用 Ethercalc 以網際同步方式可取得各分組的學員學號, 但因無自動定組序的方法 (可類比至後續若要設法導入自動化流程讀取各組的分組網站, 則必須設法讓電腦程式可以讀取各分組的分組網站內容), 因此需要人工介入訂定組序並收集各組分組網站的連結並發布在網際環境中, 目前所面臨的問題是, 除了各組兩名組員可自選外, 其他流程 (定各班組序, 取得各班分組網站連結並自動嵌入預定的 content.htm 檔案中) 都希望以自動化方式完成. \n 目前已知 ethercalc-python 可協助讀取特定的 Ethercalc 表單, 以下列程式為例, 因為利用 Python 的 set 去除各列中重複的 None 值, 但因 set 資料的特性是 unordered, 因此雖達成去除重複資料的目的, 但卻弄亂原先的資料順序, 因此或可採直接讀取 Ethercalc 表單資料後, 依照各行固定位置的學員學號 (第二與第三行資料), 並設法忽略中間的空白列 (row) 內容後, 再與最終的各班選課名單 (透過  https://github.com/mdecourse/nfulist  讀取資料) 進行比對後 (因其中可能包含未自選組員的情況, 則必須由電腦進行自動配對), 再進行各班組序的訂定, 並依各組組序與組長 Github 帳號 (如何取得?), 自動產生各組的分組倉儲連結與分組網站連結後, 設法產生對應的 html 資料後, 再設法嵌入指定的 content.htm 中. \n 特別注意: 只有在上課時段,  http://140.130.17.17:8000  Ethercalc 主機才會開啟, 各組若要自行建立測試用的 Ethercalc 主機, 請參考:  http://mde.tw/cad2020/content/Ethercalc.html   \n #!/usr/bin/env python3\nimport ethercalc\nimport pprint\n \npp = pprint.PrettyPrinter(indent=4)\ne = ethercalc.EtherCalc("http://140.130.17.17:8000")\noutput = e.export("h9qd54jy0kfp")\nfor i in range(len(output)):\n    #print(output[i])\n    # 設法除掉 None element\n    soutput = set(output[i])\n    print(soutput) \n 且從甲班表單取回的資料如下: \n {\'member 2\', \'member 1\', \'member 3\', \'2a cad2021\'}\n{None, 40823145.0, \'stage1-ag1\', 40823108.0}\n{None, 40623121.0, \'stage1-ag2\', 40523252.0}\n{None, 40623234.0}\n{None, 40423113.0}\n{\'stage1-ag5\', 40823106.0, None, 40823102.0}\n{None}\n{None}\n{\'stage1-ag9\', 40823112.0, 40823109.0, None}\n{None, 40823139.0, \'stage1-ag10\', 40823111.0}\n{None, 40823129.0, \'stage1-ag11\', 40823149.0}\n{\'stage1-ag12\', 40823107.0, None, 40823103.0}\n{None, 40823115.0, 40823140.0, \'stage1-ag13\'}\n{40823104.0, \'stage1-ag14\', 40823101.0, None}\n{None, \'stage1-ag15\', 40823150.0, 40823119.0}\n{40823120.0, 40823124.0, None, \'stage1-ag16\'}\n{None, \'stage1-ag18\', 40823122.0, 40823117.0}\n{40823132.0, 40823125.0, 40823110.0, \'stage1-ag19\'}\n{40823128.0, \'stage1-ag20\', 40823126.0, None}\n{None, 40823146.0, 40823114.0, \'stage1-ag19\'}\n{40823144.0, \'stage1-ag20\', 40823142.0, None}\n{None, 40823121.0, \'stage1-ag21\', 40823135.0}\n{40823136.0, \'stage1-ag22\', 40823123.0, None}\n{None, 40823148.0, \'stage1-ag23\', 40823127.0}\n{40823152.0, 40823153.0, \'stage1-ag24\', None}\n{None, 40871106.0, \'stage1-ag25\', 40823151.0}\n{None, 40823131.0, \'stage1-ag26\', 40823116.0} \n 而從乙班表單取回的資料如下: \n {\'member 3\', None, \'member 1\', \'cd2021 2b\', \'member 2\'}\n{None, \'stage1-bg1\', 40823251.0, 40823245.0}\n{None, 40823234.0, 40823235.0, \'stage1-bg2\'}\n{None, 40823207.0, 40823206.0, \'stage1-bg3\'}\n{40723128.0, 40723215.0, None, \'stage1-bg4\'}\n{None, \'stage1-bg5\', 40823218.0, 40823238.0}\n{None, \'stage1-bg6\', 40823225.0, 40823214.0}\n{None, 40823236.0, 40823212.0, \'stage1-bg7\'}\n{40823208.0, \'stage1-bg8\', None, 40823246.0}\n{None, 40823201.0, 40823217.0, \'stage1-bg9\'}\n{40723106.0, 40723139.0, 40723143.0, None, \'stage1-bg10\'}\n{None, 40823239.0, \'stage1-bg11\', 40823205.0}\n{\'stage1-bg12\', 40823202.0, 40823203.0, None}\n{\'stage1-bg13\', None, 40823223.0, 40823224.0, \'^\'}\n{None, \'stage1-bg14\', 40823242.0, 40823228.0}\n{40823216.0, 40823211.0, \'stage1-bg15\', None}\n{40823237.0, \'stage1-bg16\', 40823221.0, None}\n{None, \'stage1-bg17\', 40823250.0, 40832244.0}\n{None, 40823209.0, 40823210.0, \'stage1-bg18\'}\n{None, \'stage1-bg19\', 40823219.0, 40823231.0}\n{40823232.0, None, \'stage1-bg20\', 40823213.0}\n{40823248.0, \'stage1-bg21\', None, 40823247.0}\n{None, 40823244.0, 40823222.0, \'stage1-bg22\'}\n{40723224.0, 40623144.0, \'stage1-bg23\', None}\n{None, \'stage1-bg24\', 40823220.0, 40823204.0}\n{None, 40823241.0, 40823227.0, \'stage1-bg25\'}\n{\'stage1-bg26\', 40823204.0, None}\n{None, \'stage1-bg27\', 40723141.0}\n{None, 40723233.0, \'stage1-bg28\'}\n{None, 40823233.0, \'stage1-bg29\'}\n{None}\n{None}\n{None}\n{None}\n{None}\n{None}\n{None}\n{None}\n{None}\n{None}\n{None}\n{None}\n{None}\n{None}\n{None}\n{None}\n{None}\n{None}\n{None}\n{None}\n{None}\n{None}\n{None}\n{None}\n{None}\n{None}\n{None, \'WWW\'} \n 創建實體元件是產品設計, 創建數位工具也是產品設計, 不斷提升各種服務品質也是產品設計, 解決設計流程中的重點議題也是產品設計, 產品不分大小與虛實, 只看有沒有價值, 而且該價值能否持續被重用延伸. \n 對了, 設法激發學生潛力, 令其可以日日進步, 每天生活都陽光普照, 也應該算產品設計, 成敗端看這個產品能否及時養成良好的生活習慣, 吸飽各種有價值的元素, 貼上貨真價實的標籤...... \n Collaborative \n involving two of more people working together for a special purpose. \n The presentation was a collaborative effort by all the children in the class. \n \n Product \n an article (物品) or substance (物質) that is manufactured or refined (精製或改良) for sale (可供販售). \n food produts \n 可供販售, 表示經過製造或改良的物品或物質, 具有特定價值 \n a substance (物質) produced during a natural, chemical, or manufacturing process. \n waste (廢棄或無用) products \n 在產品開發過程所衍生的其他內容 (歷程資料或所使用的各種工具與使用方法), 也應視為產品的一環 \n commercially manufactured articles (物品), especially recordings, viewed collectively. \n too much product of too little quality \n \n design \n to make or draw plans for something, for example clothes or buildings. \n Who designed this building/dress/funiture? \n This range of clothing is specially designed for shorter women. \n \n practice \n action rather than thought or ideas. \n How do you intend to put these proposals into practice, Mohamed? \n \n Intro to Collaborative Design \n Collaborative Design \n What is Collaborative Design \n Why You Should Pursue Collaborative Design to Build Product?  \n How Collaboration Makes us Better Designers? \n The Right Way to Do Collaborative Design \n Product Development \n Hacking Product Design', 'tags': '', 'url': 'Topics.html'}, {'title': 'Stage1', 'text': '第一階段分組協同實習: \n 每週分組報告必須包含 html, pdf 與 Youtube 影片: \n 標題:  2021-協同產品設計實習-stage1-ag1 \n 專題題目: \n 第一位組員學號:( Curriculum Vitae 範例 ) \n 第二位組員學號:( CV 範例 ) \n 其他組員學號: \n 交付給各組的實習任務: \n \n 請在各組組長的 Github 帳號下建立各組的分組網站, 惟在 W1 進行各班定組序過程中, 發現即便採用 Ethercalc 以網際協同方式同步讓各班自選組員填入兩兩成組的學員學號, 但仍缺人工或自動定各班組序的有效方案, 在此責成各組在進行自選的協同產品開發項目之際 (W2-W4), 將此議題列為必選的題目之一, 詳細說明各組認為最有效率的第一階段與訂定組序的方法及流程. \n 此外, 為了讓各組在 stage1 分組協同實習過程, 能透過網誌發表各組組員在 W2-W4 過程中的各項作為與心得報告, 說明可利用 Leo Editor 協助 CMSiMDE 中的 Pelican 發表協同網誌, 其目的是讓各分組在協同期間, 能完整呈現各階段所留下的網誌紀錄. 但此方式必須熟悉 Leo Editor 的操作, 因此有關透過 Pelican 建立協同網誌一事, 除利用 Leo Editor 協助設定並建立 pelican 網誌外, 也將此議題列為各組在 Stage1 協同產品設計流程中必選題目之二, 請各組詳細說明採用或不採用 Leo Editor 的兩種情況下, 各組員在設定與建立協同網誌的過程所可能遭遇或產生的問題與解決方案. \n \n 2021 協同產品設計實習 W4 分組專題報告與影片繳交處 \n 2a stage1 分組: \n stage1-ag1 repo  |  stage1-ag1 site  |  40823145 repo  |  40823145 site  |  40823108 repo  |  40823108 site stage1-ag2 repo  |  stage1-ag2 site  |  40523252 repo  |  40523252 site  |  40623121 repo  |  40623121 site stage1-ag3 repo  |  stage1-ag3 site  |  40623234-1 repo  |  40623234-1 site  |  40423113 repo  |  40423113 site stage1-ag4 repo  |  stage1-ag4 site  |  40823101 repo  |  40823101 site  |  40823104 repo  |  40823104 site stage1-ag5 repo  |  stage1-ag5 site  |  40823102 repo  |  40823102 site  |  40823106 repo  |  40823106 site stage1-ag6 repo  |  stage1-ag6 site  |  40823111 repo  |  40823111 site  |  40823139 repo  |  40823139 site stage1-ag7 repo  |  stage1-ag7 site  |  40823129 repo  |  40823129 site  |  40823149 repo  |  40823149 site stage1-ag8 repo  |  stage1-ag8 site  |  40823103 repo  |  40823103 site  |  40823107 repo  |  40823107 site stage1-ag9 repo  |  stage1-ag9 site  |  40823115 repo  |  40823115 site  |  40823140 repo  |  40823140 site stage1-ag10 repo  |  stage1-ag10 site  |  40823109 repo  |  40823109 site  |  a40823112 repo  |  a40823112 site stage1-ag11 repo  |  stage1-ag11 site  |  40823119 repo  |  40823119 site  |  40823150 repo  |  40823150 site stage1-ag12 repo  |  stage1-ag12 site  |  40823120 repo  |  40823120 site  |  40823124 repo  |  40823124 site stage1-ag13 repo  |  stage1-ag13 site  |  40823117 repo  |  40823117 site  |  40823122 repo  |  40823122 site stage1-ag14 repo  |  stage1-ag14 site  |  40823125 repo  |  40823125 site  |  40823110 repo  |  40823110 site  |  40823132 repo |  40823132 site stage1-ag15 repo  |  stage1-ag15 site  |  40823126 repo  |  40823126 site  |  40823128 repo  |  40823128 site stage1-ag16 repo  |  stage1-ag16 site  |  40823146 repo  |  40823146 site  |  40823114 repo  |  40823114 site stage1-ag17 repo  |  stage1-ag17 site  |  40823142 repo  |  40823142 site  |  40823144 repo  |  40823144 site stage1-ag18 repo  |  stage1-ag18 site  |  40823135 repo  |  40823135 site  |  40823121 repo  |  40823121 site stage1-ag19 repo  |  stage1-ag19 site  |  40823123 repo  |  40823123 site  |  40823136 repo  |  40823136 site stage1-ag20 repo  |  stage1-ag20 site  |  40823127 repo  |  40823127 site  |  40823148 repo  |  40823148 site stage1-ag21 repo  |  stage1-ag21 site  |  40823152 repo  |  40823152 site  |  40823153 repo  |  40823153 site stage1-ag22 repo  |  stage1-ag22 site  |  40823151 repo  |  40823151 site  |  40871106 repo  |  40871106 site stage1-ag23 repo  |  stage1-ag23 site  |  40823116 repo  |  40823116 site  |  40823131 repo  |  40823131 site \n 2b stage1 分組: \n stage1-bg1 repo  |  stage1-bg1 site  |  40823245 repo  |  40823245 site  |  40823251 repo  |  40823251 site stage1-bg2 repo  |  stage1-bg2 site  |  40823234 repo  |  40823234 site  |  40823235 repo  |  40823235 site stage1-bg3 repo  |  stage1-bg3 site  |  40823206 repo  |  40823206 site  |  40823207 repo  |  40823207 site stage1-bg4 repo  |  stage1-bg4 site  |  40723215 repo  |  40723215 site  |  40723128 repo  |  40723128 site stage1-bg5 repo  |  stage1-bg5 site  |  40823238 repo  |  40823238 site  |  40823218 repo  |  40823218 site stage1-bg6 repo  |  stage1-bg6 site  |  40823214 repo  |  40823214 site  |  40823225 repo  |  40823225 site stage1-bg7 repo  |  stage1-bg7 site  |  40823212 repo  |  40823212 site  |  40823236 repo  |  40823236 site stage1-bg8 repo  |  stage1-bg8 site  |  40823208 repo  |  40823208 site  |  40823246 repo  |  40823246 site stage1-bg9 repo  |  stage1-bg9 site  |  40823201 repo  |  40823201 site  |  40823217 repo  |  40823217 site stage1-bg10 repo  |  stage1-bg10 site  |  40723106 repo  |  40723106 site  |  40723139 repo  |  40723139 site  |  40723143 repo |  40723143 site stage1-bg11 repo  |  stage1-bg11 site  |  40823205 repo  |  40823205 site  |  40823239 repo  |  40823239 site stage1-bg12 repo  |  stage1-bg12 site  |  40823202 repo  |  40823202 site  |  40823203 repo  |  40823203 site stage1-bg13 repo  |  stage1-bg13 site  |  40823223 repo  |  40823223 site  |  40823224 repo  |  40823224 site stage1-bg14 repo  |  stage1-bg14 site  |  40823228 repo  |  40823228 site  |  40823242 repo  |  40823242 site stage1-bg15 repo  |  stage1-bg15 site  |  40823211 repo  |  40823211 site  |  40823216 repo  |  40823216 site stage1-bg16 repo  |  stage1-bg16 site  |  40823221 repo  |  40823221 site  |  40823237 repo  |  40823237 site stage1-bg17 repo  |  stage1-bg17 site  |  40832244 repo  |  40832244 site  |  40823250 repo  |  40823250 site stage1-bg18 repo  |  stage1-bg18 site  |  40823209 repo  |  40823209 site  |  40823210 repo  |  40823210 site stage1-bg19 repo  |  stage1-bg19 site  |  40823219 repo  |  40823219 site  |  40823231 repo  |  40823231 site stage1-bg20 repo  |  stage1-bg20 site  |  40823213 repo  |  40823213 site  |  40823232 repo  |  40823232 site stage1-bg21 repo  |  stage1-bg21 site  |  40823247 repo  |  40823247 site  |  40823248 repo  |  40823248 site stage1-bg22 repo  |  stage1-bg22 site  |  40823222 repo  |  40823222 site  |  40823244 repo  |  40823244 site stage1-bg23 repo  |  stage1-bg23 site  |  40723224 repo  |  40723224 site  |  40623144 repo  |  40623144 site stage1-bg24 repo  |  stage1-bg24 site  |  40823204 repo  |  40823204 site  |  40823220 repo  |  40823220 site stage1-bg25 repo  |  stage1-bg25 site  |  40823241 repo  |  40823241 site  |  40823227 repo  |  40823227 site stage1-bg26 repo  |  stage1-bg26 site  |  40723233 repo  |  40723233 site  |  40723141 repo  |  40723141 site stage1-bg27 repo  |  stage1-bg27 site  |  40423155 repo  |  40423155 site  |  40823233 repo  |  40823233 site stage1-bg28 repo  |  stage1-bg28 site  |  40723140 repo  |  40723140 site  |  40723135 repo  |  40723135 site stage1-bg29 repo  |  stage1-bg29 site  |  40623251 repo  |  40623251 site  |  40823230 repo  |  40823230 site', 'tags': '', 'url': 'Stage1.html'}, {'title': 'W2', 'text': '利用下列程式查驗尚未納分組人員: \n #https://nfulist.herokuapp.com/?semester=1092&courseno=0764&column=True\n\'\'\'\n2021 spring:\n0741 1a\n0764 2a\n0776 2b\n2384 5j\n\'\'\'\n# for read data from url\nimport urllib.request\n# for execution through proxy\nimport os\n# for converting 2d list into 1d\nfrom itertools import chain \n \nproxy = \'http://[2001:288:6004:17::69]:3128\'\n \nos.environ[\'http_proxy\'] = proxy \nos.environ[\'HTTP_PROXY\'] = proxy\nos.environ[\'https_proxy\'] = proxy\nos.environ[\'HTTPS_PROXY\'] = proxy\n\n# read data from url\nwith urllib.request.urlopen(\'https://nfulist.herokuapp.com/?semester=1092&courseno=0764&column=True\') as response:\n   html = response.read().decode(\'utf-8\')\n\n# split data with "</br>" into list, up to here we get the student list of the cd2021 2a\nUdata = html.split("</br>")\n#print("total:" + str(len(Udata)))\n\n# set group as vacent list\ngroup = []\n# open w2_a_list.txt which copied from http://c.kmol.info:8000/o616appencye at 2021/03/04 15:00\nwith open("w2_a_list.txt") as file: \n    content = file.readlines()\nfor i in range(len(content)):\n    data = content[i].rstrip("\\n").split("\\t")\n    group.append(data)\n#print(group)\n\n# converting 2d list into 1d \n# using chain.from_iterables \nflatten_group= list(chain.from_iterable(group)) \nfor stud in Udata:\n    if stud not in flatten_group:\n        print(stud)\n\n\n \n 2a 初步查驗結果: \n \n 2b 初步查驗結果: \n \n 2a stage1 分組名單 \n 2b stage1 分組名單', 'tags': '', 'url': 'W2.html'}, {'title': 'cmsimde', 'text': '修改動機: \n 1. 希望動態系統能夠直接在倉儲根目錄中直接以 cms.bat 啟動, 無需進入 cmsimde 子目錄中操作. \n 只要建立一個 cms.bat 內容為 python cmsimde/wsgi.py 即可. \n 2. 為了能夠在倉儲根目錄執行 wsgi.py, 必須將 localhost.key 與 localhost.crt 從 cmsimde 移到 up_dir 目錄. \n 3. localhost.key 與 localhost.crt 可以在命令列中執行 sh.exe 後, 以下列命令完成: \n openssl req -x509 -nodes -days 365 -newkey rsa:4096 -keyout localhost.key -out localhost.crt \n 4. 若已經採用 ssh 推送, 能否直接使用 acp.bat 加上提交字串完成 git add commit push. 其內容為: \n acp.bat 內容 \n echo off\nset message=%1\ngit add .\ngit commit -m %message%\ngit push \n cms.bat 內容: python cmsimde/wsgi.py \n up.bat 內容: \n @echo off\nrobocopy up_dir ./../ /E \n', 'tags': '', 'url': 'cmsimde.html'}, {'title': 'Wink3', 'text': '在電腦輔助設計室可以下載  http://a.kmol.info:88/wink3.7z \n Wink 官方網站 \n Wink user guide.pdf \n Wink3 tutorial 1: \n \n Wink 3 tutorial 2: \n', 'tags': '', 'url': 'Wink3.html'}, {'title': 'Group Project', 'text': 'W1: 課程說明 \n 2D 工程圖, 3D 爆炸圖, BOM, 設計分析規劃簡報 (html) 與產品設計報告書 (pdf) \n 設計工具, 設計動機, 協同設計方法與流程, 設計結果與自評 \n 每週分組報告必須包含 html, pdf 與 Youtube 影片: \n 標題: 2021-協同產品設計實習-stage1-ag1 \n 專題題目: \n 第一位組員學號:( Curriculum Vitae 範例 ) \n 第二位組員學號:( CV 範例 ) \n 其他組員學號: \n 參考: \n Math: \n http://mde.tw/cad2020/content/Sigmoid.html \n Onshape: \n https://www.onshape.com/en/resource-center/articles/6-challenges-in-machine-design-part-1 \n https://news.aucotec.com/how-to-solve-the-5-top-engineering-design-challenges/ \n http://mde.tw/cad2020/content/Onshape.html \n Coppeliasim: \n https://www.coppeliarobotics.com/helpFiles/index.html \n http://mde.tw/cad2020/content/CoppeliaSim.html \n Webots: \n https://cyberbotics.com/doc/guide/index \n https://cyberbotics.com/doc/discord/ \n https://discord.com/invite/nTWbN9m \n http://mde.tw/cd2019/content/Webots%20doc.html \n http://mde.tw/webots_R2019a/ \n https://github.com/mdecourse/webots_R2019a \n CAE: \n https://en.wikipedia.org/wiki/Abaqus \n https://www.standoutvitae.com/article/gautampuri050534/abaqus-fea-tutorial-series/ \n https://freefem.org/ \n https://github.com/mdecourse/range3 \n https://ngsolve.org/ \n Presentation: \n https://www.debugmode.com/wink/ \n PDF: \n https://github.com/annProg/PanBook \n use Pandoc and LaTeX \n https://www.itread01.com/content/1546783751.html \n Projects: \n https://www.diva-portal.org \n mechaical design related project reports  \n toward_a_theory_of_engineeing_design.pdf  (for @gm users only) \n Development of a Fast Pick-and-Place Robot with cylindrical drive.pdf \n transmission device patent  ( ref ) \n slide-o-cam transmission device \n https://github.com/mdecourse/tinyc.games \n https://publications.gbdirect.co.uk//c_book/ \n https://github.com/Immediate-Mode-UI/Nuklear \n ps2020: \n https://github.com/mdecourse/ps2020 \n ps2020_ref  (for @gm users only) \n robots: \n http://www.cim.mcgill.ca/~rmsl/Index/RVS4W.htm \n ref  (for @gm users only) \n Design_Prototyping_Interfacing_and_Control_of_Schonflies_motion_generator \n Optimization: \n single-variable optimization \n optimum_design_lecture_notes \n fundamental_multivariable optimization \n constrained optimization \n orthogonal-decomposition for constrained optimization \n inequality-constrained optimization \n optimum design course \n oda.c \n cursyn.c \n ODA functions basic.7z \n ODA functions arbitrary.7z \n index \n 兩人一組產品開發 (stage1) \n W2-W3 \n 兩人共同快速 (兩週) 開發一組產品設計與實作模擬 (分組自評與互評, 說明遭遇問題與解決方法) \n W4 上課之前必須將各組報告 html, pdf 與 Youtube 影片連結繳交至  2021 協同產品設計實習 W4 分組專題報告與影片繳交處  \n W4: 報告與檢討 (一週) \n 四人一組產品開發 (stage2) \n W5-W8 \n 四人共同快速 (四週) 開發一組產品設計與實作模擬 (分組自評與互評, 說明遭遇問題與解決方法) \n W9 上課之前必須將各組報告 html, pdf 與 Youtube 影片連結繳交至  2021 協同產品設計實習 期中 (W9) 分組專題報告與影片繳交處  \n W9: 期中檢討報告與評分 \n 八人一組產品開發 (stage3) \n W10-W17 \n 八人共同快速 (八週) 開發一組產品設計與實作模擬 (分組自評與互評, 說明遭遇問題與解決方法) \n W18 上課之前必須將各組報告 html, pdf 與 Youtube 影片連結繳交至  2021 協同產品設計實習 期末 (W18) 分組專題報告與影片繳交處  \n W18: 期末檢討報告與評分', 'tags': '', 'url': 'Group Project.html'}, {'title': 'Programming', 'text': 'https://www.gnu.org/education/edu-schools.zh-tw.html  (為什麼學校只應採用自由軟體) \n 相同概念: Why Engineers Should Exclusively Use English \n 四設一甲網際內容管理:  https://nfulist.herokuapp.com/?semester=1092&courseno=0741&column=True \n 五精一甲網際內容管理:\xa0 https://nfulist.herokuapp.com/?semester=1092&courseno=2384&column=True \n 四設二甲協同產品設計實習:  https://nfulist.herokuapp.com/?semester=1092&courseno=0764&column=True \n 四設二乙協同產品設計實習:  https://nfulist.herokuapp.com/?semester=1092&courseno=0776&column=True \n 原始碼:  https://github.com/mdecourse/nfulist \n 上述程式的 \n 服務對象: 希望透過網際模式取得特定課程修課人員名單的用戶. \n 價值: 可以在教務修課資料持續維護的任何時段, 即時取得當時的最新資料. \n 可重用時機: 透過相同模式讓機械設計工程師在任何設計階段, 即時取得當時與設計流程有關的最新資料. \n 討論: \n 在多人整合模式下的產品設計流程中, 採網際程式流程進行設計時, 若能以動態協同互動的機制整合, 將可有效透過網路, 電腦程式與即時資料進行設計最佳化. \n 實習: \n https://ethercalc.net  或自行利用 Ubuntu 20.04 及  https://github.com/audreyt/ethercalc \n \xa0建立 ethercalc 伺服主機 (請參考:  http://mde.tw/cad2020/content/Ethercalc.html  ) \n https://github.com/audreyt/ethercalc/blob/master/API.md \n https://ethercalc.docs.apiary.io/ \n https://github.com/mdecourse/ethercalc-python \n https://www.aosabook.org/en/posa/from-socialcalc-to-ethercalc.html \n https://www.mdeditor.tw/pl/2XA2/zh-tw \n hello_ethercalc.py \n #!/usr/bin/env python3\nimport ethercalc\nimport pprint\n\npp = pprint.PrettyPrinter(indent=4)\ne = ethercalc.EtherCalc("http://140.130.17.17:8000")\n# http://140.130.17.17:8000/kkcao0lc2ew7\nprint(e)\n# 設定 id 為 kkcao0lc2ew7 的 sheet C1 值為 number 2\ne.command("kkcao0lc2ew7", ["set C1 value n 2"])\n# C2 設為字串 "電腦輔助設計", 但是字串前面必須加一個單引號\ne.command("kkcao0lc2ew7", [ethercalc.set("C2", "\'電腦輔助設計")])\ne.command("kkcao0lc2ew7", [ethercalc.set("C3", 3),\n                                           ethercalc.set("C4", 4),\n                                           # C5 為 C3+C4\n                                           ethercalc.set("C5", "=C3+C4"),\n                                          ])\npp.pprint(e.cells("kkcao0lc2ew7"))\npp.pprint(e.cells("kkcao0lc2ew7", "C5"))\npp.pprint(e.export("kkcao0lc2ew7"))\n \n 上述程式執行結果: \n <ethercalc.EtherCalc object at 0x000001DD9D7195E0>\n{   \'C1\': {   \'coord\': \'C1\',\n              \'datatype\': \'v\',\n              \'datavalue\': 2,\n              \'formula\': \'\',\n              \'readonly\': False,\n              \'valuetype\': \'n\'},\n    \'C2\': {   \'coord\': \'C2\',\n              \'datatype\': \'t\',\n              \'datavalue\': \'電腦輔助設計\',\n              \'formula\': \'\',\n              \'readonly\': False,\n              \'valuetype\': \'t\'},\n    \'C3\': {   \'coord\': \'C3\',\n              \'datatype\': \'v\',\n              \'datavalue\': 3,\n              \'formula\': \'\',\n              \'readonly\': False,\n              \'valuetype\': \'n\'},\n    \'C4\': {   \'coord\': \'C4\',\n              \'datatype\': \'v\',\n              \'datavalue\': 4,\n              \'formula\': \'\',\n              \'readonly\': False,\n              \'valuetype\': \'n\'},\n    \'C5\': {   \'coord\': \'C5\',\n              \'datatype\': \'f\',\n              \'datavalue\': 7,\n              \'formula\': \'C3+C4\',\n              \'parseinfo\': [   {\'opcode\': 0, \'text\': \'C3\', \'type\': 2},\n                               {\'opcode\': \'+\', \'text\': \'+\', \'type\': 3},\n                               {\'opcode\': 0, \'text\': \'C4\', \'type\': 2}],\n              \'readonly\': False,\n              \'valuetype\': \'n\'}}\n{   \'coord\': \'C5\',\n    \'datatype\': \'f\',\n    \'datavalue\': 7,\n    \'formula\': \'C3+C4\',\n    \'parseinfo\': [   {\'opcode\': 0, \'text\': \'C3\', \'type\': 2},\n                     {\'opcode\': \'+\', \'text\': \'+\', \'type\': 3},\n                     {\'opcode\': 0, \'text\': \'C4\', \'type\': 2}],\n    \'readonly\': False,\n    \'valuetype\': \'n\'}\n[   [None, None, 2.0],\n    [None, None, \'電腦輔助設計\'],\n    [None, None, 3.0],\n    [None, None, 4.0],\n    [None, None, 7.0]] \n 有關 ethercalc: \n 若 ethercalc 與 redis 合用, sheet 資料將會存入 /var/lib/redis/dump.rdb, 此一檔案儲存設定位於 /etc/redis/redis.conf 中的 dbfilename dump.rdb \n 使用者若要以 root 身分檢視 /var/lib/redis/dump.rdb 可以透過 sudo -s 以 root 身分執行命令. \n 若以 /etc/init.d/redis-server stop 關閉 redis, 然後執行 ethercalc, sheet 資料將會存在執行命令目錄下的 dump 目錄中. \n 在結合 redis 使用下的 ethercalc, 若希望 reset /var/lib/redis/dump.rdb 中的資料: \n sudo -s \n /etc/init.d/redis-server stop \n rm /var/lib/redis/dump.rdb \n /etc/init.d/redis-server start \n ethercalc \n 則 /var/lib/redis/dump.rdb 中為空資料. \n 有關 GDrive: \n 教育版 GDrive 無限空間期限到 2022/07, 之後一個學校總人數不到 20000 者免費額度將只有 100TB, 額外空間則必須付費.  https://support.google.com/a/answer/10403871 \n 我們是否能夠延伸  https://github.com/mdecourse/cd2020pj1  利用 GDrive API, 寫一個方便管理或轉移相關檔案的網際系統程式? \n 參考: \n https://github.com/wkentaro/gdown \n 有關 ps2020: \n https://github.com/mdecourse/ps2020/discussions/3 \n https://fossil.kmol.info/ps2020 \n https://github.com/mdecourse/ps2020 \n https://github.com/KmolYuan/Pyslvs-UI \n \n', 'tags': '', 'url': 'Programming.html'}, {'title': 'git config', 'text': 'y:\\home\\.gitconfig settings: \n git config --global user.email "your github account associated email address" \n git config --global user.name "your github account name" \n Default pull stratege: pull = fetch + merge \n git config --global pull.rebase false \n', 'tags': '', 'url': 'git config.html'}, {'title': 'Reveal', 'text': 'Why Reveal.js? \n https://revealjs.com/ \n', 'tags': '', 'url': 'Reveal.html'}, {'title': 'Blogs', 'text': 'Why Blogs? \n https://www.blogger.com \n https://blog.getpelican.com/ \n https://fossil.kmol.info/fosgit/doc/0f7bf53ab9/content/index.html \n', 'tags': '', 'url': 'Blogs.html'}, {'title': 'LaTeX or Word', 'text': 'Why LaTeX? \n https://en.wikibooks.org/wiki/LaTeX/Collaborative_Writing_of_LaTeX_Documents \n https://www.natureindex.com/news-blog/three-ways-to-collaborate-on-writing \n https://www.authorea.com/ \n https://github.com/PHPirates/travis-ci-latex-pdf \n https://medium.com/@baymac/continuous-integration-of-latex-documents-using-travis-ci-a1916c89e978 \n https://dfm.io/posts/travis-latex/ \n \n \n', 'tags': '', 'url': 'LaTeX or Word.html'}, {'title': 'CAD', 'text': '', 'tags': '', 'url': 'CAD.html'}, {'title': 'Onshape', 'text': "https://cad.onshape.com \n What's new in Onshape 1.124 We've added new functionality to Onshape since your last sign in.  Click to learn more . \n Your Free subscription only allows public data. Try Onshape Professional to create, edit and share private data with your team \n https://www.onshape.com/en/pricing \n Standard: $1,500 per user, per year \n Professional: $2,100 per user, per year \n https://www.onshape.com/en/resource-center/ \n https://cad.onshape.com/FsDoc/ \n https://forum.onshape.com/discussions/tagged/api/p1 \n https://github.com/onshape \n https://cad.onshape.com/help/Content/realtimecollaboration.htm \n https://www.onshape.com/en/resource-center/articles/3-ways-to-improve-your-cad-collaboration \n \n \n \n", 'tags': '', 'url': 'Onshape.html'}, {'title': 'Solidworks', 'text': 'https://www.solidworks.com/ \n Download Solidworks 2017 DVD  (for @gm users only) - permanent license for 500 vpn users \n', 'tags': '', 'url': 'Solidworks.html'}, {'title': 'Inventor', 'text': 'https://www.autodesk.com/products/inventor/overview \n', 'tags': '', 'url': 'Inventor.html'}, {'title': 'Solvespace', 'text': 'https://solvespace.com \n', 'tags': '', 'url': 'Solvespace.html'}, {'title': 'Simulation', 'text': 'https://github.com/mdecourse/Bipedal \n https://github.com/mdecourse/biped_trajectory_optimization \n https://cyberbotics.com/doc/guide/samples-howto#passive_dynamic_walker-wbt \n https://github.com/m2n037/awesome-mecheng \n https://github.com/NicoSchlueter/HelicalGearPlus \n https://github.com/fangohr/introduction-to-python-for-computational-science-and-engineering \n https://github.com/mdecourse/AutoCkt \n https://github.com/rsmith-nl/beammech \n https://github.com/mdecourse/SolveSpace-Daily-Engineering  ( video ) \n https://github.com/KmolYuan/program-learning \n https://github.com/mdecourse/FreeCAD_Mod_Dev_Guide \n https://arnemertz.github.io/online-compilers/ \n', 'tags': '', 'url': 'Simulation.html'}, {'title': 'CoppeliaSim', 'text': 'https://www.coppeliarobotics.com/ \n', 'tags': '', 'url': 'CoppeliaSim.html'}, {'title': 'Webots', 'text': 'https://cyberbotics.com/ \n https://robotbenchmark.net/ \n', 'tags': '', 'url': 'Webots.html'}, {'title': 'Pybullet', 'text': 'https://pybullet.org/ \n', 'tags': '', 'url': 'Pybullet.html'}, {'title': 'CAE', 'text': '', 'tags': '', 'url': 'CAE.html'}, {'title': 'Abaqus', 'text': 'https://www.3ds.com/products-services/simulia/products/abaqus/ \n Download Abaqus 2020 DVD  (for @gm users only) - License up to 2021/08/08 \n', 'tags': '', 'url': 'Abaqus.html'}, {'title': 'Comsol', 'text': 'https://www.comsol.com/ \n', 'tags': '', 'url': 'Comsol.html'}, {'title': 'ANSYS', 'text': 'https://www.ansys.com/ \n', 'tags': '', 'url': 'ANSYS.html'}, {'title': 'Range3', 'text': 'https://github.com/Range-Software/range3 \n', 'tags': '', 'url': 'Range3.html'}, {'title': 'NGSolve', 'text': 'https://ngsolve.org/ \n', 'tags': '', 'url': 'NGSolve.html'}, {'title': 'Prototyping', 'text': '', 'tags': '', 'url': 'Prototyping.html'}, {'title': '3D printing', 'text': 'https://github.com/mdecourse/virtualkossel \n http://mde.tw/virtualkossel/ \n https://en.wikipedia.org/wiki/Hangprinter \n https://gcode.ws/ \n http://shapeforge.loria.fr/vrprinter/', 'tags': '', 'url': '3D printing.html'}]};