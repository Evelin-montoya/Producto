from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://dahayrpt:GYaXGTJN-5gLoPTz7ApKVS1gcpG4s8EZ@bubble.db.elephantsql.com/dahayrpt')

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
