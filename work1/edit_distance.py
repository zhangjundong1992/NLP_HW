def count_chars_distance(s1, s2):
    m, n = len(s1) + 1, len(s2) + 1
    matrix = [[0] * n for i in range(m)]
    matrix[0] = [i for i in range(n)]
    for i in range(m):
        matrix[i][0] = i
    for i in range(1, m):
        for j in range(1, n):
            if s1[i - 1] == s2[j - 1]:
                temp = 0
            else:
                temp = 1
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + temp)
    return matrix[m - 1][n - 1]


print("请输入str1:")
s1 = str(input())
print("请输入str2:")
s2 = str(input())
dist = count_chars_distance(s1, s2)
print(dist)
