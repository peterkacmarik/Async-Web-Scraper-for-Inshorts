import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Table, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


# Database tables definition (declarative base)
Base = declarative_base()

# Load environment variables
load_dotenv()


class Inshorts(Base):
    # Set the table name and primary key column name (automatically generated if not specified)
    __tablename__ = os.getenv("DATABASE_TABLE_SQLITE")   # Set the table name
    id = Column(Integer, primary_key=True, autoincrement=True)   # Set the primary key
    category = Column(String)  # Set the column name
    titles = Column(String)  # Set the column name
    date = Column(String)  # Set the column name
    descriptions = Column(Text)  # Set the column name
    urls = Column(String)  # Set the column name



class DatabaseManagerSettings:
    def __init__(self) -> None:
        """
        Initializes the DatabaseManagerSettings class.

        This method creates an engine using the `create_engine` function from the `sqlalchemy` module, 
        passing the database URL from the `DATABASE_URL_SQLITE` environment variable as an argument. 
        It then creates a session using the `sessionmaker` function from the `sqlalchemy.orm` module, 
        binding it to the engine. Finally, it creates a session using the `Session` class and assigns it 
        to the `session` attribute of the class.

        Parameters:
            None

        Returns:
            None
        """
        self.engine = create_engine(os.getenv("DATABASE_URL_SQLITE"))   # Create an engine
        self.Session = sessionmaker(bind=self.engine)   # Create a session
        self.session = self.Session()   # Create a session

    def create_table(self, table: Table):
        """
        Create a table in the database using the provided Table object.

        Args:
            table (Table): The Table object representing the table to be created.

        Returns:
            None
        """
        # Create a table in the database using the provided Table object
        table.create(self.engine)

    def insert_data(self, df: pd.DataFrame, Model: declarative_base):
        """
        Insert data into the database using the provided DataFrame and Model.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to be inserted.
            Model (declarative_base): The SQLAlchemy model representing the table schema.

        Returns:
            None
        """
        # Insert data into the database using the provided DataFrame and Model
        for _, row in df.iterrows():
            obj = Model(**row.to_dict())    # Convert the row to a dictionary and pass it to the Model
            self.session.add(obj)   # Add the object to the session
        self.session.commit()   # Commit the changes to the database

    def read_data(self, model, conditions=None):
        """
        Read data from the database using the provided Model and conditions.

        Parameters:
            model (DeclarativeMeta): The model class to query.
            conditions (Optional[BinaryExpression]): The optional conditions to filter the query results.

        Returns:
            pandas.DataFrame: The queried data as a DataFrame.
        """
        # Read data from the database using the provided Model and conditions
        query = self.session.query(model)
        
        # Apply the conditions if provided
        if conditions:
            query = query.filter(conditions)
        
        # Execute the query and return the results as a DataFrame
        data = pd.read_sql(query.statement, self.session.bind)
        return data

    def update_data(self, model, updates):
        """
        Updates data in the database using the provided Model and updates.

        Parameters:
            model (DeclarativeMeta): The SQLAlchemy model representing the table schema.
            updates (dict): A dictionary containing the column names and their corresponding new values.

        Returns:
            None
        """
        # Update data in the database using the provided Model and updates
        self.session.query(model).update(updates, synchronize_session=False)
        self.session.commit()   # Commit the changes to the database

    def delete_all_data(self, model):
        """
        Deletes all data from the database using the provided Model.

        Parameters:
            model (DeclarativeMeta): The SQLAlchemy model representing the table schema.

        Returns:
            None
        """
        # Delete all data from the database using the provided Model
        self.session.query(model).delete()
        self.session.commit()   # Commit the changes to the database

    def close_connection(self):
        """
        Close the database connection.

        This method closes the session object, which releases any resources held by the session and closes the database connection.

        Parameters:
            self (DatabaseManagerSettings): The instance of the DatabaseManagerSettings class.

        Returns:
            None
        """
        # Close the database connection
        self.session.close()

