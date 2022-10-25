# from platform import architecture
# import pandas as pd
# import numpy as np

# def SJF(df):
#     df = df.reindex(columns=['Process Name','Arrival Time','Burst Time','Start','End'],fill_value = 10000)
#     row0 = df.loc[0].copy()
#     row0['Start'] = row0['Arrival Time']
#     row0['End'] = row0['Burst Time'] + row0['Start']
#     df.loc[0] = row0
#     ran_out_process = False
#     waitting = False
#     for i in range(1,df.shape[0]):
#         pre_end = df.loc[i-1]['End']
#         pos = i
#         count = 0
#         while True:
#             count += 1
#             if(pos < df.shape[0]):
#                 arrival_time = df.loc[pos]['Arrival Time']
#             else: 
#                 ran_out_process = True
#             if(ran_out_process): 
#                 pos -= 1
#                 break
#             if(arrival_time == pre_end): 
#                 if(count == 1): waitting = True
#                 break
#             if(arrival_time > pre_end): 
#                 if (count != 1):
#                     pos -= 1
#                 if(count == 1):
#                     waitting = True
#                 break
#             pos += 1
#         if ran_out_process:
#             pos_min_BurstTime = df.loc[i:]['Burst Time'].idxmin()
#         else:
#             pos_min_BurstTime = df.loc[i:pos]['Burst Time'].idxmin()
#         row_min_BT = df.loc[pos_min_BurstTime].copy()
#         if waitting:
#             row_min_BT['Start'] = row_min_BT['Arrival Time']
#             row_min_BT['End'] = row_min_BT['Start'] + row_min_BT['Burst Time']
#         else:
#             row_min_BT['Start'] = pre_end
#             row_min_BT['End'] = row_min_BT['Start'] + row_min_BT['Burst Time']
#         df.loc[pos_min_BurstTime] = row_min_BT
#         df = df.sort_values(by="Start", ignore_index=True)
#     return df

# arrival = [1, 2, 7, 15]
# name = [3, 4, 5, 8]
# burst = [15, 1 ,3, 2]
# total = 10
# df = pd.DataFrame({'Process Name': name,
#                    'Arrival Time': arrival,
#                    'Burst Time': burst})
# df['Timeline'] = (df['Burst Time'] - df['Arrival Time'])/total * 100
# timeline = """<g>
#     <rect
#       width="{width}%"
#       height="40"
#       x="{pos}%"
#       style="fill: rgb(122, 184, 0); stroke-width: 0%; stroke: black"
#     ></rect>
#     <text
#       x="{text_pos}%"
#       y="50%"
#       dy="0.35em"
#       style="fill: white; font-size: 90%"
#     >
#       {name}
#     </text>
#     <title>{name}: Start: {start} End: {end} </title>
#   </g>"""
# print(timeline.format(width=0,pos=0,text_pos=0,name=0,start=0,end=10))

str = ''
print(str.split())
if str.split() == []: print('Ngon lành')