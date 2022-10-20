import streamlit as st
import pandas as pd
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("Style.css")
st.title('CPU SCHEDULING')
st.image('https://computersales.ir/wp-content/uploads/i9-11900KB.jpg')
st.selectbox('Scheduling Algorithim',('Shorted Job First', 'Shorted Remaining Time First', 'Round Robin'), key='SA')
st.header("Nhập danh sách")
form = st.form("my_form",clear_on_submit=True)
with form.container():
    ProcessName, ArrivalTime, BurstTime = st.columns((1,1,1))
    with ProcessName:
        name = st.text_input('Process Name',placeholder='P1')
    with ArrivalTime:
        arrival = st.text_input('Arrival Time',placeholder='0')
    with BurstTime:
        burst = st.text_input('Burst Time',placeholder='10')
    if "count" not in st.session_state:
        st.session_state.count = 0
    add = form.form_submit_button("Add process")
    if add:
        st.session_state.count += 1
        st.session_state['member' + str(st.session_state.count)] = [name,arrival,burst]
members = []
for i in range(1,st.session_state.count+1):
    members.append(st.session_state['member'+str(i)])
df = pd.DataFrame(data=members,columns=['Process Name','Arrival Time','Burst Time'],index= (i for i in range(1,st.session_state.count+1)))
if st.session_state.count != 0:
    st.subheader("List Process")
    st.table(df)
buttonDone, down, emp = st.columns((2,2,6))
buttonDone.button("Caculate",key="Caculate")
if st.session_state.Caculate:
    df.to_excel("Data.xlsx",index=False)
    with open("Data.xlsx", "rb") as fileData:
        down.download_button("Tải file .xlsx dùng cho năm sau",data=fileData,file_name="Danh_Sach.xlsx", key="downData")