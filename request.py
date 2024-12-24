from sqlmodel import Session, SQLModel, create_engine, select
from models import *

engine = create_engine("sqlite:///database.db")

SQLModel.metadata.create_all(engine)

# Просто SELECT к дазе банных 
def mySelect(table: str):
    with Session(engine) as session:
        if(table == 'order'):
            statement = select(order)
        elif(table == 'reservation'):
            statement = select(reservation)
        elif(table == 'user'):
            statement = select(user)
        elif(table == 'crush'):
            statement = select(crushes)
        elif(table == 'userTime'):
            statement = select(userTime)

        result = session.exec(statement).all()
        
        return result

# Функции добавление новых полей в дазу банных
def myAdd(data: order):
    with Session(engine) as session:
        session.add(data)
        session.commit()

        return 1

def myAdd(data: reservation):
    with Session(engine) as session:
        session.add(data)
        session.commit()

        return 1
 
def myAdd(data: user):
    with Session(engine) as session:
        session.add(data)
        session.commit()

        return 1
 
def myAdd(data: crushes):
    with Session(engine) as session:
        session.add(data)
        session.commit()

        return 1
 
def myAdd(data: userTime):
    with Session(engine) as session:
        session.add(data)
        session.commit()

        return 1
 
# Изменение статуса заказа
def changeStatus(table:str, id:int, newStatus:int):
    with Session(engine) as session:
        if(table == 'order'):
            statement = select(order).where(order.id == id)
        elif(table == 'crush'):
            statement = select(crushes).where(crushes.id == id)
        results = session.exec(statement)
        result = results.one()
        result.status = newStatus
        session.add(result)
        session.commit()
        session.refresh(result)
        
        return 1
        
# Удаление строки
def deleteRow(table:str, id:int):
    with Session(engine) as session:
        if(table == 'order'):
            statement = select(order).where(order.id == id)
        elif(table == 'reservation'):
            statement = select(reservation).where(reservation.id == id)
        elif(table == 'user'):
            statement = select(user).where(user.id == id)
        elif(table == 'crush'):
            statement = select(crushes).where(crushes.id == id)
        elif(table == 'userTime'):
            statement = select(userTime).where(userTime.id == id)
        results = session.exec(statement)
        result = results.one()
        session.delete(result)
        session.commit()

        return 1