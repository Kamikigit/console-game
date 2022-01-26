from contains import *
import unicodedata, copy
from room import Room
from ghost import Ghost
import time

class Node:
    def __init__(self, parent=None, position=None, depth=0):
        self.position = position
        self.parent = parent
        self.depth = 0
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
        # print(self.doors)
        # print(self.boxes)
        # print(self.lights)

    def set_destination(self, ghosts):
        self.height = len(self.map)
        self.width = len(self.map[0])

        if self.SAN < 30: # SAN値が30未満のときは灯りを目的地に
            pass #目的地を灯探索へ
        elif self.have_key: # 鍵を取得しているときは出口を目的地に
            pass # 目的地を出口探索へ
        # 部屋に箱がないときは扉を目的地に
        elif [True for i in self.boxes if i[0] == self.room_id] == []: 
            # この部屋についている最短距離の扉を目指す
            min_door = []
            min_manhattan = 1000
            for d in self.doors:
                if d[0] == self.room_id: 
                    manhattan = abs(d[1] - self.y) + abs(d[2] - self.x)
                    # print(manhattan)
                    if manhattan < min_manhattan:
                        min_manhattan = manhattan
                        min_door = d
            # 定めた扉から目的地のx, yを決定
            print("今あるドア", self.doors,"最短", min_door)
            self.des_y = min_door[1]
            self.des_x = min_door[2]
            self.bfs(self.y, self.x, self.des_y, self.des_x, ghosts)
        elif [True for i in self.lights if i[0] == self.room_id]  == []: # 部屋に灯りがないときは箱を目的地に
            for b in self.boxes:
                if b[0] == self.room_id:
                    self.des_y = b[1]
                    self.des_x = b[2]
                    break
            self.bfs(self.y ,self.x, self.des_y, self.des_x, ghosts)
        elif self.SAN <= 70: # SAN値が70以下で灯りを目的地に
            for l in self.lights:
                if l[0] == self.room_id:
                    self.des_y = l[1]
                    self.des_x = l[2]
                    break
            self.bfs(self.y ,self.x, self.des_y, self.des_x, ghosts)           
        else:
            for b in self.boxes:
                if b[0] == self.room_id:
                    self.des_y = b[1]
                    self.des_x = b[2]
                    break
            self.bfs(self.y ,self.x, self.des_y, self.des_x, ghosts)

    def bfs(self, sy, sx, gy, gx, ghosts):
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
            d = current_node.depth + 1
            # print("depth", d)

            if [y, x] == [gy, gx]:
                print("Breadth First Search success!!")
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
                    ghost_new_y = ghost.y
                    ghost_new_x = ghost.x
                    ghost_vy = ghost.vy #プラマイを変更するので上書きしないようにコピー
                    ghost_vx = ghost.vx
                    map_tmp[ghost.y][ghost.x] = 0
                    #幽霊で場合分け
                    if ghost.type == YUU:
                        for i in range(d): # 深さdのときの位置を当てる
                            if (ghost_new_y == 0 or ghost_new_y == self.height -1):
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
                        print("霊の位置pre", ghost.y, ghost_new_x, ghost_vx)
                        for i in range(d):
                            if ghost_new_x == 0:
                                ghost_vx = 1
                            elif ghost_new_x == self.width -1:
                                ghost_vx = -1
                            ghost_new_x += ghost_vx
                        print("霊の位置aft", ghost.y, ghost_new_x, ghost_vx)
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
                     10 < map_tmp[new_y][new_x] < 23 or map_tmp[new_y][new_x] == 0 or map_tmp[new_y][new_x] == map_tmp[gy][gx]:
                    # print("insert depth", current_node)
                    # print(new_y, new_x)
                    node = Node(current_node, [new_y, new_x], current_node.depth+1) # I ノード作成
                    # 訪問済みかどうか
                    if [new_y, new_x]  not in visited:
                        if [new_y, new_x] not in queue:
                            queue.append(node)
                            # print(node.position, node.parent.print_node(), node.depth+1)
        
        # 経路が見つからずに探索終了（幽霊にどうしてもぶつかるしかない場合）
        if [y, x] != [gy, gx]:
            for i in range(self.height):
                for j in range(self.width):
                    print(map_tmp[i][j], end="\t")
                print()
            print()
            print("ぶつかるが仕方ない")
            #とりあえず動けるところに移動（幽霊に挟まれたときなど）
            if self.can_set_destination:
                for j, k in ([1, 0], [-1, 0], [0, 1], [0, -1]):
                    if 0 <= sy + j < self.height and 0 <= sx + k < self.width:
                        print(sy, j, sx,  k)
                        if self.map[sy + j][sx + k] == 0:
                            self.set_command(sy, sx, sy + j, sx+k) 
                            self.can_set_destination = False
                            break
            # 2回以上詰まっていたらその目的地にはたどり着けないので、削除
            else:
                self.check_items(gy, gx)
                self.set_destination(ghosts)   # 目的地再設定
                self.can_set_destination = True
            print("再設定しました")
            print(y, x, gy, gx)
            time.sleep(1)


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
        print(self.next)

    # 箱や灯りを取ったか
    def check_items(self, next_y, next_x):
        if self.map[next_y][next_x] == BOX:
            self.boxes.remove([self.room_id, next_y, next_x])
        if self.map[next_y][next_x] == LIGHT:
            self.lights.remove([self.room_id, next_y, next_x])
        if 25 < self.map[next_y][next_x] < 49:
            self.doors.remove([self.room_id, next_y, next_x])
