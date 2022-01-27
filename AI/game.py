import copy, time, os
from contains import *
from player import Player
from room import Room

class Game:
    def __init__(self):
        self.game_finished = GAME_NOT_FINISHED
        self.rooms = []
        self.current_room = None
        self.player = Player()
        self.last_move = EMPTY
        self.ending_count = 0  # エンディング分岐用変数
        self.clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')


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
            os.system("cls")
            
            self.player.show_status()  # ステータスの表示
            self.current_room.show_room()  # 部屋情報を表示
            if (self.check_san()):  # プレイヤーのSAN値が0以下だった場合
                break

            change_room = self.current_room.move_player()  # プレイヤーの移動
            time.sleep(0.5)
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
            if self.ending_count == 0:
              print("宿題を取りに来た時と変わらない、ごく普通の学校がそびえたっていた▼")
              print("NOMAL END")
            if self.ending_count == 50:
              print("実験室の窓からたくさんの目が付いた猫が自分を睨んでいた▼")
              print("BAD END")
            if self.ending_count == 100:
              print("実験室の窓から女の子が手を振っていた▼")
              print("TRUE END")
            if self.ending_count == 150:
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