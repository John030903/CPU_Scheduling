import pandas as pd
import random

def RR(df,quantum_time):
    queue = [0]
    print("Len truoc",len(queue))
    execute_time = df.at[0,'Arrival Time']
    pre_execute_time = df.at[0,'Arrival Time']
    index = 0
    len_dataframe = df.shape[0]
    added_process_list = [0]
    while(True):
        if(df.at[index,'Burst Time'] < quantum_time):
            execute_time += df.at[index,'Burst Time']
        else:
            execute_time += quantum_time
        pos = 1
        while(pos != len_dataframe and df.at[pos,'Arrival Time'] <= execute_time and len(added_process_list) < len_dataframe):
            if(pos not in added_process_list):
                if execute_time == 1:
                    print("Có thêm process 1")
                queue.append(pos)
                added_process_list.append(pos)
            pos += 1
        start = pre_execute_time
        df.at[index,'Start'] = start
        executed_time = execute_time - start 
        df.at[index,'End'] = start + executed_time
        if(executed_time < df.at[index,'Burst Time']):
            remaining_time = df.at[index,'Burst Time'] - executed_time
            df.at[index,'Remain Time'] = remaining_time
            df = pd.concat([df, df.loc[index]], ignore_index=True)

            df.at[df.shape[0]-1,'Burst Time'] = remaining_time
            queue.append(df.shape[0]-1)
        print("Len",len(queue))
        queue.pop(0)
        if(len(queue) == 0): break
        index = queue[0]
        pre_execute_time = execute_time
    sorted_df = df.loc[:,['Color Code','Process Name','Arrival Time','Burst Time','Start','End']].sort_values(by='Start', ignore_index=True)
    return sorted_df

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
                 'Remain Time':10000})
print(RR(df,2))