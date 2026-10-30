from fastapi import FastAPI, HTTPException, status
from sqlmodel import SQLModel, Field, create_engine, Session, select

'''
1. Modelo de datos
Crear un modelo Estudiante utilizando SQLModel con los siguientes atributos:
id: identificador autogenerado.
nombre: nombre del estudiante.
apellido: apellido del estudiante.
correo: correo electrónico.
edad: edad del estudiante
'''


class Estudiante(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nombre: str
    apellido: str
    correo: str
    edad: int


'''
2. Conexión con la base de datos
Configurar una base de datos SQLite local.
Crear la conexión utilizando SQLModel.
Generar automáticamente la tabla correspondiente.
Configurar la inicialización de la base de datos al iniciar FastAPI.
'''

sqlite_url = f"sqlite:///database.db"

engine = create_engine(sqlite_url, echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI(lifespan=create_tables())


# 3. Desarrollo de endpoints
# POST Endpoint /estudiantes/ FUNCIONALIDAD Registrar un estudiante.
@app.post("/estudiantes/", status_code=status.HTTP_201_CREATED)
def crear_estudiante(estudiante: Estudiante):
    estudiante = Estudiante(**estudiante.model_dump())
    with Session(engine) as session:
        session.add(estudiante)
        session.commit()
        session.refresh(estudiante)
        return estudiante

# GET Endpoint /estudiantes/ FUNCIONALIDAD Consultar todos los estudiantes.
@app.get("/estudiantes/")
def obtener_estudiantes():
    with Session(engine) as session:
        return session.exec(select(Estudiante)).all()


# GET Endpoint /estudiantes/{id} FUNCIONALIDAD Consultar un estudiante por ID.
@app.get("/estudiantes/{id}")
def obtener_estudiante(id: int):
    with Session(engine) as session:
        estudiante = session.get(Estudiante, id)
        if estudiante is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
        return estudiante

# DELETE Endpoint /estudiantes/{id} FUNCIONALIDAD Eliminar un estudiante.
@app.delete("/estudiantes/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_estudiante(id: int):
    with Session(engine) as session:
        estudiante = session.get(Estudiante, id)
        if not estudiante:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
        session.delete(estudiante)
        session.commit()