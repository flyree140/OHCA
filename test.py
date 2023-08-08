# ##########################################################
# #2023/01/17
# #兩個CSV檔，A的所有點去找到B當中找距離最近點的點
# #，使用QGIS的PYTHON程式，需要參照真實地圖的路來找最近的點。
# #改2步驟
# ##########################################################

import csv
csv_path = '/home/john/network/OHCA/116-110OHCA - 111.csv'  #1 改檔案路徑及名稱 <--------------------------------------------------------------

csv_count = 0
points_111 = []
with open(csv_path, 'r',encoding='utf-8',errors='ignore') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    # 遍歷每一行數據
    for row in reader:
        csv_count = csv_count + 1   
        # 建立座標點
        # if row[7] != '' and csv_count < 4: #跑前3筆
        if row[5] != '':
          points_111.append([row[0],float(row[5]),float(row[6])]) #2 改ID欄位及經緯度欄位 <------------------------------------------------

#111 [5] [6]
#110 [7] [8]
#109 [11] [12]
#108 [9] [10]
#107 [7] [8]
#106 [6] [7]

# 108
# 計數：307 項
# 平均距離：393.99 公尺
# 中位數距離：299.01 公尺
# 四分位數：[186.11800000000002, 299.015, 547.335] 公尺
# 標準差：272.35254989388443 公尺
# 合計：120955.64700000004 公尺
# 最小值：5.725 公尺
# 最大值：1923.29 公尺

# 111
# 計數：325 項
# 平均距離：439.79 公尺
# 中位數距離：305.98 公尺
# 四分位數：[196.08700000000002, 305.98299999999995, 586.1220000000001] 公尺
# 標準差：379.27910333917293 公尺
# 合計：142933.072 公尺
# 最小值：5.725 公尺
# 最大值：3105.868 公尺


row_index = 0
csv_path = '/home/john/network/OHCA/AED20211102.csv'
points_AED = []

with open(csv_path, 'r',encoding='utf-8',errors='ignore') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    # 遍歷每一行數據
    for row in reader:
        if row_index > 0 :
            # 建立座標點
            points_AED.append([row[0],float(row[11]), float(row[12])])
        else:
            row_index+=1


import osmnx as ox #紀錄OSM地圖 免費無限制額度
import folium #沒用到 繪製漂亮地圖工具
import networkx as nx #計算節點的工具


G = ox.graph_from_point((25.1173052, 121.7298188), dist =10000, network_type='walk')


# 建立空字典，儲存對應結果
result = {}

# 對每個座標 A 進行處理
for points_111_i in points_111:
    # 儲存最小距離
    min_distance = float('inf')
    # 儲存最近的 B 座標
    closest_b = None
    
    
    # if points_111_i[0] != "O110-260" or points_111_i[0] != "O110-261":
    #     continue
    # print(min_distance)

    # 獲取 origin 點(OHCA)
    origin = ox.nearest_nodes(G, float(points_111_i[2]), float(points_111_i[1])) #建立節點時經緯度反過來放!!

    # 計算每個 origin 座標與 destination 座標之間的距離
    for points_AED_i in points_AED:
        
        # 獲取 destination 點(AED)
        destination = ox.nearest_nodes(G, float(points_AED_i[2]), float(points_AED_i[1])) #建立節點時經緯度反過來放!!

        # 獲取 A 點和 B 點之間的最短路徑
        distance = nx.shortest_path_length (G, origin, destination, weight='length')

        # if points_AED_i[0] == "A197" or points_AED_i[0] == "A151" or points_AED_i[0] == "A12":
        #     print(points_AED_i[0] + ":" + str(distance))
        #     route = nx.shortest_path(G, origin, destination, weight='length')
        #     fig, ax = ox.plot_graph_route(G, route) 

        # 比較最短距離
        if distance < min_distance and distance > 0:
            min_distance = distance
            closest_b = points_AED_i
    # 將結果儲存到字典中
    result[points_111_i[0]] = (closest_b, min_distance)

print(result)

import statistics


# 將距離抽出來並建立列表
distances = [distance for _, distance in result.values()]


# 計算距離的平均、中位數、四分位數
mean = statistics.mean(distances)
median = statistics.median(distances)
quartiles = statistics.quantiles(distances, n=4)
stdev = statistics.stdev(distances)

print(f'計數：{len(distances)} 項')
print(f'平均距離：{mean:.2f} 公尺')
print(f'中位數距離：{median:.2f} 公尺')
print(f'四分位數：{quartiles} 公尺')
print(f'標準差：{stdev} 公尺')
print(f'合計：{sum(distances)} 公尺')
print(f'最小值：{min(distances)} 公尺')
print(f'最大值：{max(distances)} 公尺')
# m