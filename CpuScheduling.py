import streamlit as st
import pandas as pd
import random
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("Style.css")

def formatNumber(num):
    if num == int(num): 
        return int(num)
    if num % 1 == 0:
        return int(num)
    else:
        return num

@st.cache(allow_output_mutation=True)
def CreateDataFrame(name,arrival,burst):
    color_board = ['#AEA2C5','#BBDF32','#00504B','#F83FA0','#5d5c61','#7395ae','#557a95','#64495c','#3500d4','#950741','#c3083f','#e7717d','#c2c9cf','#afd275','#66fcf1','#c5c6c8','#46a29f','#f13c10','#106466','#ff652f','#ffe401','#13a76c','#8265a7','#65ccb8','#a4a61e']
    name = name.split()
    arrival = arrival.split()
    burst = burst.split()
    if name == []:
      name = ['P'+str(i+1) for i in range(len(arrival))]
    colors = [random.choice(color_board) for i in range(len(arrival))]
    df = pd.DataFrame({'Color Code': colors,
                    'Process Name': name,
                     'Arrival Time': arrival,
                     'Burst Time': burst,
                     'Start':10000,
                     'End':10000})
    df['Arrival Time'] = [formatNumber(float(i)) for i in df['Arrival Time']]
    df['Burst Time'] = [formatNumber(float(i)) for i in df['Burst Time']]
    df['Remain Time'] = df['Burst Time']
    sorted_df = df.sort_values(by='Arrival Time', ignore_index=True)
    return sorted_df

@st.cache(allow_output_mutation=True)
def SJF(df):
    row0 = df.loc[0].copy()
    row0['Start'] = row0['Arrival Time']
    row0['End'] = row0['Burst Time'] + row0['Start']
    df.loc[0] = row0
    ran_out_process = False
    for i in range(1,df.shape[0]):
        waitting = False
        pre_end = df.loc[i-1]['End']
        pos = i
        count = 0
        while True:
            count += 1
            if(pos < df.shape[0]):
                arrival_time = df.loc[pos]['Arrival Time']
            else: 
                ran_out_process = True
            if(ran_out_process): 
                pos -= 1
                break
            if(arrival_time > pre_end): 
                if (count != 1):
                    pos -= 1
                if(count == 1):
                    waitting = True
                break
            pos += 1
        if ran_out_process:
            pos_min_BurstTime = df.loc[i:]['Burst Time'].idxmin()
        else:
            pos_min_BurstTime = df.loc[i:pos]['Burst Time'].idxmin()
        row_min_BT = df.loc[pos_min_BurstTime].copy()
        if waitting:
            row_min_BT['Start'] = row_min_BT['Arrival Time']
            row_min_BT['End'] = row_min_BT['Start'] + row_min_BT['Burst Time']
        else:
            row_min_BT['Start'] = pre_end
            row_min_BT['End'] = row_min_BT['Start'] + row_min_BT['Burst Time']
        df.loc[pos_min_BurstTime] = row_min_BT
        df = df.sort_values(by="Start", ignore_index=True)
    return df.loc[:,['Color Code','Process Name','Arrival Time','Burst Time','Start','End']]

@st.cache(allow_output_mutation=True)
def SRTF(df):
    execute_time = df.at[0,'Arrival Time']
    executed_time = 0
    pre_execute_time = df.at[0,'Arrival Time']
    index_min = 0
    len_dataframe = df.shape[0]
    indexes_ready = [0]
    process_ready = pd.DataFrame()
    finished_processes = []
    finish_adding = False
    pre_index_min = 0
    compared_index = 1
    again = False
    watting_new_process = False
    while(True):        
        if(watting_new_process):
            execute_time += df.at[index_min,'Remain Time']
        else:
            if (not again):
                if(df.at[compared_index,'Arrival Time'] < df.at[index_min,'Burst Time'] + execute_time):
                    execute_time = df.at[compared_index,'Arrival Time']
                    watting_new_process = False
                else:
                        execute_time += df.at[index_min,'Burst Time']                        
                        watting_new_process = True
            else:                
                if (not finish_adding):
                    if(df.at[compared_index,'Arrival Time'] < df.at[index_min,'Remain Time'] + execute_time):
                        execute_time = df.at[compared_index,'Arrival Time']
                        watting_new_process = False
                else:
                    execute_time += df.at[index_min,'Remain Time']                    
                    watting_new_process = True

                
        pos = 1
        while(not finish_adding):            
            if len(indexes_ready) == len_dataframe or pos == len_dataframe:                
                finish_adding = True
                break
            if df.at[pos,'Arrival Time'] > execute_time:
                break
            if(len(indexes_ready)-1 < pos):
                indexes_ready.append(pos)
            pos += 1        
        start = pre_execute_time
        executed_time = execute_time - start         
        if(not again):
            df.at[index_min,'Start'] = start
            df.at[index_min,'End'] = start + executed_time
        else:
            df.at[index_min,'End'] += executed_time
        if(executed_time <= df.at[index_min,'Burst Time']):
            if not again:
                remaining_time = df.at[index_min,'Burst Time'] - executed_time
            else:
                remaining_time = df.at[index_min,'Remain Time'] - executed_time
            df.at[index_min,'Remain Time'] = remaining_time
            if (remaining_time == 0):
                finished_processes.append(index_min)
        if (len(finished_processes) != len_dataframe):            
            process_ready = df.iloc[[i for i in indexes_ready if i not in finished_processes],:]            
            pre_index_min = index_min            
            index_min = process_ready['Remain Time'].idxmin()
            if index_min == pre_index_min:
                compared_index += 1
                again = True
            else:
                again = False
                compared_index = index_min + 1
                if(remaining_time != 0):
                    df = df.append(df.loc[pre_index_min], ignore_index = True)
                    indexes_ready[pre_index_min] = df.shape[0]-1
                    df.at[df.shape[0]-1,'Burst Time'] = remaining_time
            
            pre_execute_time = execute_time
        else:
            break            
    sorted_df = df.loc[:,['Color Code','Process Name','Arrival Time','Burst Time','Start','End']].sort_values(by='Start', ignore_index=True)
    return sorted_df

@st.cache(allow_output_mutation=True)
def RR(df,quantum_time):
    queue = [0]
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
        pos = 0
        while(pos != len_dataframe and df.at[pos,'Arrival Time'] <= execute_time and len(added_process_list) < len_dataframe):
            if(pos not in added_process_list):
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
            df = df.append(df.loc[index], ignore_index = True)
            df.at[df.shape[0]-1,'Burst Time'] = remaining_time
            queue.append(df.shape[0]-1)
        queue.pop(0)
        if(len(queue) == 0): break
        index = queue[0]
        pre_execute_time = execute_time
    sorted_df = df.loc[:,['Color Code','Process Name','Arrival Time','Burst Time','Start','End']].sort_values(by='Start', ignore_index=True)
    return sorted_df

def GraphTimeline(df):
    total = df.loc[df.shape[0]-1]['End'] - df.loc[0]['Start']
    df['Width'] = (df['End'] - df['Start'])/total * 100
    # Widths = [i for i in df['Width']]
    gantt = '<svg id="hsbar" width="100%" height="40">'
    tail = '</svg>'
    timeline = '''  
    <g>
      <rect
        width="{0}%"
        height="40"
        x="{1}%"
        style="fill: {2}; stroke-width: 0%; stroke: black"
      ></rect>
      <text
        x="{3}%"
        y="50%"
        dy="0.35em"
        style="fill: white; font-size: 90%"
      >
        {4}
      </text>
      <title>{4}: Start: {5} End: {6} </title>
    </g>'''
    row0 = df.loc[0]
    gantt += timeline.format(row0['Width'],0,row0['Color Code'],1,row0['Process Name'],row0['Start'],row0['End'])
    pos = 0
    for i in range(1,df.shape[0]):
      tuple_i = df.loc[i]
      tuple_pre_i = df.loc[i-1]
      start_i = tuple_i['Start']
      end_pre_i = tuple_pre_i['End']
      if(end_pre_i != start_i):
        pos += (start_i - end_pre_i)/total * 100
      pos += tuple_pre_i['Width']
      gantt += timeline.format(tuple_i['Width'],pos,tuple_i['Color Code'],pos+1,tuple_i['Process Name'],start_i,tuple_i['End'])
    gantt += tail
    return gantt

st.title('CPU SCHEDULING')
st.image('https://computersales.ir/wp-content/uploads/i9-11900KB.jpg')
st.selectbox('Scheduling Algorithim',('Shorted Job First', 'Shorted Remaining Time First', 'Round Robin'), key='SA')
st.header("Enter List Process")
form = st.form("my_form")
with form.container():
    ProcessName, ArrivalTime, BurstTime = st.columns((1,1,1))
    with ProcessName:
        name = st.text_input('Process Name(not required)',placeholder='P1 P2 P3')
    with ArrivalTime:
        arrival = st.text_input('Arrival Time',placeholder='0 1 2')
    with BurstTime:
        burst = st.text_input('Burst Time',placeholder='10 20 30')
    form.form_submit_button("Caculate")
    if(st.session_state["SA"] == "Round Robin"):
        _,  quantum_time, _ = st.columns((3,1,3))
        with quantum_time:
            quantum = st.text_input('Quantum Time',placeholder='2',key='QuantumTime')
    if 'submitted' not in st.session_state:
      st.session_state.submitted = False
if st.session_state['FormSubmitter:my_form-Caculate'] or st.session_state.submitted:
    st.session_state.submitted = True
    df = CreateDataFrame(name,arrival,burst)
    show_list = df.loc[:,['Process Name','Arrival Time','Burst Time']].astype(str)
    st.subheader("List Process")
    st.table(show_list)
    if st.session_state["SA"] == "Shorted Job First":
      df = SJF(df)
    elif st.session_state["SA"] == "Shorted Remaining Time First":
      df = SRTF(df)
    elif st.session_state["SA"] == "Round Robin":
      if st.session_state.QuantumTime != '':
        df = RR(df,int(st.session_state.QuantumTime))

    if st.session_state["SA"] != "Round Robin":
        st.markdown(GraphTimeline(df), unsafe_allow_html=True)
    else:
        if st.session_state.QuantumTime != '':
            st.markdown(GraphTimeline(df), unsafe_allow_html=True)
