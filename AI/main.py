import time, random,  os, copy
from contains import *
from game import *

if __name__ in "__main__": 
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