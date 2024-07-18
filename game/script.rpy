init python:
    import random
    import time
    import requests
    def get_first_title(url):
        try:
            response = requests.get(f'http://localhost:8000/get_title?url={url}')
            response.raise_for_status()
            data = response.json()
            return data['title']
        except requests.RequestException:
            return "未連上網路"

    url = "https://travel.ettoday.net/category/%E6%A1%83%E5%9C%92/"
    title_text = get_first_title(url)

# Ren'Py 腳本部分
# 定義角色
define j = Character("蔣中正")
define w = Character("王采玉")
define m = Character("毛福梅")
define d = Character("董顯光")
define n = Character("日本軍醫教官")

define audio.gamemusic = "audio/china.m4a"
image bg blackscreen = "bg blackscreen.png"
image bg yutai = "imgoldhouse"
image bg yutai2 = "imgyutai"

image bg imgchi1 = "imgchi1.jpg"
image bg imgchi2 = "imgchi2.jpg"
image bg imgchi3 = "imgchi3(AI).png"
image bg imgchi4 = "imgchi4.jpg"
image bg imgchi5 = "imgchi5(AI).png"
image bg imgchi6 = "imgchi6.jpg"
image bg imgchi7 = "imgchi7.jpg"
image bg imgchi8 = "imgchi8.jpg"
image bg imgchi9 = "imgchi9(AI).png"
image bg imgchi10 = "imgchi10.jpg"
image bg imgchi11 = "imgchi11.jpg"

image johndraw = "johndraw.png"
image maofumei = "maofumei.png"
image maofumeicry = "maofumeicry.png"
image maofumei happy = "maofumeihappy.png"

transform bounce:
    yalign 1.0
    linear 3.0 xalign 0
    linear 3.0 xalign 1.0
    repeat

transform left_to_right:
    yalign 1.0
    xalign 0.0
    linear 2.0 xalign 1.0
    repeat

# 遊戲開始
label start:
    play music gamemusic
    jump chapter1_act1

# 第一幕：家世背景
label chapter1_act1:
    scene bg yutai
    with fade

    "第一章：早年生活與革命生涯"

    show johndraw at left
    voice "john01_01.wav"
    j "我是西元1887年10月31日出生於浙江奉化溪口鎮玉泰鹽鋪。家裡很有錢，是當地的五大首富之一，我祖父開設的鹽鋪後來給我爸經營"
    


    show johnyoung at right
    voice "john01_02.wav"
    j "你看看，我年輕時有多帥"
    

    voice "john01_03.wav"
    j "我爸爸蔣肇聰曾與三房夫人結婚，其中王采玉是我的媽媽。"
    

    show wang:
        xalign 0.5
        yalign 0.5 
    j "右邊就是我的母親王采玉~"

    "OS:製作組每次看到照片就嚇到一次"(what_color="#808080")

    voice "voichi1.wav"
    j "接下來，我會講我的生平故事"
    
    voice "voichi2.wav"
    j "除了生平故事外，我還會講一些與我有關的歷史的故事"

    jump chapter1_act2

# 第二幕：家庭背景
label chapter1_act2:
    scene bg yutai2
    with fade
    
    "1895年，奉化溪口鎮蔣家"

    show wang at right:
        yalign 0.5
    show johndraw at left

    w "中正，你父親走了，今後家裡就靠你了。"
    j "母親，我一定會努力讀書，光耀門楣的。"
    w "孩子。記住，要刻苦讀書，但更要懂得做人的道理。"

    voice "voichi7.wav"
    "父親去世後，我由母親王采玉撫育成人。這段經歷深深影響了我的性格形成。"
    

    jump chapter1_act3

# 第三幕：婚姻
label chapter1_act3:
    scene bg imgchi1
    with fade

    "1901年冬，奉化蔣家"

    show johndraw at left
    show wang at right:
        yalign 0.5 

    j "母親，我才14歲，真的要結婚嗎？"
    w "中正，這是我們家族的決定。毛家姑娘比你大5歲，賢良淑德，會是個好媳婦的。"
    j "我明白了，母親。我會盡到丈夫的責任的。"

    hide johndraw
    hide wang

    "婚禮當天"

    show maofumei happy

    m "(獨自坐在新房裡，低聲自語) 新郎怎麼還不來？"

    hide maofumei happy
    "蔣中正在外面跟小孩子們搶爆竹蒂頭"
    show maofumei
    m "果然是小孩子....我居然要跟這種小孩"
    m "我該不會這輩子就這樣了吧...."
    show wang at right:
        yalign 0.5 
    w "(憂心忡忡) 這孩子，怎麼在這種時候還這麼調皮!"

    voice "voichi3.wav"
    j "我當時還是個頑童，不懂事。這句奉化諺語 '新郎拾蒂頭，夫妻難到頭' 竟成了預言。這場婚姻從一開始就缺乏感情基礎。"
    
    scene bg imgchi2
    "新婚之夜"
    show johndraw at right:
        xzoom -1

    "蔣中正疲倦地進入新房，倒在床上就睡"
    show maofumeicry at left
    "毛福梅默默地看著熟睡的丈夫，眼中含淚"
    m"討厭... 嫁給不認識的小孩，還要被這樣對待"
    m"真希望以後情況能越變越好..."

    voice "voichi4.wav"
    j "毛福梅雖然比我大，但她對我母親很孝順。這是維繫我們關係的重要原因。"
    

    jump chapter1_act4

# 第四幕：求學
label chapter1_act4:
    scene bg imgchi3
    with fade
    "1903年，奉化鳳麓學堂"

    show johndraw at left
    d "蔣同學，你又在看報紙了？"
    j "是的，董老師。我覺得了解時事很重要。"
    d "很好。但不要忘了課本上的內容。"
    j "老師，您覺得我們應該如何改變中國的命運？"
    d "這個問題很深奧。也許你應該先學好英文，看看外面的世界是什麼樣子。"

    jump chapter1_act5

# 第五幕：首次赴日
label chapter1_act5:
    scene bg imgchi4
    with fade

    "1906年4月，上海碼頭"
    show johndraw at left

    j "母親，我一定會在日本好好學習，為祖國爭光。"
    w "中正，要記住你的初心。無論遇到什麼困難，都不要放棄。"
    j "我明白，母親。我會努力的。"
    
    voice "voichi5.wav"
    j "結果，在我抵達日本後，才發現公費生不能入軍校，只好在同年冬天返回中國，並進入了清政府開辦的陸軍速成學堂"
    

    scene bg imgchi5
    "學校教室"

    n "(引取一立方寸的土放在講桌上) 這一塊土約一立方寸，可容納四萬萬微生蟲。 這一立方寸的土，好比中國一國。中國有四萬萬人，好比微生蟲寄生在這土裡一樣。"
    j "(蔣中正聽後非常生氣，衝上講臺，把泥土碎成八塊) 日本有五千萬人，是否也像五千萬微生蟲，寄生在這八分之一方寸的土塊中？"
    n "........... 你是不是革命黨？"
    j "..........."

    voice "voichi6.wav"
    "由於我在陸軍速成學堂深受校長和教官賞識，第二年就成為第一批派往日本深造之四人之一。"
    

    return