GAME_NOT_FINISHED = 0
GAME_FINISHED = 1

ROOF_TOP = 100 # 屋上
HALL_3F = 101 # 廊下３F
HALL_2F = 102 # 廊下２F
HALL_1F = 103 # 廊下１F
CLASSROOM_3F = 104 # 教室３Ｆ
CLASSROOM_2F = 105 # 教室２Ｆ
CLASSROOM_1F = 106 # 教室１Ｆ
MUSICROOM_3F = 107 # 音楽室３F
ARTROOM_3F = 108 # 美術室３F
LABLATOR_2F = 109 #  実験室２F
CLOTHINGROOM_2F = 110 # 被服室２F
FACULTYROOM_1F = 111 # 教員室１F
FRONT_1F = 112 # 玄関１F

EMPTY = 0 # 何もないマス
GOAL = 1 # 「出」のマス
UP = 2 # 「上」のマス
DOWN = 3 # 「下」のマス
DOOR = 4 # 「扉」のマス
DESK = 5 # 「机」のマス
PICTURE = 6 # 「絵」のマス
PIANO_PI = 7 # 「ピ」のマス
PIANO_A = 8 # 「ア」のマス
PIANO_NO = 9 # 「ノ」のマス
SHOES = 10 # 「靴」のマス
BOX = 11 # 「箱」のマス
LIGHT = 12 # 「灯」のマス
YUU = 13 # 「幽」のマス
REI = 14 # 「霊」のマス
MONKEY = 15 # 「猿」のマス
PHANTOM = 16 # 「幻」のマス
MIRROR = 17 # 「鏡」のマス
CAT = 18 # 「猫」のマス
TRAP = 19 # 「罠」のイベント
MISS = 20 # 「空箱」のイベント
KEY = 21 # 「鍵」
DIARY = 22 # 「□」
PLAYER = 99 # プレイヤーのマス

# 上
TO_ROOF_TOP_UP = 26
TO_HALL_3F_UP = 27
TO_HALL_2F_UP = 28
# 下
TO_HALL_3F_DOWN = 29
TO_HALL_2F_DOWN = 30
TO_HALL_1F_DOWN  = 31
# 扉
TO_CLASSROOM_3F = 32 # 教室３Ｆ
TO_CLASSROOM_2F = 33 # 教室２Ｆ
TO_CLASSROOM_1F = 34 # 教室１Ｆ
TO_MUSICROOM_3F = 35 # 音楽室３F
TO_ARTROOM_3F = 36 # 美術室３F
TO_LABLATOR_2F = 37 #  実験室２F
TO_CLOTHINGROOM_2F = 38 # 被服室２F
TO_FACULTYROOM_1F = 39 # 教員室１F
TO_FRONT_1F = 40 # 玄関１F

TO_CLASSROOM_3F_OUT = 41 # 教室３Ｆ
TO_CLASSROOM_2F_OUT = 42 # 教室２Ｆ
TO_CLASSROOM_1F_OUT = 43 # 教室１Ｆ
TO_MUSICROOM_3F_OUT = 44 # 音楽室３F
TO_ARTROOM_3F_OUT = 45 # 美術室３F
TO_LABLATOR_2F_OUT = 46 #  実験室２F
TO_CLOTHINGROOM_2F_OUT = 47 # 被服室２F
TO_FACULTYROOM_1F_OUT = 48 # 教員室１F
TO_FRONT_1F_OUT = 49 # 玄関１F

EVENTS = [LIGHT,LIGHT,LIGHT,LIGHT,TRAP,TRAP,TRAP,MISS,MISS,KEY]  # 箱の中身

PORTAL = {TO_ROOF_TOP_UP : [ROOF_TOP, 4, 4], TO_HALL_3F_UP : [HALL_3F, 1, 9], TO_HALL_2F_UP : [HALL_2F, 1, 9], 
          TO_HALL_3F_DOWN : [HALL_3F, 0, 9], TO_HALL_2F_DOWN : [HALL_2F, 0, 9], TO_HALL_1F_DOWN : [HALL_1F, 0, 9],
          TO_CLASSROOM_3F : [CLASSROOM_3F, 0, 0], TO_CLASSROOM_3F_OUT : [HALL_3F, 1, 0],
          TO_CLASSROOM_2F : [CLASSROOM_2F, 0, 0], TO_CLASSROOM_2F_OUT : [HALL_2F, 1, 0],
          TO_CLASSROOM_1F : [CLASSROOM_1F, 0, 4], TO_CLASSROOM_1F_OUT : [HALL_1F, 0, 0],
          TO_MUSICROOM_3F : [MUSICROOM_3F, 0, 0], TO_MUSICROOM_3F_OUT : [HALL_3F, 1, 4],
          TO_ARTROOM_3F : [ARTROOM_3F, 0, 0], TO_ARTROOM_3F_OUT : [HALL_3F, 1, 7],
          TO_LABLATOR_2F : [LABLATOR_2F, 0 ,0], TO_LABLATOR_2F_OUT : [HALL_2F, 1, 4],
          TO_CLOTHINGROOM_2F : [CLOTHINGROOM_2F, 0, 0], TO_CLOTHINGROOM_2F_OUT : [HALL_2F, 1, 7],
          TO_FACULTYROOM_1F : [FACULTYROOM_1F, 0, 4], TO_FACULTYROOM_1F_OUT : [HALL_1F, 1, 3],
          TO_FRONT_1F : [FRONT_1F, 0, 2], TO_FRONT_1F_OUT : [HALL_1F, 1, 7]}

ROOF_TOP_MAP = [[ 0, 11, 12, 11, 13],
                [ 0,  0,  0,  0,  0],
                [ 0,  0, 14,  0,  0],
                [ 0,  0,  0,  0,  0],
                [ 0,  0,  0,  0, 29]]
HALL_3F_MAP  = [[99,  0,  0,  0,  0, 15,  0,  0,  0, 26],
                [32,  0,  0,  0, 35,  5,  0, 36,  0, 30]]
HALL_2F_MAP  = [[ 0, 12,  0,  0, 16,  0,  0,  0,  0, 27],
                [33,  0,  0,  0, 37,  0,  0, 38,  0, 31]]
HALL_1F_MAP  = [[34,  12,  0,  0,  0,  0,  0,  0,  0, 28],
                [ 0,  0,  0, 39,  0,  0, 12, 40,  0,  0]]
CLASSROOM_3F_MAP = [[41,  0,  0,  0,  0],
                    [ 0,  5,  0,  0,  0],
                    [ 0, 22,  0,  0,  0],
                    [ 0,  0,  5,  0,  0],
                    [13, 11,  0,  0,  0]]
CLASSROOM_2F_MAP = [[42,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0],
                    [ 0, 13,  0,  5,  0],
                    [ 0,  0,  5, 11,  0],
                    [ 0,  0,  0,  0,  0]]
CLASSROOM_1F_MAP = [[ 0,  0,  0,  0, 43],
                    [ 0,  0,  0,  0,  0],
                    [11,  5, 13,  5,  0],
                    [ 0,  0,  0,  0,  0],
                    [ 0,  0,  5,  0,  0]]
FRONT_1F_MAP = [[  0,  0, 49,  0,  0],
                [ 14,  0,  0,  0, 14],
                [ 10,  0,  0,  0, 10],
                [ 10,  0,  0,  0, 10],
                [ 10,  0,  1,  0, 10]]
FACULTYROOM_1F_MAP = [[ 14,  0,  0,  0, 48],
                      [  0,  0,  0,  0,  0],
                      [ 11,  5,  0,  5,  0],
                      [  0,  0, 13,  0,  0],
                      [  0,  0,  0,  0, 12]]
CLOTHINGROOM_2F_MAP = [[ 47,  0,  0,  0, 12],
                       [  0,  5,  0,  5,  0],
                       [  0,  0, 13,  0,  0],
                       [ 17,  5,  0,  5,  0],
                       [  0, 11,  0,  0,  0]]
LABLATOR_2F_MAP = [[ 46,  0,  0,  0,  0],
                   [  0,  5,  5,  5,  0],
                   [  0, 14,  0,  0, 11],
                   [  0,  5,  5,  5,  0],
                   [ 12,  0, 18,  0,  0]]
ARTROOM_3F_MAP = [[ 45,  0,  0,  0, 14],
              [  0,  0,  6,  0,  0],
              [  0,  0,  6,  0, 12],
              [ 11,  0,  6,  0,  0],
              [  0,  0,  0,  0,  14]]
MUSICROOM_3F_MAP = [[ 44,  0,  0,  0, 11],
                [  0,  0,  0,  0,  0],
                [  0,  7,  0, 13,  0],
                [  0,  8,  9,  0,  0],
                [  0,  0, 12,  0,  0]]

SHOW_NAME = { EMPTY: "・", GOAL : "出", UP : "上", DOWN : "下", DOOR : "扉", DESK : "机", PICTURE : "絵", PIANO_PI : "ピ", PIANO_A : "ア", PIANO_NO : "ノ",
              SHOES : "靴", BOX : "箱", LIGHT : "灯", YUU : "幽", REI : "霊", MONKEY : "・", PHANTOM : "・", MIRROR : "鏡", CAT : "猫", DIARY : "□□",
              TO_CLASSROOM_3F: "扉", TO_CLASSROOM_2F: "扉", TO_CLASSROOM_1F: "扉", TO_MUSICROOM_3F: "扉", TO_ARTROOM_3F : "扉", 
              TO_LABLATOR_2F : "扉", TO_CLOTHINGROOM_2F : "扉", TO_FACULTYROOM_1F : "扉", TO_FRONT_1F : "扉",
              TO_CLASSROOM_3F_OUT: "扉", TO_CLASSROOM_2F_OUT: "扉", TO_CLASSROOM_1F_OUT: "扉", TO_MUSICROOM_3F_OUT: "扉", TO_ARTROOM_3F_OUT : "扉", 
              TO_LABLATOR_2F_OUT : "扉", TO_CLOTHINGROOM_2F_OUT : "扉", TO_FACULTYROOM_1F_OUT : "扉", TO_FRONT_1F_OUT : "扉", 
              TO_ROOF_TOP_UP : "上", TO_HALL_3F_UP : "上", TO_HALL_2F_UP : "上",
              TO_HALL_3F_DOWN : "下", TO_HALL_2F_DOWN : "下", TO_HALL_1F_DOWN : "下"}

MOVE_POINT = {"S" : [1, 0], "W": [-1, 0], "D" :  [0, 1], "A": [0, -1]}

MAPS = [ROOF_TOP_MAP, HALL_3F_MAP, HALL_2F_MAP, HALL_1F_MAP, CLASSROOM_3F_MAP, CLASSROOM_2F_MAP, CLASSROOM_1F_MAP, MUSICROOM_3F_MAP,
        ARTROOM_3F_MAP, LABLATOR_2F_MAP, CLOTHINGROOM_2F_MAP, FACULTYROOM_1F_MAP, FRONT_1F_MAP]

SHOW_ROOM = { ROOF_TOP : "屋上", HALL_3F : "廊下３F", HALL_2F : "廊下２F", HALL_1F : "廊下１F", CLASSROOM_3F : "教室３Ｆ",
              CLASSROOM_2F : "教室２Ｆ", CLASSROOM_1F : "教室１Ｆ", MUSICROOM_3F : "音楽室３F", ARTROOM_3F :  "美術室３F", 
              LABLATOR_2F : "実験室２F", CLOTHINGROOM_2F : "被服室２F", FACULTYROOM_1F : "教員室１F", FRONT_1F :"玄関１F"}

YUU_ROOP = [1, 2, 3, 4, 3, 2, 1, 0]
REI_ROOP = [4, 3, 2, 1, 0, 1, 2, 3]