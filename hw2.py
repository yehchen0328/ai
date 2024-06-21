#參考老師程式碼與Chatgpt
import random

citys = [
    (0,3),(0,0),
    (0,2),(0,1),
    (1,0),(1,3),
    (2,0),(2,3),
    (3,0),(3,3),
    (3,1),(3,2)
]

#path = [i for i in range(len(citys))]
l = len(citys)
path = [(i+1)%l for i in range(l)]
print("起點:", path)

def distance(p1, p2):
    print('p1=', p1)
    x1, y1 = p1
    x2, y2 = p2
    return ((x2-x1)**2+(y2-y1)**2)**0.5

#設定最大迭代次數
max_iterations = 10

def pathLength(p):
    dist = 0
    plen = len(p)
    for i in range(plen):
        # dist += distance(citys[p[i]], citys[p[(i+1)%plen]])
        dist += distance(citys[i], citys[p[i]])
    return dist

def hill(path, max_iterations):
    #避免修改原本資料因此做淺拷貝
    now_path = path[:]
    now_distance = pathLength(now_path)
    
    for interation in range(max_iterations):
        new_path = now_path[:]
        i,j = random.sample(range(len(citys)),2)
        new_path[i], new_path[j] = new_path[j], new_path[i]
        new_distance = pathLength(new_path)

        if new_distance < now_distance:
            now_path = new_path
            now_distance = new_distance

            print("路徑", now_path, "距離", now_distance)

    return now_path, now_distance

best_path, best_distance = hill(path, max_iterations)

print("最佳路徑:", best_path)
print("最短距離:", best_distance)
