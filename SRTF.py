import pandas as pd
import random

def SRTF(df):
    execute_time = df.at[0,'Arrival Time']
    remaining_time = 0
    index_min = 0
    ready = 0
    split_part = df.shape[0] # Các process >= split_part là các process đã được tách ra
    splitted = 0
    for i in range(df.shape[0]):
        print('\n I: ',i)
        while(ready < split_part): #Nếu vị trí < ready => Các process đó đã ready
            if (df.at[ready,'Arrival Time'] > execute_time): break
            ready += 1
        if(i==ready): index_min = split_part
        else: index_min = i
        for j in range(i+1,ready): # Chọn process có burst time min
            if(df.at[j,'Burst Time'] < df.at[index_min,'Burst Time']): index_min = j
        if (splitted): #Tìm min trong các phần còn lại của process bị tách
            for k in range(split_part,df.shape[0]): 
                if(df.at[k,'Burst Time'] < df.at[index_min,'Burst Time']): index_min = k
        if(index_min >= split_part): split_part += 1
        df.at[index_min,'Start']= execute_time
        df.at[index_min,'Response Time']= execute_time - df.at[index_min,'Arrival Time']
        df = df.sort_values(by="Start", ignore_index=True)
        df.at[i,'End']= df.at[i+1,'Arrival Time']
        remaining_time = df.at[i,'Burst Time'] - df.at[i,'End'] + df.at[i,'Start']
        split = 0
        for j in range(i+2,split_part+1): # Xử lý trường hợp nhiều process cùng arr nhưng có burst time < remaining time process đang chạy
            if(remaining_time > df.at[i+1,'Burst Time']):
                split = 1
                print('\nSplit: ',split)
                break
            if(df.at[j,'Arrival Time'] != df.at[i+1,'Arrival Time']): break
            if(remaining_time > df.at[j,'Burst Time']): split = 1
        if(split): # Thêm một process mới cùng pn, arr, bur = remaining time của process ban đầu
            splitted = 1
            df.at[i,'End'] = df.at[i+1,'Arrival Time']
            df = pd.concat([df, df.loc[i]], ignore_index=True)
            # df.at[df.shape[0],'Process Name'] = df.at[i,'Process Name']
            # df.arr[*size] = df.arr[i]
            df.at[df.shape[0],'Burst Time'] = remaining_time
            # df.star[*size] = 10000
            # (*size)++
        else: df.at[i,'End'] = df.at[i,'Start'] + df.at[i,'Burst Time']
        execute_time = df.at[i,'End']
        if(df.at[i+1,'Arrival Time'] > df.at[i,'End'] and  not splitted): execute_time = df.at[i+1,'Arrival Time'] # Có khoảng nghỉ giữa các process
        print(df,'\n')
    return df

# struct dataframe Caculate_WT_TAT(struct dataframe df, *size) 
# {
#     # Tính wt, tat
#     # struct dataframe merge_process
#     index = 0
#     is_first = 1
#     burst
#     resp
#     SortDataframe(&df,*size,0) 
#     for(i=0i<*sizei++) 
#     {   
#         if(df.pn[i+1] == df.pn[i])
#         {   
#             if(is_first)
#             {
#                 burst = df.bur[i]
#                 resp = df.resp[i]
#                 is_first = 0
#             }
#             continue
#         }
#         else if(is_first)
#         {
#             burst = df.bur[i]
#             resp = df.resp[i]
#         } 
#         is_first = 1
#         df.pn[index] = df.pn[i]
#         df.resp[index] = resp
#         df.wt[index] = df.finish[i] - burst - df.arr[i]
#         df.tat[index] = df.finish[i] - df.arr[i]
#         index++ 
#     }
#     *size = index
#     return df
# }

color_board = ['#AEA2C5','#BBDF32','#00504B','#F83FA0','#5d5c61','#7395ae','#557a95','#64495c','#3500d4','#950741','#c3083f','#e7717d','#c2c9cf','#afd275','#66fcf1','#c5c6c8','#46a29f','#f13c10','#106466','#ff652f','#ffe401','#13a76c','#8265a7','#65ccb8','#a4a61e']
# name = [4,3,2,1]
name = []
arrival = [0,1,2,3,4]
burst = [4,3,2,1,1]
if name == []:
  name = ['P'+str(i+1) for i in range(len(arrival))]
colors = [random.choice(color_board) for i in range(len(arrival))]
df = pd.DataFrame({'Color Code': colors,
                'Process Name': name,
                 'Arrival Time': arrival,
                 'Burst Time': burst,
                 'Start':10000,
                 'End':10000,
                 'Remain Time':10000,
                 'Waiting Time':0,
                 'Response Time':0,
                 'Turnaround Time':0})
print(df)
# print(SRTF(df))
SRTF(df)

#   Color Code Process Name  Arrival Time  Burst Time  Start    End  Remain Time
# 0    #66fcf1           P1             0           4      0      1            3
# 1    #106466           P2             1           3  10000  10000            3
# 2    #e7717d           P3             2           2  10000  10000            2
# 3    #557a95           P4             3           1  10000  10000            1
# 4    #5d5c61           P5             4           1  10000  10000            1