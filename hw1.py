#參考Chatgpt
import random

# 課程、老師、教室和時段的信息
courses = [
    {'teacher': '甲', 'name':'機率', 'hours': 2},
    {'teacher': '甲', 'name':'線代', 'hours': 3},
    {'teacher': '甲', 'name':'離散', 'hours': 3},
    {'teacher': '乙', 'name':'視窗', 'hours': 3},
    {'teacher': '乙', 'name':'科學', 'hours': 3},
    {'teacher': '乙', 'name':'系統', 'hours': 3},
    {'teacher': '乙', 'name':'計概', 'hours': 3},
    {'teacher': '丙', 'name':'軟工', 'hours': 3},
    {'teacher': '丙', 'name':'行動', 'hours': 3},
    {'teacher': '丙', 'name':'網路', 'hours': 3},
    {'teacher': '丁', 'name':'媒體', 'hours': 3},
    {'teacher': '丁', 'name':'工數', 'hours': 3},
    {'teacher': '丁', 'name':'動畫', 'hours': 3},
    {'teacher': '丁', 'name':'電子', 'hours': 4},
    {'teacher': '丁', 'name':'嵌入', 'hours': 3},
    {'teacher': '戊', 'name':'網站', 'hours': 3},
    {'teacher': '戊', 'name':'網頁', 'hours': 3},
    {'teacher': '戊', 'name':'演算', 'hours': 3},
    {'teacher': '戊', 'name':'結構', 'hours': 3},
    {'teacher': '戊', 'name':'智慧', 'hours': 3}
]

slots = [
    'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17',
    'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27',
    'A31', 'A32', 'A33', 'A34', 'A35', 'A36', 'A37',
    'A41', 'A42', 'A43', 'A44', 'A45', 'A46', 'A47',
    'A51', 'A52', 'A53', 'A54', 'A55', 'A56', 'A57',
    'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17',
    'B21', 'B22', 'B23', 'B24', 'B25', 'B26', 'B27',
    'B31', 'B32', 'B33', 'B34', 'B35', 'B36', 'B37',
    'B41', 'B42', 'B43', 'B44', 'B45', 'B46', 'B47',
    'B51', 'B52', 'B53', 'B54', 'B55', 'B56', 'B57'
]

# 創建初始解
def create_initial_solution(courses, slots):
    solution = {}
    for course in courses:
        slot = random.choice(slots)
        solution[course['name']] = slot
    return solution

# 目標函數：計算解的適應度
def evaluate_solution(solution):
    score = 0
    teacher_slots = {}
    for course, slot in solution.items():
        teacher = next(c['teacher'] for c in courses if c['name'] == course)
        if teacher not in teacher_slots:
            teacher_slots[teacher] = []
        teacher_slots[teacher].append(slot)
    
    for teacher, slots in teacher_slots.items():
        days = set(slot[1] for slot in slots)  # 獲取每個老師授課的天數
        score += len(days)  # 天數越少，分數越高
    return score

# 生成鄰近解
def generate_neighbor(solution):
    new_solution = solution.copy()
    course1, course2 = random.sample(list(new_solution.keys()), 2)
    new_solution[course1], new_solution[course2] = new_solution[course2], new_solution[course1]
    return new_solution

# 爬山算法
def hill_climbing(courses, slots):
    current_solution = create_initial_solution(courses, slots)
    current_score = evaluate_solution(current_solution)
    
    while True:
        neighbor_solution = generate_neighbor(current_solution)
        neighbor_score = evaluate_solution(neighbor_solution)
        
        if neighbor_score > current_score:
            current_solution = neighbor_solution
            current_score = neighbor_score
        else:
            break
    
    return current_solution, current_score

# 執行爬山算法
solution, score = hill_climbing(courses, slots)
print("最終解:", solution)
print("最終得分:", score)
