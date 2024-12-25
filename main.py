from typing import Union

from fastapi import FastAPI, HTTPException, Query
from fastapi.encoders import jsonable_encoder

import json
from request import *
from models import *
from datetime import datetime,time

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

# # Получаем из URL данные для нового заказа
# # Из файла request берем функцию для добавление нового заказа и передаем ей 
# @app.get("/newOrder/{user_id}/{price}")
# def readNewOrder(user_id: int,price: int):
#     newOrder = order(user_id=user_id,price=price,status=2)
#     if(myAdd(newOrder)):
#         return {"response": "Заказ успешно создан"}
#     else:
#         return {"response": 0}
    
@app.post("/newOrder")
def create_item(
    user_id: int = Query(..., description="ИД пользователя"),
    price: int = Query(0, description="Стоимость заказ")
):
    with Session(engine) as session:
        new_order = order(user_id=user_id, price=price)
        session.add(new_order)
        session.commit()
        session.refresh(new_order)
        return {"message": "Заказ создан", "order": new_order}

# Дату записывать в формате "год_месяц_день_часы_минуты_секунды", пример: "2024_9_16_15_0_0"
@app.post("/newReserv")
def readNewReserv(dateStr: str = Query(..., description="Дата и время резерва"),
                  order_id: int = Query(0, description="ИД заказа")):
    with Session(engine) as session:
        dateList = dateStr.split('_')
        date = datetime(year=int(dateList[0]),month=int(dateList[1]),day=int(dateList[2]),hour=int(dateList[3]),minute=int(dateList[4]),second=int(dateList[5]))
        newReserv = reservation(date=date,order_id=order_id)
        session.add(newReserv)
        session.commit()
        session.refresh(newReserv)
        return {"message": "Резерв создан", "reservation": newReserv}
    
@app.post("/newUser")
def readNewUser(fio: str = Query(..., description="Фамилия имя и отчество"),
                phone: str  = Query(..., description="Номер телефона")):
    with Session(engine) as session:
        newUser = user(fio=fio,phone=phone)
        session.add(newUser)
        session.commit()
        session.refresh(newUser)
        return {"message": "Пользователь создан", "user": newUser}
    
@app.post("/newCrush")
def readNewCrush(order_id: int = Query(0, description="ИД заказа"),
                 user_id: int = Query(0, description="ИД пользователя"),
                 fine: int = Query(0, description="Размер штрафа"), 
                 status: int = Query(0, description="Статус")):
    with Session(engine) as session:
        newCrush = crushes(order_id=order_id,user_id=user_id,fine=fine,status=status)
        session.add(newCrush)
        session.commit()
        session.refresh(newCrush)
        return {"message": "Авария создана", "crushes": newCrush}

# Дату записывать в формате "часы_минуты_секунды", пример: "0_45_13"
@app.post("/newUserTime")
def readNewUserTime(finishStr: time = Query(..., description="Время полного круга"),
                    user_id: int = Query(0, description="ИД пользователя")):
    with Session(engine) as session:
        timeList = finishStr.split('_')
        finishTime = time(hour=int(timeList[0]),minute=int(timeList[1]),second=int(timeList[2]))
        newUserTime = userTime(finishTime=finishTime,user_id=user_id)
        session.add(newUserTime)
        session.commit()
        session.refresh(newUserTime)
        return {"message": "Время пользователя записано", "userTime": newUserTime}


    
# Изменение статуса заказа
@app.put("changeStatus/{table}/{id}/{status}")
def changeCrushesStatusAPI(table: str, id: int,status:int):
    if(changeStatus(table, id, status)):
        return {"response": 1}
    else:
        return {"response": 0}

# Запрос и вывод результата
@app.get("/select/{table}")
def selectAPI(table: str, offset: int = 0, limit: int = Query(default=100, le=100)):
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
        result = session.exec(statement.offset(offset).limit(limit)).all()
        return result
    
# Запрос и вывод результата
@app.get("/get/{table}/{id}")
def selectAPI(table: str, id: int):
    with Session(engine) as session:
        if(table == 'order'):
            item = session.get(order, id)
        elif(table == 'reservation'):
            item = session.get(reservation, id)
        elif(table == 'user'):
            item = session.get(user, id)
        elif(table == 'crush'):
            item = session.get(crushes, id)
        elif(table == 'userTime'):
            item = session.get(userTime, id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

# Удаление строки
@app.delete("/delete/{table}/{id}")
def selectAPI(table: str, id: int):
    with Session(engine) as session:
        if(table == 'order'):
            item = session.get(order, id)
        elif(table == 'reservation'):
            item = session.get(reservation, id)
        elif(table == 'user'):
            item = session.get(user, id)
        elif(table == 'crush'):
            item = session.get(crushes, id)
        elif(table == 'userTime'):
            item = session.get(userTime, id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        session.delete(item)
        session.commit()
        return {"response": 1}