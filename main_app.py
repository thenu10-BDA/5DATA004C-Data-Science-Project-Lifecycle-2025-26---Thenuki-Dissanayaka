import streamlit as st
import pandas as pd

st.set_page_config(page_title="LPI Dashboard", layout="wide")

df = pd.read_csv("cleaned_LPI_data.csv")

df["LPI_Score"] = df["LPI_Score"] / 100

st.title("Logistics Performance Dashboard")

st.write("This dashboard explores Logistics Performance Index scores across countries and years.")

st.subheader("Dataset Preview")
st.write(df.head())

year = st.selectbox("Select Year", sorted(df["Year"].unique()))

filtered_df = df[df["Year"] == year]

st.subheader(f"Top 10 Countries by LPI Score in {year}")

top10 = filtered_df.sort_values(by="LPI_Score", ascending=False).head(10)
st.bar_chart(top10.set_index("Country")["LPI_Score"])

st.subheader("Compare Countries Over Time")

countries = st.multiselect(
    "Select Countries",
    sorted(df["Country"].unique()),
    default=["Germany", "Singapore", "Sri Lanka"]
)

if countries:
    compare_df = df[df["Country"].isin(countries)]
    
    chart_df = compare_df.pivot_table(
    index="Year",
    columns="Country",
    values="LPI_Score",
    aggfunc="mean"
)
    st.line_chart(chart_df)

st.subheader("Average LPI Score Over Time")

trend_df = df.groupby("Year")["LPI_Score"].mean()
st.line_chart(trend_df)

st.subheader("Key Insights")

top_country = filtered_df.sort_values(by="LPI_Score", ascending=False).iloc[0]
avg_score = filtered_df["LPI_Score"].mean()

st.write(f"Top performing country in {year}: **{top_country['Country']}** with score **{top_country['LPI_Score']:.2f}**")
st.write(f"Average LPI score in {year}: **{avg_score:.2f}**")
