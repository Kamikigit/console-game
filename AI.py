import time, random, unicodedata, os, copy
import b.contains 


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
            game.player.room_id = self.room_id
            game.player.room_map = self.map
            game.player.check_room() #部屋の探索
            game.player.set_destination()
            # プレイヤーの移動決定
            # move = random.choice("WASD")
            move = game.player.next
            if not(move == "W" or move == "A" or move == "S" or move == "D"):
                if (move == "R"):
                    game.show_gamerule()  # ゲームルールを表示
                    print()
                    # os.system("clear")
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
                    print("鍵がない…▼")
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
                print("今のうちに逃げよ！幽霊は５ターン動かない！▼")
                

    def valid_event(self, new_x, new_y):
        if self.map[new_y][new_x] == MONKEY:
            Ghost.show_monkey()
            print()
            print("おもちゃの猿がこちらを見つめている。 SAN値が5ポイント減少した。▼")
            game.player.SAN -= 5
        if self.map[new_y][new_x] == PHANTOM:
            print("見えない何かが横切った。 SAN値が5ポイント減少した。▼")
            print()
            game.player.SAN -= 5
        if self.map[new_y][new_x] == MIRROR:
            print("鏡の向こうの自分がほほ笑んだ… SAN値が5ポイント減少した。▼")
            print()
            game.player.SAN -= 5
        if self.map[new_y][new_x] == CAT:
            Ghost.show_cat()
            if game.ending_count == 100:
              print("女の子の影が猫を追い払ってくれた▼")
            print("……。SAN値が5ポイント減少した…▼")
            
            game.ending_count += 50
            game.player.SAN -= 5
        if self.map[new_y][new_x] == LIGHT:
            Box.show_light()
            print("懐中電灯を手に入れた。 SAN値が20ポイント回復した。▼")
            game.player.SAN += 20
            if game.player.SAN > 101:
                game.player.SAN = 101
        if self.map[new_y][new_x] == DIARY:
            # os.system("clear")
            print("7月12日　晴れ\n親の仕事の関係で引っ越してきた。\nもうすぐ夏休みだし、新しい学校では友達作りたいな　▽　")
            # os.system("clear")
            print("7月13日　雨\n今日は夏休み前のレクリエーションがあった。\nあんまりみんなの輪には入れなかったけど\n2種目目のトランプゲームはとても楽しかった。　▽　")
            # os.system("clear")
            print("7月15日　雨\nクラスの子たちが夏休みの予定を立てていたけど声をかけることができなかった…\n私の家はパパとママも忙しいだろうし今年も1人なのかな…　▽　")
            # os.system("clear")
            print("7月18日　晴れ\n今日は理科のおばあちゃんの先生に連れられて実験室に来た\nたぶん引っ越してきたばかりの私を心配してくれたのかな？\n暇なときはいつでもここに来ていいみたい！\n実験室にはネコも遊びにくるみたいだし日記はここで書くことに決めた　▽　")
            # os.system("clear")
            print("7月19日　曇り\n今日も実験室に遊びに行った。昨日見かけたネコもいたからネコちゃんと遊んだ\n遊んでるときにどこかから視線を感じたけど気のせいだったかな？　▽　")
            # os.system("clear")
            print("7月20日　曇り\n明後日から夏休みが始まるから宿題を配られた　\n今日全部終わらせるって言ってる子もいたけど、私は毎日コツコツやろうかな\n放課後実験室に遊びに行ったけど今日はネコはいなかった\n部屋のはしっこで何かが動いた。この部屋は様子がおかしいかもしれない\nめまいがしたので今日は早めに家に帰ろうと決めた　▽　")
            # os.system("clear")
            print("7月21日　曇り\n今日は終業式があった。みんなは楽しそうにしてた\n夏休みの間ネコちゃんに会えないから、会うために実験室に行った\nネコちゃんはいなかったから待ってみることにした　▽　")
        
            print("夕方になってしまった\n帰ろうかなって思ったらネコちゃんが来てくれた！\n今日は友達もつれてきたみたいだけどずっとかべをカリカリとひっかいていた　▽　")
            # os.system("clear")
            print("カリカリカリカリカリカリカリカリカリカリカリカリカリカリカリカリ\nカリカリカリカリカリカリカリカリカリカリカリカリカリカリカリカリ　▽　")
            # os.system("clear")
            print("ここで日記は終わっている　▽　")
            # os.system("clear")
            print("裏に何か書いてある　▽　")
            # os.system("clear")
            print("「me me curse you」　▽　")
            # os.system("clear")
            game.ending_count += 100
        if self.map[new_y][new_x] == BOX:
            Box.show_box()
            game.player.box_count += 1
            print("Enterで開ける")
            while True:
                item = random.choice(game.events)
                if (game.player.box_count < 5 and item == KEY and (self.room_id == CLASSROOM_3F or 
                                    self.room_id == ARTROOM_3F or self.room_id == MUSICROOM_3F)):
                    continue  # 鍵が三階の部屋に出た場合、選択しなおす
                break
            game.events.remove(item)
            if item == LIGHT:
                Box.show_light()
                print("懐中電灯を手に入れた。 SAN値が20ポイント回復した▼")
                game.player.SAN += 20
                if game.player.SAN > 101:
                    game.player.SAN = 101
            if item == TRAP:
                Box.show_trap()
                print("罠だ！ SAN値が10ポイント減少した▼")
                game.player.SAN -= 10
            if item == MISS:
                Box.show_empty()
                print("空箱だった・・・▼")
            if item == KEY:
                Box.show_key()
                print("鍵を入手した！▼")
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
        
        # os.system("clear")

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
        print()
        # os.system("clear")

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

        print()

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

class Node:
    def __init__(self, parent=None, position=None, depth=0):
        self.position = position
        self.parent = parent
        self.depth = 0

class Player():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.player_name = None
        self.SAN = 100
        self.have_key = False
        self.box_count = 0

        self.room_id = None
        self.room_map = None
        self.doors = []
        self.boxes = []
        self.lights = []
        self.room_visited = []
        self.exit_room_id = None

        self.des_y = None
        self.des_x = None

        self.next = None
        self.hegiht = None
        self.width = None
    def show_status(self):
        print("SAN値：" + str(self.SAN), end=",  ")
        if self.have_key == True:
            print("鍵：○ ")
        else:
            print("鍵：× ")

    def input_name(self):
        while True:
            name = "人工知能"
            if name == "":
                continue
            self.player_name = name[0]
            if unicodedata.east_asian_width(self.player_name) != "W":
                print("その名前はダメだ…（全角で入力）") 
                continue
            else:
                break

        print(name + "というのかい？▼ ")
        
        print("贅沢な名だね。▼ ")
        self.player_name = name[0]
        print("今からお前の名前は" + self.player_name + "だ。いいかい、" + self.player_name + "だよ。\nわかったら返事をするんだ、" + self.player_name + "！▼")
        SHOW_NAME[PLAYER] =  self.player_name
        # os.system("clear")

    
    def check_room(self):
        self.height = len(self.room_map)
        self.width = len(self.room_map[0])

        for y in range(self.height):
            for x in range(self.width):
                space = self.room_map[y][x]
                if 32 <= space <= 49: #扉を見つけた時
                    self.doors.append([self.room_id, y, x, space])

                if space == 12: #灯りを見つけた時
                    self.lights.append([self.room_id, y, x])

                if space == 11: #箱を見つけた時
                    self.boxes.append([self.room_id, y, x])
        # print(self.doors)

    def set_destination(self):
        if self.SAN < 30: # SAN値が30未満のときは灯りを目的地に
            pass #目的地を灯探索へ
        elif self.have_key: # 鍵を取得しているときは出口を目的地に
            pass # 目的地を出口探索へ
        elif self.boxes == []: # 部屋に箱がないときは扉を目的地に
            self.des_y = self.doors[0][1] # ここのとり方も工夫したい
            self.des_x = self.doors[0][2]
            self.bfs(self.y, self.x, self.des_y, self.des_x)
        elif self.lights == []: # 部屋に灯りがないときは箱を目的地に
            self.des_y = self.boxes[0][1]
            self.des_x = self.boxes[0][2]
            self.bfs(self.y ,self.x, self.des_y, self.des_x)
        elif self.SAN <= 70: # SAN値が70以下で灯りを目的地に
            self.des_y = self.lights[0][1]
            self.des_x = self.lights[0][2]
            self.bfs(self.y ,self.x, self.des_y, self.des_x)           
        else:
            self.des_y = self.boxes[0][1]
            self.des_x = self.boxes[0][2]
            self.bfs(self.y ,self.x, self.des_y, self.des_x)

    def bfs(self, sy, sx, gy, gx):
        queue = []
        visited = []
        start_node = Node(None, [sy, sx], 0)
        queue.append(start_node)
        print(sy, sx, gy, gx)
        print("Starting Breadth First Search...")
        while queue:
            current_node = queue.pop(0)
            visited.append(current_node.position)
            y = current_node.position[0]
            x = current_node.position[1]

            if [y, x] == [gy, gx]:
                print("Breadth First Search success!!")
                self.return_path(current_node, sy, sx, gy, gx)
                break

            # 4-c　移動可能な場所の把握
            for j, k in ([1, 0], [-1, 0], [0, 1], [0, -1]):
                new_y, new_x = y+j, x+k
                if new_y < 0 or new_y >= self.height or new_x < 0 or new_x >= self.width:
                    continue
                # 移動不可マスは踏めない
                elif 10 < self.room_map[new_y][new_x] < 23 or self.room_map[new_y][new_x] == 0 or self.room_map[new_y][new_x] == self.room_map[gy][gx]:
                    node = Node(current_node, [new_y, new_x], current_node.depth+1) # I ノード作成
                    # II 訪問済みかどうか
                    if [new_y, new_x]  not in visited:
                        if [new_y, new_x] not in queue:
                            queue.append(node)
                            
    def return_path(self, current_node, sy, sx, gy, gx):
        path = []
        while True:
            current_node = current_node.parent
            path.append(current_node.position)
            if current_node.position == [sy, sx]:
                break
        print("Path to goal:")
        for i in path[:0:-1]:
            print(i, "->", end=" ")
        print(path[0], "->", [gy, gx])
        path = path[::-1] #逆方向にする
        path.append([gy, gx]) #ゴールがないので追加する
        print("Next AI move:", path[0], "->", path[1])

        self.set_command(path[0][0], path[0][1], path[1][0], path[1][1] )

    # 有利度マップの作成
    # def create_aspiration_map(self):


    def set_command(self, sy, sx, gy, gx):
        move_y =  gy - sy #縦方向で考える
        move_x = gx - sx
        if move_y == 1:
            self.next = "S"
        if move_y == -1:
            self.next = "W"
        if move_x == 1:
            self.next = "D"
        if move_x == -1:
            self.next = "A"
        print(self.next)




class Game():
    def __init__(self):
        self.game_finished = GAME_NOT_FINISHED
        self.rooms = []
        self.current_room = None
        self.player = Player()
        self.last_move = EMPTY
        self.ending_count = 0  # エンディング分岐用変数


    def game_title(self):
        print('\033[31m' + "■■■■■■  ■■■■■   ■      ■■■■■■       ")
        print("■    ■      ■   ■        ■         ■")
        print("■    ■      ■   ■        ■        ■ ")
        print("     ■     ■    ■   ■  ■■■■■■    ■  ")
        print("    ■     ■■■   ■■■■     ■      ■■  ")
        print("   ■     ■   ■            ■■   ■   " + '\033[37m')
        print()
        time.sleep(1)

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
        print('\033[31m' +self.player.player_name  + '\033[37m'+ '=プレイヤー, ・=何もないマス')
        print("扉=別の部屋に移動, 上=上の階へ, 下=下の階へ, 出=出口")
        print("机, 絵, ピ, ア, ノ, 靴=移動不可マス")
        print('\033[33m' + "箱" + '\033[37m' + "=ランダムなアイテムを入手, " + '\033[33m' + "灯" + '\033[37m'+ "=SAN値+20, 罠=SAN値-10")
        
        print("~~~ おばけ ~~~")
        print('\033[36m' + "幽" + '\033[37m' + "=上下に動くお化け," + '\033[36m' + "霊" + '\033[37m' + "=左右に動くお化け")
        print("おばけの縦横1マスに近づくとSAN値が10減り,お化けが5ターン動かなくなる")

        print("~~~~~~~~~~ Enterで続く ~~~~~~~~~~~")

    def print_prologue(self):
        # os.system("clear")
        print("7月21日▼")
        # os.system("clear")
        print("先生「皆さんさようなら、夏休み中体に気を付けて過ごしてくださいね」▼")
        # os.system("clear")
        print("自分「よーし、学校終わって夏休みだー！いっぱい遊ぶぞ！！！」▼")
        # os.system("clear")
        print("クラスの人達「コソコソ...10年前だけど、夏休み前に行方不明になっちゃった女の子がいるんだって」\n　　　　　　「こえーなそれ今年は肝試しでもしようぜ！！」▼")
        # os.system("clear")
        print("自分も誘ってもらえないかな～と考えつつ家に帰った▼")
        # os.system("clear")
        print("▼")
        # os.system("clear")
        print("7時間後… 自宅にて▼")
        # os.system("clear")
        print("自分「ごちそうさまでした～」▼")
        # os.system("clear")
        print("母「夏休みの宿題は毎日ちゃんとやるのよ」▼")
        # os.system("clear")
        print("自分「わかってるよ」\n　　「そんなこと言われなくてもやるって」▼")
        # os.system("clear")
        print("自分は母親に愚痴を言いつつ2階に上って自分の部屋に入った▼")
        # os.system("clear")
        print("自分「ってあれ！？」▼")
        # os.system("clear")
        print("カバンに宿題がはいってないことに気が付いた▼")
        # os.system("clear")
        print("自分「明日から1週間学校がしまるから今すぐいかないと」▼")
        # os.system("clear")
        print("自分「お母さん学校行ってくる！」▼")
        # os.system("clear")
        print("階段を駆け下りて母親にそう告げると急いで学校に向かった▼")
        # os.system("clear")
        print("学校に着くころにはあたりは暗くなっていた▼")
        # os.system("clear")
        print("裏口から忍び込んで早く帰ることにした▼")
        # os.system("clear")
        print("宿題を手に取ったところで女性の笑い声が聞こえた\n何かをひっかいた変な音が耳に響きわたる\n自分はその場に倒れてしまった▼")
        # os.system("clear")
        print("・・・・・・・・・・・・・・・")
        # os.system("clear")
        print("目が覚めるとなぜか廊下に立っていた▼")
        # os.system("clear")
        print("あたりは暗いがぼんやりと周りが見えるくらいの不思議な雰囲気が漂っていた▼")
        # os.system("clear")
        print("ぼんやりしていると急に目の前に1人のおばあさんらしき人が現れた▼")
        # os.system("clear")

    def check_san(self):
        if (self.player.SAN <= 0):
            print("SANがなくなった…")
            print("ゲームオーバー！")
            print()
            return True
        return False
            

    def init_game(self):
        for i in range(len(MAPS)):
            self.rooms.append(Room(i+100, copy.deepcopy(MAPS[i])))
        for room in self.rooms:
            room.init_room()
        self.current_room = self.rooms[HALL_3F - 100]
        self.door_x, self.door_y = (self.player.x, self.player.y)
        self.door_id = EMPTY
        self.events = copy.deepcopy(EVENTS)

        self.print_prologue()   #ゲームのプロローグ表示
        self.game_title()   # ゲームタイトルの表示
        print()
        # os.system("clear") 
        self.player.input_name()  # 名前を入力させる

    def save_door(self):
        self.door_x, self.door_y = (self.player.x, self.player.y)  # 扉の座標を保存
        self.door_id = self.current_room.map[self.door_y][self.door_x]  # 扉のidを保存
        self.current_room.map[self.door_y][self.door_x] = PLAYER

    def game_loop(self):
        self.show_gamerule()  # ルールの表示
        print()  # 入力待ち
        while (self.game_finished == GAME_NOT_FINISHED):
            # os.system("clear")
            
            self.player.show_status()  # ステータスの表示
            self.current_room.show_room()  # 部屋情報を表示
            if (self.check_san()):  # プレイヤーのSAN値が0以下だった場合
                break

            change_room = self.current_room.move_player()  # プレイヤーの移動
            time.sleep(1)
            if change_room:
                self.save_door()
                continue
            if (self.door_id != EMPTY):
                self.current_room.map[self.door_y][self.door_x] = self.door_id  # 扉を確保
            self.current_room.move_ghosts()  # 幽霊の移動
            self.current_room.ghost_check_around()  # 幽霊の周りにプレイヤーがいるかどうかを確認
        else:
            # os.system("clear")
            self.player.show_status()  # ステータスの表示
            self.current_room.show_room()  # 部屋情報を表示
            print("自分はふと学校を振り返った")
            if game.ending_count == 0:
              print("宿題を取りに来た時と変わらない、ごく普通の学校がそびえたっていた▼")
              print("NOMAL END")
            if game.ending_count == 50:
              print("実験室の窓からたくさんの目が付いた猫が自分を睨んでいた▼")
              print("BAD END")
            if game.ending_count == 100:
              print("実験室の窓から女の子が手を振っていた▼")
              print("TRUE END")
            if game.ending_count == 150:
              print("実験室の窓から女の子が手を振っていた▼")
              print("またくるね▼")
              print("HAPPY END")
            print("\nGame Clear▼")


    def replay(self):
        while True:
            answer = print("リプレイしますか(y/n)？")
            answer = answer.upper()
            if answer == "Y" or answer == "N":
                return answer
            else:
                print("y, nを入力して下さい")

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
        
    # os.system("clear")
print("ありがとうございました！▼")