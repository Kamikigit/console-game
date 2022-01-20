import time, random, unicodedata, os, copy

GAME_NOT_FINISHED = 0
GAME_FINISHED = 1

ROOF_TOP = 100 # 屋上
HALL_3F = 101 # 廊下３F
HALL_2F = 102 # 廊下２F
HALL_1F = 103 # 廊下１F
CLASSROOM_3F = 104 # 教室３Ｆ
CLASSROOM_2F = 105 # 教室２Ｆ
CLASSROOM_1F = 106 # 教室１Ｆ
MUSICROOM_3F = 107 # 音楽室３F
ARTROOM_3F = 108 # 美術室３F
LABLATOR_2F = 109 #  実験室２F
CLOTHINGROOM_2F = 110 # 被服室２F
FACULTYROOM_1F = 111 # 教員室１F
FRONT_1F = 112 # 玄関１F

EMPTY = 0 # 何もないマス
GOAL = 1 # 「出」のマス
UP = 2 # 「上」のマス
DOWN = 3 # 「下」のマス
DOOR = 4 # 「扉」のマス
DESK = 5 # 「机」のマス
PICTURE = 6 # 「絵」のマス
PIANO_PI = 7 # 「ピ」のマス
PIANO_A = 8 # 「ア」のマス
PIANO_NO = 9 # 「ノ」のマス
SHOES = 10 # 「靴」のマス
BOX = 11 # 「箱」のマス
LIGHT = 12 # 「灯」のマス
YUU = 13 # 「幽」のマス
REI = 14 # 「霊」のマス
MONKEY = 15 # 「猿」のマス
PHANTOM = 16 # 「幻」のマス
MIRROR = 17 # 「鏡」のマス
CAT = 18 # 「猫」のマス
TRAP = 19 # 「罠」のイベント
MISS = 20 # 「空箱」のイベント
KEY = 21 # 「鍵」
DIARY = 22 # 「□」
PLAYER = 99 # プレイヤーのマス

# 上
TO_ROOF_TOP_UP = 26
TO_HALL_3F_UP = 27
TO_HALL_2F_UP = 28
# 下
TO_HALL_3F_DOWN = 29
TO_HALL_2F_DOWN = 30
TO_HALL_1F_DOWN  = 31
# 扉
TO_CLASSROOM_3F = 32 # 教室３Ｆ
TO_CLASSROOM_2F = 33 # 教室２Ｆ
TO_CLASSROOM_1F = 34 # 教室１Ｆ
TO_MUSICROOM_3F = 35 # 音楽室３F
TO_ARTROOM_3F = 36 # 美術室３F
TO_LABLATOR_2F = 37 #  実験室２F
TO_CLOTHINGROOM_2F = 38 # 被服室２F
TO_FACULTYROOM_1F = 39 # 教員室１F
TO_FRONT_1F = 40 # 玄関１F

TO_CLASSROOM_3F_OUT = 41 # 教室３Ｆ
TO_CLASSROOM_2F_OUT = 42 # 教室２Ｆ
TO_CLASSROOM_1F_OUT = 43 # 教室１Ｆ
TO_MUSICROOM_3F_OUT = 44 # 音楽室３F
TO_ARTROOM_3F_OUT = 45 # 美術室３F
TO_LABLATOR_2F_OUT = 46 #  実験室２F
TO_CLOTHINGROOM_2F_OUT = 47 # 被服室２F
TO_FACULTYROOM_1F_OUT = 48 # 教員室１F
TO_FRONT_1F_OUT = 49 # 玄関１F

EVENTS = [LIGHT,LIGHT,LIGHT,LIGHT,TRAP,TRAP,TRAP,MISS,MISS,KEY]  # 箱の中身

PORTAL = {TO_ROOF_TOP_UP : [ROOF_TOP, 4, 4], TO_HALL_3F_UP : [HALL_3F, 1, 9], TO_HALL_2F_UP : [HALL_2F, 1, 9], 
          TO_HALL_3F_DOWN : [HALL_3F, 0, 9], TO_HALL_2F_DOWN : [HALL_2F, 0, 9], TO_HALL_1F_DOWN : [HALL_1F, 0, 9],
          TO_CLASSROOM_3F : [CLASSROOM_3F, 0, 0], TO_CLASSROOM_3F_OUT : [HALL_3F, 1, 0],
          TO_CLASSROOM_2F : [CLASSROOM_2F, 0, 0], TO_CLASSROOM_2F_OUT : [HALL_2F, 1, 0],
          TO_CLASSROOM_1F : [CLASSROOM_1F, 0, 4], TO_CLASSROOM_1F_OUT : [HALL_1F, 0, 0],
          TO_MUSICROOM_3F : [MUSICROOM_3F, 0, 0], TO_MUSICROOM_3F_OUT : [HALL_3F, 1, 4],
          TO_ARTROOM_3F : [ARTROOM_3F, 0, 0], TO_ARTROOM_3F_OUT : [HALL_3F, 1, 7],
          TO_LABLATOR_2F : [LABLATOR_2F, 0 ,0], TO_LABLATOR_2F_OUT : [HALL_2F, 1, 4],
          TO_CLOTHINGROOM_2F : [CLOTHINGROOM_2F, 0, 0], TO_CLOTHINGROOM_2F_OUT : [HALL_2F, 1, 7],
          TO_FACULTYROOM_1F : [FACULTYROOM_1F, 0, 4], TO_FACULTYROOM_1F_OUT : [HALL_1F, 1, 3],
          TO_FRONT_1F : [FRONT_1F, 0, 2], TO_FRONT_1F_OUT : [HALL_1F, 1, 7]}

ROOF_TOP_MAP = [[ 0, 11, 12, 11, 13],
                [ 0,  0,  0,  0,  0],
                [ 0,  0, 14,  0,  0],
                [ 0,  0,  0,  0,  0],
                [ 0,  0,  0,  0, 29]]
HALL_3F_MAP  = [[99,  0,  0,  0,  0, 15,  0,  0,  0, 26],
                [32,  0,  0,  0, 35,  5,  0, 36,  0, 30]]
HALL_2F_MAP  = [[ 0, 12,  0,  0, 16,  0,  0,  0,  0, 27],
                [33,  0,  0,  0, 37,  0,  0, 38,  0, 31]]
HALL_1F_MAP  = [[34,  12,  0,  0,  0,  0,  0,  0,  0, 28],
                [ 0,  0,  0, 39,  0,  0, 12, 40,  0,  0]]
CLASSROOM_3F_MAP = [[41,  0,  0,  0,  0],
                    [ 0,  5,  0,  0,  0],
                    [ 0, 22,  0,  0,  0],
                    [ 0,  0,  5,  0,  0],
                    [13, 11,  0,  0,  0]]
CLASSROOM_2F_MAP = [[42,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0],
                    [ 0, 13,  0,  5,  0],
                    [ 0,  0,  5, 11,  0],
                    [ 0,  0,  0,  0,  0]]
CLASSROOM_1F_MAP = [[ 0,  0,  0,  0, 43],
                    [ 0,  0,  0,  0,  0],
                    [11,  5, 13,  5,  0],
                    [ 0,  0,  0,  0,  0],
                    [ 0,  0,  5,  0,  0]]
FRONT_1F_MAP = [[  0,  0, 49,  0,  0],
                [ 14,  0,  0,  0, 14],
                [ 10,  0,  0,  0, 10],
                [ 10,  0,  0,  0, 10],
                [ 10,  0,  1,  0, 10]]
FACULTYROOM_1F_MAP = [[ 14,  0,  0,  0, 48],
                      [  0,  0,  0,  0,  0],
                      [ 11,  5,  0,  5,  0],
                      [  0,  0, 13,  0,  0],
                      [  0,  0,  0,  0, 12]]
CLOTHINGROOM_2F_MAP = [[ 47,  0,  0,  0, 12],
                       [  0,  5,  0,  5,  0],
                       [  0,  0, 13,  0,  0],
                       [ 17,  5,  0,  5,  0],
                       [  0, 11,  0,  0,  0]]
LABLATOR_2F_MAP = [[ 46,  0,  0,  0,  0],
                   [  0,  5,  5,  5,  0],
                   [  0, 14,  0,  0, 11],
                   [  0,  5,  5,  5,  0],
                   [ 12,  0, 18,  0,  0]]
ARTROOM_3F_MAP = [[ 45,  0,  0,  0, 14],
              [  0,  0,  6,  0,  0],
              [  0,  0,  6,  0, 12],
              [ 11,  0,  6,  0,  0],
              [  0,  0,  0,  0,  14]]
MUSICROOM_3F_MAP = [[ 44,  0,  0,  0, 11],
                [  0,  0,  0,  0,  0],
                [  0,  7,  0, 13,  0],
                [  0,  8,  9,  0,  0],
                [  0,  0, 12,  0,  0]]

SHOW_NAME = { EMPTY: "・", GOAL : "出", UP : "上", DOWN : "下", DOOR : "扉", DESK : "机", PICTURE : "絵", PIANO_PI : "ピ", PIANO_A : "ア", PIANO_NO : "ノ",
              SHOES : "靴", BOX : "箱", LIGHT : "灯", YUU : "幽", REI : "霊", MONKEY : "・", PHANTOM : "・", MIRROR : "鏡", CAT : "猫", DIARY : "□□",
              TO_CLASSROOM_3F: "扉", TO_CLASSROOM_2F: "扉", TO_CLASSROOM_1F: "扉", TO_MUSICROOM_3F: "扉", TO_ARTROOM_3F : "扉", 
              TO_LABLATOR_2F : "扉", TO_CLOTHINGROOM_2F : "扉", TO_FACULTYROOM_1F : "扉", TO_FRONT_1F : "扉",
              TO_CLASSROOM_3F_OUT: "扉", TO_CLASSROOM_2F_OUT: "扉", TO_CLASSROOM_1F_OUT: "扉", TO_MUSICROOM_3F_OUT: "扉", TO_ARTROOM_3F_OUT : "扉", 
              TO_LABLATOR_2F_OUT : "扉", TO_CLOTHINGROOM_2F_OUT : "扉", TO_FACULTYROOM_1F_OUT : "扉", TO_FRONT_1F_OUT : "扉", 
              TO_ROOF_TOP_UP : "上", TO_HALL_3F_UP : "上", TO_HALL_2F_UP : "上",
              TO_HALL_3F_DOWN : "下", TO_HALL_2F_DOWN : "下", TO_HALL_1F_DOWN : "下"}

MOVE_POINT = {"S" : [1, 0], "W": [-1, 0], "D" :  [0, 1], "A": [0, -1]}

MAPS = [ROOF_TOP_MAP, HALL_3F_MAP, HALL_2F_MAP, HALL_1F_MAP, CLASSROOM_3F_MAP, CLASSROOM_2F_MAP, CLASSROOM_1F_MAP, MUSICROOM_3F_MAP,
        ARTROOM_3F_MAP, LABLATOR_2F_MAP, CLOTHINGROOM_2F_MAP, FACULTYROOM_1F_MAP, FRONT_1F_MAP]

SHOW_ROOM = { ROOF_TOP : "屋上", HALL_3F : "廊下３F", HALL_2F : "廊下２F", HALL_1F : "廊下１F", CLASSROOM_3F : "教室３Ｆ",
              CLASSROOM_2F : "教室２Ｆ", CLASSROOM_1F : "教室１Ｆ", MUSICROOM_3F : "音楽室３F", ARTROOM_3F :  "美術室３F", 
              LABLATOR_2F : "実験室２F", CLOTHINGROOM_2F : "被服室２F", FACULTYROOM_1F : "教員室１F", FRONT_1F :"玄関１F"}


class Room():
    def __init__(self, room_id, room_map):
        self.room_id = room_id
        self.id = room_id - 100
        self.map = room_map
        self.height = len(room_map)
        self.width  = len(room_map[0])
        self.ghosts = []

    def init_room(self):
        for y in range(self.height):
            for x in range(self.width):
                if (self.map[y][x] == YUU or self.map[y][x] == REI):  # 幽霊であったら初期化
                    self.ghosts.append(Ghost(self.map[y][x], x, y))

    def show_room(self):
        print("[ " + SHOW_ROOM[self.room_id] + " ]")
        print("--------------------------")
        for i in range(self.height):
            for j in range(self.width):
                piece = self.map[i][j]
                if piece == 11 or piece == 12 or (piece >= 19 and piece <= 21):  # 箱と灯りは黄色
                    print('\033[33m' + SHOW_NAME[self.map[i][j]] + '\033[0m', end="")
                elif piece == 13 or piece == 14:  # 幽霊は水色
                    print('\033[36m' + SHOW_NAME[self.map[i][j]] + '\033[0m', end="")
                elif piece == 99:  # プレイヤーは赤
                    print('\033[31m' + SHOW_NAME[self.map[i][j]] + '\033[0m', end="")
                elif piece == 0 or (piece >= 15 and piece <= 16): # 点を灰色
                    print('\033[38;2;125;125;125m' + SHOW_NAME[piece] + '\033[0m', end="")
                else:
                    print(SHOW_NAME[piece], end="")
            print("")
        print("--------------------------")

    def move_player(self):
        while True:
            move = input("移動方向を入力して下さい（w,a,s,d）（rでルール表示）：")
            move = move.upper()
            if not(move == "W" or move == "A" or move == "S" or move == "D"):
                if (move == "R"):
                    game.player.show_gamerule()  # ゲームルールを表示
                    input()
                    clearConsole()
                    game.player.show_status()  # ステータスの表示
                    self.show_room()  # 部屋情報を表示
                else: print("w, a, s, dを入力して下さい")
                continue
            move = MOVE_POINT[move]
            new_y, new_x = game.player.y + move[0], game.player.x + move[1]
            # print(starty, startx, new_y, new_x)
            # 壁判定
            if new_y < 0 or new_y >= self.height or new_x < 0 or new_x >= self.width:
                print("そこには移動できません")
                continue
            # 障害物判定
            if DESK <= self.map[new_y][new_x] <= SHOES:
                print("そこには移動できません")
                continue
            # 幽霊判定
            if YUU <= self.map[new_y][new_x] <= REI:
                print("そこには移動できません")
                continue
            # 出口判定
            if (self.map[new_y][new_x] == GOAL):
                if (game.player.have_key):
                    game.game_finished = GAME_FINISHED
                else:
                    input("鍵がない…▼")
            # 元のマズに戻す
            if ((BOX <= game.last_move <= LIGHT) or (MONKEY <= game.last_move <= DIARY)):
                self.map[game.player.y][game.player.x] = EMPTY
            else:
                self.map[game.player.y][game.player.x] = game.last_move    
            # 部屋移動
            if (26 <= self.map[new_y][new_x] <= 49):
                # 上下の確保
                if (TO_ROOF_TOP_UP <= self.map[new_y][new_x] <= TO_HALL_2F_DOWN):
                    if (TO_ROOF_TOP_UP <= self.map[new_y][new_x] <= TO_HALL_2F_UP):
                        game.last_move = self.map[new_y][new_x] + 3  # 上から下へ
                    elif (TO_HALL_3F_DOWN <= self.map[new_y][new_x] <= TO_HALL_1F_DOWN):
                        game.last_move = self.map[new_y][new_x] - 3  # 下から上へ

                game.current_room = game.rooms[PORTAL[self.map[new_y][new_x]][0] - 100]
                game.player.x = PORTAL[self.map[new_y][new_x]][2]
                game.player.y = PORTAL[self.map[new_y][new_x]][1]
                return True
            self.valid_event(new_x, new_y)
            game.player.y = new_y
            game.player.x = new_x
            game.last_move = self.map[new_y][new_x]  # 元のマズを確保
            self.map[new_y][new_x] = 99
            game.player.SAN -= 1
            # self.show_room()
            return False

    def move_ghosts(self):
        for ghost in self.ghosts:
            if (ghost.hit):  # プレイヤーに当ったことある場合
                ghost.count += 1  # カウントを増やす
                if (ghost.count >= 5):  # カウントが５以上になった場合
                    ghost.count = 0  # カウントをリセット
                    ghost.hit = False  # 当たり判定を解除
                    continue
            else:
                # 壁にぶつかったら反転
                if (0 > ghost.x+ghost.vx or ghost.x+ghost.vx > self.width-1):
                    ghost.vx *= -1
                if (0 > ghost.y+ghost.vy or ghost.y+ghost.vy > self.height-1):
                    ghost.vy *= -1
                # 移動できないマスとぶつかった場合も反転
                if (UP <= self.map[ghost.y+ghost.vy][ghost.x+ghost.vx] <= BOX or
                    TO_ROOF_TOP_UP <= self.map[ghost.y+ghost.vy][ghost.x+ghost.vx] <= TO_FRONT_1F_OUT):
                    ghost.vx *= -1
                    ghost.vy *= -1
                # 幽の移動先が霊だった場合、幽が反転
                if (ghost.type == YUU):
                    # for文でghostsを読み取る
                    for gh in self.ghosts:
                        # 確認している幽霊自体の場合はcontinue
                        if (gh == ghost):
                            continue
                        if (gh.type == REI and ghost.y+ghost.vy == gh.y+gh.vy and ghost.x+ghost.vx == gh.x+gh.vx):
                            ghost.vx *= -1
                            ghost.vy *= -1
                # 移動先がプレイヤーである場合、当たり判定をTrueにして、移動をやめる（ダメージは別関数で処理）
                if (self.map[ghost.y+ghost.vy][ghost.x+ghost.vx] == PLAYER):
                    ghost.hit = True
                    continue

                self.map[ghost.y][ghost.x] = EMPTY  # 今いるマスを空にする
                # 幽霊を移動する
                ghost.x += ghost.vx
                ghost.y += ghost.vy
        for ghost in self.ghosts:  # 移動後のマスの表示をまとめて変える
                                   # （上のfor文でやると表示が上書きされる可能性がある）
            self.map[ghost.y][ghost.x] = ghost.type

    def ghost_check_around(self):
        for ghost in self.ghosts:
            # 幽霊の上下左右にプレイヤーがいるかどうかを確認
            # いた場合は当たり判定をTrueにする
            if (ghost.x + 1 < self.width):
                if (self.map[ghost.y][ghost.x+1] == PLAYER and ghost.hit != True):
                    ghost.hit = True
            if (ghost.x - 1 >= 0):
                if (self.map[ghost.y][ghost.x-1] == PLAYER and ghost.hit != True):
                    ghost.hit = True
            if (ghost.y + 1 < self.height):
                if (self.map[ghost.y+1][ghost.x] == PLAYER and ghost.hit != True):
                    ghost.hit = True
            if (ghost.y - 1 >= 0):
                if (self.map[ghost.y-1][ghost.x] == PLAYER and ghost.hit != True):
                    ghost.hit = True
            
            # 当たり判定を変えたターンにはプレイヤーのSAN値を削る
            if (ghost.hit and ghost.count==0):
                game.player.SAN -= 10
                print("幽霊に当たった…SAN値が10ポイント減少した…")
                input("今のうちに逃げよ！幽霊は５ターン動かない！▼")
                

    def valid_event(self, new_x, new_y):
        if self.map[new_y][new_x] == MONKEY:
            Ghost.show_monkey()
            input()
            input("おもちゃの猿がこちらを見つめている。 SAN値が5ポイント減少した。▼")
            game.player.SAN -= 5
        if self.map[new_y][new_x] == PHANTOM:
            input("見えない何かが横切った。 SAN値が5ポイント減少した。▼")
            input()
            game.player.SAN -= 5
        if self.map[new_y][new_x] == MIRROR:
            input("鏡の向こうの自分がほほ笑んだ… SAN値が5ポイント減少した。▼")
            input()
            game.player.SAN -= 5
        if self.map[new_y][new_x] == CAT:
            Ghost.show_cat()
            if game.ending_count == 100:
              input("女の子の影が猫を追い払ってくれた▼")
            input("……。SAN値が5ポイント減少した…▼")
            
            game.ending_count += 50
            game.player.SAN -= 5
        if self.map[new_y][new_x] == LIGHT:
            Box.show_light()
            input("懐中電灯を手に入れた。 SAN値が20ポイント回復した。▼")
            game.player.SAN += 20
            if game.player.SAN > 101:
                game.player.SAN = 101
        if self.map[new_y][new_x] == DIARY:
            clearConsole()
            input("7月12日　晴れ\n親の仕事の関係で引っ越してきた。\nもうすぐ夏休みだし、新しい学校では友達作りたいな　▽　")
            clearConsole()
            input("7月13日　雨\n今日は夏休み前のレクリエーションがあった。\nあんまりみんなの輪には入れなかったけど\n2種目目のトランプゲームはとても楽しかった。　▽　")
            clearConsole()
            input("7月15日　雨\nクラスの子たちが夏休みの予定を立てていたけど声をかけることができなかった…\n私の家はパパとママも忙しいだろうし今年も1人なのかな…　▽　")
            clearConsole()
            input("7月18日　晴れ\n今日は理科のおばあちゃんの先生に連れられて実験室に来た\nたぶん引っ越してきたばかりの私を心配してくれたのかな？\n暇なときはいつでもここに来ていいみたい！\n実験室にはネコも遊びにくるみたいだし日記はここで書くことに決めた　▽　")
            clearConsole()
            input("7月19日　曇り\n今日も実験室に遊びに行った。昨日見かけたネコもいたからネコちゃんと遊んだ\n遊んでるときにどこかから視線を感じたけど気のせいだったかな？　▽　")
            clearConsole()
            input("7月20日　曇り\n明後日から夏休みが始まるから宿題を配られた　\n今日全部終わらせるって言ってる子もいたけど、私は毎日コツコツやろうかな\n放課後実験室に遊びに行ったけど今日はネコはいなかった\n部屋のはしっこで何かが動いた。この部屋は様子がおかしいかもしれない\nめまいがしたので今日は早めに家に帰ろうと決めた　▽　")
            clearConsole()
            input("7月21日　曇り\n今日は終業式があった。みんなは楽しそうにしてた\n夏休みの間ネコちゃんに会えないから、会うために実験室に行った\nネコちゃんはいなかったから待ってみることにした　▽　")
        
            input("夕方になってしまった\n帰ろうかなって思ったらネコちゃんが来てくれた！\n今日は友達もつれてきたみたいだけどずっとかべをカリカリとひっかいていた　▽　")
            clearConsole()
            input("カリカリカリカリカリカリカリカリカリカリカリカリカリカリカリカリ\nカリカリカリカリカリカリカリカリカリカリカリカリカリカリカリカリ　▽　")
            clearConsole()
            input("ここで日記は終わっている　▽　")
            clearConsole()
            input("裏に何か書いてある　▽　")
            clearConsole()
            input("「me me curse you」　▽　")
            clearConsole()
            game.ending_count += 100
        if self.map[new_y][new_x] == BOX:
            Box.show_box()
            game.player.box_count += 1
            input("Enterで開ける")
            while True:
                item = random.choice(game.events)
                if (game.player.box_count < 5 and item == KEY and (self.room_id == CLASSROOM_3F or 
                                    self.room_id == ARTROOM_3F or self.room_id == MUSICROOM_3F)):
                    continue  # 鍵が三階の部屋に出た場合、選択しなおす
                break
            game.events.remove(item)
            if item == LIGHT:
                Box.show_light()
                input("懐中電灯を手に入れた。 SAN値が20ポイント回復した▼")
                game.player.SAN += 20
                if game.player.SAN > 101:
                    game.player.SAN = 101
            if item == TRAP:
                Box.show_trap()
                input("罠だ！ SAN値が10ポイント減少した▼")
                game.player.SAN -= 10
            if item == MISS:
                Box.show_empty()
                input("空箱だった・・・▼")
            if item == KEY:
                Box.show_key()
                input("鍵を入手した！▼")
                game.player.have_key = True


class Box:
    def show_box():
        print("　 ＿＿＿＿＿")
        print("　/￣/三/￣/⌒i")
        print("　L＿LO_L＿L／|")
        print("　{二二二二}／|")
        print("　{二二二二}／")

    def show_trap():
        print("　　＿＿＿＿_")
        print("　∠_∠∠_／ ＼")
        print("　ＶＶＶＶ＼　｜")
        print("　 >(･ヽノ･)＼/")
        print("　∧ / ⌒ ⌒ ∧ ／|")
        print("　{｜｜ |  }／|")
        print("　{｜｜ |二}／")
        print("　 ﾉ ﾉ　|")
        print("　(＿＿ノ")

    def show_empty():
        print("　　＿＿＿＿_")
        print("　∠__∠∠__／  ＼")
        print("　 \      ＼  ｜")
        print("　  >       ＼/")
        print("　 / ーーー/／|")
        print("　{二二二二}／|")
        print("　{二二二二}／")

    def show_key():
        print("　　　　　（○）")
        print("　　　ｐ──‐{ﾆ}──‐ｑ")
        print("　　　l┌───lﾆl───┐|")
        print("　　　||＿_|ﾆ|＿_|│")
        print("　　　＼＿_厂{_＿／")
        print(".　　　　  |⌒|")
        print("　 　 　 　│.|")
        print("　　　 　　| |")
        print("　　 　　　| |")
        print("　 　　　　| |ｰ─┐")
        print("　 　　　　| |Σ二、")
        print("　 　　　　| |r─‐┘")
        print("　　　　　 | |ｰｖ‐┐")
        print("　　　　　 l_,｢￣")

    def show_light():
        print("　　　　　　　　 ＿◯")
        print("　　　 ＼　　／⌒ ＼/＼＿＿＿＿＿＿＿＿＿＿")
        print(".　　ピ　>　/　 　 \　 ∨ ∧ ┴┴┘　 　 　 　｀,")
        print(".　　カ　> ｛　　　 }◯ ｝　　　　　　　　　  )")
        print("　　 ｜  >  \　 　 /　 ////＿＿＿＿＿＿＿＿ノ")
        print("　　　 ／　　＼＿∠/／")
        print("　　　　　　　　 ￣◯´")

class Ghost:
    def __init__(self, type, x, y):
        self.type = type  # 幽か霊か
        self.change_SAN = 10  # プレイヤーに与えるダメージ
        self.hit = False  # 当たり判定
        self.count = 0    # 当たりカウント

        self.x = x  # x座標
        self.y = y  # y座標
        
        if (type == YUU):
            self.vx, self.vy = (0, 1)  # 幽は横移動
        else:
            self.vx, self.vy = (-1, 0)  # 霊は縦移動


    def show_cat():
        
        clearConsole()

        print("ねこだ！！SAN値が…")
        print("        ,-､　　　　　　　　　　　 　,.-､")
        print("      ./:::::＼　　　　　　　　　 ／::::::ヽ")
        print("      /::::::::::::;ゝ--──-- ､._/:::::::::::|")
        print("　　　 /,.-‐---´ 　　　　　　　　 ＼:::::::::|")
        print("　　／　 　　　　　　　　　　　　　　ヽ､::::|")
        print("　/　　　　　　　　　　　　　　　　　　　ヽ|")
        print("　l　　　　　　　　　　　　 　 　 　 　 　 l")
        print(". |　　　 〇　　　　　　　　　　　　　　　　|")
        print("　l　　, , ,　　　　　　　　　　　〇　　　　l ") 
        print("　` ､　　　　　　(__人__丿　　　　､､､ 　 /　　　")
        print("　　　`ｰ ､__　　　　　　　 　　 　　　 ／")
        print("　　　　　　　 `---ｰ‐‐──‐‐‐┬-----------´")
        input()
        clearConsole()

        print("        ,-､　　　　　　　　　　　   　,.-､")
        print("      ./:::::＼　　　　　　　　　 ／::::::ヽ")
        print("      /::::::::::::;ゝ--──-- ､._/:::::::::::|")
        print("　　　 /,.-‐---´ 　　　　　　　　 ＼::::::::|")
        print("　　／　 　　　＜" + '\033[31m' + "〇" + '\033[37m' + "＞　　　　　　　　ヽ､::::|")
        print("　/　　＜" + '\033[31m' + "〇" + '\033[37m' + "＞    　　    ＜" + '\033[31m' + "〇" + '\033[37m' + "＞　　　　  ヽ|")
        print("　l　　　　　＜" + '\033[31m' + "〇" + '\033[37m' + "＞          　　 ＜" + '\033[31m' + "〇" + '\033[37m' + "＞　 l")
        print(". |　　　   　　　 　＜" + '\033[31m' + "〇" + '\033[37m' + "＞　        　　　|")
        print("　l　　  ＜" + '\033[31m' + "〇" + '\033[37m' + "＞   　　　　　　　＜" + '\033[31m' + "〇" + '\033[37m' + "＞　　l ") 
        print("　` ､　　　　　　　＜" + '\033[31m' + "〇" + '\033[37m' + "＞　　　　    　 /　　　　　　me me corse you...")
        print("　　　`ｰ ､__　　　　　　　 　　＜" + '\033[31m' + "〇" + '\033[37m' + "＞  ／")
        print("　　　　　　　 `---ｰ‐‐──‐‐‐┬-----------´")

        input()

    def show_monkey():
        print("　　　　 ／￣＼")
        print("　　　_ /へ―へ ヽ_")
        print("　　 ((f(◎ ＿◎ )|))")
        print("　　 ヽ| 〉‥ 〈 |ノ")
        print("　　　 ((三三三))")
        print("　　 ／)ヽ＿＿ノ(＼")
        print("　 ／ ｜　 ∩∩　  ｜ ＼")
        print("　(　―- /8||||8ヽ―　)")
        print("　 ＼＿_L8||||8_|＿／")
        print("　　　｜ー∪ ∪ ー｜")
        print("　　／￣￣＼／￣￣＼")
        print("　 ｜　｜　　　｜　｜")
        print("　　＼＿＼￣￣／＿／")
        print("　　 (oooo)　(oooo)")
        print("　　　￣￣　　￣￣")

class Player():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.player_name = None
        self.SAN = 100
        self.have_key = False
        self.box_count = 0

    def show_gamerule(self):
        print("~~~~~~~~~~ ゲームルールの表示 ~~~~~~~~~~")
        print("ターン制, プレイヤーが行動動くとお化けも動く")
        print("脱出には鍵が必要, 鍵は箱の中に入っている")

        print("~~~ プレイヤーのステータス ~~~")
        print("プレイヤーにはSAN値という数値がある")
        print("SAN値の最大値,初期値は100")
        print("1マス移動するごとにSAN値は1減少する")
        print("SAN値が0になるとゲームオーバー")   
        
        print("~~~ マス ~~~")
        print('\033[31m' +self.player_name  + '\033[37m'+ '=プレイヤー, ・=何もないマス')
        print("扉=別の部屋に移動, 上=上の階へ, 下=下の階へ, 出=出口")
        print("机, 絵, ピ, ア, ノ, 靴=移動不可マス")
        print('\033[33m' + "箱" + '\033[37m' + "=ランダムなアイテムを入手, " + '\033[33m' + "灯" + '\033[37m'+ "=SAN値+20, 罠=SAN値-10")
        
        print("~~~ おばけ ~~~")
        print('\033[36m' + "幽" + '\033[37m' + "=上下に動くお化け," + '\033[36m' + "霊" + '\033[37m' + "=左右に動くお化け")
        print("おばけの縦横1マスに近づくとSAN値が10減り,お化けが5ターン動かなくなる")

        print("~~~~~~~~~~ Enterで続く ~~~~~~~~~~~")

    def show_status(self):
        print("SAN値：" + str(self.SAN), end=",  ")
        if self.have_key == True:
            print("鍵：○ ")
        else:
            print("鍵：× ")

    def input_name(self):
        while True:
            name = input("おばあさんが名前を聞いてきた（名前を入力して下さい）：")
            if name == "":
                continue
            self.player_name = name[0]
            if unicodedata.east_asian_width(self.player_name) != "W":
                print("その名前はダメだ…（全角で入力）") 
                continue
            else:
                break

        input(name + "というのかい？▼ ")
        
        input("贅沢な名だね。▼ ")
        self.player_name = name[0]
        input("今からお前の名前は" + self.player_name + "だ。いいかい、" + self.player_name + "だよ。\nわかったら返事をするんだ、" + self.player_name + "！▼")
        SHOW_NAME[PLAYER] =  self.player_name
        clearConsole()

    def game_title(self):
        print('\033[31m' + "■■■■■■  ■■■■■   ■      ■■■■■■       ")
        print("■    ■      ■   ■        ■         ■")
        print("■    ■      ■   ■        ■        ■ ")
        print("     ■     ■    ■   ■  ■■■■■■    ■  ")
        print("    ■     ■■■   ■■■■     ■      ■■  ")
        print("   ■     ■   ■            ■■   ■   " + '\033[37m')
        print()
        print("Enterを押してゲーム開始")

    def print_prologue(self):
        clearConsole()
        input("7月21日▼")
        clearConsole()
        input("先生「皆さんさようなら、夏休み中体に気を付けて過ごしてくださいね」▼")
        clearConsole()
        input("自分「よーし、学校終わって夏休みだー！いっぱい遊ぶぞ！！！」▼")
        clearConsole()
        input("クラスの人達「コソコソ...10年前だけど、夏休み前に行方不明になっちゃった女の子がいるんだって」\n　　　　　　「こえーなそれ今年は肝試しでもしようぜ！！」▼")
        clearConsole()
        input("自分も誘ってもらえないかな～と考えつつ家に帰った▼")
        clearConsole()
        input("▼")
        clearConsole()
        input("7時間後… 自宅にて▼")
        clearConsole()
        input("自分「ごちそうさまでした～」▼")
        clearConsole()
        input("母「夏休みの宿題は毎日ちゃんとやるのよ」▼")
        clearConsole()
        input("自分「わかってるよ」\n　　「そんなこと言われなくてもやるって」▼")
        clearConsole()
        input("自分は母親に愚痴を言いつつ2階に上って自分の部屋に入った▼")
        clearConsole()
        input("自分「ってあれ！？」▼")
        clearConsole()
        input("カバンに宿題がはいってないことに気が付いた▼")
        clearConsole()
        input("自分「明日から1週間学校がしまるから今すぐいかないと」▼")
        clearConsole()
        input("自分「お母さん学校行ってくる！」▼")
        clearConsole()
        input("階段を駆け下りて母親にそう告げると急いで学校に向かった▼")
        clearConsole()
        input("学校に着くころにはあたりは暗くなっていた▼")
        clearConsole()
        input("裏口から忍び込んで早く帰ることにした▼")
        clearConsole()
        input("宿題を手に取ったところで女性の笑い声が聞こえた\n何かをひっかいた変な音が耳に響きわたる\n自分はその場に倒れてしまった▼")
        clearConsole()
        input("・・・・・・・・・・・・・・・")
        clearConsole()
        input("目が覚めるとなぜか廊下に立っていた▼")
        clearConsole()
        input("あたりは暗いがぼんやりと周りが見えるくらいの不思議な雰囲気が漂っていた▼")
        clearConsole()
        input("ぼんやりしていると急に目の前に1人のおばあさんらしき人が現れた▼")
        clearConsole()

    def check_san(self):
        if (self.SAN <= 0):
            print("SANがなくなった…")
            print("ゲームオーバー！")
            input()
            return True
        return False
            

class Game():
    def __init__(self):
        self.game_finished = GAME_NOT_FINISHED
        self.rooms = []
        self.current_room = None
        self.player = Player()
        self.last_move = EMPTY
        self.ending_count = 0  # エンディング分岐用変数

    def init_game(self):
        for i in range(len(MAPS)):
            self.rooms.append(Room(i+100, copy.deepcopy(MAPS[i])))
        for room in self.rooms:
            room.init_room()
        self.current_room = self.rooms[HALL_3F - 100]
        self.door_x, self.door_y = (self.player.x, self.player.y)
        self.door_id = EMPTY
        self.events = copy.deepcopy(EVENTS)

        self.player.print_prologue()   #ゲームのプロローグ表示
        self.player.game_title()   # ゲームタイトルの表示
        input()
        clearConsole() 
        self.player.input_name()  # 名前を入力させる

    def save_door(self):
        self.door_x, self.door_y = (self.player.x, self.player.y)  # 扉の座標を保存
        self.door_id = self.current_room.map[self.door_y][self.door_x]  # 扉のidを保存
        self.current_room.map[self.door_y][self.door_x] = PLAYER

    def game_loop(self):
        self.player.show_gamerule()  # ルールの表示
        input()  # 入力待ち
        while (self.game_finished == GAME_NOT_FINISHED):
            clearConsole()
            
            self.player.show_status()  # ステータスの表示
            self.current_room.show_room()  # 部屋情報を表示
            if (self.player.check_san()):  # プレイヤーのSAN値が0以下だった場合
                break

            change_room = self.current_room.move_player()  # プレイヤーの移動
            if change_room:
                self.save_door()
                continue
            if (self.door_id != EMPTY):
                self.current_room.map[self.door_y][self.door_x] = self.door_id  # 扉を確保
            self.current_room.move_ghosts()  # 幽霊の移動
            self.current_room.ghost_check_around()  # 幽霊の周りにプレイヤーがいるかどうかを確認
        else:
            clearConsole()
            self.player.show_status()  # ステータスの表示
            self.current_room.show_room()  # 部屋情報を表示
            print("自分はふと学校を振り返った")
            if game.ending_count == 0:
              input("宿題を取りに来た時と変わらない、ごく普通の学校がそびえたっていた▼")
              input("NOMAL END")
            if game.ending_count == 50:
              input("実験室の窓からたくさんの目が付いた猫が自分を睨んでいた▼")
              input("BAD END")
            if game.ending_count == 100:
              input("実験室の窓から女の子が手を振っていた▼")
              input("TRUE END")
            if game.ending_count == 150:
              input("実験室の窓から女の子が手を振っていた▼")
              input("またくるね▼")
              input("HAPPY END")
            input("\nGame Clear▼")


    def replay(self):
        while True:
            answer = input("リプレイしますか(y/n)？")
            answer = answer.upper()
            if answer == "Y" or answer == "N":
                return answer
            else:
                print("y, nを入力して下さい")

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

while True:
    game = Game()
    game.init_game()  # ゲームの初期化

    start_time = time.time()   # スタートタイムを記録
    game.game_loop()  # メインループ

    play_time = time.time() - start_time # プレイ時間を計算
    min = int(play_time / 60)  # 分
    sec = int(play_time % 60)  # 秒
    print(f"プレイ時間：{min}分{sec}秒\n")  # プレイ時間をprint

    if game.replay() == "N":  # リプレイ確認
        break
        
    clearConsole()
input("ありがとうございました！▼")