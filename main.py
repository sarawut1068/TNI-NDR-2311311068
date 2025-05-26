# Importing Libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import matplotlib
import streamlit as st  
from PIL import Image
import os #for opening png -> # os.system("start DELTA_Graph.png") 
import matplotlib.dates as mdates

st.markdown("<h1 style='text-align: center;'>Asia Aviation Public Company Limited (AAV)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>บริษัท เอเชีย เอวิเอชั่น จำกัด (มหาชน)</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>ข้อมูลย้อนหลัง 6 เดือน</p>", unsafe_allow_html=True)


df = pd.read_excel("AAV.xlsx", sheet_name="AAV", skiprows=1)

# Setting Column names
df.columns = [
    "Date", "Opening_price", "Highest_price", "Lowest_price", "Average_price", "Closing_price",
    "change", "change_(%)", "Volume_('000 shares)", "Value_(million baht)",
    "SET_Index", "change _(%)"
]

# Converting Months
thai_months = {
    "ม.ค.": "01", "ก.พ.": "02", "มี.ค.": "03", "เม.ย.": "04",
    "พ.ค.": "05", "มิ.ย.": "06", "ก.ค.": "07", "ส.ค.": "08",
    "ก.ย.": "09", "ต.ค.": "10", "พ.ย.": "11", "ธ.ค.": "12"
}

# Converting thai dates into global dates
def convert_thai_date(thai_date_str):
    for th, num in thai_months.items():
        if th in thai_date_str:
            day, month_th, year_th = thai_date_str.replace(",", "").split()
            month = thai_months[month_th]
            year = int(year_th) - 543
            return f"{year}-{month}-{int(day):02d}"
    return None


df = df[~df["Date"].isna()]
df = df[~df["Date"].astype(str).str.contains("date")]


df["Date"] = df["Date"].apply(convert_thai_date)
df = df.dropna(subset=["Date"])
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
df = df.dropna(subset=["Date"])


# show month in termianl
print(df.head(10))
 
# Building and Setting Graph
df_sorted = df.sort_values("Date")
X = df_sorted["Date"].map(pd.Timestamp.toordinal).values.reshape(-1, 1)
y = df_sorted["Closing_price"].values

model = LinearRegression()
model.fit(X, y)
trend = model.predict(X)

plt.figure(figsize=(12, 6))
plt.plot(df_sorted["Date"], y, label="Actual Closing Price")
plt.plot(df_sorted["Date"], trend, label="Trend (Linear Regression)", linestyle="--", color="red")
plt.title("AAV Closing Price Trend")
plt.xlabel("Date")
plt.ylabel("Closing Price (Baht)")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("AAV_Graph.png")
plt.close()
img = Image.open("AAV_Graph.png")

# month,year column 
df["month"] = df["Date"].dt.month
df["years"] = df["Date"].dt.year

# month choices
months = df["month"].unique()
months.sort()

# looping through month in option 
month_options = ["All"] + [f"{month:02d}" for month in months]

# select box for selecting month
selected_month = st.selectbox("Select month", month_options)

# filtering data by choice selected
if selected_month != "All":
    filtered_df = df[df["month"] == int(selected_month)]
else:
    filtered_df = df.copy()

# filtering to show only date (without showing time)
filtered_df["Date"] = filtered_df["Date"].dt.date

# filtering index starting from 1 to n
filtered_df.index = range(1, len(filtered_df) + 1)

# displaying filtered data  
st.dataframe(filtered_df)


if "show_graph" not in st.session_state:
    st.session_state.show_graph = False 
if st.button("Click to open/hide"):
    st.session_state.show_graph = not st.session_state.show_graph

if st.session_state.show_graph:
    st.image(img, caption="",use_container_width=True)

st.sidebar.markdown("<h1 style='text-align: center;'>ข้อมูลบริษัท(AAV)</h1>", unsafe_allow_html=True)
st.sidebar.markdown("""
**ตลาด:** SET  
**วันที่เริ่มต้นซื้อขาย:** 31 พ.ค. 2555  
**กลุ่มอุตสาหกรรม:** บริการ  
**หมวดธุรกิจ:** ขนส่งและโลจิสติกส์  
**ข้อจำกัดการถือหุ้นต่างด้าว:** 0.10% (ณ วันที่ 23 พ.ค. 2568)  
**Free Float:** 36.17%  
**ราคาพาร์:** 0.10 บาท  
**เลขรหัสหลักทรัพย์สากล:**  
- ในประเทศ: TH3437010004  
- ต่างด้าว: TH3437010012  
- NVDR: TH3437010R19  
""")

st.sidebar.markdown("### นโยบายการจ่ายปันผล")
st.sidebar.markdown("""
จ่ายเงินปันผลโดยคำนึงถึงผลการดำเนินงาน สภาพคล่อง กระแสเงินสด และสถานะทางการเงิน  
ของบริษัทฯ เงื่อนไขและข้อจำกัดในการจ่ายเงินปันผลตามที่กำหนดไว้ใน  
สัญญาเงินกู้ หุ้นกู้ หรือสัญญาต่าง ๆ ที่เกี่ยวข้อง
""")

st.sidebar.markdown("### วันปิดรอบบัญชี")
st.sidebar.markdown("31 ธันวาคม ของทุกปี")

st.sidebar.markdown("### ผู้สอบบัญชี (สิ้นสุด 31 ธ.ค. 2568)")
st.sidebar.markdown("""
1. นาย นรินทร์ จูระมงคล  
2. นาย ธีรศักดิ์ ฉั่วศรีสกุล  
3. นาย ไกรแสง ธีรนุลักษณ์  
(**บริษัท บีดีโอ ออดิท จำกัด**)
""")

st.sidebar.markdown("### ผู้บริหารสายบัญชีและการเงิน")
st.sidebar.markdown("""
**นาย ไพรัชล์ พรพัฒนนางกูร**  
(เริ่มต้น 31 ม.ค. 2563)
""")

st.sidebar.markdown("### ผู้ควบคุมการทำบัญชี")
st.sidebar.markdown("""
**นางสาว นวพร คำนิล**  
(เริ่มต้น 1 ส.ค. 2566)
""")

st.sidebar.title("รายละเอียดเกี่ยวกับทุน")

# แสดงข้อมูลใน Sidebar
st.sidebar.markdown("**หุ้นสามัญ**")
st.sidebar.markdown(f"- ทุนจดทะเบียน (บาท): **1,285,000,000.00**")
st.sidebar.markdown(f"- ทุนจดทะเบียนชำระแล้ว (บาท): **1,284,999,999.70**")

st.sidebar.markdown("### หุ้นและทุนจดทะเบียน")
st.sidebar.markdown("""
**หุ้นบุริมสิทธิ:**  
**ทุนจดทะเบียน:**  
**ทุนจดทะเบียนชำระแล้ว:** 
""")

st.sidebar.markdown("### รายละเอียดเกี่ยวกับจำนวนหุ้น")

st.sidebar.markdown("**หุ้นสามัญ**")
st.sidebar.markdown("""
- จำนวนหุ้นจดทะเบียนกับตลาดหลักทรัพย์ฯ: 12,849,999,997  
- จำนวนหุ้นชำระแล้ว: 12,849,999,997  
- สิทธิออกเสียง: 1 : 1  
- จำนวนหุ้นซื้อคืน
- จำนวนหุ้นที่มีสิทธิออกเสียง (หักหุ้นซื้อคืน):  
  - ณ วันที่ 26 พ.ค. 2568: 12,849,999,997  
  - ณ วันที่ 30 เม.ย. 2568: 12,849,999,997  
""")

st.sidebar.markdown("**หุ้นบุริมสิทธิ**")
st.sidebar.markdown("""
- จำนวนหุ้นจดทะเบียนกับตลาดหลักทรัพย์ฯ:   
- จำนวนหุ้นชำระแล้ว
- จำนวนหุ้นซื้อคืน
- จำนวนหุ้นที่มีสิทธิออกเสียง (หักหุ้นซื้อคืน)
""")