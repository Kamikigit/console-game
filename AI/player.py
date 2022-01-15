from contains import *
import unicodedata, copy
from room import Room
from ghost import Ghost

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
        self.doors = set()
        self.boxes = set()
        self.lights = set()
        self.room_visited = set()
        self.exit_room_id = None

        self.des_y = None
        self.des_x = None

        self.next = None
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
                if 32 <= space <= 49: #扉を見つけた時
                    self.doors.add([self.room_id, y, x, space])

                if space == 12: #灯りを見つけた時
                    self.lights.add([self.room_id, y, x])

                if space == 11: #箱を見つけた時
                    self.boxes.add([self.room_id, y, x])
        # print(self.doors)

    def set_destination(self, ghosts):
        if self.SAN < 30: # SAN値が30未満のときは灯りを目的地に
            pass #目的地を灯探索へ
        elif self.have_key: # 鍵を取得しているときは出口を目的地に
            pass # 目的地を出口探索へ
        elif self.boxes == []: # 部屋に箱がないときは扉を目的地に
            self.des_y = self.doors[0][1] # ここのとり方も工夫したい
            self.des_x = self.doors[0][2]
            self.bfs(self.y, self.x, self.des_y, self.des_x, ghosts)
        elif self.lights == []: # 部屋に灯りがないときは箱を目的地に
            self.des_y = self.boxes[0][1]
            self.des_x = self.boxes[0][2]
            self.bfs(self.y ,self.x, self.des_y, self.des_x, ghosts)
        elif self.SAN <= 70: # SAN値が70以下で灯りを目的地に
            self.des_y = self.lights[0][1]
            self.des_x = self.lights[0][2]
            self.bfs(self.y ,self.x, self.des_y, self.des_x, ghosts)           
        else:
            self.des_y = self.boxes[0][1]
            self.des_x = self.boxes[0][2]
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
                    ghost_new_y = 0
                    ghost_new_x = 0
                    map_tmp[ghost.y][ghost.x] = 0
                    #幽霊で場合分け
                    if ghost.type == YUU:
                        for i in range(d): # 深さdのときの位置を当てる
                            if i < d:
                                ghost_new_y = ghost.y - i - 1
                            else:
                                ghost_new_y = YUU_ROOP[(i-ghost.y) % 8]
                        # おばけの前後左右マスにいかないようにおばけがいると仮配置
                        # print("おばけ: ", ghost_new_y, ghost.x)
                        map_tmp[ghost_new_y][ghost.x] = YUU
                        for l, m in ([1, 0], [-1, 0], [0, 1], [0, -1]):
                            if 0 <= ghost_new_y + l < self.height and 0 <= ghost_new_x + m < self.width:
                                map_tmp[ghost_new_y + l][ghost.x + m] = YUU
                    if ghost.type == REI:
                        for i in range(d):
                            if i < 4-d:
                                ghost_new_x = ghost.x + i + 1
                            else:
                                ghost_new_x = REI_ROOP[(i+ghost.x-3) % 8]
                        map_tmp[ghost.y][ghost_new_x] = REI
                        # おばけの前後左右マスにいかないようにおばけがいると仮配置
                        for l, m in ([1, 0], [-1, 0], [0, 1], [0, -1]):
                            if 0 <= ghost_new_y + l < self.height and 0 <= ghost_new_x + m < self.width:
                                map_tmp[ghost.y + l][ghost_new_x + m] = REI
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
                    node = Node(current_node, [new_y, new_x], current_node.depth+1) # I ノード作成
                    # 訪問済みかどうか
                    if [new_y, new_x]  not in visited:
                        if [new_y, new_x] not in queue:
                            queue.append(node)
                            # print(node.position, node.parent.print_node(), node.depth+1)
                            
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


