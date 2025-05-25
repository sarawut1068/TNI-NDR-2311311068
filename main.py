
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

st.title("AAV.graph")


df = pd.read_excel("AAV.xlsx", sheet_name="AAV", skiprows=1)

# Setting Column names
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

# ----- End of dealing with months ----- #
# show month in termianl
print(df.head(10))

# ----- Start working with Graph ----- #
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


st.image(img, caption="graph",use_container_width=True)


# month,year column 
df["เดือน"] = df["วันที่"].dt.month
df["ปี"] = df["วันที่"].dt.year

# month choices
months = df["เดือน"].unique()
months.sort()

# looping through month in option (ย้อนหลัง 6 เดือน)
month_options = ["ทั้งหมด"] + [f"{month:02d}" for month in months]

# select box for selecting month
selected_month = st.selectbox("เลือกเดือน", month_options)

# filtering data by choice selected
if selected_month != "ทั้งหมด":
    # if choice != ทั้งหมด then choice = selected int month (converted into number already)
    filtered_df = df[df["เดือน"] == int(selected_month)]
else:
    # copy all data (choice = ทั้งหมด) || สร้างสําเนา dataframe โดยไม่ให้เกิดการเปลี่ยนเเปลงตาม choice 
    filtered_df = df.copy()

# filtering to show only date (without showing time)
filtered_df["วันที่"] = filtered_df["วันที่"].dt.date

# filtering index starting from 1 to n
filtered_df.index = range(1, len(filtered_df) + 1)

# displaying filtered data
st.dataframe(filtered_df)



