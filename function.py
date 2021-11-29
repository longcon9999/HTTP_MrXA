#
# # n = 3
# # m = 6
# # conn = 6
# # p1 = "8, 7, 9"
# # p2 = "5, 11, 9"
# # p3 = "5, 7, 14"
# # c1 = "1,1-2,2"
# # c2 = "3,1-1,2"
# # c3 = "3,2-2,4"
# # c4 = "2,3-1,4"
# # c5 = "1,3-3,4"
# # c6 = "2,5-3,6"
# # p = [p1, p2, p3]
# # c = [c1, c2, c3, c4, c5, c6]
# n = 3
# m = 8
# conn = 7
# p1 = "5, 8, 11"
# p2 = "8, 11, 14"
# p3 = "8, 11, 14"
# c1 = "1,1-2,2"
# c2 = "3,1-1,2"
# c3 = "2,3-1,4"
# c4 = "3,2-2,4"
# c5 = "1,3-3,4"
# c6 = "2,5-3,6"
# c7 = "1,6-2,7"
# p = [p1, p2, p3]
# c = [c1, c2, c3, c4, c5, c6, c7]
# P = {}
# Conn = {}
# try:
#     for i in range(len(p)):
#         P[i + 1] = [[int(tmp.strip()) for tmp in p[i].split(",")]]
#     print(P)
#     for i in c:
#         tmp = i.split("-")
#         Conn[",".join([x.strip() for x in tmp[1].split(",")])] = ",".join([x.strip() for x in tmp[0].split(",")])
#     print(Conn)
#     for i in range(1, m+1):
#         for j in range(1, n+1):
#             tmp = P.get(j)
#             if tmp is None:
#                 tmp = [[0, 0, 0]]
#             pre_tmp = tmp[i - 1]
#             after_tmp = []
#             for _i in range(len(pre_tmp)):
#                 if _i == j - 1:
#                     after_tmp.append(pre_tmp[_i] + 1)
#                 else:
#                     after_tmp.append(pre_tmp[_i])
#             if Conn.get(f"{j},{i}") is not None:
#                 compare_item = str(Conn.get(f"{j},{i}"))
#                 compare_vector = P.get(int(compare_item.split(",")[0]))[int(compare_item.split(",")[1])]
#                 for _i in range(len(after_tmp)):
#                     if after_tmp[_i] < compare_vector[_i]:
#                         after_tmp[_i] = compare_vector[_i]
#             tmp.append(after_tmp)
#             P[j] = tmp
#     for k, v in P.items():
#         print(k)
#         print(v)
#
# except Exception as e:
#     print(e)
