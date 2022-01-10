from contains import *

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
