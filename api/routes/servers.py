from typing import List
from fastapi import APIRouter, Depends
from api.enums import Region
from api.model.server import Server, ServerGroups

from api.view_model.server import ServerView
from sqlalchemy.orm import Session
from api.db import get_db
from sourceserver.masterserver import MasterServer

servers_route = APIRouter(prefix="/server")


@servers_route.get('s', response_model=List[ServerView])
def gat_all(page: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Server).limit(limit).offset(limit * page).all()

@servers_route.get('/list/{listId}', response_model=List[ServerView])
def gat_list(listId: int, db: Session = Depends(get_db)):
    return db.query(ServerGroups).filter(ServerGroups.id == listId).first().servers

@servers_route.get('/region/{region}', response_model=List[ServerView])
def gat_region(region: Region, db: Session = Depends(get_db)):
    return db.query(Server).filter(Server.region == region).all()