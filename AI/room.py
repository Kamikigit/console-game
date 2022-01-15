import random
from contains import *
from ghost import Ghost
from box import Box
import global_value

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
            global_value.game.player.room_id = self.room_id
            global_value.game.player.map = self.map
            global_value.game.player.check_room() #部屋の探索
            global_value.game.player.set_destination(self.ghosts)
            # プレイヤーの移動決定
            # move = random.choice("WASD")
            move = global_value.game.player.next
            if not(move == "W" or move == "A" or move == "S" or move == "D"):
                if (move == "R"):
                    global_value.game.show_gamerule()  # ゲームルールを表示
                    print()
                    # os.system("clear")
                    global_value.game.player.show_status()  # ステータスの表示
                    self.show_room()  # 部屋情報を表示
                else: print("w, a, s, dを入力して下さい")
                continue
            move = MOVE_POINT[move]
            new_y, new_x = global_value.game.player.y + move[0], global_value.game.player.x + move[1]
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
                if (global_value.game.player.have_key):
                    global_value.game.game_finished = GAME_FINISHED
                else:
                    print("鍵がない…▼")
            # 元のマズに戻す
            if ((BOX <= global_value.game.last_move <= LIGHT) or (MONKEY <= global_value.game.last_move <= DIARY)):
                self.map[global_value.game.player.y][global_value.game.player.x] = EMPTY
            else:
                self.map[global_value.game.player.y][global_value.game.player.x] = global_value.game.last_move    
            # 部屋移動
            if (26 <= self.map[new_y][new_x] <= 49):
                # 上下の確保
                if (TO_ROOF_TOP_UP <= self.map[new_y][new_x] <= TO_HALL_2F_DOWN):
                    if (TO_ROOF_TOP_UP <= self.map[new_y][new_x] <= TO_HALL_2F_UP):
                        global_value.game.last_move = self.map[new_y][new_x] + 3  # 上から下へ
                    elif (TO_HALL_3F_DOWN <= self.map[new_y][new_x] <= TO_HALL_1F_DOWN):
                        global_value.game.last_move = self.map[new_y][new_x] - 3  # 下から上へ

                global_value.game.current_room = global_value.game.rooms[PORTAL[self.map[new_y][new_x]][0] - 100]
                global_value.game.player.x = PORTAL[self.map[new_y][new_x]][2]
                global_value.game.player.y = PORTAL[self.map[new_y][new_x]][1]
                return True
            self.valid_event(new_x, new_y)
            global_value.game.player.y = new_y
            global_value.game.player.x = new_x
            global_value.game.last_move = self.map[new_y][new_x]  # 元のマズを確保
            self.map[new_y][new_x] = 99
            global_value.game.player.SAN -= 1
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
                global_value.game.player.SAN -= 10
                print("幽霊に当たった…SAN値が10ポイント減少した…")
                print("今のうちに逃げよ！幽霊は５ターン動かない！▼")
                

    def valid_event(self, new_x, new_y):
        if self.map[new_y][new_x] == MONKEY:
            Ghost.show_monkey()
            print()
            print("おもちゃの猿がこちらを見つめている。 SAN値が5ポイント減少した。▼")
            global_value.game.player.SAN -= 5
        if self.map[new_y][new_x] == PHANTOM:
            print("見えない何かが横切った。 SAN値が5ポイント減少した。▼")
            print()
            global_value.game.player.SAN -= 5
        if self.map[new_y][new_x] == MIRROR:
            print("鏡の向こうの自分がほほ笑んだ… SAN値が5ポイント減少した。▼")
            print()
            global_value.game.player.SAN -= 5
        if self.map[new_y][new_x] == CAT:
            Ghost.show_cat()
            if global_value.game.ending_count == 100:
              print("女の子の影が猫を追い払ってくれた▼")
            print("……。SAN値が5ポイント減少した…▼")
            
            global_value.game.ending_count += 50
            global_value.game.player.SAN -= 5
        if self.map[new_y][new_x] == LIGHT:
            Box.show_light()
            print("懐中電灯を手に入れた。 SAN値が20ポイント回復した。▼")
            global_value.game.player.SAN += 20
            if global_value.game.player.SAN > 101:
                global_value.game.player.SAN = 101
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
            global_value.game.ending_count += 100
        if self.map[new_y][new_x] == BOX:
            Box.show_box()
            global_value.game.player.box_count += 1
            print("Enterで開ける")
            while True:
                item = random.choice(global_value.game.events)
                if (global_value.game.player.box_count < 5 and item == KEY and (self.room_id == CLASSROOM_3F or 
                                    self.room_id == ARTROOM_3F or self.room_id == MUSICROOM_3F)):
                    continue  # 鍵が三階の部屋に出た場合、選択しなおす
                break
            global_value.game.events.remove(item)
            if item == LIGHT:
                Box.show_light()
                print("懐中電灯を手に入れた。 SAN値が20ポイント回復した▼")
                global_value.game.player.SAN += 20
                if global_value.game.player.SAN > 101:
                    global_value.game.player.SAN = 101
            if item == TRAP:
                Box.show_trap()
                print("罠だ！ SAN値が10ポイント減少した▼")
                global_value.game.player.SAN -= 10
            if item == MISS:
                Box.show_empty()
                print("空箱だった・・・▼")
            if item == KEY:
                Box.show_key()
                print("鍵を入手した！▼")
                global_value.game.player.have_key = True

