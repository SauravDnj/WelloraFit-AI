"""
Chart generation utilities using Plotly
"""
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List
import pandas as pd

def create_macro_donut_chart(protein: float, carbs: float, fat: float) -> go.Figure:
    """Create donut chart showing macro distribution"""
    # Calculate calories from macros
    protein_cal = protein * 4
    carbs_cal = carbs * 4
    fat_cal = fat * 9
    
    total_cal = protein_cal + carbs_cal + fat_cal
    
    if total_cal == 0:
        # Empty chart
        fig = go.Figure(data=[go.Pie(
            labels=['No data'],
            values=[1],
            hole=0.6,
            marker_colors=['#E0E0E0']
        )])
        fig.add_annotation(
            text="No data",
            x=0.5, y=0.5,
            font_size=20,
            showarrow=False
        )
    else:
        labels = ['Protein', 'Carbs', 'Fat']
        values = [protein_cal, carbs_cal, fat_cal]
        colors = ['#FF6B6B', '#4ECDC4', '#FFE66D']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.6,
            marker=dict(colors=colors),
            textinfo='label+percent',
            textfont_size=14
        )])
        
        # Add total calories in center
        fig.add_annotation(
            text=f"{int(total_cal)}<br>calories",
            x=0.5, y=0.5,
            font_size=20,
            showarrow=False
        )
    
    fig.update_layout(
        showlegend=False,
        height=300,
        margin=dict(t=20, b=20, l=20, r=20)
    )
    
    return fig

def create_progress_bar_chart(current: float, goal: float, label: str, color: str = "#00D9A3") -> go.Figure:
    """Create horizontal progress bar"""
    percentage = (current / goal * 100) if goal > 0 else 0
    percentage = min(percentage, 100)  # Cap at 100%
    
    fig = go.Figure(go.Bar(
        x=[percentage],
        y=[label],
        orientation='h',
        marker=dict(
            color=color,
            line=dict(color=color, width=3)
        ),
        text=f"{current:.0f} / {goal:.0f}",
        textposition='inside',
        textfont=dict(size=14, color='white')
    ))
    
    fig.update_layout(
        xaxis=dict(range=[0, 100], showticklabels=False, showgrid=False),
        yaxis=dict(showticklabels=False),
        height=60,
        margin=dict(t=0, b=0, l=0, r=0),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_weight_progress_chart(weight_history: List[Dict]) -> go.Figure:
    """Create line chart for weight progress"""
    if not weight_history:
        fig = go.Figure()
        fig.add_annotation(
            text="No weight data yet",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(height=300)
        return fig
    
    # Convert to DataFrame
    df = pd.DataFrame(weight_history)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    
    fig = go.Figure()
    
    # Add weight line
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['weight'],
        mode='lines+markers',
        name='Weight',
        line=dict(color='#00D9A3', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Weight Progress",
        xaxis_title="Date",
        yaxis_title="Weight (kg)",
        height=400,
        hovermode='x unified',
        showlegend=False
    )
    
    return fig

def create_weekly_calorie_chart(daily_data: List[Dict]) -> go.Figure:
    """Create bar chart for weekly calorie intake"""
    if not daily_data:
        fig = go.Figure()
        fig.add_annotation(
            text="No data for this week",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(height=300)
        return fig
    
    df = pd.DataFrame(daily_data)
    
    fig = go.Figure(data=[
        go.Bar(
            x=df['date'],
            y=df['calories'],
            marker_color='#00D9A3',
            text=df['calories'],
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title="Daily Calorie Intake - This Week",
        xaxis_title="Date",
        yaxis_title="Calories",
        height=400,
        showlegend=False
    )
    
    return fig
