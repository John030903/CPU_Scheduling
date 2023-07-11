import pandas as pd
import random


def SJF(df):
    execute_time = df.at[0,'Arrival Time']
    ready = 0
    size = df.shape[0]
    index_min = 0
    for i in range(size):
        print("Index min: ",index_min)
        print("I: ",i)
        while(ready < size): #Nếu vị trí < ready => Các process đó đã ready
            if (df.at[ready,'Arrival Time'] > execute_time): break
            ready += 1
        index_min = i
        for j in range(i+1,ready): # Chọn process có burst time min
            if(df.at[j,'Burst Time'] < df.at[index_min,'Burst Time']): 
                index_min = j
        print("Min: ", index_min)
        df.at[index_min,'Start'] = execute_time
        df.at[index_min,'Response Time'] = execute_time - df.at[index_min,'Arrival Time']
        df.at[index_min,'Waiting Time'] = df.at[index_min,'Response Time']
        df.at[index_min,'End'] = df.at[index_min,'Start'] + df.at[index_min,'Burst Time']
        df.at[index_min,'Turnaround Time'] = df.at[index_min,'End'] - df.at[index_min,'Start']
        execute_time = df.at[index_min,'End']
        df = df.sort_values(by="Start", ignore_index=True)
        if i+1 == size: break
        if(df.at[i+1,'Arrival Time'] > df.at[i,'End']): # Có khoảng nghỉ giữa các process
            execute_time = df.at[i+1,'Arrival Time']
        print(df,"\n")
    return df.loc[:,['Color Code','Process Name','Arrival Time','Burst Time','Start','End','Waiting Time','Response Time','Turnaround Time']]


color_board = ['#AEA2C5','#BBDF32','#00504B','#F83FA0','#5d5c61','#7395ae','#557a95','#64495c','#3500d4','#950741','#c3083f','#e7717d','#c2c9cf','#afd275','#66fcf1','#c5c6c8','#46a29f','#f13c10','#106466','#ff652f','#ffe401','#13a76c','#8265a7','#65ccb8','#a4a61e']
name = [1,3,5]
arrival = [2,4,6]
burst = [3,5,7]
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
print(SJF(df)) 