
default player_question = ""
init python:

    import random
    import time
    import requests
    import threading
    from threading import Lock

    
    # 初始化變數
    ai_chat_history = []
    intro_text = "正在加載..."
    is_loading = False
    is_waiting_response = False  # 新增等待回應狀態
    API_URL = "http://localhost:8000"
    config.overlay_screens.append("ai_teacher_button")



    class ChatMessage:
        def __init__(self, content, is_player=False):
            self.content = content
            self.is_player = is_player
            self.timestamp = time.time()
            self.displayed_content = ""
            self.is_typing = False
            self.typing_index = 0
            self.typing_lock = Lock()  # 添加锁来保护打字状态
            
        def start_typing(self):
            if self.is_player:
                self.displayed_content = self.content
                self.is_typing = False
                return
            
            with self.typing_lock:
                if self.is_typing:  # 如果已经在打字，就不要重新开始
                    return
                self.is_typing = True
                self.typing_index = 0
                self.displayed_content = ""
            
            def typing_effect():
                try:
                    while True:
                        with self.typing_lock:
                            if self.typing_index >= len(self.content) or not self.is_typing:
                                self.is_typing = False
                                break
                            
                            # 每次显示 1-3 个字符，使打字效果更自然
                            chars_to_add = min(random.randint(1, 3), 
                                            len(self.content) - self.typing_index)
                            self.typing_index += chars_to_add
                            self.displayed_content = self.content[:self.typing_index]
                        
                        # 强制更新界面
                        renpy.invoke_in_main_thread(renpy.restart_interaction)
                        
                        # 随机延迟，使打字效果更自然
                        delay = random.uniform(0.05, 0.15)
                        time.sleep(delay)
                        
                except Exception as e:
                    print(f"打字效果错误: {str(e)}")
                finally:
                    with self.typing_lock:
                        self.is_typing = False
                        self.displayed_content = self.content  # 确保显示完整内容
                    renpy.invoke_in_main_thread(renpy.restart_interaction)
            
            thread = threading.Thread(target=typing_effect)
            thread.daemon = True
            thread.start()

    # 取得網頁標題
    def get_first_title(url):
        try:
            response = requests.get(f'http://localhost:8000/get_title?url={url}', timeout=5)
            response.raise_for_status()
            data = response.json()
            return data['title']
        except requests.RequestException as e:
            print(f"獲取標題錯誤: {str(e)}")
            return "未連上網路"

    # 非同步獲取 AI 回應
    def async_get_intro(question):
        global intro_text, is_loading, is_waiting_response
        
        if is_waiting_response:  # 如果正在等待回應，則不執行
            return
            
        is_loading = True
        is_waiting_response = True

        def network_request():
            global intro_text, is_loading, ai_chat_history, is_waiting_response
            try:
                print(f"正在發送問題: {question}")
                response = requests.get(f'{API_URL}/ask', 
                                     params={'question': str(question)},
                                     timeout=30)  # 加入超時設定
                print(f"API 回應狀態: {response.status_code}")
                
                response.raise_for_status()
                data = response.json()
                print(f"收到回應: {data}")

                # 移除等待提示（如果存在）
                if ai_chat_history and ai_chat_history[-1].content == "正在思考中...":
                    ai_chat_history.pop()

                # 添加 AI 回應並開始打字效果
                new_message = ChatMessage(data['answer'], is_player=False)
                ai_chat_history.append(new_message)
                new_message.start_typing()  # 開始打字效果

            except requests.Timeout:
                handle_error("請求超時，請稍後再試")
            except requests.ConnectionError:
                handle_error("無法連接到伺服器，請檢查網路連接")
            except requests.RequestException as e:
                handle_error(f"API請求錯誤: {str(e)}")
            except Exception as e:
                handle_error(f"未知錯誤: {str(e)}")
            finally:
                is_loading = False
                is_waiting_response = False
                renpy.restart_interaction()

        def handle_error(error_message):
            global ai_chat_history
            print(f"發生錯誤: {error_message}")
            if ai_chat_history and ai_chat_history[-1].content == "正在思考中...":
                ai_chat_history.pop()
            ai_chat_history.append(ChatMessage(error_message, is_player=False))

        thread = threading.Thread(target=network_request)
        thread.daemon = True  # 設置為守護線程
        thread.start()

    # 發送消息函數
    def send_message():
        global ai_chat_history, is_waiting_response
        
        if is_waiting_response:  # 如果正在等待回應，則不執行
            return
            
        screen = renpy.get_screen('ai_chat_screen')
        if screen:
            player_question = screen.scope["player_question"]
            if player_question and player_question.strip():
                current_question = player_question.strip()
                print(f"問題是: {current_question}")

                # 清空輸入框
                screen.scope["player_question"] = ""
                
                # 添加玩家問題到歷史
                ai_chat_history.append(ChatMessage(current_question, is_player=True))
                
                # 添加等待提示
                waiting_message = ChatMessage("正在思考中...", is_player=False)
                ai_chat_history.append(waiting_message)
                waiting_message.start_typing()
                
                # 使用非同步方式獲取回應
                async_get_intro(current_question)
                
                # 更新界面
                renpy.restart_interaction()

    class place:
        def __init__(self, location):
            self.location = location

    class chaptchoosing:
        def __init__(self, chapter):
            self.chapter = chapter


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


# 使用方式：
# call test_combined

# 使用方式：call screen test_input_screen

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

define chencheng = Character("陳誠")
define heyingqin = Character("何應欽")
define zhangzhizhong = Character("張治中")

define igov = Character("專賣局查緝員")
define cshop = Character("菸販")
define peoplea = Character("群眾甲")
define peopleb = Character("群眾乙")
define peoplec = Character("群眾丙")
define peopled = Character("群眾丁")
define peoplee = Character("群眾戊")
define peoplel = Character("民眾代表")
define reporter = Character("記者")
define tdstudent = Character("臺大學生")
define ttp = Character("臺灣省參議會議員")
define chenyi = Character("陳儀")
define armyl = Character("憲兵團長")
define armya = Character("士兵甲")
define tpa = Character("臺灣居民甲")
define tpb = Character("臺灣居民乙")
define pal = Character("民軍領袖")
define cpa = Character("嘉義居民甲")
define cpb = Character("嘉義居民乙")
define cpc = Character("嘉義居民丙")
define keyuanfen = Character("柯遠芬")

define fusinian = Character("傅斯年")
define zhujiahua = Character("朱家驊")
define assistant = Character("助理")
define peoples = Character("群眾")
define faramy = Character("軍團長")
define saramy = Character("軍官")
define wangshijie = Character("王世傑")
define allp = Character("全場")

define minister = Character("經濟部長")
define johnson = Character("蔣經國")
define diplomat = Character("外交部長")

#第五章角色
define mzd = Character("毛澤東")
define solc = Character("士兵甲")
define gmdg = Character("國民黨將軍")
define soli = Character("士兵乙")
define igl = Character("指揮官")
define zc = Character("戰士甲")
define zi = Character("戰士乙")
define gsol = Character("國民黨士兵")
define gz = Character("共產黨戰士")
define gigl = Character("共軍指揮官")
define gg = Character("國民黨將領")
define ggz = Character("共軍戰士")
define znl = Character("周恩來")
define igl2 = Character("副官")
define zhu = Character("指揮員")
define ggunz = Character("國民黨高官甲")
define gguni = Character("國民黨高官乙")
define gunb = Character("高官丙")
define gunz = Character("高官甲")
define crowd = Character("群眾")
define gzg = Character("共產黨幹部")
define nonz = Character("農民甲")
define noni = Character("農民乙")
define zu = Character("助手")
define amegun = Character("美國官員")
define su = Character("蘇聯顧問")
define chd = Character("中共代表")

define audio.gamemusic = "audio/chapter1.wav"

define p = Character("彭孟緝")
define g = Character("外交官")
define l = Character("雷震")
define y = Character("殷海光")
define f = Character("傅正")
define yan = Character("嚴家淦")

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
image bg imgchi14 = "imgchi14.png"
image bg imgchi15 = "imgchi15.jpg"
image bg imgchi16 = "imgchi16.jpg"
image bg imgchi17 = "imgchi17.jpg"
image bg imgchi18 = "imgchi18.jpg"

image bg imgfeng1 = "imgfeng1.png"
image bg imgfeng2 = "imgfeng2.png"
image bg imgfeng3 = "imgfeng3.png"
image bg imgfeng4 = "imgfeng4.png"
image bg imgfeng5 = "imgfeng5.png"

image bg imghui1 = "imghui1.png"
image bg imghui2 = "imghui2.png"
image bg imghui3 = "imghui3.png"
image bg imghui4 = "imghui4.png"
image bg imghui5 = "imghui5.png"

image bg imgyalan1 = "imgyalan1.png"
image bg imgyalan2 = "imgyalan2.png"
image bg imgyalan3 = "imgyalan3.png"
image bg imgyalan4 = "imgyalan4.png"
image bg imgyalan5 = "imgyalan5.png"
image bg imgyalan6 = "imgyalan6.png"
image bg imgyalan7 = "imgyalan7.png"
image bg imgyalan8 = "imgyalan8.png"
image bg imgyalan9 = "imgyalan9.png"
image bg imgyalan10 = "imgyalan10.png"
image bg imgyalan11 = "imgyalan11.png"
image bg imgyalan12 = "imgyalan12.png"
image bg imgyalan13 = "imgyalan13.png"
image bg imgyalan14 = "imgyalan14.png"
image bg imgyalan15 = "imgyalan15.png"

image bg imgjcf1 = "imgjcf1.jpg"
image bg imgjcf2 = "imgjcf2.jpg"
image bg imgjcf3 = "imgjcf3.jpg"
image bg imgjcf4 = "imgjcf4.jpg"
image bg imgjcf5 = "imgjcf5.jpg"
image bg imgjcf6 = "imgjcf6.jpg"
image bg imgjcf8 = "imgjcf8.jpg"

image bg imgjcs1 = "imgjcs1.jpg"
image bg imgjcs2 = "imgjcs2.jpg"
image bg imgjcs3 = "imgjcs3.jpg"
image bg imgjcs4 = "imgjcs4.jpg"
image bg imgjcs6 = "imgjcs6.jpg"

#第五章背景
image bg imgli1 ="imgli1@3.jpg"
image bg imgli2 ="imgli2.png"
image bg imgli3 ="imgli3.png"
image bg imgli4 ="imgli4.png"
image bg imgli5 ="imgli5.png"
image bg imgli6 ="imgli6.png"
image bg imgli7 ="imgli7.png"
image bg imgli8 ="imgli8.jpg"
image bg imgli9 ="imgli9.png"
image bg imgli10 ="imgli10.jpg"
image bg imgli11 ="imgli11.jpg"
image bg imgli12 ="imgli12.jpg"
image bg imgli13 ="imgli13.jpg"

image bg imgchung = "imgchung.jpg"

image imgjcf7 = "imgjcf7.jpg"
image imgjcs5 = "imgjcs5.jpg"





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
image johndrawold = "johnold.png"


image xueliang = "xueliang.png"
image chencheng = "chencheng.png"
image zhangzhizhong = "zhangzhizhong.png"
image heyingqin = "yingqin.png"


image paper1 = "paper.jpg"
image flag1 = "flag1.png"
image dust = "dust.png"
image dustbroken = "dustbroken.png"
image wall = "wall.png"
image prison = "prison.png"
image plane = "plane.png"






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

transform left_to_middle:
    yalign 1.0
    linear 0.5 xalign 0.2
    
transform right_to_middle:
    yalign 1.0
    xalign 1.0
    linear 0.5 xalign 0.75

transform middle_to_left:
    yalign 1.0
    xalign 0.5
    linear 0.5 xalign 0.25

transform right_:
    yalign 1.0
    xalign 0.75

transform plane_landing:
    xzoom -1  
    xanchor 0.5 yanchor 0.5  
    xpos 2100 ypos -200  
    rotate -20  
    zoom 0.5  
    linear 2.0 xpos 1600 ypos 200 zoom 0.7 rotate -15  
    linear 3.0 xpos 450 ypos 650 zoom 1.0 rotate 0


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

screen imagemap():
    imagemap:
        idle "hugemap idle"
        hover "hugemap hover"

        hotspot (91, 250, 392, 229) action Jump("chap1go") alt "Chap1go"
        hotspot (529, 250, 392, 229) action Jump("chap2go") alt "Chap2go"
        hotspot (986, 248, 389, 230) action Jump("chap3go") alt "Chap3go"
        hotspot (1435, 252, 393, 227) action Jump("chap4go") alt "Chap4go"
        hotspot (95, 679, 388, 223) action Jump("chap5go") alt "Chap5go"
        hotspot (530, 680, 393, 225) action Jump("chap6go") alt "Chap6go"
        hotspot (981, 675, 393, 233) action Jump("chap7go") alt "Chap7go"
        hotspot (1435, 676, 397, 232) action Jump("chap8go") alt "Chap8go"

screen choice_screen():
    window id "window":
        vbox:
            xalign 0.4
            ypos 65
            textbutton "確認" action Jump(now_chapter.chapter) text_size 100
        vbox:
            xalign 0.6
            ypos 65
            textbutton "返回" action Jump("start") text_size 100


label chap1go:
    $ now_chapter.chapter = "chapter1_act1"
    $ renpy.block_rollback()
    show maofumei:
        xalign 0.4
        yalign 0.4
    "是否確認進入章節1?"
    $ renpy.block_rollback()
    call screen choice_screen

label chap2go:
    $ now_chapter.chapter = "chapter2_act1"
    $ renpy.block_rollback()
    show maofumei:
        xalign 0.4
        yalign 0.4
    "是否確認進入章節2?"
    $ renpy.block_rollback()
    call screen choice_screen

label chap3go:
    $ now_chapter.chapter = "chapter3_act1"
    $ renpy.block_rollback()
    show maofumei:
        xalign 0.4
        yalign 0.4
    "是否確認進入章節3?"
    $ renpy.block_rollback()
    call screen choice_screen
 
label chap4go:
    $ now_chapter.chapter = "chapter4_act1"
    $ renpy.block_rollback()
    show maofumei:
        xalign 0.4
        yalign 0.4
    "是否確認進入章節4?"
    $ renpy.block_rollback()
    call screen choice_screen

label chap5go:
    $ now_chapter.chapter = "chapter5_act1"
    $ renpy.block_rollback()
    show maofumei:
        xalign 0.4
        yalign 0.4
    "是否確認進入章節5?"
    $ renpy.block_rollback()
    call screen choice_screen


label chap6go:
    $ now_chapter.chapter = "chapter6_act1"
    $ renpy.block_rollback()
    show maofumei:
        xalign 0.4
        yalign 0.4
    "是否確認進入章節6?"
    $ renpy.block_rollback()
    call screen choice_screen

label chap7go:
    $ now_chapter.chapter = "chapter7_act1"
    $ renpy.block_rollback()
    show maofumei:
        xalign 0.4
        yalign 0.4
    "是否確認進入章節7?"
    $ renpy.block_rollback()
    call screen choice_screen

label chap8go:
    $ now_chapter.chapter = "chapter8_act1"
    $ renpy.block_rollback()
    show maofumei:
        xalign 0.4
        yalign 0.4
    "是否確認進入章節8?"
    $ renpy.block_rollback()
    call screen choice_screen
 
# 遊戲開始
label start:
    $ renpy.block_rollback()
    $now_venue = place("startplace")
    $now_chapter = chaptchoosing("init")
    call screen imagemap


# 第一幕：家世背景
label chapter1_act1:
    $ renpy.block_rollback()
    play music gamemusic
    scene bg yutai
    with fade

    $ now_venue.location = "玉泰鹽鋪"

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
    $ now_venue.location = "奉化鳳麓學堂"
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
    $ now_venue.location = "上海碼頭"
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
    $ now_venue.location = "陸軍速成學堂"
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
    $ now_venue.location = "東京"
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
    $ now_venue.location = "日本振武學校"
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
    $ now_venue.location = "上海碼頭"
    "1911年10月，上海碼頭"

    show johndraw

    "志清" "張群，武昌起義的消息你聽說了嗎？"
    z "聽說了。看來我們等待已久的機會終於來了。"
    "志清" "是啊，我們必須立即行動。陳其美大哥在上海已經開始準備了。"
    z "那我們趕快去找他吧。祖國需要我們了。"

    $ now_venue.location = "陳其美居所"
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
    $ now_venue.location = "浙江杭州"
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
    $ now_venue.location = "中華革命黨總部"
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
    $ now_venue.location = "上海"
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
    $ now_venue.location = "張靜江家"
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
    $ now_venue.location = "陳氏宅"
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


# 第一幕：事變前夕
label chapter2_act1:
    $ renpy.block_rollback()
    scene bg imgfeng1

    play music "chapter2.mp3" 
    
    with fade
    $ now_venue.location = "西安行營"
    "1936年12月11日，西安行營"

    show screen location_ui

    show johndrawold
        

    voice "voifeng1.wav"
    j "1936年12月11日，我察覺到張學良的行為有些異常，這引起了我的警覺。我在日記中寫道：『今日漢卿形色急遽，精神恍惚，甚覺有異。』但我沒想到第二天凌晨就發生了驚人的變故。"

    voice "voifeng2.wav"
    j "張將軍，你最近看起來心事重重啊。是否有什麼困擾？"

    show johndrawold :
        xalign 0.5
        xzoom -1
        linear 0.5 xalign 0.25
        xzoom 1

    with move
    $ renpy.pause(0.2)
    
    show xueliang at right_to_middle
        
    xueliang "委座，只是有些疲勞罷了，請不必擔心。我們在剿共問題上或許有些分歧，但這並不影響我對您的忠誠。"

    voice "voifeng3.wav"
    j "希望如此。記得好好休息，我們還有很多事情要做。明天我們還要討論新一輪的剿共計劃。"

    show johndrawold:
        xalign 0.25 
        xzoom -1
        linear 1.0 xalign -0.5


    with move  

    
    $ renpy.pause(0.5)

    show xueliang:
        xalign 1.0
        linear 1.0 xalign 0.25

    with move  

    xueliang "(內心獨白) 委座啊，您怎麼就不明白呢？現在最重要的是抗日，而不是繼續內戰啊！"

    jump chapter2_act2


#第二幕：突襲與逃脫
label chapter2_act2:

    scene bg imgfeng2
    with fade

    $ now_venue.location = "臨潼華清池"
    "1936年12月12日凌晨，臨潼華清池"
    "（突然槍聲四起，喊叫聲不斷）"

    show soldier
    guard "委座！有人襲擊，是東北軍！我們必須立刻撤離！"

    hide soldier

    show johndrawold 

    voice "voifeng4.wav"
    j "什麼？張學良竟敢...快，準備撤退！"

    
    xiaozhen "委座，我來掩護您，跟我來！"

    show wall

    show johndrawold at left

    voice "voifeng5.wav"
    j "在那混亂之中，蔣孝鎮背著我翻牆逃走。我甚至來不及穿鞋，是他將自己的鞋子脫下給我穿上。我們分頭逃跑，希望能分散追兵的注意力。"


    voice "voifeng6.wav"
    j "啊！"


    voice "voifeng7.wav"
    j "我從牆上跳下，重重地摔進了牆外的溝裡，腰部劇痛。但我不敢停下，忍著疼痛繼續向驪山方向逃去。最後，我躲進了一個窪坑裡。"
    jump chapter2_act3


#第三幕：被俘
label chapter2_act3:
    scene bg imgfeng3
    with fade

    $ now_venue.location = "華清池附近的山坡"
    "華清池附近的山坡，天色漸明"

    show soldier

    soldier "在這裡！我們找到蔣委員長了！"

    hide soldier

    show johndrawold

    show prison:
        xalign 0.5
        yalign 0.1
        linear 1.0 yalign 0.7
   
    voice "voifeng8.wav"
    j "你們...你們這是要做什麼？知道自己在犯什麼罪嗎？"


    hide johndrawold
    hide prison

    show xueliang
    
    xueliang "委座，請原諒我們的無禮。我知道這樣做很冒險，但這是為了國家的未來。我們只是想請您聽聽我們的想法。"


    hide xueliang

    show johndrawold

    show prison

    voice "voifeng9.wav"
    j "張學良！你可知道這樣做的後果？"

    jump chapter2_act4


#第四幕：談判過程
label chapter2_act4:
    scene bg imgfeng4
    with fade

    $ now_venue.location = "西安新城大樓會議室"
    "西安新城大樓會議室"

    show xueliang
    
    
    xueliang "委座，我們苦苦哀求您停止內戰已經很久了。現在日本虎視眈眈，我們再不團結起來抗日，國家就真的危險了！"

    hide xueliang

    show johndrawold

    voice "voifeng10.wav"
    j "你們以為用這種方式能解決問題嗎？這只會讓國家更加動盪！你們這是在破壞國家統一！"


    j "我曾說過 :「能戰始能言和，不能戰而言和，是投降，投降後就是繳械，繳械後就是被屠殺。你們應該明白這個道理。」"
  
    voice "voifeng16.wav"
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

    show plane at plane_landing
    
    "這是波音247。"(what_color="#808080")

    "軍閥「少帥」張學良購買兩架波音247D給他的空軍部隊。其中一架為他本人所用，名為「白鷹號」。"(what_color="#808080")

    $ renpy.pause(3.0, hard=True)

    show xueliang
    

    
    xueliang "委座，我們已經準備好送您回南京了。我知道我的行為可能會招致嚴重後果，但為了國家，我願意承擔。"
    

    hide xueliang
    show johndrawold

    voice "voifeng12.wav"
    j "張學良，你們的行為雖然錯誤，但出發點我能理解。記住，國家的未來需要我們共同努力。我會考慮你們的建議，但你必須為自己的行為負責。"

    "蔣介石最終沒有對張學良痛下殺手，而是讓張學良失去了54年的自由。"(what_color="#808080")
    "臨終前更是對蔣經國說「絕對不可放虎歸山」。"(what_color="#808080")
    "楊虎城的結局與張學良不同，楊虎城在事變後被處決，他的家人也遭到迫害。"(what_color="#808080")
    
    voice "voifeng13.wav"
    j "1936年12月25日，我終於重獲自由。這次西安事變，讓我深刻認識到國內的矛盾和挑戰，也讓我更加重視對外的抗戰準備。這段經歷對我來說，既是挑戰，也是轉機。"

    voice "voifeng17.wav"
    j "正如我在日記中所寫:「從前種種譬如昨日死，此後種種譬如今日生。」"

    voice "voifeng14.wav"
    j "當飛機起飛時，我望著窗外的西安，心中充滿了複雜的情緒。這次事變雖然結束了，但它所揭示的問題卻遠未解決。"

    voice "voifeng15.wav"
    j "我知道，未來還有更艱巨的任務等待著我，等待著整個中國。西安事變後，我更加堅定了抗日的決心，也開始重新思考國內政策。這次經歷，無疑是我政治生涯中的一個重要轉折點。"

    return

#第一幕：七七事變
label chapter3_act1:
    $ renpy.block_rollback()
    scene bg imgyalan1
    with fade

    play music "chapter3.mp3" 

    $ now_venue.location = "南京，國民政府軍事委員會"

    show screen location_ui

    "1937年7月7日"

    show johndrawold

    voice "voiyalan1.wav"
    j "1937年7月7日晚，駐紮在豐台的日軍在盧溝橋附近進行所謂的「夜間演習」。這次演習成為了全面抗戰的導火線。"

    voice "voiyalan2.wav"
    j "諸位，日軍已經在華北發動全面進攻，我們必須立即做出反應。這不再是局部衝突，而是關乎國家存亡的戰爭。"

    show johndrawold:
        xalign 0.5
        xzoom -1
        linear 0.5 xalign 0.25
        xzoom 1

    with move
    $ renpy.pause(0.2)

    show heyingqin at right_to_middle
        
    heyingqin "委座，是否考慮先與日方談判，爭取時間？我們的軍備還不足以應對全面戰爭。"

    voice "voiyalan3.wav"
    j "談判可以進行，但絕不能放棄抵抗。發布全國總動員令，我們要讓全國上下都明白，這是一場關乎民族存亡的戰爭。何應欽，你立即安排各戰區的防禦部署。"

    hide heyingqin
    show chencheng at right_to_middle

    chencheng "委座，我認為我們應該採取積極防禦的策略。在正面戰場上消耗日軍的實力，同時在敵後發動游擊戰。"

    voice "voiyalan4.wav"
    j "好主意。陳誠，你負責華北戰場，要靈活運用這種策略。張治中，你負責沿海地區的防務，特別是上海周邊。"

    hide chencheng

    show zhangzhizhong at right_to_middle

    zhangzhizhong "是，委座。我會立即著手部署。"

    voice "voiyalan5.wav"
    j "記住，我們可能會失敗，可能會遭受巨大的損失，但我們絕不會屈服！我們要讓全世界都看到中國人民的決心！"

    jump chapter3_act2


#第二幕：淞滬會戰
label chapter3_act2:
    scene bg imgyalan2
    with fade
    $ now_venue.location = "上海指揮部"
    "1937年8月，上海指揮部"

    show johndrawold

    voice "voiyalan6.wav"
    j "為了分散日軍注意力，減輕華北戰場的壓力，我決定在上海發動一場大規模戰役。這是一個冒險的決定，但我們別無選擇。"

    voice "voiyalan7.wav"
    j "張治中，你來指揮這次淞滬會戰。記住，我們不僅是在打仗，更是在向世界展示中國人民的抗戰決心。"

    hide johndrawold

    show zhangzhizhong

    zhangzhizhong "是，委座。我們的德械師已經做好了戰鬥準備，一定能給日軍一個迎頭痛擊！"

    hide zhangzhizhong

    show heyingqin

    heyingqin "但是委座，我們在裝備上還是有劣勢。日軍的海空優勢明顯，我們可能會遭受重創。"

    hide heyingqin

    show johndrawold

    voice "voiyalan8.wav"
    j "我明白這個風險。但是我們有地利，有民心。更重要的是，我們是在保衛自己的國家。這種精神力量是無法估量的。"

    hide johndrawold

    show chencheng

    chencheng "我同意委座的看法。我們必須在上海一戰，否則日軍很快就會威脅南京了。"

    hide chencheng

    show johndrawold

    voice "voiyalan9.wav"
    j "沒錯。張治中，你要充分利用租界的特殊地位，在國際社會面前展示日軍的暴行。"

    scene bg imgyalan3
    with fade

    $ now_venue.location = "上海戰場"
    "上海戰場"

    show zhangzhizhong

    zhangzhizhong "弟兄們，堅持住！每一條街道，每一座房屋，都要與敵人爭奪！"

    hide zhangzhizhong

    show soldier

    soldier "是，長官！我們誓死保衛上海！"

    hide soldier

    show zhangzhizhong

    zhangzhizhong "報告委座，我軍在羅店一線給予日軍沈重打擊，但敵人正在增兵，形勢嚴峻。"

    hide zhangzhizhong

    show johndrawold

    voice "voiyalan10.wav"
    j "堅持住，張將軍。我會調集更多部隊支援上海。記住，我們是在為時間而戰。"

    voice "voiyalan11.wav"
    j "淞滬會戰持續了三個月之久，我們的軍隊表現出了前所未有的勇氣和決心。雖然最終上海還是陷落了，但我們的頑強抵抗大大延緩了日軍的進攻步伐，為後續的戰略調整爭取了寶貴的時間。"

    jump chapter3_act3


#第三幕：南京保衛戰
label chapter3_act3:
    scene bg imgyalan4
    with fade

    $ now_venue.location = "南京指揮部"
    "1937年12月，南京指揮部"

    
    show johndrawold:
        yalign 1.0
        linear 2 xalign 0.6
        xzoom -1
        linear 1 xalign 0.45

    voice "voiyalan12.wav"
    j "1937年12月，日軍向南京推進。我面臨著一個艱難的抉擇。"

    voice "voiyalan13.wav"
    j "諸位，南京是我們的首都，絕不能輕易放棄。但我們也要考慮長遠的抗戰大局。"

    hide johndrawold

    show heyingqin

    heyingqin "委座，我們是否應該考慮將政府遷往其他地方？敵軍兵鋒正盛，我們未必能守住南京。"

    hide heyingqin

    show johndrawold

    voice "voiyalan14.wav"
    j "是的，政府必須轉移，以保存實力。但我們絕不能放棄南京的防禦。陳誠，你留下來指揮防衛戰。"

    hide johndrawold

    show chencheng

    chencheng "是，委座。我們會死守南京，絕不讓日軍輕易得逞！"

    hide chencheng

    show zhangzhizhong

    zhangzhizhong "委座，我建議我們在撤退時實行堅壁清野政策，不給日軍留下任何可用之物。"

    hide zhangzhizhong

    show johndrawold

    voice "voiyalan15.wav"
    j "好主意。但要注意保護平民。我們打仗，是為了保護百姓，而不是為了增加他們的苦難。"

    voice "voiyalan16.wav"
    j "12月13日，南京陷落。日軍在南京犯下了令人髮指的暴行，這就是後來震驚世界的南京大屠殺。"

    scene bg imgyalan5
    with fade

    $ now_venue.location = "重慶臨時指揮部"
    "重慶臨時指揮部"

    show johndrawold

    voice "voiyalan17.wav"
    j "南京的慘劇讓我們心如刀割，但也更堅定了我們抗戰到底的決心。從現在起，我們要實行持久戰略，消耗日軍的實力，等待國際局勢的變化。"

    hide johndrawold

    show heyingqin

    heyingqin "委座英明。我們確實需要調整戰略了。"

    hide heyingqin

    show chencheng

    chencheng "我建議我們加強敵後游擊戰，擾亂日軍後勤補給線。"

    hide chencheng

    show johndrawold

    voice "voiyalan18.wav"
    j "很好。陳誠，你負責組織和協調各地的游擊隊。何應欽，你負責與國際社會聯絡，爭取更多支持。張治中，你負責重新整編我們的部隊，為下一階段的反攻做準備。"

    jump chapter3_act4

#第四幕：武漢會戰
label chapter3_act4:
    scene bg imgyalan6
    with fade

    $ now_venue.location = "武漢指揮部"
    "1938年，武漢指揮部"

    show johndrawold

    voice "voiyalan19.wav"
    j "1938年，日軍開始向武漢發起進攻。武漢是我們的臨時首都，也是抗戰的重要基地，我們必須全力防守。"

    voice "voiyalan20.wav"
    j "諸位，武漢是我們最後的防線。我們必須不惜一切代價守住它！"

    hide johndrawold

    show chencheng

    chencheng "是，委座！我們已經做好了全面防守的準備。我們在武漢周圍構築了多道防線，並且集中了我們最精銳的部隊。"

    hide chencheng

    show heyingqin

    heyingqin "委座，根據情報，日軍這次投入了大量兵力，他們顯然是想一舉拿下武漢。"

    hide heyingqin

    show zhangzhizhong

    zhangzhizhong "我們已經動員了全城的百姓參與防禦工事的修築，全民皆兵！"

    hide zhangzhizhong

    show johndrawold

    voice "voiyalan21.wav"
    j "很好。我們還要充分利用地形優勢。長江、漢水，這些天然屏障要成為日軍的噩夢。"

    scene bg imgyalan7

    with fade

    $ now_venue.location = "武漢戰場"
    "武漢戰場"

    show chencheng

    chencheng "弟兄們，堅持住！我們要讓日本人付出慘重的代價！"

    hide chencheng

    show zhangzhizhong

    zhangzhizhong "陳將軍，日軍的炮火太猛烈了，我們的防線快要撐不住了！"

    hide zhangzhizhong

    show chencheng

    chencheng "不要怕！記住我們身後就是武漢，就是全中國的希望。死戰不退！"

    hide chencheng

    show johndrawold

    voice "voiyalan22.wav"
    j "儘管我們奮勇抵抗，但最終還是不得不放棄武漢。然而，這場戰役極大地消耗了日軍的實力，為我們的持久戰略贏得了時間。"

    scene bg imgyalan8
    with fade

    $ now_venue.location = "撤退路上"
    "撤退路上"

    show johndrawold

    voice "voiyalan23.wav"
    j "諸位，武漢的失守並不意味著我們的失敗。相反，這標誌著我們抗戰進入了一個新的階段。我們將採取持久戰略，消耗日軍的實力，等待國際局勢的變化。"

    hide johndrawold

    show heyingqin

    heyingqin "委座，接下來我們該如何部署？"

    hide heyingqin

    show johndrawold

    voice "voiyalan24.wav"
    j "陳誠，你負責組織游擊戰，騷擾日軍後方。張治中，你負責重新整編我們的部隊。何應欽，你負責與國際社會聯絡，爭取更多支持。"

    hide johndrawold

    show chencheng
    show zhangzhizhong at left
    show heyingqin at right

    chencheng "是，委座！"
    zhangzhizhong "是，委座！"
    heyingqin "是，委座！"

    hide chencheng
    hide zhangzhizhong
    hide heyingqin

    show johndrawold:
        yalign 1.0
        xzoom -1
        xalign 0.5
        linear 1 xalign 0.1

    voice "voiyalan25.wav"
    j "記住，這是一條艱難的道路，但我相信，只要我們堅持下去，最終的勝利一定是屬於我們的。"

    jump chapter3_act5

#第五幕：長沙會戰
label chapter3_act5:
    scene bg imgyalan9
    with fade

    $ now_venue.location = "長沙指揮部"
    "1939年，長沙指揮部"

    show johndrawold

    voice "voiyalan26.wav"
    j "1939年，日軍向長沙發起進攻。這是一個重要的轉折點，我們終於在正面戰場上取得了重大勝利。"

    voice "voiyalan27.wav"
    j "陳誠，長沙的防務就交給你了。記住，這可能是我們扭轉戰局的機會。"

    hide johndrawold

    show chencheng

    chencheng "請委座放心，我一定不辱使命！我已經制定了一個詳細的防禦計劃。"

    hide chencheng

    show heyingqin

    heyingqin "我們的情報顯示，日軍這次投入了約10萬兵力，由岡村寧次指揮。"

    hide heyingqin

    show zhangzhizhong

    zhangzhizhong "但我們已經做好了充分的準備，相信能給日軍一個迎頭痛擊。"

    hide zhangzhizhong

    show johndrawold

    voice "voiyalan28.wav"
    j "很好。記住，我們不僅要防守，更要主動出擊。要充分利用地形優勢，實施誘敵深入、圍而殲之的策略。"

    scene bg imgyalan10
    with fade

    $ now_venue.location = "長沙戰場"
    "長沙戰場"

    show chencheng

    chencheng "按照計劃，先誘敵深入，然後實施包圍！"

    hide chencheng

    show zhangzhizhong

    zhangzhizhong "陳將軍，日軍已經進入我們預設的包圍圈了！"

    hide zhangzhizhong

    show chencheng

    chencheng "好！命令各部隊立即展開反擊！"

    hide chencheng

    show johndrawold

    voice "voiyalan29.wav"
    j "在陳誠的指揮下，我軍採用了聰明的戰術，先誘敵深入，然後實施包圍殲滅。這個策略取得了巨大的成功。"

    scene bg imgyalan11
    with fade

    $ now_venue.location = "戰後的戰場"
    "戰後的戰場"

    show chencheng

    chencheng "報告委座，我軍已經徹底殲滅了日軍的主力部隊！此役我軍殲敵近3萬，創下了抗戰以來最大的勝績！"

    hide chencheng

    show johndrawold

    voice "voiyalan30.wav"
    j "非常好！這是我們抗戰以來，第一個重大勝利，它將極大地鼓舞全國軍民的士氣！"

    hide johndrawold

    show heyingqin

    heyingqin "委座，這次勝利不僅在軍事上意義重大，在政治和外交上也會產生深遠影響。"

    hide heyingqin

    show zhangzhizhong

    zhangzhizhong "是的，這證明了我們的持久戰略是正確的。日軍並非不可戰勝！"

    hide zhangzhizhong

    show johndrawold

    voice "voiyalan31.wav"
    j "諸位說得對。這次勝利向全世界證明了中國抗戰的決心和能力。我們要乘勝追擊，繼續削弱日軍的實力。"

    jump chapter3_act6

#第六幕：豫湘桂會戰與反攻
label chapter3_act6:
    scene bg imgyalan12
    with fade

    $ now_venue.location = "重慶指揮部"
    "1944年，重慶指揮部"

    show johndrawold

    voice "voiyalan32.wav"
    j "1944年，日軍發動了最後一次大規模進攻，即豫湘桂會戰。儘管我們遭受了重創，但這也為我們的最終反攻創造了條件。"

    voice "voiyalan33.wav"
    j "諸位，日軍已經開始了他們的最後一搏。我們必須堅持住，等待反攻的時機。"

    hide johndrawold

    show heyingqin

    heyingqin "是的，委座。我們的美式裝備已經開始大量到達，我軍的實力正在迅速增強。"

    hide heyingqin

    show chencheng

    chencheng "但日軍這次投入了大量兵力，我們在正面戰場上可能會遭受重創。"

    hide chencheng

    show zhangzhizhong

    zhangzhizhong "我建議我們採取靈活機動的戰術，避免與日軍硬拼，保存實力。"

    hide zhangzhizhong

    show johndrawold

    voice "voiyalan34.wav"
    j "你們說得都對。我們要既堅持抵抗，又要保存實力。更重要的是，我們要開始為最後的反攻做準備。"

    scene bg imgyalan13
    with fade

    $ now_venue.location = "戰場"
    "戰場"

    show chencheng

    chencheng "報告委座，日軍已經攻佔了長沙和衡陽，正向貴州推進。"

    hide chencheng

    show johndrawold

    voice "voiyalan35.wav"
    j "我們必須在貴州設防，絕不能讓日軍威脅到重慶！"

    hide johndrawold

    show heyingqin

    heyingqin "委座，美國已經同意增加對我們的援助。我們很快就能獲得更多的武器裝備。"

    hide heyingqin

    show johndrawold

    voice "voiyalan36.wav"
    j "很好。我們要抓住這個機會，加快部隊的訓練和改編。"

    scene bg imgyalan14
    with fade

    $ now_venue.location = "1945年，中國軍隊反攻"
    "1945年，中國軍隊反攻"

    show johndrawold

    voice "voiyalan37.wav"
    j "全軍聽令，現在是我們反攻的時候了！"

    hide johndrawold

    show heyingqin

    heyingqin "各路大軍已經準備就緒，隨時可以發起總攻擊！"

    hide heyingqin

    show chencheng

    chencheng "委座，我軍已經收復了長沙和衡陽，正向武漢挺進。"

    hide chencheng

    show zhangzhizhong

    zhangzhizhong "我部已經解放了南昌，正在向浙江推進。"

    hide zhangzhizhong

    show johndrawold

    voice "voiyalan38.wav"
    j "在盟軍的配合下，我們開始了大規模的反攻。我們收復了大片失地，日本侵略者節節敗退。"

    scene bg imgyalan15
    with fade

    $ now_venue.location = "南京"
    "1945年8月15日，南京"

    show johndrawold

    voice "voiyalan39.wav"
    j "今天，我們終於迎來了這一天。日本無條件投降，我們的抗戰勝利了！"

    hide johndrawold

    show heyingqin

    heyingqin "委座，這是全國軍民共同奮鬥的結果！"

    hide heyingqin

    show chencheng

    chencheng "我們終於實現了驅逐日寇、收復失地的目標！"

    hide chencheng

    show zhangzhizhong

    zhangzhizhong "這場勝利來之不易，我們付出了巨大的犧牲。"

    hide zhangzhizhong

    show johndrawold

    voice "voiyalan40.wav"
    j "是的，這場勝利來之不易。我們付出了巨大的代價，但我們捍衛了國家的獨立和民族的尊嚴。現在，我們要開始重建我們的國家了。"

    voice "voiyalan41.wav"
    j "抗日戰爭的勝利，標誌著中國近代以來反抗外來侵略的第一次完全勝利。這場戰爭改變了中國的命運，也改變了世界的格局。"
    
    voice "voiyalan42.wav"
    j"我們必須銘記這段歷史，珍惜來之不易的和平，為中華民族的偉大復興而繼續奮鬥。"


    return

# 第一幕：事件爆發
label chapter4_act1:
    $ renpy.block_rollback()
    scene bg imgjcf1
    with fade

    $ now_venue.location = "臺北市延平北路"
    show screen location_ui

    "1947年2月27日傍晚，臺北市延平北路"

    show igov at right

    igov "站住！交出私菸！"

    show cshop at left

    cshop "大人，求求您高抬貴手。我只是想養家糊口...至少把錢和一些香菸還給我吧。"

    igov "法律就是法律！不許討價還價！"

    cshop "（跪地哀求）大人，我家裡還有老小要養..."

    "專賣局查緝員用槍柄擊打菸販，引發群眾憤怒"

    hide cshop

    hide igov

    show imgjcf2 :
        yalign 0.45 
        xalign 0.5
        size(1920,1080)  #size(1024,576)

    show peoplea

    peoplea "打人啦！欺負老百姓！"

    hide peoplea

    show peopleb

    peopleb "太過分了！大家一起上！"

    hide peopleb

    show igov

    igov "後退！否則我們就開槍了！"

    hide igov

    "專賣局查緝員開槍示警，誤殺一旁路人"

    show peoplec

    peoplec "天啊！有人中槍了！"

    hide peoplec

    show peopled

    peopled "快叫救護車！"

    hide peopled

    show peoplee

    peoplee "他們殺人了！抓住他們！"

    hide peoplee

    hide imgjcf2

    jump chapter4_act2

# 第二幕：局勢升級
label chapter4_act2:
    scene bg imgjcf3 :
        size(1920,1080)
    with fade

    $ now_venue.location = "臺北市"
    "1947年2月28日，臺北市"

    show peoplel

    peoplel "我們要求立即懲處兇手，廢除專賣制度！還要求政府公開道歉！"

    hide peoplel

    show reporter

    reporter "各位同胞，我們必須組織起來，向政府表達我們的訴求。但要保持理性，避免暴力。"

    hide reporter

    show tdstudent

    tdstudent "光是和平請願是不夠的！我們要罷市、罷課、罷工，讓政府知道我們的決心！"

    hide tdstudent

    show ttp

    ttp "冷靜點，各位。我們可以組織一個處理委員會，代表民眾與政府談判。"

    hide ttp

    scene bg imgjcf4:
        size(1920,1080) 
    with fade

    $ now_venue.location = "南京"
    "南京，國民政府 "

    show chenyi

    chenyi "（通過電話）：委座，臺北局勢失控。民眾組織了「二二八事件處理委員會」，提出三十二條政治改革要求。"

    hide chenyi

    show johndraw

    voice "voijcf1.wav"
    j "具體要求是什麼？"

    hide johndraw

    show chenyi

    chenyi "他們要求廢除長官公署，實施地方自治，甚至要求軍隊撤出臺灣。"

    hide chenyi

    show johndraw

    voice "voijcf2.wav"
    j "這已經超出了單純的民生訴求，變成了政治挑戰。陳儀，你立即採取行動穩定局勢，必要時請求軍事支援。"

    hide johndraw

    show chenyi

    chenyi "是，委座。但是...如果動用軍隊，恐怕會造成更大的反彈。"

    hide chenyi

    show johndraw

    voice "voijcf3.wav"
    j "我們必須維護國家統一。你先試圖安撫民眾，同時準備軍事行動。"

    hide johndraw

    jump chapter4_act3


# 第三幕：軍隊進駐
label chapter4_act3:
    scene bg imgjcf5 :
        size(1920,1080)
    with fade

    $ now_venue.location = "基隆港"
    "基隆港，1947年3月8日 "

    show armyl

    armyl "弟兄們，我們的任務是平定叛亂，恢復秩序。全面進攻！"

    hide armyl

    show armya

    armya "長官，那些看起來只是普通百姓啊。"

    hide armya

    show armyl

    armyl "執行命令！叛亂分子往往隱藏在平民中。"

    hide armyl

    show tpa

    tpa "天啊！他們在開槍！快逃啊！"

    hide tpa

    show tpb

    tpb "為什麼？我們又沒有做錯什麼！"

    hide tpb

    scene bg imgjcf6 :
        size(1920,1080)
    with fade

    $ now_venue.location = "臺北市長官公署"
    "臺北市長官公署 "

    show chenyi 

    chenyi "我已下令全臺戒嚴，解散處理委員會等非法組織。"

    hide chenyi

    show imgjcf7 :
        yalign 0.45 
        xalign 0.5
        size(1024,576)

    "當時戒嚴圖片"

    hide imgjcf7

    show johndraw

    voice "voijcf4.wav"
    j "（通過電話）：務必迅速恢復秩序，但要避免過度傷亡。我們的目標是穩定局勢，不是激化矛盾。"

    hide johndraw

    show chenyi

    chenyi "明白，委座。但是...有些軍官似乎過於激進。"

    hide chenyi

    show johndraw

    voice "voijcf5.wav"
    j "那就約束他們！記住，我們最終還是要在臺灣長治久安。"

    hide johndraw

    jump chapter4_act4


# 第四幕：衝突加劇
label chapter4_act4:
    scene bg imgjcf8 :
        size(1920,1080)
    with fade

    $ now_venue.location = "嘉義市"
    "嘉義市，1947年3月中旬 "

    show peoplel

    peoplel "同胞們！政府軍正在屠殺我們的親人！我們必須保衛家園！"

    hide peoplel

    show cpa

    cpa "可是許大哥，我們怎麼可能抵抗正規軍？"

    hide cpa

    show cpb

    cpb "對啊，他們有飛機、大炮，我們只有一些老舊的槍枝。"

    hide cpb

    show peoplel

    peoplel "寧為玉碎，不為瓦全！我們別無選擇。拿起武器，保衛我們的權利！就算死，也要讓他們付出代價！"

    hide peoplel

    show cpc

    cpc "許大哥說得對！為了我們的子孫後代，我們不能坐以待斃！"

    hide cpc

    jump chapter4_act5


# 第五幕：鎮壓與清算
label chapter4_act5:
    scene bg imgjcf6 :
        size(1920,1080)
    with fade

    $ now_venue.location = "臺北市"
    "臺北市，1947年3月下旬  "

    show keyuanfen

    keyuanfen "（警備總司令部參謀長）：委座，我們已掌握大量參與叛亂者的名單。包括許多知識分子和社會領袖。"

    hide keyuanfen

    show johndraw

    voice "voijcf6.wav"
    j "具體有哪些人？"

    hide johndraw

    show keyuanfen

    keyuanfen "有臺大教授、醫生、律師，還有一些地方上有影響力的人士。"

    hide keyuanfen

    show johndraw

    voice "voijcf7.wav"
    j "依法處置。但要注意區分首謀和跟從者。我們的目的是肅清叛亂，不是濫殺無辜。"

    hide johndraw

    show keyuanfen

    keyuanfen "明白。那麼...對於那些逃跑的人，我們該如何處理？"

    hide keyuanfen

    show johndraw

    voice "voijcf8.wav"
    j "發布通緝令。必要時可以考慮赦免那些主動投案的人，以分化瓦解他們。"

    hide johndraw

    jump chapter4_act6


# 第五幕：鎮壓與清算
label chapter4_act6:
    scene bg imgjcf6 :
        size(1920,1080)
    with fade

    $ now_venue.location = "臺北市"
    "臺北市，1949年"

    show chencheng

    chencheng "（臺灣省主席）：委座，二二八事件後，許多知識分子逃往海外或轉向地下活動。我們必須加強社會控制。"

    hide chencheng

    show johndraw

    voice "voijcf9.wav"
    j "具體情況如何？"

    hide johndraw

    show chencheng

    chencheng "有人加入了共產黨的地下組織，也有人開始宣傳臺灣獨立的理念。"

    hide chencheng

    show johndraw

    voice "voijcf10.wav"
    j "這是個嚴峻的挑戰。威權統治是現階段的必要之舉。但長遠來看，我們需要贏得民心。"

    hide johndraw

    show chencheng

    chencheng "是的。我們正在推行一些文化政策，強化中國認同。"

    hide chencheng

    show johndraw

    voice "voijcf11.wav"
    j "很好。記住，治臺灣，關鍵是要讓臺灣人認同我們。"

    hide johndraw

    voice "voijcf12.mp3"
    "二二八事件不僅是一場悲劇，更成為臺灣社會長期分裂的根源。它深刻影響了臺灣的政治發展，也成為推動臺灣民主化的重要動力。"

    voice "voijcf13.mp3"
    "這段歷史提醒我們，面對矛盾與衝突，對話與理解比暴力更能解決問題。今天的臺灣，正是在這樣的反思和和解中，逐步走向更加開放、民主的社會。"

    return

# 第五章：第二次國共內戰  

label chapter5:
    scene bg blackscreen
    with fade

        

    "第五章：第二次國共內戰"

    # 第一幕：和平破裂 
    label chapter5_act1:
        scene bg imgchung
        with fade
        play music "ch5bgm.wav" volume 0.4

        $ now_venue.location = "重慶談判現場"

        voice "voili1.wav"
        j "1945年8月,日本投降。表面上國共同慶勝利,暗地裡卻已劍拔弩張。這場看似和平的較量,很快就要演變成一場你死我活的較量。"

        

        
        voice "voili2.wav"
        j "毛先生,抗戰勝利了,是時候放下成見,接受國民政府的領導,共建統一的中國了。"

        
        voice "mao1.wav"
        mzd "蔣委員長,您這是要當大家長啊?我們可都長大了,誰也不願意被誰領導。"


        voice "voili3.wav"
        j "荒唐!沒有國民政府,哪來的抗戰勝利?你們應該感恩戴德!"

        
        voice "mao2.wav"
        mzd "別氣嘛,蔣委員長。我們在敵後打游擊,也沒閒著。這勝利,是全中國人民共同奮鬥的結果。"


        voice "voili4.wav"
        j "那你的意思是?"

        voice "mao3.wav"
        mzd "很簡單,平起平坐,共組聯合政府。"


        voice "voili5.wav"
        j "休想!"

        voice "voili6.wav"
        j "就這樣,雙方進行了長達43天的談判,你來我往,唇槍舌劍,最終不歡而散。和平的希望,像泡沫一樣破滅了。"

       

    # 第二幕：內戰爆發
    label chapter5_act2:
        scene bg imgli2
        with fade

        $ now_venue.location = "國民黨軍營"

        voice "voili7.wav"
        j "1946年6月,國共衝突全面爆發。這場內戰,就像是一場你死我活的麻將對弈,誰也不肯認輸。"


        gmdg "弟兄們,共軍那些土八路,連像樣的槍都沒有,還想跟我們鬥?我們有美國大爺的先進武器,這仗不打都要贏!"

        solc "將軍,我們一定能把他們打得落花流水!"

        soli "就是!到時候我們就能吃香的喝辣的了!"

        gmdg "少說兩句,小心舌頭把腦袋給害了。"

        scene bg imgli3
        with fade

        $ now_venue.location = "共軍陣地"

    

        igl "同志們,國民黨那些傢伙以為有洋槍洋炮就了不起了。他們忘了一句老話:槍再好,沒有人也不中用!"

        zc "報告首長,我們的武器確實不如國軍..."

        igl "沒關係!我們有最厲害的武器 - 人民群眾!只要我們依靠群眾,就能以小搏大,以弱勝強!"

        zi "對!我們還可以打游擊,讓國民黨的坦克都用不上勁!"

        igl "說得好!我們就要像泥鰍一樣,滑溜溜的,讓國民黨這條大鯉魚抓不住我們!"

        gsol "長官,不好了!共軍的游擊戰術太厲害了,我們被包圍了!"

        gz "同志們,衝啊!讓國民黨的洋槍洋炮都變成我們的玩具!"

        voice "voili8.wav"
        j "就這樣,中國大地上再次硝煙四起。這場內戰,註定要改變中國的命運..."

        

    # 第三幕：三大戰役
    label chapter5_act3:
        scene bg imgli4
        with fade
        "：遼沈戰役"

        $ now_venue.location = "遼沈戰役"

        voice "voili9.wav"
        j "1948年下半年到1949年初,共產黨發動了改變戰局的三大戰役。這三場戰役,就像是三記重拳,直接把國民黨打得找不到北。"

        

        gigl "同志們,我們要圍點打援,全殲國民黨東北軍!這就像下棋,把對方的軍隊圍在中間,然後一口一口吃掉!"

        zc "首長,這仗要怎麼打?"

        gigl "很簡單,我們先裝作很弱,引誘國民黨軍隊進來。等他們進來了,我們再關上門,一網打盡!"

        zi "哦!這不就是關門打狗嗎?"

        gigl "聰明!不過千萬別讓國民黨聽見,不然他們肯定不上當。"

        scene bg imgli5
        with fade
        $ now_venue.location = "國民黨指揮部"

        "國民黨指揮部"

        gg "援軍呢?為什麼還不到?我們快要撐不住了!"

        igl2 "將軍,共軍已經...已經把我們包圍了..."

        gg "完了...這下我們成了甕中之鱉..."

        scene bg imgli6
        with fade
        $ now_venue.location = "平津戰役"

        "平津戰役"

        ggz "報告!北平城內的同志發來消息,說傅作義將軍有意投誠!"

        mzd "好!要促成和平解放北平!這可比打仗省事多了。"

        znl "是啊,這樣既保存了實力,又贏得了民心。"

        mzd "沒錯!這就叫做不戰而屈人之兵。孫子兵法果然博大精深啊!"

        scene bg imgli7
        with fade
        $ now_venue.location = "淮海戰役"

        "淮海戰役"

        gg "我們被包圍了,彈藥糧食都快耗盡了...這下真的是山窮水盡了..."

        igl2 "將軍,我們...我們要不要投降?"

        gg "投降?我寧可戰死!"

        zhu "同志們,勝利在望!再加把勁!我們就要徹底殲滅國民黨的精銳部隊了!"

        ggz "報告首長,我們繳獲了大量武器彈藥!"

        zhu "好啊!這下我們不但打敗了敵人,還發了一筆橫財!"

    # 第四幕：國共策略對比
    label chapter5_act4:
        scene bg imgli8
        with fade
        $ now_venue.location = "國民黨高層會議"

        "國民黨高層會議"

        ggunz "我們需要更多的資金來維持戰爭。再這樣下去,連軍餉都發不出來了。"

        gguni "那還不簡單?再加稅唄,反正老百姓已經習慣了。"

        gunb "對對對!再來個臨時條例,把老百姓的口袋都掏空!"

        voice"voili10.wav"
        j "混帳!你們這是要逼民反嗎?"

        

        gunz "委員長息怒,我們也是為了江山社稷著想啊..."

        voice"voili11.wav"
        j "唉...我看這江山社稷怕是保不住了..."

        

        scene bg imgli9
        with fade
        $ now_venue.location = "共產黨群眾大會"

        "共產黨群眾大會"

        mzd "同志們,我們要與人民站在一起,依靠他們的力量取得勝利!人民,只有人民,才是創造世界歷史的動力!"

        crowd "毛主席萬歲!共產黨萬歲!"

        gzg "同志們,我們要減租減息,把土地分給農民!讓大家都能吃飽飯,穿暖衣!"

        nonz "真的嗎?我們真的能有自己的土地了?"

        noni "共產黨好啊!共產黨是我們老百姓的救星!"

    # 第五幕：國際影響
    label chapter5_act5:
        scene bg imgli10
        with fade
        $ now_venue.location = "美國大使館"

        "美國大使館"

        amegun "我們必須支持蔣委員長,以遏制共產主義在亞洲的擴張。"

        zu "可是長官,國民黨的腐敗問題很嚴重..."

        amegun "管不了那麼多了!先把這批武器送過去再說!"

        scene bg imgli11
        with fade
        $ now_venue.location = "中蘇邊境"

        "中蘇邊境"

        su "同志,這些先進武器和作戰經驗,會幫助你們取得勝利的。"

        chd "謝謝!我們一定不負蘇聯同志的期望!"

    # 第六幕：戰局逆轉
    label chapter5_act6:
        scene bg imgli12
        with fade
        $ now_venue.location = "南京總統府"

        "南京總統府"

        voice"voili12.wav"
        j "我們...輸了嗎..."

        

        igl2 "委員長,我們必須立即撤退到台灣!"

        voice"voili13.wav"
        j "好,帶上能帶的一切。我們還有機會東山再起!"

        

    # 第七幕：開國大典
    label chapter5_act7:
        scene bg imgli13
        with fade
        $ now_venue.location = "北京天安門廣場"

        "北京天安門廣場"

        mzd "中華人民共和國,中央人民政府,今天成立了!"

        crowd "毛主席萬歲!新中國萬歲!"

        voice"voili14.wav"
        j "就這樣,歷時四年的國共內戰落下帷幕。中國大陸易主,進入了新的歷史階段。這場內戰不僅改變了中國的政治格局,也對整個亞洲乃至世界產生了深遠的影響。"
        return 




# 第六章：中華民國政府遷台 (此章沒分幕)
label chapter6_act1:
    $ renpy.block_rollback()
    scene bg imgjcs1 :
        size(1920,1080)
    with fade

    $ now_venue.location = "南京總統府"
    show screen location_ui

    "南京總統府，1949年1月"

    voice "voijcs1.wav"
    "1949年，國共內戰進入最後階段。國民黨政府面臨著前所未有的危機。我們不僅要應對軍事失利，還要處理經濟崩潰、民心動搖等諸多問題。"

    show johndraw

    voice "voijcs2.wav"
    j "（神情凝重，手指在地圖上移動）何應欽將軍，平津已經失守，華北幾乎全部淪陷。我們必須立即啟動『國光計劃』。"

    hide johndraw

    show heyingqin

    heyingqin "是，委員長。但『國光計劃』涉及將近200萬軍民的撤退，時間緊迫，困難重重。"

    hide heyingqin

    show johndraw

    voice "voijcs3.wav"
    j "我明白。首先，空軍必須立即遷至台灣。你親自督促，確保300多架戰機和65艘艦艇24小時內準備就緒。"

    hide johndraw

    show heyingqin

    heyingqin "遵命。但委座，您何時撤離？共軍推進速度遠超我們預期。"

    hide heyingqin

    show johndraw

    voice "voijcs4.wav"
    j "（沉重地）我會在最後時刻離開。現在，立即開始疏散重要人員和物資。記住，黃金儲備和文物是重中之重。"

    hide johndraw

    show heyingqin

    heyingqin "是。那麼龐大的中央銀行黃金儲備..."

    hide heyingqin

    show johndraw

    voice "voijcs5.wav"
    j "由嚴密的武裝部隊護送，務必確保安全。這是我們在台灣重建的根基。"

    hide johndraw

    scene bg imgjcs2 :
        size(1920,1080)
    with fade

    $ now_venue.location = "中央研究院"
    "中央研究院，1949年2月"

    show fusinian

    fusinian "（焦急地翻閱文件）朱院長，日本投降後歸還的圖書文獻近30萬冊，我們根本無法全部帶走！"

    hide fusinian

    show zhujiahua

    zhujiahua "形勢危急，我們必須有所取捨。優先保護珍本善本和重要檔案資料。"

    hide zhujiahua

    show fusinian

    fusinian "這些都是中華文化的根基啊！每一本都彌足珍貴。"

    hide fusinian

    show zhujiahua

    zhujiahua "我同意。但現實很殘酷，我們的運輸能力有限。"

    hide zhujiahua

    show assistant

    assistant "（衝進房間）傅先生，朱先生，共軍已突破淮海戰場，隨時可能進入南京！"

    hide assistant

    show fusinian

    fusinian "（痛苦地）好吧，我們必須立即行動。朱兄，你負責聯繫軍方協調運輸，我來組織人手分類裝箱。我們一定要盡最大努力保護這些文化瑰寶！"

    hide fusinian

    voice "voijcs6.wav"
    "隨著共產黨的勢力不斷擴大，大規模撤退行動在各地展開。這是一場驚心動魄的大遷徙，也是一場悲壯的告別。"

    scene bg imgjcs3 :
        size(1920,1080)
    with fade

    $ now_venue.location = "上海港口"
    "上海港口，1949年5月"

    "碼頭上人山人海，混亂場面中充滿哭喊聲"

    show johndraw

    voice "voijcs7.wav"
    j "（對著麥克風）同胞們，我們暫時撤離，但終將光復大陸！請保持秩序，相信政府！"

    hide johndraw

    peoples"（此起彼伏）我們的家園怎麼辦？共產黨會不會殺我們的家人？"

    show faramy

    faramy "委員長，民眾情緒激動，恐慌情緒可能引發踩踏事故。"

    hide faramy

    show johndraw

    voice "voijcs8.wav"
    j "加強警戒，維持秩序。優先撤離重要機構人員和家屬。"

    hide johndraw

    "突然，遠處傳來炮聲"

    show saramy

    saramy "（衝上甲板）委員長，共軍已攻入上海市區！"

    hide saramy

    show johndraw

    voice "voijcs9.wav"
    j "（看著岸上絕望的人群，痛苦地）「再等十分鐘。我們要盡力帶走每一個人！"

    hide johndraw

    voice "voijcs10.wav"
    "1949年12月7日，國民政府正式宣布遷都台北。這不僅是一個政權的遷移，更是無數人命運的轉折點。"

    scene bg imgjcs4 :
        size(1920,1080)
    with fade

    $ now_venue.location = "台北臨時總統府 "
    "台北臨時總統府，1950年3月"

    show johndraw

    voice "voijcs11.wav"
    j "王部長，我們的經濟情況如何？"

    hide johndraw

    show wangshijie

    wangshijie "報告委員長，情況危急。雖然我們帶來了約300萬兩黃金，但通貨膨脹嚴重，物價飛漲。"

    hide wangshijie

    show johndraw

    voice "voijcs12.wav"
    j "立即實施貨幣改革。以新台幣取代舊台幣，比率定為1:40,000。"

    hide johndraw

    show imgjcs5 :
        yalign 0.45 
        xalign 0.5
        size(1024,576)

    "當時歷史圖片"

    hide imgjcs5

    show wangshijie

    wangshijie "這可能引起社會動盪..."

    hide wangshijie


    show johndraw

    voice "voijcs13.wav"
    j "別無選擇。同時，啟動土地改革，實施耕者有其田政策。我們必須在台灣站穩腳跟。"

    hide johndraw

    scene bg imgjcs6 :
        size(1920,1080)
    with fade

    $ now_venue.location = "台北中山堂"
    "台北中山堂，1952年"

    show johndraw

    voice "voijcs14.wav"
    j "同志們，經過艱苦努力，我們的黨員從最初5萬人增加到近30萬，其中超過一半是台灣本省人。"

    hide johndraw

    show chencheng

    chencheng "報告委員長，我們已在全台建立了3萬多個工作小組，深入社會各階層。"

    hide chencheng

    show johndraw

    voice "voijcs15.wav"
    j "很好。但我們面臨的挑戰還很多。必須加強軍事戒備，防範共軍進攻；同時推動經濟建設，為反攻大陸做準備。"

    hide johndraw

    allp"反攻大陸！收復河山！"

    voice "voijcs16.wav"
    "就這樣，中華民國政府在台灣艱難地站穩了腳跟。雖然『反攻大陸』的夢想最終未能實現，但這個曾經的小島在之後的幾十年裡，卻創造了驚人的經濟奇蹟和政治轉型。"

    voice "voijcs17.wav"
    "這段歷史，不僅見證了一個政權的轉折，一個島嶼的蛻變，更記錄了無數人在動盪中奮鬥、在逆境中重生的故事。"

    return

# 第七章：白色恐怖時期

# 第一幕：戒嚴令頒布（1949年5月）
label chapter7_act1:
    scene bg imghui1
    with fade
    $ now_venue = place("台灣省政府會議室")
    "台灣省政府會議室"
    show screen location_ui
    show chencheng at left_to_middle

    chencheng "委座,《台灣省戒嚴令》草案已經擬好,請過目。"

    show johndraw:
        yalign 1.0
        xalign 0.5
        xzoom -1

    voice "voihui1.wav"
    j "內容很全面。陳誠,你怎麼看這個決定可能帶來的影響？"

    chencheng "民眾可能會有些不安,但為了國家安全,這是必要之舉。我們必須防止共匪滲透。自從二二八事件後,台灣社會一直不穩定。"

    voice "voihui2.wav"
    j "我明白。我們必須盡一切努力防止共產黨滲透。為了國家安全,實施戒嚴是必要的。但我們也要謹慎行事,避免重蹈二二八事件的覆轍。柯遠芬,你有什麼看法？"

    hide chencheng
    hide johndraw

    show keyuanfen at right_to_middle
    show johndraw at middle_to_left
    keyuanfen "是的,委座。我建議我們加強宣傳,讓民眾理解這是為了他們的安全。同時,我們需要建立一個有效的情報系統,以便及時發現和打擊共產黨的滲透活動。"

    voice "voihui3.wav"
    j "這個想法不錯。彭孟緝,你來負責組建這個情報系統。"

    show p at left

    p "是,委座。我會立即著手進行。不過,我們是否需要考慮對某些特定群體加強監控？比如知識分子和學生。"

    voice "voihui4.wav"
    j "這是個敏感問題。我們必須小心行事,不要激起不必要的反彈。"

    show chencheng at right

    chencheng "我同意彭將軍的建議。知識分子和學生往往最容易受到共產主義思想的影響。"

    voice "voihui5.wav"
    j "那麼我們可以適度加強監控,但要注意方式方法。絕不能讓人感覺我們在針對特定群體。"

    keyuanfen "委座,我們是否需要制定一些具體的執行細則？比如,如何界定'叛亂'行為？"

    voice "voihui6.wav"
    j "這個問題很重要。我們需要一個明確的標準,但同時也要保留一定的彈性。陳誠,你和法務部門商議一下,擬定一個初步方案。"

    chencheng "明白,我會盡快安排。"

    voice "voihui7.wav"
    j "記住,我們的目標是保護國家安全,不要過度擴大打擊範圍。我們要讓人民感到安全,而不是恐懼。以和日掩護外交,以交通掩護軍事,以實業掩護經濟,以教育掩護國防,韜光養晦乃為國家唯一自處之道。"

    hide chencheng
    hide johndraw
    hide keyuanfen
    hide p
    voice "voihui8.wav"
    "當時,我們都沒有意識到這個決定會帶來如此深遠的影響。我們低估了權力的誘惑和濫用的危險。這個決定開啟了長達數十年的白色恐怖時期。"
    jump chapter7_act2

# 第二幕：大規模肅清行動（1950年）
label chapter7_act2:
    scene bg imghui2
    with fade
    $ now_venue = place("警備總部")

    show screen location_ui

    show keyuanfen at left
    keyuanfen "報告司令,我們發現多起疑似共產黨滲透的案件。"

    show p at right
    p "詳細說明。"

    keyuanfen "基隆中學有學生組織名為《光明報》的地下刊物,疑似受共產黨影響。另外,澎湖也發現大規模的共黨組織。"

    p "情況比我們想像的要嚴重。立即採取行動！逮捕所有涉案人員。"

    show g at center
    g "司令,是否需要擴大調查範圍？我懷疑還有更多隱藏的共產黨員。"

    p "可以,但要注意分寸。我們不能引起民眾的恐慌。"

    keyuanfen "還有一件事,司令。我們在調查中發現,有些人可能只是無意中接觸了這些思想,並不是真正的共產黨員。"

    p "即便如此,我們也不能掉以輕心。寧可錯抓一百,不可漏網一個。"

    g "司令,我們是否需要使用...特殊手段來獲取情報？"

    p "如果必要的話,可以。但要控制在合理範圍內。我們不是在製造恐怖,而是在維護安全。"

    keyuanfen "我有些擔心,這樣做會不會引起民眾的不滿？"

    p "這就是為什麼我們需要加強宣傳。要讓民眾明白,我們這麼做都是為了保護他們。"

    hide keyuanfen
    hide p
    hide g

    show johndraw at center
    j "奢言抗日者,殺無赦。對於共產黨的滲透,我們也要採取同樣堅決的態度。但要注意,不要過度擴大打擊範圍,避免造成無辜者的傷害。"

    voice "voihui9.wav"
    j "1950年,我們展開了多起大規模逮捕行動,包括基隆中學的《光明報案》和造成大量山東籍軍人傷亡的《澎湖七一三事件》。"
    hide johndraw
   
    voice "voihui10.wav"
    "當時,我們認為這些行動是必要的,但現在看來,我們犯了嚴重的錯誤。我們的恐懼和猜疑導致了無數無辜者遭受牽連。這些行動不僅沒有增強國家安全,反而埋下了社會分裂的種子。"

    jump chapter7_act3  

# 第三幕：軍中白色恐怖（1955年）
label chapter7_act3:
    scene bg imghui3
    with fade
    $ now_venue = place("總統辦公室")

    show screen location_ui
    show johndraw at left
    voice "voihui11.wav"
    j "這個孫立人似乎野心勃勃,我們必須警惕。"

    show g at right
    g "是的,總統。我們掌握了一些情報,顯示孫立人可能有不軌企圖。他近期頻繁與美國官員接觸,而且在軍中的影響力越來越大。"

    voice "voihui12.wav"
    j "這確實值得關注。你有什麼具體證據嗎？"

    g "目前還沒有確鑿證據,但有多個可靠線人的報告。他們說孫立人私下批評我們的軍事策略,甚至暗示要 '改變現狀'。"

    voice "voihui13.wav"
    j "'改變現狀'？這話什麼意思？"

    g "我們認為,他可能在醞釀一場軍事政變。"

    voice "voihui14.wav"
    j "這是個嚴重的指控。我們不能僅憑猜測就採取行動。"

    show p at center
    p "報告總統,我們在孫立人的親信中安插了一名線人。他提供了一些有趣的信息。"

    voice "voihui15.wav"
    j "說說看。"

    p "孫立人最近幾次與美國軍事顧問的會面都沒有事先報備。而且,他正在秘密調動一些忠於他的部隊。"

    voice "voihui16.wav"
    j "這確實可疑。但我們還是需要更多證據。"

    g "總統,如果我們等到有確鑿證據,可能就為時已晚了。"

    voice "voihui17.wav"
    j "我明白你的顧慮。但是,孫立人在軍中威望很高,如果我們貿然行動,可能會引起軍中動盪。我們必須確保軍隊的忠誠,但也要避免無端的猜疑。能戰始能言和,不能戰而言和,是投降,投降後就是繳械,繳械後就是被屠殺。我們要保持警惕,但不能失去理智。"

    p "那麼,我們是否可以先進行秘密調查?同時,密切監視孫立人的一舉一動。"

    voice "voihui18.wav"
    j "好主意。郭廷亮,你負責這項工作。記住,要謹慎行事,不要打草驚蛇。"

    voice "voihui19.wav"
    "1955年的『孫立人兵變案』,又稱『郭廷亮匪諜案』,牽連了約三百餘人。這次事件嚴重打擊了軍中異己,但也埋下了日後軍中不信任的種子。蔣中正開始意識到,過度的猜疑可能會傷害我們自己。權力的行使如履薄冰,一個不慎,就可能造成無法挽回的錯誤。"

    hide johndraw
    hide g
    hide p
    jump chapter7_act4  

# 第四幕：知識分子的迫害（1960年）
label chapter7_act4:
    scene bg imghui4
    with fade
    $ now_venue = place("《自由中國》雜誌社")

    show screen location_ui

    show l at left
    l "諸位,最新一期的稿件我都看過了。內容很好,但我擔心可能會引起當局的不滿。"

    show y at center
    y "雷老,我們是不是該考慮稍微溫和一些?最近的政治氛圍越來越緊張了。"

    show f at right
    f "但如果我們自我審查,那還有什麼言論自由可言?"

    show l at left
    l "傅正說得對。我們辦這份雜誌,就是為了說出真話。"

    show y at center
    y "我完全理解,但我們也要為員工的安全著想。上週,有人跟蹤我回家。"

    l "我明白你們的顧慮。但是,如果我們不說,誰來說?我們不能讓台灣陷入完全的言論黑暗。"

    show f at right
    f "那麼,我們是否可以採取一些策略?比如用更委婉的語言?"

    l "不,現在不是妥協的時候。我們必須堅持真理,即使付出代價。"

    y "雷老,我敬佩你的勇氣。但我擔心的不只是我們自己,還有我們的家人和朋友。他們也可能因此受到牽連。"

    l "我明白你們的顧慮。但請相信我,堅持正義終將得到回報。台灣需要我們的聲音。"

    hide l
    hide y
    hide f

    voice "voihui20.wav"
    "對於知識分子的控制,蔣中正曾說過:'中國在國民黨以外,除了共產黨,再沒有什麼其他黨派了。所謂其他黨派實際是不能算數的。'這種思維導致了對異見者的打壓。現在看來,這是一個嚴重的錯誤。"
    jump chapter7_act5  
# 第五幕中的對話需要相應修改
label chapter7_act5:
    scene bg imghui5
    with fade
    $ now_venue = place("總統府")

    show screen location_ui

    show johndraw at left
    voice "voihui21.wav"
    j "美國對我們的人權狀況越來越不滿了。"

    show yan at right
    yan "是的,總統。特別是在1970年的『泰源監獄案』之後,國際輿論對我們非常不利。聯合國也開始關注台灣的人權問題。"

    voice "voihui22.wav"
    j "這個趨勢很危險。我們如何在維護國家安全和應對國際壓力之間取得平衡?歷來亡國之原因,並不在於敵寇外患之強大,而是在於內部之分崩離析。我們必須在維護國家安全和推進改革之間找到平衡。"

    yan "我們可以考慮逐步放寬一些限制,展現我們改革的決心。比如,可以減少對新聞媒體的管控。"

    show johnson at center  # 使用 johnson 而不是 jj
    johnson "父親,同意嚴副總統的看法。世界在變,我們也必須改變。"
    
    voice "voihui23.wav"
    j "但是,如果我們放鬆管控,共產黨會不會趁機滲透?"

    johnson "這個風險確實存在。但我認為,我們可以通過其他方式來防範,比如加強經濟建設,提高人民生活水平。"

    yan "沒錯,一個繁榮的社會更容易抵禦共產主義的誘惑。"

    voice "voihui24.wav"
    j "你們說得有道理。但這些年來,我們付出了這麼多代價,難道就這樣放棄嗎?"

    johnson "父親,這不是放棄,而是轉變。我們可以通過經濟發展和逐步的政治改革來鞏固政權,而不是單純依賴高壓政策。"

    j "（長嘆一聲）"

    hide johndraw
    hide yan
    hide johnson

    # 這裡可以添加一個結束的旁白或過場動畫
    "隨著時代的變遷,蔣中正和他的政府開始反思過去的政策。白色恐怖時期逐漸走向尾聲,但它留下的傷痕將長期影響台灣社會。"

    # 跳轉到下一章或結束畫面
    jump chapter8_act1  # 假設下一章是第八章
# 第八章：後期統治
label chapter8_act1:
    $ renpy.block_rollback()
    play music "chapter8.mp3" volume 0.4
    scene bg imgchi14
    with fade
    $ now_venue.location = "台北總統府花園"
    "第八章：後期統治"
    "第一幕：十大建設"
    "1973年，台北總統府"

    show screen location_ui
    show johndraw at left

    j "1973年，我們正式啟動了十大建設計劃。這是台灣經濟發展的關鍵時刻。"

    show minion at right
    minister "總統，十大建設計劃已經開始實施。我們預計這將大大提升台灣的經濟實力。"

    j "很好。記住，我們不僅要追求經濟增長，更要為人民創造更好的生活。"

    show minion at center
    johnson "父親，您放心。我會親自監督這些項目的進展。"

    hide minion

    jump chapter8_act2

label chapter8_act2:
    scene bg imgchi15
    with fade
    $ now_venue.location = "總統府會議室"
    "第二幕：外交挑戰"
    "1975年，總統府會議室"

    show johndraw at left

    j "1975年，我們失去了在聯合國的席位。這是一個巨大的外交挫折。"

    show minion at right
    diplomat "總統，美國已經與中共建交。我們在國際上的處境越來越困難了。"

    j "哼，短視！他們不明白這樣做的後果。但我們不能就此放棄。要積極尋求新的外交突破口。"

    hide minion

    jump chapter8_act3

label chapter8_act3:
    scene bg imgchi16
    with fade
    $ now_venue.location = "蔣中正的私人書房"
    "第三幕：政治改革的壓力"
    "1977年，蔣中正的私人書房"

    show johndraw at left

    j "隨著社會的發展，要求政治改革的聲音越來越大。我知道改變是必要的，但如何改變，是個艱難的抉擇。"

    show minion at right
    johnson "父親，中壢事件後，民間對政治改革的呼聲更高了。我們是否應該考慮放寬一些政策？"

    j "經國，改革是必要的，但必須謹慎。我們要在保持穩定和推動變革之間找到平衡。"

    hide minion

    jump chapter8_act4

label chapter8_act4:
    scene bg imgchi17
    with fade
    $ now_venue.location = "行政院會議室"
    "第四幕：經濟奇蹟"
    "1979年，行政院會議室"

    show johndraw at left

    j "看著台灣的經濟快速發展，我感到欣慰。但我也知道，經濟發展帶來的社會變革，將給我們的統治帶來新的挑戰。"

    show minion at right
    minister "報告總統，我們的經濟增長率連續多年保持在高位，外國媒體稱之為'台灣奇蹟'。"

    j "經濟發展很重要，但我們更要關注財富分配和社會公平。不能讓發展的果實只被少數人享有。"

    hide minion

    jump chapter8_act5

label chapter8_act5:
    scene bg imgchi18
    with fade
    $ now_venue.location = "陽明山中興賓館"
    "第五幕：最後的日子"
    "1975年，陽明山中興賓館"

    show johndraw at left

    j "我知道自己時日無多，但我仍然牽掛著這個國家的未來。"

    show minion at right
    johnson "父親，您要保重身體。國家還需要您的指導。"

    j "經國，未來的路還很長。記住，國家利益高於一切。但也要明白，只有贏得人民的心，才能真正穩固政權。時代在變，我們也必須與時俱進。"

    j "看著經國，我既感到欣慰，又充滿擔憂。我知道，我的時代即將結束，新的挑戰不斷出現。我只希望，我的經驗教訓能夠成為後人的借鑒，讓這個國家走向更好的未來。"

    hide minion

    "完結。"

    return



