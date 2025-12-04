from database import Base, engine

# Esto crea todas las tablas según tus modelos actuales
Base.metadata.create_all(bind=engine)

print("Base de datos creada correctamente")
