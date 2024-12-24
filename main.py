from typing import Union

from fastapi import FastAPI

import json
from request import *
from models import *
from datetime import datetime,time

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

# Получаем из URL данные для нового заказа
# Из файла request берем функцию для добавление нового заказа и передаем ей 
@app.get("/newOrder/{user_id}/{price}")
def readNewOrder(user_id: int,price: int):
    newOrder = order(user_id=user_id,price=price,status=2)
    if(myAdd(newOrder)):
        return {"response": "Заказ успешно создан"}
    else:
        return {"response": 0}

# Дату записывать в формате "год_месяц_день_часы_минуты_секунды", пример: "2024_9_16_15_0_0"
@app.get("/newReserv/{dateStr}/{order_id}")
def readNewReserv(dateStr: str,order_id: int):
    dateList = dateStr.split('_')
    date = datetime(year=int(dateList[0]),month=int(dateList[1]),day=int(dateList[2]),hour=int(dateList[3]),minute=int(dateList[4]),second=int(dateList[5]))
    newReserv = reservation(date=date,order_id=order_id)
    if(myAdd(newReserv)):
        return {"response": 1}
    else:
        return {"response": 0}
    
@app.get("/newUser/{fio}/{phone}")
def readNewUser(fio: str,phone: str):
    newUser = user(fio=fio,phone=phone)
    if(myAdd(newUser)):
        return {"response": 1}
    else:
        return {"response": 0}
    
@app.get("/newCrush/{order_id}/{user_id}/{fine}/{status}")
def readNewCrush(order_id: int,user_id: int,fine: int, status: int):
    newCrush = crushes(order_id=order_id,user_id=user_id,fine=fine,status=status)
    if(myAdd(newCrush)):
        return {"response": 1}
    else:
        return {"response": 0}

# Дату записывать в формате "часы_минуты_секунды", пример: "0_45_13"
@app.get("/newUserTime/{dateStr}/{order_id}")
def readNewUserTime(finishStr: time,user_id: int):
    timeList = finishStr.split('_')
    finishTime = time(hour=int(timeList[0]),minute=int(timeList[1]),second=int(timeList[2]))
    newUserTime = userTime(finishTime=finishTime,user_id=user_id)
    if(myAdd(newUserTime)):
        return {"response": 1}
    else:
        return {"response": 0}

    
# Изменение статуса заказа
@app.get("/changeStatus/{table}/{id}/{status}")
def changeStatusAPI(table: str, id: int,status:int):
    if(changeStatus(table, id, status)):
        return {"response": 1}
    else:
        return {"response": 0}
    
# Запрос и вывод результата
@app.get("/select/{table}")
def selectAPI(table: str):
    results = mySelect(table)

    return {"response": results}

# Удаление строки
@app.get("/delete/{table}/{id}")
def selectAPI(table: str, id: int):

    if(deleteRow(table,id)):
        return {"response": 1}
    else:
        return {"response": 0}