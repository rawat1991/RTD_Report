import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_bar_chart(df):
    """Create department distribution bar chart"""
    dept_counts = df['Department'].value_counts()
    fig = px.bar(
        x=dept_counts.index,
        y=dept_counts.values,
        title="Employee Distribution by Department",
        labels={'x': 'Department', 'y': 'Number of Employees'}
    )
    return fig

def create_line_chart(df):
    """Create salary trends line chart"""
    dept_avg_salary = df.groupby('Department')['Salary'].mean().reset_index()
    fig = px.line(
        dept_avg_salary,
        x='Department',
        y='Salary',
        title="Average Salary by Department",
        markers=True
    )
    return fig

def create_daily_report_chart(df):
    """Create daily hours distribution chart"""
    daily_hours = df.groupby(["Date", "Employee"])["Hours"].sum().reset_index()
    fig = px.bar(
        daily_hours,
        x="Date",
        y="Hours",
        color="Employee",
        title="Daily Hours by Employee",
        labels={"Date": "Date", "Hours": "Hours Worked"}
    )
    return fig

def create_task_distribution_chart(df):
    """Create task type distribution chart"""
    task_dist = df.groupby("TaskType")["Hours"].sum().reset_index()
    fig = px.pie(
        task_dist,
        values="Hours",
        names="TaskType",
        title="Distribution of Time Across Task Types"
    )
    return fig

def create_daily_production_chart(df):
    """Create daily production overview chart"""
    daily_prod = df.groupby(["Date", "VariantName"])[["TotalCase", "LooseCans"]].sum().reset_index()
    fig = px.bar(
        daily_prod,
        x="Date",
        y="TotalCase",
        color="VariantName",
        title="Daily Production by Variant",
        labels={"Date": "Date", "TotalCase": "Total Cases"}
    )
    return fig

def create_rejection_summary_chart(df):
    """Create rejection analysis chart"""
    rejection_columns = [
        "EmptyRejection", "FilledRejection", "BreakdownRejection",
        "ManpowerDentRejection", "HighPressureRejection", "WaterCanRejection",
        "MachineDentCans", "FadeCans", "UnprintedCans", "ScratchedCans",
        "LidRejection"
    ]

    rejection_totals = df[rejection_columns].sum().reset_index()
    rejection_totals.columns = ['RejectionType', 'Count']

    fig = px.pie(
        rejection_totals,
        values="Count",
        names="RejectionType",
        title="Distribution of Rejections by Type"
    )
    return fig