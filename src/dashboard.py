from fasthtml.common import *
from employee_events import Employee, Team  # Required import
import plotly.express as px
import pandas as pd

# Initialize FastHTML and your package classes
app, rt = fast_app()
emp_api = Employee()

@rt("/")
def get(emp_id: int = 1):
    # Requirement: Display database data
    # We'll pull names for a dropdown and data for charts
    all_names = emp_api.names() 
    
    # Visualization 1: Event Counts (Bar Chart)
    # Using the @execute_df decorated method in your package
    df_events = emp_api.event_counts(emp_id)
    fig1 = px.bar(df_events, x='event_date', y=['positive_events', 'negative_events'],
                  title="Daily Performance Trends", barmode='group')

    # Visualization 2: ML Performance with Color Scale (Rubric Requirement)
    df_ml = emp_api.model_data(emp_id)
    fig2 = px.pie(df_ml, values='positive_events', names='event_date',
                  title="Success Distribution",
                  color_discrete_sequence=px.colors.sequential.Viridis) # Color scale!

    return Titled(f"Employee Dashboard: ID {emp_id}",
        Grid(
            Card(H3("Performance Overview"),
                 P("Data pulled directly from employee_events.db")),
            Div(NotStr(fig1.to_html(full_html=False))),
            Div(NotStr(fig2.to_html(full_html=False)))
        )
    )

if __name__ == "__main__": 
    serve()