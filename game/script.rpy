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

define xueliang = Character("張學良")
define guard = Character("守衛")
define xiaozhen = Character("蔣孝鎮")
define soldier = Character("東北軍士兵")
define yang = Character("楊虎城")
define zhou = Character("周恩來")


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

image bg imgfeng1 = "imgfeng1.png"
image bg imgfeng2 = "imgfeng2.png"
image bg imgfeng3 = "imgfeng3.png"
image bg imgfeng4 = "imgfeng4.png"
image bg imgfeng5 = "imgfeng5.png"
image bg imgfeng6 = "imgfeng6.png"


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

image chenqimei = "chenqimei.png"
image chenqimei glasses = "chenqimeiglasses.png"
image zhangqun = "maofumei.png"
image chenmother = "maofumei.png"
image principal = "maofumei.png"
image sunzhongshan = "sunzhongshan.png"
image minion = "minion.png"
image soldier = "minion.png"
image minionenemy = "minionenemy.png"
image zhangdynasty = "maofumei.png"
image Maozedong = "Maozedong@2.PNG"
image wang2 = "wang@7.png"
image johnkid = "johnyoung@7.png"
image johnkidsad = "johnyoungsad@7.png"

image johnyoungpic = "johnyoung1.jpg"

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

    show minion at left
    show minionenemy at right

    while player.hp > 0 and enemy.hp > 0:
        # 玩家回合
        menu:
            "攻擊":

                show minion at left_to_right
                $ renpy.block_rollback()
                pause 2
                $ damage = calculate_damage(player, enemy)
                $ enemy.hp -= damage
                "你對[enemy.name]造成了[damage]點傷害！"
            "特殊技能" if player.mp >= 3:
                $ renpy.block_rollback()
                $ player.mp -= 3
                $ damage = calculate_damage(player, enemy) * 2
                $ enemy.hp -= damage
                "你使用特殊技能，對[enemy.name]造成了[damage]點傷害！"
            "防禦":
                $ renpy.block_rollback()
                $ player.defense += 1
                "你提高了防禦力！"

        if enemy.hp <= 0:
            "你贏了戰鬥！"
            hide screen battle_ui
            $ renpy.block_rollback()
            return "victory"

        # 敵人回合
        show minionenemy at right_to_left
        pause 2
        $ damage = calculate_damage(enemy, player)
        $ player.hp -= damage
        "[enemy.name]對你造成了[damage]點傷害！"

        if player.hp <= 0:
            "你輸了戰鬥..."
            hide screen battle_ui
            $ renpy.block_rollback()
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
    


    show johnyoungpic at right
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

    show wang2:
        xalign 0.5
        yalign 0.6

    w "瑞元，你父親走了，今後家裡就靠你了。"
    "瑞元是蔣中正小時候的名子"(what_color="#808080")
    "瑞元" "母親，我一定會努力讀書，光耀門楣的。"
    w "孩子。記住，要刻苦讀書，但更要懂得做人的道理。"
    
    hide wang2

    voice "voichi7.wav"
    "父親去世後，我由母親王采玉撫育成人。這段經歷深深影響了我的性格形成。"
    

    jump chapter1_act3

# 第三幕：婚姻
label chapter1_act3:
    scene bg imgchi1
    with fade

    $ now_venue.location = "蔣家內"
    "1901年冬，蔣家內"

    show johnkidsad


    "瑞元" "母親，我才14歲，真的要結婚嗎？"
    hide johnkidsad
    show wang2:
        xalign 0.5
        yalign 0.6
    w "瑞元，這是我們家族的決定。毛家姑娘比你大5歲，賢良淑德，會是個好媳婦的。"
    hide wang2
    
    show johnkid

    "瑞元" "我明白了，母親。我會盡到丈夫的責任的。"

    hide johnkid
    hide wang
    hide wang2

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
    show johnkid:
        yalign 1.0
        xalign -0.5
        linear 3.0 xalign 0.71
        transform_anchor True
        linear 0.5 rotate 65


    "蔣中正疲倦地進入新房，倒在床上就睡"
    $ renpy.pause(delay=3.5,hard=True)
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

    show johnyoung
    d "蔣同學，你又在看報紙了？"
    show paper1:
        yalign 0.25 
        xalign 0.5
    hide johnyoung
    "志清" "是的，董老師。我覺得了解時事很重要。"
    "志清是蔣中正上學時的學名! 中正這個名子是蔣中正30多歲時取的"(what_color="#808080")
    d "很好。但不要忘了課本上的內容。"
    show johnyoung
    hide paper1
    "志清" "老師，您覺得我們應該如何改變中國的命運？"
    d "這個問題很深奧。也許你應該先學好英文，看看外面的世界是什麼樣子。"

    jump chapter1_act5

# 第五幕：首次赴日
label chapter1_act5:
    scene bg imgchi4
    with fade
    $ now_venue = place("上海碼頭")
    "1906年4月，上海碼頭"
    show johnyoung
    "志清" "母親，我一定會在日本好好學習，為祖國爭光。"
    hide johnyoung
    show wang2:
        xalign 0.5
        yalign 0.6
    w "中正，要記住你的初心。無論遇到什麼困難，都不要放棄。"
    show johnyoung
    hide wang2
    "志清" "我明白，母親。我會努力的。"
    show johnyoung at left_to_right_out
    pause 2
    hide johnyoung
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
    "志清" "(蔣中正聽後非常生氣，衝上講臺，把泥土碎成八塊) 日本有五千萬人，是否也像五千萬微生蟲，寄生在這八分之一方寸的土塊中？"
    n "........... 你是不是革命黨？??"
    "志清" "..........."
    "志清" "我只是一個愛國青年!!!"
    n "........"

    voice "voichi6.wav"
    "由於我在陸軍速成學堂深受校長和教官賞識，第二年就成為第一批派往日本深造之四人之一。"

# 第六幕：加入同盟會
label chapter1_act6:
    scene bg imgchi6
    with fade
    $ now_venue = place("東京")
    "1908年，東京"

    
    show flag1:
        zoom 0.7
        yalign 0.45 
        xalign 0.1
    show chenqimei glasses

    c "中正，我想邀請你加入同盟會。我們需要像你這樣有志之士。"
    "這是同盟會的旗幟圖案"(what_color="#808080")
    "志清" "陳大哥，同盟會的宗旨是什麼？"
    c "驅除韃虜，恢復中華，建立民國，平均地權。"
    "志清" "這與我的理想相符。我願意加入。"
    c "很好。記住，革命是一條艱難的道路，需要堅強的意志。"
    "志清" "我明白。我已經準備好了。"

# 第七幕：畢業與歸國
label chapter1_act7:
    scene bg imgchi12
    with fade
    $ now_venue = place("日本振武學校")
    "1910年11月，日本振武學校畢業典禮"

    show johndraw 

    s "蔣中正同學，你的成績雖然不是最好的，但你的愛國熱情令人欽佩。"
    "志清" "感謝校長的教誨。我會將在這裡學到的知識用於振興中華。"

    z "中正，聽說你要去陸軍實習？"
    "志清" "是的，這是一個難得的機會，可以學習日本軍隊的先進經驗。"
    z "不要忘記我們的初心。總有一天，我們要用這些知識來服務於我們自己的國家。"
    "志清" "我永遠不會忘記的。"

# 第八幕：參加辛亥革命
label chapter1_act8:
    scene bg imgchi4
    with fade
    $ now_venue = place("上海碼頭")
    "1911年10月，上海碼頭"

    show johndraw

    "志清" "張群，武昌起義的消息你聽說了嗎？"
    z "聽說了。看來我們等待已久的機會終於來了。"
    "志清" "是啊，我們必須立即行動。陳其美大哥在上海已經開始準備了。"
    z "那我們趕快去找他吧。祖國需要我們了。"

    $ now_venue = place("陳其美居所")
    scene bg imgchi13 
    
    "上海，陳其美的住所"

    show chenqimei glasses
    c "中正，你來得正好。我需要你率領一支敢死隊去杭州。"
    "志清" "我明白。這是我們改變中國命運的機會，我不會辜負您的期望。"
    c "記住，革命是一項艱巨的事業。我們可能會失敗，但絕不能放棄。"
    "志清" "我準備好了，無論付出什麼代價。"

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
        call battle_system
    show screen location_ui
    scene bg imgchi8

    show soldier

    "小兵" "報告! 我們已攻佔巡撫府，俘虜增韞!"
    j "辛苦了，看來我們的第一步已經成功了。"

    scene black
    with fade
    show soldier
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
    "志清" "先生您說的我會遵守，讓我們一起完成革命大業。"
    sun "我期待你的表現。你是否想要任何職位？"
    "志清" "我蔣某人，不需要職位，只要先生能借我力量即可。"

    voice "voichi13.wav"
    "至此，我開始了我的軍政之路。"

    scene bg imgchi10
    with fade
    $ now_venue = place("上海")
    "1913年7月，上海"

    voice "voichi14.wav"
    "1913年7月，孫先生發動二次革命討伐袁世凱，我在上海討袁軍總司令陳其美的指揮下參加攻打江南製造局之役。"

    show chenqimei

    c "志清，我們必須奪取江南製造局，切斷袁世凱的軍火供應。"
    "志清" "明白，我們一定要成功。"

    hide chenqimei
    voice "voichi15.wav"
    "不幸的是，各地討袁軍先後失敗。上海滬軍都督楊善德下令緝捕我"

    voice "voichi16.wav"
    "我被迫逃進陳其美之娘姨姚冶誠臥室內，遂納姚納姚冶誠為側室。"

    show johndraw
    hide chenqimei

    "志清" "姚小姐，謝謝你救了我。"
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

    jump chapter2_act1


# 第一幕：事變前夕
label chapter2_act1:
    scene bg imgfeng1
    
    with fade
    $ now_venue = place("西安行營")
    "1936年12月11日，西安行營"

    show screen location_ui

    show johndraw:
        xalign 0.5
        yalign 0.92
        

    voice "voifeng1.wav"
    j "1936年12月11日，我察覺到張學良的行為有些異常，這引起了我的警覺。我在日記中寫道：『今日漢卿形色急遽，精神恍惚，甚覺有異。』但我沒想到第二天凌晨就發生了驚人的變故。"

    voice "voifeng2.wav"
    j "張將軍，你最近看起來心事重重啊。是否有什麼困擾？"

    show johndraw:
        xalign 0.5
        yalign 0.92
        linear 1.0 xalign 0.1

    show xueliang:
        xalign 1.0
        yalign 0.92 
        
    xueliang "委座，只是有些疲勞罷了，請不必擔心。我們在剿共問題上或許有些分歧，但這並不影響我對您的忠誠。"

    voice "voifeng3.wav"
    j "希望如此。記得好好休息，我們還有很多事情要做。明天我們還要討論新一輪的剿共計劃。"

    show johndraw:
        xalign 0.1
        yalign 0.95
        xzoom 1  # 确保开始时是正常方向
        parallel:
            linear 0.1 xzoom -1  # 在0.5秒内水平翻转
        parallel:
            linear 1.0 xalign -0.5  # 同时在1秒内移动到左边

    with move  # 这会创建一个移动的过渡效果

    # 暂停一小段时间，让两个动作之间有一个间隔
    $ renpy.pause(0.5)

    show xueliang:
        xalign 1.0
        yalign 0.92
        linear 1.0 xalign 0.1

    with move  # 再次使用移动过渡效果

    xueliang "(內心獨白) 委座啊，您怎麼就不明白呢？現在最重要的是抗日，而不是繼續內戰啊！"

    jump chapter2_act2


#第二幕：突襲與逃脫
label chapter2_act2:
    scene bg imgfeng2
    with fade

    $ now_venue.location = "臨潼華清池"
    "1936年12月12日凌晨，臨潼華清池"
    "（突然槍聲四起，喊叫聲不斷）"

    show guard:
        xalign 0.5
        yalign 0.92
    guard "委座！有人襲擊，是東北軍！我們必須立刻撤離！"

    show guard:
        xalign 0.5
        yalign 0.92
        linear 1.0 xalign 0.1

    show johndraw:
        xalign 1.0
        yalign 0.92 

    voice "voifeng4.wav"
    j "什麼？張學良竟敢...快，準備撤退！"

    hide guard
    xiaozhen "委座，我來掩護您，跟我來！"

    show imgfeng6:
        xalign 0.5
        yalign 0.92

    show johndraw:
        xalign 1.0
        yalign 0.95
        xzoom 1  # 确保开始时是正常方向
        parallel:
            linear 0.1 xzoom -1  # 在0.1秒内水平翻转
        parallel:
            linear 1.0 xalign 0.6  # 在1秒内移动到中间偏左
            ease 0.5 yalign 20  

    with move


    voice "voifeng5.wav"
    j "在那混亂之中，蔣孝鎮背著我翻牆逃走。我甚至來不及穿鞋，是他將自己的鞋子脫下給我穿上。我們分頭逃跑，希望能分散追兵的注意力。"




#    show imgfeng6:
#        xalign 0.5
#        yalign 1.2  # 將 yalign 值增加到大於 1,使圖像移動到更低的位置
#        parallel:
#            linear 0.1 yalign 3.0  # 將目標 yalign 值增加,使圖像移動到螢幕外

    show johndraw:
        yalign 20  # 从上一个动作结束的位置开始
        xalign 0.6
        xzoom -1
        parallel:
            ease 2.0 yalign 0.0  # 继续向上移动，但停在屏幕顶部附近
        parallel:
            block:
                ease 0.08 xalign 0.58  # 增加震动幅度
                ease 0.08 xalign 0.62
                repeat 10  # 减少重复次数以适应更慢的震动
    with move

    voice "voifeng6.wav"
    j "啊！"

    show johndraw:
        yalign 20
        xalign 0.6
        xzoom -1
        parallel:
            linear 2.0 rotate 0
        # 旋轉和躺平
        rotate 0
        parallel:
            ease 0.2 yalign 20
        parallel:
            ease 0.5 rotate -360
        parallel:
            ease 0.1 xzoom 1
        rotate 90
        yalign 10
        # 新添加的動作：站起來並往左跑
        pause 0.5  # 躺平後稍作停頓
        parallel:
            ease 0.5 rotate 0  # 站起來
            ease 0.5 yalign 10  # 確保角色站在地面上
        parallel:
            linear 1.0 xalign -0.5  # 同时在1秒内移动到左边


    voice "voifeng7.wav"
    j "我從牆上跳下，重重地摔進了牆外的溝裡，腰部劇痛。但我不敢停下，忍著疼痛繼續向驪山方向逃去。最後，我躲進了一個窪坑裡。"

    jump chapter2_act3


#第三幕：被俘
label chapter2_act3:
    scene bg imgfeng3
    with fade

    $ now_venue.location = "華清池附近的山坡"
    "華清池附近的山坡，天色漸明"

    show soldier:
        xalign 0.5
        yalign 0.92

    soldier "在這裡！我們找到蔣委員長了！"

    show johndraw:
        xalign 1.0
        yalign 0.92 
   
    voice "voifeng8.wav"
    j "你們...你們這是要做什麼？知道自己在犯什麼罪嗎？"


    show soldier:
        xalign 0.1
        yalign 0.95
        xzoom 1  # 确保开始时是正常方向
        parallel:
            linear 0.1 xzoom -1  # 在0.5秒内水平翻转
        parallel:
            linear 1.0 xalign -0.5  # 同时在1秒内移动到左边
    
    with move  # 这会创建一个移动的过渡效果

    # 暂停一小段时间，让两个动作之间有一个间隔
    $ renpy.pause(0.5)

    show xueliang:
        xalign 1.0
        yalign 0.92
        linear 1.0 xalign 0.1
    
    xueliang "委座，請原諒我們的無禮。我知道這樣做很冒險，但這是為了國家的未來。我們只是想請您聽聽我們的想法。"

    voice "voifeng9.wav"
    j "張學良！你可知道這樣做的後果？"

    jump chapter2_act4


#第四幕：談判過程
label chapter2_act4:
    scene bg imgfeng4
    with fade

    $ now_venue.location = "西安新城大樓會議室"
    "西安新城大樓會議室"

    show xueliang:
        xalign 0.5
        yalign 0.92
    
    xueliang "委座，我們苦苦哀求您停止內戰已經很久了。現在日本虎視眈眈，我們再不團結起來抗日，國家就真的危險了！"

    show xueliang:
        xalign 0.5
        yalign 0.92
        linear 1.0 xalign 0.1

    show johndraw:
        xalign 1.0
        yalign 0.92 
    voice "voifeng10.wav"
    j "你們以為用這種方式能解決問題嗎？這只會讓國家更加動盪！你們這是在破壞國家統一！"

    show xueliang:
        xalign 0.1
        yalign 0.95
        xzoom 1  # 确保开始时是正常方向
        parallel:
            linear 0.1 xzoom -1  # 在0.5秒内水平翻转
        parallel:
            linear 1.0 xalign -0.5  # 同时在1秒内移动到左边

    show johndraw:
        xalign 1.0
        yalign 0.95
        xzoom 1  # 确保开始时是正常方向
        parallel:
            linear 0.1 xzoom -1  # 在0.5秒内水平翻转
        parallel:
            linear 1.0 xalign 0.5  # 同时在1秒内移动到左边
    
    yang "但是委座，如果我們不團結一致對外，國家將會面臨更大的危機。請您三思啊！"

    
    
    zhou "蔣委員長，我代表中國共產黨，也希望能與您坦誠相談。我們願意在您的領導下，共同抗日。"

    voice "voifeng11.wav"
    j "在多次艱難的談判後，我逐漸理解了他們的用意。雖然我依然認為他們的方式是錯誤的，但我也意識到，國家確實需要改變。最終，我同意了停止內戰，改組政府，加強對日抗戰，並進行一系列政治改革。"

    jump chapter2_act5


#第五幕：釋放與反思
label chapter2_act5:
    scene bg imgfeng5
    with fade

    $ now_venue.location = "西安機場"
    "1936年12月25日，西安機場"
        
    show xueliang:
        xalign 0.5
        yalign 0.92
    
    xueliang "委座，我們已經準備好送您回南京了。我知道我的行為可能會招致嚴重後果，但為了國家，我願意承擔。"

    show xueliang:
        xalign 0.5
        yalign 0.92
        linear 1.0 xalign 0.1

    show johndraw:
        xalign 1.0
        yalign 0.92 
    voice "voifeng12.wav"
    j "張學良，你們的行為雖然錯誤，但出發點我能理解。記住，國家的未來需要我們共同努力。我會考慮你們的建議，但你必須為自己的行為負責。"

    show xueliang:
        xalign 0.1
        yalign 0.95
        xzoom 1  # 确保开始时是正常方向
        parallel:
            linear 0.1 xzoom -1  # 在0.5秒内水平翻转
        parallel:
            linear 1.0 xalign -0.5  # 同时在1秒内移动到左边

    show johndraw:
        xalign 1.0
        yalign 0.95
        xzoom 1  # 确保开始时是正常方向
        parallel:
            linear 0.1 xzoom -1  # 在0.5秒内水平翻转
        parallel:
            linear 1.0 xalign 0.5  # 同时在1秒内移动到左边


    voice "voifeng13.wav"
    j "1936年12月25日，我終於重獲自由。這次西安事變，讓我深刻認識到國內的矛盾和挑戰，也讓我更加重視對外的抗戰準備。這段經歷對我來說，既是挑戰，也是轉機。"

    voice "voifeng14.wav"
    j "當飛機起飛時，我望著窗外的西安，心中充滿了複雜的情緒。這次事變雖然結束了，但它所揭示的問題卻遠未解決。"

    voice "voifeng15.wav"
    j "我知道，未來還有更艱巨的任務等待著我，等待著整個中國。西安事變後，我更加堅定了抗日的決心，也開始重新思考國內政策。這次經歷，無疑是我政治生涯中的一個重要轉折點。"

    return