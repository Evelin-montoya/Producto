from database import Base, engine
from models import Producto

print('Creating database.....')

Base.metadata.create_all(engine)

