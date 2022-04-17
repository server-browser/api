from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, Text, DATETIME
from sqlalchemy import Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from api.db import Base

class Server(Base):
    __tablename__ = 'server'
    id = Column(Integer, primary_key=True)
    hostname = Column(Text, nullable=True)
    ip = Column(Text, nullable=False)
    port = Column(Integer, nullable=False)
    mapname = Column(Text, nullable=True)
    players = Column(Integer, nullable=True)
    players_max = Column(Integer, nullable=True)
    region = Column(Text, nullable=True)
    last_update = Column(DATETIME, nullable=True)
    last_try = Column(DATETIME, nullable=True)


class ServerGroupFilter(Base):
    __tablename__ = 'server_group_filter'
    id =  Column(Integer, primary_key=True)
    filter_type = Column(Text, nullable=False)
    filter_value = Column(Text, nullable=False)
    is_black_list = Column(Boolean, default=False)

class ServerGroups(Base):
    __tablename__ = 'server_group'
    id =  Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, default= lambda: f"made {datetime.utcnow()}")
    created_time = Column(DATETIME, default=datetime.utcnow, nullable=False)
    servers: List[Server] = relationship("Server", secondary="server_group_association")
    filters: List[ServerGroupFilter] = relationship("ServerGroupFilter", secondary="server_group_filter_association")


server_group_association = Table('server_group_association', Base.metadata,
    Column('server_id', ForeignKey(Server.__tablename__ + '.id'), primary_key=True, nullable=False),
    Column('server_group_id', ForeignKey(ServerGroups.__tablename__ + '.id'), primary_key=True, nullable=False)
)

server_group_filter_association = Table('server_group_filter_association', Base.metadata,
    Column('filter_id', ForeignKey(ServerGroupFilter.__tablename__ + '.id'), primary_key=True, nullable=False),
    Column('server_group_id', ForeignKey(ServerGroups.__tablename__ + '.id'), primary_key=True, nullable=False)
)
