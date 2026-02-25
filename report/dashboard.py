from fasthtml.common import *
import matplotlib.pyplot as plt

# Import QueryBase, Employee, Team from employee_events
from employee_events import QueryBase, Employee, Team

# import the load_model function from the utils.py file
from utils import load_model

"""
Below, we import the parent classes
you will use for subclassing
"""
from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
    )

from combined_components import FormGroup, CombinedComponent


# Create a subclass of base_components/dropdown
# called `ReportDropdown`
class ReportDropdown(Dropdown):
    
    # Overwrite the build_component method
    # ensuring it has the same parameters
    # as the Report parent class's method
    def build_component(self, entity_id, model):

        #  Set the `label` attribute so it is set
        #  to the `name` attribute for the model
        self.label = model.name
        
        # --- THE FIX ---
        # Ensure entity_id is a string for the component's internal logic
        # And explicitly pass it into the super() call so the parent class sees it.
        entity_id = str(entity_id) if entity_id else "1"
        self.value = entity_id
        
        # Return the output from the
        # parent class's build_component method
        return super().build_component(entity_id, model)
    
    # Overwrite the `component_data` method
    # Ensure the method uses the same parameters
    # as the parent class method
    def component_data(self, entity_id, model):
        # Using the model argument
        # call the employee_events method
        # that returns the user-type's
        # names and ids
        return model.names(entity_id, model)

# Create a subclass of base_components/BaseComponent
# called `Header`
class Header(BaseComponent):

    # Overwrite the `build_component` method
    # Ensure the method has the same parameters
    # as the parent class
    def build_component(self, entity_id, model):
        
        # Using the model argument for this method
        # return a fasthtml H1 objects
        # containing the model's name attribute
        return H1(model.name)
          

# Create a subclass of base_components/MatplotlibViz
# called `LineChart`
class LineChart(MatplotlibViz):
    
    # Overwrite the parent class's `visualization`
    # method. Use the same parameters as the parent
    def visualization(self, entity_id, model):
        import matplotlib.pyplot as plt
        plt.style.use('default')

        # Pass the `asset_id` argument to
        # the model's `event_counts` method to
        # receive the x (Day) and y (event count)
        df = model.event_counts(entity_id, model)
        
        # Use the pandas .fillna method to fill nulls with 0
        df = df.fillna(0)
        
        # User the pandas .set_index method to set
        # the date column as the index
        df = df.set_index('date')
        
        # Sort the index
        df = df.sort_index()
        
        # Use the .cumsum method to change the data
        # in the dataframe to cumulative counts
        df = df.cumsum()
        
        # Set the dataframe columns to the list
        # ['Positive', 'Negative']
        df.columns = ['Positive', 'Negative']
        
        # Initialize a pandas subplot
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        
        # call the .plot method for the
        # cumulative counts dataframe
        df.plot(ax=ax)
        
        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')
            
        # Set title and labels for x and y axis
        ax.set_title("Event Counts Over Time", fontsize=16)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Event Count", fontsize=12)

        return fig

# Create a subclass of base_components/MatplotlibViz
# called `BarChart`
class BarChart(MatplotlibViz):

    # Create a `predictor` class attribute
    # assign the attribute to the output
    # of the `load_model` utils function
    predictor = load_model()

    # Overwrite the parent class `visualization` method
    # Use the same parameters as the parent
    def visualization(self, entity_id, model):
        import matplotlib.pyplot as plt
        plt.style.use('default')

        # Using the model and asset_id arguments
        # pass the `asset_id` to the `.model_data` method
        data = model.model_data(entity_id, model)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')

        if data.empty:
            ax.text(0.5, 0.5, "No data available", ha='center', va='center')
            return fig

        # Using the predictor class attribute
        # pass the data to the `predict_proba` method
        probabilities = self.predictor.predict_proba(data)
        
        # Index the second column of predict_proba output
        risk_probs = probabilities[:, 1]
        
        # Below, create a `pred` variable set to
        # the number we want to visualize
        if model.name.lower() == "team":
            pred = risk_probs.mean()
        # Otherwise set `pred` to the first value
        else:
            pred = risk_probs[0]
        
        # Using the `ax` variable, call the .barh method
        ax.barh([''], [pred])
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20, color='black')
        
        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')

        return fig
 
# Create a subclass of combined_components/CombinedComponent
# called Visualizations       
class Visualizations(CombinedComponent):

    # Set the `children`
    # class attribute to a list
    children = [LineChart(), BarChart()]

    # Leave this line unchanged
    outer_div_type = Div(cls='grid')
            
# Create a subclass of base_components/DataTable
# called `NotesTable`
class NotesTable(DataTable):

    # Overwrite the `component_data` method
    def component_data(self, entity_id, model):
        
        # Using the model and entity_id arguments
        # pass the entity_id to the model's .notes method
        return model.notes(entity_id, model)
    

class DashboardFilters(FormGroup):

    id = "top-filters"
    action = "/update_data"
    method="POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
            ),
        ReportDropdown(
            id="selector",
            name="user-selection")
        ]

    # FIX: Synchronize the radio button with the page model
    def build_component(self, entity_id, model):
        # Force the radio to match the model class (Employee/Team)
        self.children[0].value = model.__class__.__name__
        return super().build_component(entity_id, model)
    
# Create a subclass of CombinedComponents
# called `Report`
class Report(CombinedComponent):

    # Set the `children`
    # class attribute to a list
    children = [Header(), DashboardFilters(), Visualizations(), NotesTable()]

# Initialize a fasthtml app 
app, rt = fast_app()

# Initialize the `Report` class
report = Report()


# Route for root path
@rt('/')
def get_root():
    return report.call_children(1, Employee())

# Route for employee view
@rt('/employee/{id}')
def get_emp(id: str):
    # Pass the ID through to call_children explicitly
    return report.call_children(id, Employee())

# Route for team view
@rt('/team/{id}')
def get_tm(id: str):
    # Pass the ID through to call_children explicitly
    return report.call_children(id, Team())


# Keep the below code unchanged!
@app.get('/update_dropdown')
def update_dropdown(profile_type: str):
    dropdown = DashboardFilters.children[1]
    if profile_type == 'Team':
        return dropdown(None, Team())
    elif profile_type == 'Employee':
        return dropdown(None, Employee())


@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)
    
serve()