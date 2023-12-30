from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

server = "KEITH\SQLEXPRESS"
database = "fastapi"

# Construct the connection string with Windows authentication
connection_string = f"mssql+pyodbc://{settings.server}/{settings.database}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(connection_string, echo=True)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind = engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#while True:
 #   try:
 #       server = "KEITH\\SQLEXPRESS"
 #       database = "fastapi"

        # Corrected username without the domain
  #      username = "TRACY"

        # Password is not needed for Windows authentication
  #      password = ""

        # Use Trusted_Connection=yes for Windows authentication
    #    connection_string = 'DRIVER={{SQL Server}};SERVER={};DATABASE={};UID={};PWD={};Trusted_Connection=yes'.format(server, database, username, password)

        # Establish the connection
    #    conn = pyodbc.connect(connection_string)
    #    cursor = conn.cursor()
       
    #    break
   # except Exception as error:
    #    print("Connecting to database failed")
     #   print("Error: ", error)
    #    time.sleep(2)