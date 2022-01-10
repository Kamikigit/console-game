from contains import *
import unicodedata

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


