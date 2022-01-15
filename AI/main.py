import time
from contains import *
from game import Game
import global_value

if __name__ in "__main__": 
    while True:
        global_value.game = Game()
        global_value.game.init_game()  # ゲームの初期化

        start_time = time.time()   # スタートタイムを記録
        global_value.game.game_loop()  # メインループ

        play_time = time.time() - start_time # プレイ時間を計算
        min = int(play_time / 60)  # 分
        sec = int(play_time % 60)  # 秒
        print(f"プレイ時間：{min}分{sec}秒\n")  # プレイ時間をprint

        if global_value.game.replay() == "N":  # リプレイ確認
            break
            
        # os.system("clear")
    print("ありがとうございました！▼")