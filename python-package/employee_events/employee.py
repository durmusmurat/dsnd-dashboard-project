# Import the QueryBase class
from .query_base import QueryBase

# Import dependencies needed for sql execution
# from the `sql_execution` module
from .sql_execution import query, execute_df

# Define a subclass of QueryBase
# called Employee
class Employee(QueryBase):

    # Set the class attribute `name`
    # to the string "employee"
    name = "employee"


    # Define a method called `names`
    # that receives no arguments
    # This method should return a list of tuples
    # from an sql execution
    @query
    def names(self, entity_id, model):
        
        # Query 3
        # Write an SQL query
        # that selects two columns 
        # 1. The employee's full name
        # 2. The employee's id
        # This query should return the data
        # for all employees in the database
        return "SELECT first_name || ' ' || last_name, employee_id FROM employee"
    

    # Define a method called `username`
    # that receives an `id` argument
    # This method should return a list of tuples
    # from an sql execution
    @query
    def username(self, entity_id, model):
        
        # Query 4
        # Write an SQL query
        # that selects an employees full name
        # Use f-string formatting and a WHERE filter
        # to only return the full name of the employee
        # with an id equal to the id argument
        return f"SELECT first_name || ' ' || last_name FROM employee WHERE employee_id = {entity_id}"


    # Below is method with an SQL query
    # This SQL query generates the data needed for
    # the machine learning model.
    # Without editing the query, alter this method
    # so when it is called, a pandas dataframe
    # is returns containing the execution of
    # the sql query
    @execute_df
    def model_data(self, entity_id, model):

        return f"""
                SELECT SUM(positive_events) positive_events
                     , SUM(negative_events) negative_events
                FROM {self.name}
                JOIN employee_events
                    USING({self.name}_id)
                WHERE {self.name}.{self.name}_id = {entity_id}
                """