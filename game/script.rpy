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

    class place:
        def __init__(self, location):
            self.location = location


    class Fighter:
        def __init__(self, name, level=1, max_hp=10, hp=10, max_mp=4, mp=4, attack=2, defense=1, element="None"):
            self.name = name
            self.level = level
            self.max_hp = max_hp
            self.hp = hp
            self.max_mp = max_mp
            self.mp = mp
            self.attack = attack
            self.defense = defense
            self.element = element

    def calculate_damage(attacker, defender):
        base_damage = attacker.attack - defender.defense
        return max(1, base_damage + random.randint(-1, 1))

screen battle_ui:
    frame:
        xpadding 13
        ypadding 14
        xalign 0.01 yalign 0.05
        vbox:
            text "[player.name] HP: [player.hp]/[player.max_hp]"
            text "MP: [player.mp]/[player.max_mp]"
    
    frame:
        xpadding 13
        ypadding 14
        xalign 0.99 yalign 0.05
        vbox:
            text "[enemy.name] HP: [enemy.hp]/[enemy.max_hp]"

screen location_ui:
    frame:
        xpadding 13
        ypadding 14
        xalign 0.99 yalign 0.02
        vbox:
            text "位置: [now_venue.location]" size 40


# Ren'Py 腳本部分
# 定義角色
# 定義角色
define j = Character("蔣中正")
define w = Character("王采玉")
define m = Character("毛福梅")
define d = Character("董顯光")
define n = Character("日本軍醫教官")
define c = Character("陳其美")
define z = Character("張群")
define s = Character("校長")
define sun = Character("孫中山")
define sol = Character("小兵")
define yao = Character("姚冶誠")
define zhang = Character("張靜江")
define chen = Character("陳潔如")
define chenm = Character("陳母")

define audio.gamemusic = "audio/chapter1.wav"

#圖檔區域 角色跟背景要分開放，每個人不同的背景也都要分開
image bg blackscreen = "bg blackscreen.png"
image bg yutai = "imgoldhouse"
image bg yutai2 = "imgyutai"

image bg imgchi1 = "imgchi1.jpg"
image bg imgchi2 = "imgchi2.jpg"
image bg imgchi3 = "imgchi3(AI).png"
image bg imgchi4 = "imgchi4.jpg"
image bg imgchi5 = "imgchi5(AI).png"
image bg imgchi6 = "imgchi6.png"
image bg imgchi7 = "imgchi7.jpg"
image bg imgchi8 = "imgchi8.jpg"
image bg imgchi9 = "imgchi9(AI).png"
image bg imgchi10 = "imgchi10.jpg"
image bg imgchi11 = "imgchi11.jpg"
image bg imgchi12 = "imgchi12.jpg"
image bg imgchi13 = "imgchi13.jpg"

image johndraw = "johndraw.png"
image maofumei = "maofumei.png"
image maofumeicry = "maofumeicry.png"
image maofumei happy = "maofumeihappy.png"


image minion idle = "johndraw.png"
image minion attack = "johndraw.png"
image minion hit = "johndraw.png"
image enemyminion idle = "maofumei.png"
image enemyminion attack = "maofumei.png"
image enemyminion hit = "maofumeicry.png"

image chenqimei = "maofumei.png"
image zhangqun = "maofumei.png"
image chenmother = "maofumei.png"
image principal = "maofumei.png"
image sunzhongshan = "sunzhongshan.png"
image soldier = "maofumei.png"
image zhangdynasty = "maofumei.png"
image Maozedong = "Maozedong@2.PNG"

image paper1 = "paper.jpg"
image flag1 = "flag1.png"
image dust = "dust.png"
image dustbroken = "dustbroken.png"

#角色動作的線性變化區域
transform bounce:
    yalign 1.0
    linear 3.0 xalign 0
    linear 3.0 xalign 1.0
    repeat

transform left_to_right:
    yalign 1.0
    linear 1.0 xalign 1.0
    xzoom -1
    linear 1.0 xalign 0.0
    xzoom 1

transform left_to_right_out:
    yalign 1.0
    linear 1.0 xalign 1.5


transform left_to_right_out_slow:
    yalign 1.0
    linear 3.0 xalign 1.5
    

transform right_to_left:
    yalign 1.0
    linear 1.0 xalign 0.0
    xzoom -1
    linear 1.0 xalign 1.0
    xzoom 1

label battle_system:
    $ player = Fighter("我方士兵", level=1, max_hp=20, hp=20, max_mp=10, mp=10, attack=3, defense=2)
    $ enemy = Fighter("敵方士兵", level=1, max_hp=15, hp=15, attack=3, defense=1)
    scene bg imgchi8
    hide screen location_ui
    show screen battle_ui

    show johndraw at left
    show Maozedong at right

    while player.hp > 0 and enemy.hp > 0:
        # 玩家回合
        menu:
            "攻擊":

                show johndraw at left_to_right
                pause 2
                $ damage = calculate_damage(player, enemy)
                $ enemy.hp -= damage
                "你對[enemy.name]造成了[damage]點傷害！"
            "特殊技能" if player.mp >= 3:
                $ player.mp -= 3
                $ damage = calculate_damage(player, enemy) * 2
                $ enemy.hp -= damage
                "你使用特殊技能，對[enemy.name]造成了[damage]點傷害！"
            "防禦":
                $ player.defense += 1
                "你提高了防禦力！"

        if enemy.hp <= 0:
            "你贏了戰鬥！"
            hide screen battle_ui
            return "victory"

        # 敵人回合
        show Maozedong at right_to_left
        pause 2
        $ damage = calculate_damage(enemy, player)
        $ player.hp -= damage
        "[enemy.name]對你造成了[damage]點傷害！"

        if player.hp <= 0:
            "你輸了戰鬥..."
            hide screen battle_ui
            return "defeat"


# 遊戲開始
label start:
    play music gamemusic
    jump chapter1_act1


# 第一幕：家世背景
label chapter1_act1:
    scene bg yutai
    with fade
    $ now_venue = place("玉泰鹽鋪")
    "第一章：早年生活與革命生涯"


    show screen location_ui
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
    
    $ now_venue.location = "奉化蔣家外"
    "1895年，奉化蔣家外"

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

    $ now_venue.location = "蔣家內"
    "1901年冬，蔣家內"

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
    show maofumei:
        yalign 1.0
        linear 0.5 xalign 0.6
        xzoom -1
        linear 0.5 xalign 0.45

    m "我該不會這輩子就這樣了吧...."
    show maofumei:
        yalign 1.0
        xzoom -1
        linear 2.5 xalign -0.5
    w "!!!!!!! 這孩子，怎麼在這種時候還這麼調皮!"

    voice "voichi3.wav"
    j "我當時還是個頑童，不懂事。這句奉化諺語 '新郎拾蒂頭，夫妻難到頭' 竟成了預言。這場婚姻從一開始就缺乏感情基礎。"
    
    scene bg imgchi2
    "新婚之夜"
    show johndraw:
        yalign 1.0
        xalign -0.5
        linear 3.0 xalign 0.71
        transform_anchor True
        linear 0.5 rotate 65

    "蔣中正疲倦地進入新房，倒在床上就睡"
    show maofumeicry
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
    $ now_venue = place("奉化鳳麓學堂")
    "1903年，奉化鳳麓學堂"

    show johndraw
    d "蔣同學，你又在看報紙了？"
    show paper1:
        yalign 0.25 
        xalign 0.5
    hide johndraw 
    j "是的，董老師。我覺得了解時事很重要。"
    d "很好。但不要忘了課本上的內容。"
    show johndraw
    hide paper1
    j "老師，您覺得我們應該如何改變中國的命運？"
    d "這個問題很深奧。也許你應該先學好英文，看看外面的世界是什麼樣子。"

    jump chapter1_act5

# 第五幕：首次赴日
label chapter1_act5:
    scene bg imgchi4
    with fade
    $ now_venue = place("上海碼頭")
    "1906年4月，上海碼頭"
    show johndraw

    j "母親，我一定會在日本好好學習，為祖國爭光。"
    w "中正，要記住你的初心。無論遇到什麼困難，都不要放棄。"
    j "我明白，母親。我會努力的。"
    show johndraw at left_to_right_out
    pause 2
    hide johndraw
    voice "voichi5.wav"
    j "結果，在我抵達日本後，才發現公費生不能入軍校，只好在同年冬天返回中國，並進入了清政府開辦的陸軍速成學堂"

    scene bg imgchi5
    $ now_venue = place("陸軍速成學堂")
    "陸軍速成學堂，學校教室"

    show dust:
        yalign 0.45 
        xalign 0.5
    n "(引取一立方寸的土放在講桌上) 這一塊土約一立方寸，可容納四萬萬微生蟲。 這一立方寸的土，好比中國一國。中國有四萬萬人，好比微生蟲寄生在這土裡一樣。"
    hide dust
    with fade
    show dustbroken:
        yalign 0.45 
        xalign 0.5
    j "(蔣中正聽後非常生氣，衝上講臺，把泥土碎成八塊) 日本有五千萬人，是否也像五千萬微生蟲，寄生在這八分之一方寸的土塊中？"
    n "........... 你是不是革命黨？??"
    j "..........."

    voice "voichi6.wav"
    "由於我在陸軍速成學堂深受校長和教官賞識，第二年就成為第一批派往日本深造之四人之一。"

# 第六幕：加入同盟會
label chapter1_act6:
    scene bg imgchi6
    with fade
    $ now_venue = place("東京")
    "1908年，東京"

    show chenqimei at right
    show johndraw at left
    show flag1:
        yalign 0.45 
        xalign 0.5
    c "中正，我想邀請你加入同盟會。我們需要像你這樣有志之士。"
    "這是同盟會的旗幟圖案"(what_color="#808080")
    j "陳大哥，同盟會的宗旨是什麼？"
    c "驅除韃虜，恢復中華，建立民國，平均地權。"
    j "這與我的理想相符。我願意加入。"
    c "很好。記住，革命是一條艱難的道路，需要堅強的意志。"
    j "我明白。我已經準備好了。"

# 第七幕：畢業與歸國
label chapter1_act7:
    scene bg imgchi12
    with fade
    $ now_venue = place("日本振武學校")
    "1910年11月，日本振武學校畢業典禮"

    show johndraw 

    s "蔣中正同學，你的成績雖然不是最好的，但你的愛國熱情令人欽佩。"
    j "感謝校長的教誨。我會將在這裡學到的知識用於振興中華。"

    z "中正，聽說你要去陸軍實習？"
    j "是的，這是一個難得的機會，可以學習日本軍隊的先進經驗。"
    z "不要忘記我們的初心。總有一天，我們要用這些知識來服務於我們自己的國家。"
    j "我永遠不會忘記的。"

# 第八幕：參加辛亥革命
label chapter1_act8:
    scene bg imgchi4
    with fade
    $ now_venue = place("上海碼頭")
    "1911年10月，上海碼頭"

    show johndraw

    j "張群，武昌起義的消息你聽說了嗎？"
    z "聽說了。看來我們等待已久的機會終於來了。"
    j "是啊，我們必須立即行動。陳其美大哥在上海已經開始準備了。"
    z "那我們趕快去找他吧。祖國需要我們了。"

    $ now_venue = place("陳其美居所")
    scene bg imgchi13 
    show chenqimei
    "上海，陳其美的住所"


    c "中正，你來得正好。我需要你率領一支敢死隊去杭州。"
    j "我明白。這是我們改變中國命運的機會，我不會辜負您的期望。"
    c "記住，革命是一項艱巨的事業。我們可能會失敗，但絕不能放棄。"
    j "我準備好了，無論付出什麼代價。"

    voice "voichi8.wav"
    "就這樣，我開始了我的革命生涯，為日後成為中國的領導人奠定了基礎。"

# 第九幕：革命與北伐
label chapter1_act9:
    scene bg imgchi8
    with fade
    $ now_venue = place("浙江杭州")
    "武昌起義開始，參加光復浙江之戰"

        
    "打倒你的敵人!"
    call battle_system
    if _return == "victory":
        "你成功了擊敗了敵人。"
    else:
        "你失敗了..."
        jump chapter1_act9
    show screen location_ui
    scene bg imgchi8

    show soldier at right
    show johndraw at left

    "小兵" "報告! 我們已攻佔巡撫府，俘虜增韞!"
    j "辛苦了，看來我們的第一步已經成功了。"

    scene black
    with fade
    "小兵" "杭州將軍投降了，浙江是我們的了。"

    "浙江之戰結束，成立新政府"

    voice "Voichi9.wav"
    "革命成功後，我的個人生活也發生了變化。"

# 第十幕：二次革命
label chapter1_act10:
    scene bg imgchi9
    with fade
    $ now_venue = place("中華革命黨總部")
    "1913年，中華革命黨總部"

    show sunzhongshan

    sun "今日中國革命的成敗，完全寄託在你身上。為什麼不去搞軍隊？革命要成功，必須要有軍隊。"
    j "先生您說的我會遵守，讓我們一起完成革命大業。"
    sun "我期待你的表現。你是否想要任何職位？"
    j "我蔣某人，不需要職位，只要先生能借我力量即可。"

    voice "voichi13.wav"
    "至此，我開始了我的軍政之路。"

    scene bg imgchi10
    with fade
    $ now_venue = place("上海")
    "1913年7月，上海"

    voice "voichi14.wav"
    "1913年7月，孫先生發動二次革命討伐袁世凱，我在上海討袁軍總司令陳其美的指揮下參加攻打江南製造局之役。"

    show chenqimei

    c "中正，我們必須奪取江南製造局，切斷袁世凱的軍火供應。"
    j "明白，我們一定要成功。"

    voice "voichi15.wav"
    "不幸的是，各地討袁軍先後失敗。上海滬軍都督楊善德下令緝捕我"

    voice "voichi16.wav"
    "我被迫逃進陳其美之娘姨姚冶誠臥室內，遂納姚納姚冶誠為側室。"

    show johndraw
    hide chenqimei

    j "姚小姐，謝謝你救了我。"
    "姚冶誠" "蔣先生不必客氣，我們都是為了革命。"
    "這是蔣中正的第二個老婆，毛福梅->姚冶誠"(what_color="#808080")

    voice "voichi17.wav"
    "這次革命失敗後，我深刻認識到軍事力量的重要性。我決心要建立一支強大的革命軍隊，為未來的革命事業做準備。"

# 第十一幕：新的愛情
label chapter1_act11:
    scene bg imgchi11
    with fade
    $ now_venue = place("張靜江家")
    "上海，張靜江家中，1919年"

    show johndraw

    "張靜江" "中正，來，我給你介紹一下。這是陳潔如，我女兒的同學。"
    j "陳小姐，幸會。"
    "陳潔如" "蔣先生好。"

    voice "voichi11.wav"
    "我對陳潔如一見鍾情，開始了熱烈的追求。"
    "這是蔣中正的第三個老婆，毛福梅->姚冶誠->陳潔如"(what_color="#808080")

    scene bg imgchi11
    with fade
    $ now_venue = place("陳氏宅")
    "陳家"

    show johndraw

    "陳母" "蔣先生，你已有妻妾，又無正當職業，我不能把女兒嫁給你。"
    j "請給我一個機會，我會證明自己的。"

    scene bg imgchi11
    with fade
    "陳家，幾個月後"

    j "陳母，我還是很喜歡陳潔如，請把她嫁給我"
    "陳母" "好吧，我同意了。"

    voice "voichi12.wav"
    "回顧我的婚姻生活，我確實有過四個妻子。當時覺得自己很幸運，但現在看來，我的行為確實有些不妥。"

    return