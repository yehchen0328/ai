#參考ChatGPT

from scipy.optimize import linprog

# 目標函數係數 
c = [-3, -2, -5]

# 約束係數矩陣 A_ub 和右側邊界 b_ub
A_ub = [
    [1, 1, 0],  # x + y <= 10
    [2, 0, 1],  # 2x + z <= 9
    [0, 1, 2]   # y + 2z <= 11
]
b_ub = [10, 9, 11]

# x, y, z 都是不是負的
bounds = [(0, None), (0, None), (0, None)] 

# 使用 linprog 函數求解最大化問題
res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

# 輸出結果
if res.success:
    print("最大化目標函數值:", -res.fun)  
    print("最佳解 x, y, z:", res.x)
else:
    print("線性規劃問題沒有解")
