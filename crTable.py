from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean
engine = create_engine('sqlite:///inatance/db.sqlite', echo = True)
meta = MetaData()
Todo = Table(
   'Todo', meta, 
   Column('id', Integer, primary_key = True), 
   Column('title', String), 
   Column('complete', Boolean),
)
meta.create_all(engine)