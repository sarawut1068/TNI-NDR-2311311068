# project_494
pip install streamlit

# open streamlit
python -m streamlit run main.py

# ALL liberries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import matplotlib
import streamlit as st
from PIL import Image
import os #for opening png -> # os.system("start DELTA_Graph.png") 
import matplotlib.dates as mdates 

# Setting Column
df.columns = [
    "วันที่", "ราคาเปิด", "ราคาสูงสุด", "ราคาต่ำสุด", "ราคาเฉลี่ย", "ราคาปิด",
    "เปลี่ยนแปลง", "เปลี่ยนแปลง(%)", "ปริมาณ(พันหุ้น)", "มูลค่า(ล้านบาท)",
    "SET Index", "SET เปลี่ยนแปลง(%)"
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

df = df[~df["วันที่"].isna()]
df = df[~df["วันที่"].astype(str).str.contains("วันที่")]


df["วันที่"] = df["วันที่"].apply(convert_thai_date)
df = df.dropna(subset=["วันที่"])
df["วันที่"] = pd.to_datetime(df["วันที่"], errors='coerce')
df = df.dropna(subset=["วันที่"])

# show month in termianl
print(df.head(10))


# Building and Setting Graph
df_sorted = df.sort_values("วันที่")
X = df_sorted["วันที่"].map(pd.Timestamp.toordinal).values.reshape(-1, 1)
y = df_sorted["ราคาปิด"].values

model = LinearRegression()
model.fit(X, y)
trend = model.predict(X)

plt.figure(figsize=(12, 6))
plt.plot(df_sorted["วันที่"], y, label="Actual Closing Price")
plt.plot(df_sorted["วันที่"], trend, label="Trend (Linear Regression)", linestyle="--", color="red")
plt.title("DELTA Closing Price Trend")
plt.xlabel("Date")
plt.ylabel("Closing Price (Baht)")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("AAV_Graph.png")
plt.close()
img = Image.open("AAV_Graph.png")

# open in streamlit grph
st.image(img, caption="graph",use_container_width=True)
