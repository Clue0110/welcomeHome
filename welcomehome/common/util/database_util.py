from sqlalchemy import create_engine, URL
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session, sessionmaker
from string import Template
import sys

class DatabaseConn:
    def __init__(self,db_uri=None):
        if db_uri==None:
            db_uri=URL.create(
                drivername="postgresql",
                username="postgres",
                password="clueless1001",
                host="127.0.0.1",
                database="welcomehome"
            )

        self.engine=create_engine(db_uri)
        self.db_conn=scoped_session(sessionmaker(bind=self.engine))

    def execute_query(self,query):
        result=self.db_conn.execute(text(query)).fetchall()
        return result
    
    def execute_query_with_args(self,query,arguments):
        query_template=Template(query)
        query_str=query_template.safe_substitute(arguments)
        print(f"Executing Query: {query_str}",file=sys.stdout)
        result=self.db_conn.execute(text(query_str)).fetchall()
        return result
    
    def insert_query_with_values(self,query,arguments):
        query_template=Template(query)
        query_str=query_template.safe_substitute(arguments)
        print(f"Executing Query: {query_str}",file=sys.stdout)
        self.db_conn.execute(text(query_str))
    
    def insert_query_with_values_return_id(self,query,arguments):
        pass

    def update_query_with_values(self,query,arguments):
        query_template=Template(query)
        query_str=query_template.safe_substitute(arguments)
        print(f"Executing Query: {query_str}",file=sys.stdout)
        self.db_conn.execute(text(query_str))

    def commit(self):
        self.db_conn.execute(text("commit;"))
    
