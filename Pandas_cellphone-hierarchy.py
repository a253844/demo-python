import csv , time 
import pandas as pd
import numpy as np

start = time.time()

#---- 毒入檔案 ----
df = pd.read_csv('./cellphone2.csv', encoding = 'utf-8') 

#---- 計算空值並刪減欄位 & 其他欄位空值轉變為零 ---
count_null = df.isnull().sum(axis=0)>100

null_columns = []
for i in range(len(count_null)):
    if count_null[i] == True :
        null_columns.append(df.columns[i])

df = df.drop(columns = null_columns)
df= df.fillna('0')

#---- 計算重複值並刪減 ----

#print(df.nunique())
for i in df.columns:
    df[i] = df[i].apply(str)

data_id = []
for i in df.columns[1:]:
    tamp_id = []
    count = df[i].unique()
    tamp_id.append(i)
    for j in range(len(count)):
        if count[j] == '0':
            pass
        else:
            df[i][ df[i] == count[j] ] = j+1
        tamp_id.append(count[j])
    data_id.append(tamp_id)

df_test =   df         
for i in range(22,49):
    df_test = df_test.drop(index=i) #刪除列

df_test = df_test.reset_index(drop=True)

df_data = df_test.drop(columns='產品') #刪除行 
df_data = np.array(df_data).tolist()
df_data = np.array(df_data , dtype=np.float64)

#----- 階層式 分群 --------

def cluser (data , n):
    from scipy.cluster.hierarchy import linkage, dendrogram , fcluster
    from scipy.spatial.distance import pdist
    
    
    data_dist = pdist(data) 
    data_link = linkage(data_dist,method='complete', metric='euclidean') 
    #matchdata = dendrogram(data_link,leaf_font_size=8)

    # 印出分群結果
    print("----- 分群數 "+ str(n) +"-----")
    print("----- 分群結果 -----")
    clusterData = fcluster(data_link, n, criterion='maxclust')

    for i in range(1,n+1):
        count = 0
        for j in range(len(clusterData)):
            if clusterData[j] == i:
                count += 1
   
    cluster = []
    for i in range(len(clusterData)):   
        cluster_data = []
        cluster_data.append(i)
        cluster_data.append(df_test['產品'][i])
        cluster_data.append(clusterData[i])
        cluster_data.append(data[i])
        cluster.append(cluster_data)    
    
    return cluster

def drew_heatmap (cluster , num):
    import draw_heatmap
    
    cluster_index = []
    cluster_info = []
    #num = eval(input("輸入要繪製成HeatMap的 (輸入 0 跳過) : ")) 
    count = 20
    print("----- 第 " +str(num+1)+ " Heatmap -----")
    if num == 0:
        pass
    else:
        for i in range(len(cluster)):
            if cluster[i][2] == num:
                cluster_index.append(cluster[i][1])
                cluster_info.append(cluster[i][3])
                count += 1
    
        draw_heatmap.heatmap(cluster_info,cluster_index,count)
        
#result = cluser(df_data , 5)
'''
for i in range(len(result)):
    if result[i][2] == 35:
        print(result[i][1])
'''
end = time.time() 
print(end-start)
