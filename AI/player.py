from contains import *
import unicodedata, copy
from room import Room
from ghost import Ghost
import time

class Node:
    def __init__(self, parent=None, position=None, depth=0):
        self.position = position
        self.parent = parent
        self.depth = depth
    def print_node(self):
        return self.position
        
class Player():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.player_name = None
        self.SAN = 100
        self.have_key = False
        self.box_count = 0

        self.room_id = None
        self.map = None
        self.doors = []
        self.boxes = []
        self.lights = []
        self.room_visited = set()
        self.exit_room_id = None
        self.to_exit_room = None

        self.des_y = None
        self.des_x = None

        self.next = None
        self.can_set_destination = True
        # self.hegiht = None
        # self.width = None
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
        self.height = len(self.map)
        self.width = len(self.map[0])

        for y in range(self.height):
            for x in range(self.width):
                space = self.map[y][x]
                if 25 <= space <= 49: #扉を見つけた時
                    self.doors.append([self.room_id, y, x])

                if space == 12: #灯りを見つけた時
                    self.lights.append([self.room_id, y, x])

                if space == 11: #箱を見つけた時
                    self.boxes.append([self.room_id, y, x])
                
                if space == 1: #出口を見つけた時
                    self.exit_room_id = [self.room_id, y, x]
                     #出口のある部屋に入るための扉も確保（行って戻ってくる必要ある）
                    self.to_exit_room = PORTAL[self.map[self.y][self.x]]
        # print(self.doors)
        # print(self.boxes)
        # print(self.lights)

    def set_destination(self, ghosts):
        def go_door():
            min_door = []
            min_stairs = []
            min_manhattan = 1000
            for d in self.doors:
                if d[0] == self.room_id and d[1:] != [0, 9] and d[1:] != [1, 9]:
                    manhattan = abs(d[1] - self.y) + abs(d[2] - self.x)
                    # print(manhattan)
                    if manhattan < min_manhattan:
                        min_manhattan = manhattan
                        min_door = d
                # 階段の場合、上に登るのが先
                if d[0] == self.room_id and (d[1:] == [0, 9] or d[1:] == [1, 9]):
                    if [self.y, self.x] != [0, 9] and d[0] == 101: #2, 1階のときは上にいかない
                        min_stairs = [0, 9]
                    else:
                        min_stairs = [1, 9]
            # 定めた扉から目的地のx, yを決定
            # print("今あるドア", self.doors,"最短", min_door)
            if min_door != []:
                self.des_y = min_door[1]
                self.des_x = min_door[2]
            else:
                self.des_y = min_stairs[0]
                self.des_x = min_stairs[1]
            self.bfs(self.y, self.x, self.des_y, self.des_x, ghosts)

        self.height = len(self.map)
        self.width = len(self.map[0])

        # if self.SAN < 30: # SAN値が30未満のときは灯りを目的地に
        #     for l in self.lights:
        #         if l[0] == self.room_id:
        #             self.des_y = l[1]
        #             self.des_x = l[2]
        #             break
        #     self.bfs(self.y ,self.x, self.des_y, self.des_x, ghosts)  
        #     print("目的値は灯りです")
        # elif self.have_key and self.exit_room_id == None: # 鍵を取得しているときは出口を目的地に

        if self.have_key and self.exit_room_id != None: # 鍵も出口もわかっている
            #出口と同じ部屋にいる場合
            if self.exit_room_id[0] == self.room_id:
                # print(self.exit_room_id)
                self.bfs(self.y, self.x, self.exit_room_id[1], self.exit_room_id[2], ghosts)
            # 違う部屋にいる場合
            else:
                self.doors.append(self.to_exit_room)
                go_door()
        # 部屋に箱がないときは扉を目的地に
        elif [True for i in self.boxes if i[0] == self.room_id] == []: 
            # #3階の探索が終わったら屋上に向かう
            # if self.doors == [[101, 0, 9], [101, 1, 9]]:
            #     self.bfs(self.y, self.x, 0, 9, ghosts)
            # # 2階の探索が終わったら下に降りる
            # この部屋についている最短距離の扉を目指す
            go_door()
        elif [True for i in self.lights if i[0] == self.room_id]  == []: # 部屋に灯りがないときは箱を目的地に
            for b in self.boxes:
                if b[0] == self.room_id:
                    self.des_y = b[1]
                    self.des_x = b[2]
                    break
            self.bfs(self.y ,self.x, self.des_y, self.des_x, ghosts)
            # print("目的地は箱です")
        elif self.SAN <= 70: # SAN値が70以下で灯りを目的地に
            for l in self.lights:
                if l[0] == self.room_id:
                    self.des_y = l[1]
                    self.des_x = l[2]
                    break
            self.bfs(self.y ,self.x, self.des_y, self.des_x, ghosts)           
            # print("目的地は灯りです")
        else:
            for b in self.boxes:
                if b[0] == self.room_id:
                    self.des_y = b[1]
                    self.des_x = b[2]
                    break
            self.bfs(self.y ,self.x, self.des_y, self.des_x, ghosts)
            # print("目的地は箱です")

    def bfs(self, sy, sx, gy, gx, ghosts):
        # ゴールと目的地が一緒の場合、探索できないのでとりあえず動く
        if [sy, sx] == [gy, gx]:
            for j, k in ([1, 0], [-1, 0], [0, 1], [0, -1]):
                if 0 <= sy + j < self.height and 0 <= sx + k < self.width:
                    # print(sy, j, sx,  k)
                    if self.map[sy + j][sx + k] == 0:
                        self.set_command(sy, sx, sy + j, sx+k) 
                        return
        queue = []
        visited = []
        start_node = Node(None, [sy, sx], 0)
        queue.append(start_node)
        # print(sy, sx, gy, gx)
        # print("Starting Breadth First Search...")
        while queue:
            current_node = queue.pop(0)
            visited.append(current_node.position)
            y = current_node.position[0]
            x = current_node.position[1]
            d = current_node.depth
            # print(f"node_y: {y}, node_x: {x}, depth: {d}")

            if [y, x] == [gy, gx]:
                # print("Breadth First Search success!!")
                self.return_path(current_node, sy, sx, gy, gx)
                self.can_set_destination = True
                break

            map_tmp = copy.deepcopy(self.map)
            # 移動可能な場所の把握
            for j, k in ([1, 0], [-1, 0], [0, 1], [0, -1]):
                new_y, new_x = y+j, x+k
                #壁判定
                if new_y < 0 or new_y >= self.height or new_x < 0 or new_x >= self.width:
                    continue
                #おばけの位置予測
                for ghost in ghosts:
                    if ghost.hit: #あたっているときは動かない
                        # print("あたってるよ")
                        continue
                    ghost_new_y = ghost.y
                    ghost_new_x = ghost.x
                    ghost_vy = ghost.vy #プラマイを変更するので上書きしないようにコピー
                    ghost_vx = ghost.vx
                    map_tmp[ghost.y][ghost.x] = 0
                    #幽霊で場合分け
                    if ghost.type == YUU:
                        for i in range(d+1): # 深さdのときの位置を当てる
                            if (ghost_new_y <= 0 or ghost_new_y >= self.height -1):
                                ghost_vy *= -1
                            # 幽の移動先が霊だった場合、幽が反転
                            elif (ghost.type == YUU):
                                # for文でghostsを読み取る
                                for gh in ghosts:
                                    # 確認している幽霊自体の場合はcontinue
                                    if (gh == ghost):
                                        continue
                                    if (gh.type == REI and ghost.y+ghost_vy == gh.y+gh.vy and ghost.x+ghost_vx == gh.x+gh.vx):
                                        ghost_vx *= -1
                                        ghost_vy *= -1
                            ghost_new_y += ghost_vy
                        # おばけの前後左右マスにいかないようにおばけがいると仮配置
                        # print("おばけ: ", ghost_new_y, ghost.x)
                        map_tmp[ghost_new_y][ghost.x] = YUU
                        for l, m in ([1, 0], [-1, 0], [0, 1], [0, -1]):
                            if 0 <= ghost_new_y + l < self.height and 0 <= ghost_new_x + m < self.width:
                                if map_tmp[ghost_new_y + l][ghost.x + m] == 0:
                                    map_tmp[ghost_new_y + l][ghost.x + m] = YUU
                    if ghost.type == REI:
                        # print("霊の位置pre", ghost.y, ghost_new_x, ghost_vx)
                        for i in range(d+1):
                            if ghost_new_x <= 0:
                                ghost_vx = 1
                            elif ghost_new_x >= self.width -1:
                                ghost_vx = -1
                            # 移動できないマスとぶつかった場合も反転
                            elif (UP <= map_tmp[ghost.y][ghost_new_x] <= BOX or
                                TO_ROOF_TOP_UP <= map_tmp[ghost.y][ghost_new_x] <= TO_FRONT_1F_OUT):
                                ghost_vx *= -1
                            ghost_new_x += ghost_vx
                        # print("霊の位置aft", ghost.y, ghost_new_x, ghost_vx)
                        map_tmp[ghost.y][ghost_new_x] = REI
                        # おばけの前後左右マスにいかないようにおばけがいると仮配置
                        for l, m in ([1, 0], [-1, 0], [0, 1], [0, -1]):
                            if 0 <= ghost_new_y + l < self.height and 0 <= ghost_new_x + m < self.width:
                                if map_tmp[ghost.y + l][ghost_new_x + m] == 0:
                                    map_tmp[ghost.y + l][ghost_new_x + m]= REI
                # print(new_y, new_x, d)
                # for i in range(self.height):
                #     for j in range(self.width):
                #         print(map_tmp[i][j], end="\t")
                #     print()
                # print()
                # 移動不可マスは踏めない
                if map_tmp[new_y][new_x] != 13 and map_tmp[new_y][new_x] != 14 and \
                    10 < map_tmp[new_y][new_x] < 23 or map_tmp[new_y][new_x] == 0 or map_tmp[new_y][new_x] == map_tmp[gy][gx] \
                    or map_tmp[new_y][new_x] == 1:
                    # print("insert depth", current_node)
                    # print(new_y, new_x)
                    node = Node(current_node, [new_y, new_x], current_node.depth+1) # I ノード作成
                    # 訪問済みかどうか
                    if [new_y, new_x]  not in visited:
                        if [new_y, new_x] not in queue:
                            queue.append(node)
                            # print("追加しました！", node.position, node.parent.print_node(), node.depth)
        
        # 経路が見つからずに探索終了（幽霊にどうしてもぶつかるしかない場合）
        if [y, x] != [gy, gx]:
            # for i in range(self.height):
            #     for j in range(self.width):
            #         print(map_tmp[i][j], end="\t")
            #     print()
            # print()
            # print("ぶつかるが仕方ない")
            if self.map[gy][gx] == LIGHT:
                self.check_items(gy, gx)
            #とりあえず動けるところに移動（幽霊に挟まれたときなど）
            # if self.can_set_destination:
            for j, k in ([0, 1], [0, -1], [1, 0], [-1, 0]):
                if 0 <= sy + j < self.height and 0 <= sx + k < self.width:
                    if self.map[sy + j][sx + k] == 0:
                        for l, m in ([0, 1], [0, -1], [1, 0], [-1, 0]):
                            if 0 <= sy + j + l < self.height and 0 <= sx + k + m < self.width:
                                if self.map[sy+j+l][sx+k+m] == 0:
                                    self.set_command(sy, sx, sy + j, sx+k) 
                                    # self.can_set_destination = False
                                    # print(sy, j, sx,  k)
                                    # print("再設定しました")
                                    return
            # 2回以上詰まっていたらその目的地にはたどり着けないので、削除
            # else:
            #     if 32 <= self.map[gy][gx] <= 49:
            #         self.doors.append([self.room_id, gy, gx])
            #     self.check_items(gy, gx)
            #     self.set_destination(ghosts)   # 目的地再設定

            #     if self.map[gy][gx] == BOX: #箱はぜったい取る。出口も亡くなったらダメ
            #         self.boxes.append([self.room_id, gy, gx])
            #     self.can_set_destination = True
            #     print("消して再設定しました")


    def return_path(self, current_node, sy, sx, gy, gx):
        path = []
        while True:
            current_node = current_node.parent
            path.append(current_node.position)
            if current_node.position == [sy, sx]:
                break
        # print("Path to goal:")
        # for i in path[:0:-1]:
        #     print(i, "->", end=" ")
        # print(path[0], "->", [gy, gx])
        path = path[::-1] #逆方向にする
        path.append([gy, gx]) #ゴールがないので追加する
        # print("Next AI move:", path[0], "->", path[1])

        self.set_command(path[0][0], path[0][1], path[1][0], path[1][1] )
        self.check_items(path[1][0], path[1][1])


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
        # print(self.next)

    # 箱や灯りを取ったか
    def check_items(self, next_y, next_x):
        if self.map[next_y][next_x] == BOX:
            self.boxes.remove([self.room_id, next_y, next_x])
        if self.map[next_y][next_x] == LIGHT:
            self.lights.remove([self.room_id, next_y, next_x])
        if 25 < self.map[next_y][next_x] < 49:
            self.doors.remove([self.room_id, next_y, next_x])
