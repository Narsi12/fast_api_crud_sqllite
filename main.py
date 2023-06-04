from fastapi import FastAPI,Body,Depends
import schemas
import models

from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

app=FastAPI()

# fakeDatabase = {
#     1:{'task':"Clean car"},
#     2:{'task':"Write blog"},
#     3:{'task':"Strat stream"},
# }

# @app.get("/")
# async def register_user():
#     return fakeDatabase

# @app.get("/{id}")
# def getItem(id:int):
#     return fakeDatabase[id]

# #option 1
# # @app.post("/")
# # def addItem(task:str):
# #     newId = len(fakeDatabase.keys()) + 1
# #     fakeDatabase[newId] = {"task":task}
# #     return fakeDatabase

# #option 2
# @app.post("/")
# def addItem(item:schemas.Item):
#     newId = len(fakeDatabase.keys()) + 1
#     fakeDatabase[newId] = {"task":item.task}
#     return fakeDatabase

# #option 3
# # @app.post("/")
# # def addItem(body = Body()):
# #    newId = len(fakeDatabase.keys()) + 1
# #    fakeDatabase[newId] = {"task":body['task']}
# #    return fakeDatabase

# @app.put('/{id}')
# def updateItem(id:int,item:schemas.Item):
#     fakeDatabase[id]['task'] = item.task
#     return fakeDatabase

# @app.delete('/{id}')
# def deleteItem(id:int):
#     del fakeDatabase[id] 
#     return fakeDatabase

@app.get("/")
def getItems(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items

@app.post("/")
def addItem(item:schemas.Item, session = Depends(get_session)):
    item = models.Item(task = item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@app.get("/{id}")
def getItem(id:int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item

@app.put("/{id}")
def updateItem(id:int, item:schemas.Item, session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    itemObject.task = item.task
    session.commit()
    return itemObject

@app.delete("/{id}")
def deleteItem(id:int, session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return 'Item was deleted'