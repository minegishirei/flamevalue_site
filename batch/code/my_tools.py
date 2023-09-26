import json

def del_dub_dict_list(dict_list):
    return list(map(json.loads, set(map(json.dumps, dict_list))))

def calc_distance(a, b):
    if a == b: return 0
    a_k = len(a)
    b_k = len(b)
    if a == "": return b_k
    if b == "": return a_k
#1---格納するための表
    matrix = [[] for i in range(a_k+1)]
#2---初期化
    for i in range(a_k+1):
        matrix[i] = [0 for j in range(b_k+1)]
#3---0時の初期値を設定
    for i in range(a_k+1):
        matrix[i][0] = i
    for j in range(b_k+1):
        matrix[0][j] = j
#4---表を埋める
    for i in range(1, a_k+1):
        ac = a[i-1]
        for j in range(1, b_k+1):
            bc = b[j-1]
            cost = 0 if (ac == bc) else 1
            matrix[i][j] = min([
                matrix[i-1][j] + 1,
                matrix[i][j-1] + 1,
                matrix[i-1][j-1] + cost
            ])
    return matrix[a_k][b_k]