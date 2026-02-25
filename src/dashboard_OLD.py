from flask import Flask, render_template_string
from employee_events import Employee
import plotly.express as px
import pandas as pd

class BaseComponent:

    # 1 (Line 3 in base_component.py)
    def build_component(self, entity_id, model):
        raise NotImplementedError
                                  
    # 2 (Line 10 in base_component.py)                        
    def component_data(self, entity_id, model):
        raise NotImplementedError

class CombinedComponent:
    children = []
    def call_children(self, userid, model):
        called = []
        for child_class in self.children:
            # Initialize the child and call its build method
            child_instance = child_class()
            called.append(child_instance.build_component(userid, model))
        return called

# --- 1. BaseComponent Subclasses ---

class PerformanceBarChart(BaseComponent):
    def component_data(self, entity_id, model):
        # Rule: Use 'entity_id' and 'model'
        df = model.get_all_employee_events() 
        return df[df['employee_id'] == entity_id]

    def build_component(self, entity_id, model):
        df = self.component_data(entity_id, model)
        fig = px.bar(df, x='event_type', title="Employee Event Frequency")
        return fig.to_html(full_html=False)

class EventPieChart(BaseComponent):
    def component_data(self, entity_id, model):
        # Rule: Use 'entity_id' and 'model'
        df = model.get_all_employee_events()
        return df[df['employee_id'] == entity_id]

    def build_component(self, entity_id, model):
        df = self.component_data(entity_id, model)
        fig = px.pie(df, names='event_type', title="Event Distribution", color_discrete_sequence=px.colors.sequential.Viridis)
        return fig.to_html(full_html=False)

# --- 2. CombinedComponent Subclass ---

class EmployeeDashboard(CombinedComponent):
    # Rule: Set the children attribute
    children = [PerformanceBarChart, EventPieChart]

# --- 3. Flask App Engine ---

app = Flask(__name__)

@app.route('/')
def index():
    # Initialize the model and entity_id
    model = Employee() 
    entity_id = 1  # Example ID
    
    # Use the CombinedComponent engine
    dashboard = EmployeeDashboard()
    components = dashboard.call_children(entity_id, model)
    
    # Return all built components inside a div
    return f"<div>{''.join(components)}</div>"

if __name__ == '__main__':
    app.run(port=5001, debug=True)