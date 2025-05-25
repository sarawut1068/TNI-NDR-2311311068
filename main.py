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

st.title("Asia Aviation Public Company Limited(AAV)")
st.write("Graph of AAV(ย้อนหลัง 6 เดือน)")


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
df = df[~df["Date"].astype(str).str.contains("วันที่")]


df["Date"] = df["Date"].apply(convert_thai_date)
df = df.dropna(subset=["Date"])
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
df = df.dropna(subset=["Date"])

# ----- End of dealing with months ----- #
# show month in termianl
print(df.head(10))

# ----- Start working with Graph ----- #
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
plt.title("DELTA Closing Price Trend")
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

# looping through month in option (ย้อนหลัง 6 เดือน)
month_options = ["All"] + [f"{month:02d}" for month in months]

# select box for selecting month
selected_month = st.selectbox("Selectin month", month_options)

# filtering data by choice selected
if selected_month != "All":
    # if choice != ทั้งหมด then choice = selected int month (converted into number already)
    filtered_df = df[df["month"] == int(selected_month)]
else:
    # copy all data (choice = ทั้งหมด) || สร้างสําเนา dataframe โดยไม่ให้เกิดการเปลี่ยนเเปลงตาม choice 
    filtered_df = df.copy()

# filtering to show only date (without showing time)
filtered_df["Date"] = filtered_df["Date"].dt.date

# filtering index starting from 1 to n
filtered_df.index = range(1, len(filtered_df) + 1)

# displaying filtered data  
st.dataframe(filtered_df)

if "show_graph" not in st.session_state:
    st.session_state.show_graph = False 
if st.button("show/hide"):
    st.session_state.show_graph = not st.session_state.show_graph

if st.session_state.show_graph:
    st.image(img, caption="",use_container_width=True)