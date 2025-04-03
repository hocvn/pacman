import dfs
import ucs

tiles = [
    "#####################",
    "#                   #",
    "# ### ### ### ### ###",
    "# #   #   #   #   # #",
    "# # ### # # # ### # #",
    "#     #   #   #     #",
    "### # ###   ### # ###",
    "#   #     #     #   #",
    "# ### ### # ### ### #",
    "# #   #   #   #   # #",
    "# ### ###   ### ### #",
    "#   #           #   #",
    "### # ######### # ###",
    "#   #     #     #   #",
    "# ### ### # ### ### #",
    "# #   #       #   # #",
    "# ###   #####   ### #",
    "#     #       #     #",
    "# ### # ##### # #####",
    "#                   #",
    "#####################",
]

path = [(19, 19), (18, 19), (17, 19), (16, 19), (15, 19), (15, 18), (15, 17), (15, 16), (15, 15), (15, 14), (15, 13), (15, 12), (15, 11), (15, 10), (15, 9), (15, 8), (15, 7), (15, 6), (15, 5), (16, 5), (17, 5), (17, 4), (17, 3), (17, 2), (17, 1), (16, 1), (15, 1), (14, 1), (13, 1), (13, 2), (13, 3), (13, 4), (13, 5), (12, 5), (11, 5), (11, 6), (11, 7), (11, 8), (11, 9), (11, 10), (11, 11), (10, 11), (10, 10)]

# Chuyển đổi tiles thành danh sách mutable
tiles = [list(row) for row in tiles]

# Đánh dấu đường đi bằng 'g'
for y, x in path:
    tiles[x][y] = ' '

# Chuyển đổi lại thành chuỗi
tiles = ["".join(row) for row in tiles]

# In ma trận kết quả
# for row in tiles:
#     print(row)

maze = [
    "#######",
    "#     #",
    "# ### #",
    "#     #",
    "#######",
]


path = dfs.dfs((14, 19), (10, 10), tiles)
path3 = dfs.dfs((15, 19), (10, 10), tiles)
# print(tiles[19][20])
# path = dfs.dfs((2, 1), (3, 5), maze)
path2 = ucs.ucs((19, 19), (10, 10), tiles)
# print(path)
# print('\n')
# print(path3)


import binascii
import base64

encoded_secret = "3d3d516343746d4d6d6c315669563362"

# Chuyển từ Hex về chuỗi
decoded_hex = binascii.unhexlify(encoded_secret)
print(decoded_hex)

# Đảo ngược chuỗi
reversed_string = decoded_hex[::-1]
print(reversed_string)

# Giải mã Base64
original_secret = base64.b64decode(reversed_string).decode()

print("Secret:", original_secret)
