import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)


# ---------------- CSS ----------------
st.markdown("""
<style>
.main{
    background-color:#F4F6F8;
}
h1{
    color:#1E88E5;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)


st.title("🎓 Student Performance Analytics Dashboard")


st.write("Analyze student performance using interactive filters and charts.")


# ---------------- LOAD DATA ----------------


current_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(current_dir, "student_performance.csv")


try:
    df = pd.read_csv(csv_file)
except Exception as e:
    st.error(f"Error loading CSV file:\n{e}")
    st.stop()


# ---------------- SIDEBAR ----------------


st.sidebar.header("Filters")


department = st.sidebar.multiselect(
    "Department",
    options=df["Department"].unique(),
    default=df["Department"].unique()
)


semester = st.sidebar.multiselect(
    "Semester",
    options=sorted(df["Semester"].unique()),
    default=sorted(df["Semester"].unique())
)


attendance = st.sidebar.slider(
    "Attendance",
    int(df["Attendance"].min()),
    int(df["Attendance"].max()),
    (
        int(df["Attendance"].min()),
        int(df["Attendance"].max())
    )
)


filtered_df = df[
    (df["Department"].isin(department)) &
    (df["Semester"].isin(semester)) &
    (df["Attendance"] >= attendance[0]) &
    (df["Attendance"] <= attendance[1])
]


# ---------------- TABLE ----------------


st.subheader("Filtered Student Data")


st.dataframe(filtered_df, use_container_width=True)


# ---------------- SUMMARY ----------------


st.subheader("Summary Statistics")


st.write(filtered_df.describe())


# ---------------- BAR CHART ----------------


st.subheader("Average Marks by Department")


avg = filtered_df.groupby("Department")["Marks"].mean()


fig, ax = plt.subplots()


avg.plot(kind="bar", ax=ax)


ax.set_ylabel("Average Marks")


st.pyplot(fig)


# ---------------- PIE CHART ----------------


st.subheader("Semester Distribution")


fig, ax = plt.subplots()


filtered_df["Semester"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    ax=ax
)


ax.set_ylabel("")


st.pyplot(fig)


# ---------------- HISTOGRAM ----------------


st.subheader("Marks Distribution")


fig, ax = plt.subplots()


ax.hist(filtered_df["Marks"], bins=10)


ax.set_xlabel("Marks")


ax.set_ylabel("Students")


st.pyplot(fig)


# ---------------- SCATTER ----------------


st.subheader("Attendance vs Marks")


fig, ax = plt.subplots()


ax.scatter(
    filtered_df["Attendance"],
    filtered_df["Marks"]
)


ax.set_xlabel("Attendance")


ax.set_ylabel("Marks")


st.pyplot(fig)


# ---------------- DOWNLOAD ----------------


csv = filtered_df.to_csv(index=False).encode("utf-8")


st.download_button(
    "Download Filtered Data",
    csv,
    "filtered_students.csv",
    "text/csv"
)


st.success("Dashboard Loaded Successfully!")
