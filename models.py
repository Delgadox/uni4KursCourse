from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime, time


class reservation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime = Field(nullable=False)
    order_id: int | None = Field(default=None, foreign_key="order.id")


class order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    # Статус имеет 3 значения: 1 - оплачен, 2 - не оплачен, 3 - отменён 
    status: int = Field(default=2)
    price: int = Field(nullable=False)

class user(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fio: str = Field(nullable=False)
    phone: str = Field(nullable=False)

class crushes(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int | None = Field(default=None, foreign_key="order.id")
    user_id: int = Field(default=None, foreign_key="user.id")
    fine: int = Field(nullable=False)
    status: int = Field(default=2)

class userTime(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    finishTime: time = Field(nullable=False)
    user_id: int = Field(default=None, foreign_key="user.id")


engine = create_engine("sqlite:///database.db")

SQLModel.metadata.create_all(engine)

# with Session(engine) as session:
#     session.add(order_1)
#     session.add(reservation_1)
#     session.commit()