a = 2
YUU_ROOP = [1, 2, 3, 4, 3, 2, 1, 0]
REI_ROOP = [4, 3, 2, 1, 0, 1, 2, 3]

for i in range(15):
    print("num:", i+1, end="\t")
    if i < 4-a:
        print(a+i+1)
    else:
        print(REI_ROOP[(i+(a-3))%8])

# for i in range(0, 20):
#     print("num:", i+1, end="\t")
#     if i < a:
#         print(a-i-1)
#     else:
#         print(YUU_ROOP[(i-a)%8])
    