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
    color_board = ['#5d5c61','#7395ae','#557a95','#64495c','#3500d4','#950741','#c3083f','#e7717d','#c2c9cf','#afd275','#66fcf1','#c5c6c8','#46a29f','#f13c10','#d79922','#106466','#ff652f','#272727','#ffe401','#13a76c','#8265a7','#65ccb8','#a4a61e']
    name = name.split()
    arrival = arrival.split()
    burst = burst.split()
    if name == []:
      name = ['P'+str(i+1) for i in range(len(arrival))]
    colors = [random.choice(color_board) for i in range(3)]
    df = pd.DataFrame({'Color Code': colors,
                    'Process Name': name,
                     'Arrival Time': arrival,
                     'Burst Time': burst})
    sorted_df = df.sort_values(by='Arrival Time', ignore_index=True)
    return sorted_df

@st.cache(allow_output_mutation=True)
def SJF(df):
    df = df.reindex(columns=['Color Code','Process Name','Arrival Time','Burst Time','Start','End'],fill_value = 10000)
    row0 = df.loc[0].copy()
    row0['Start'] = row0['Arrival Time']
    row0['End'] = row0['Burst Time'] + row0['Start']
    df.loc[0] = row0
    ran_out_process = False
    waitting = False
    for i in range(1,df.shape[0]):
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
            if(arrival_time == pre_end): 
                if(count == 1): waitting = True
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
    return df

def SRTF():
    pass

def RR():
    pass

st.title('CPU SCHEDULING')
st.image('https://computersales.ir/wp-content/uploads/i9-11900KB.jpg')
st.selectbox('Scheduling Algorithim',('Shorted Job First', 'Shorted Remaining Time First', 'Round Robin'), key='SA')
st.header("Enter List Process")
form = st.form("my_form",clear_on_submit=True)
with form.container():
    ProcessName, ArrivalTime, BurstTime = st.columns((1,1,1))
    with ProcessName:
        name = st.text_input('Process Name(not required)',placeholder='P1 P2 P3')
    with ArrivalTime:
        arrival = st.text_input('Arrival Time',placeholder='0 1 2')
    with BurstTime:
        burst = st.text_input('Burst Time',placeholder='10 20 30')
    form.form_submit_button("Caculate")
    if 'submitted' not in st.session_state:
      st.session_state.submitted = False

if st.session_state['FormSubmitter:my_form-Caculate'] or st.session_state.submitted:
  st.session_state.submitted = True
  df = CreateDataFrame(name,arrival,burst)
  df['Arrival Time'] = [formatNumber(float(i)) for i in df['Arrival Time']]
  df['Burst Time'] = [formatNumber(float(i)) for i in df['Burst Time']]
  if st.session_state["SA"] == "Shorted Job First":
    df = SJF(df)
  elif st.session_state["SA"] == "Shorted Remaining Time First":
    df = SRTF(df)
  elif st.session_state["SA"] == "Round Robin":
    df = SRTF(df)

  show_list = df.astype(str)
  st.subheader("List Process")
  st.table(show_list)
  total = df.loc[df.shape[0]-1]['End'] - df.loc[0]['Start']
  df['Timeline'] = (df['End'] - df['Start'])/total * 100
#   st.table(df)
  timelines = [i for i in df['Timeline']]
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
  gantt += timeline.format(row0['Timeline'],0,row0['Color Code'],1,row0['Process Name'],row0['Start'],row0['End'])
  pos = 0
  for i in range(1,df.shape[0]):
    tuple_i = df.loc[i]
    pos += df.loc[i-1]['Timeline']
    gantt += timeline.format(tuple_i['Timeline'],pos,tuple_i['Color Code'],pos+1,tuple_i['Process Name'],tuple_i['Start'],tuple_i['End'])

  st.markdown(gantt+tail, unsafe_allow_html=True)
  # for key in st.session_state.keys():
  #     del st.session_state[key]