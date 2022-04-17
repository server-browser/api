from datetime import datetime
from typing import List
from api.logger import get_logger
from api.model.server import Server
from api.db import get_session_local

from sqlalchemy.orm import Session

from sourceserver.sourceserver import SourceServer

from api.celery_worker import celery

from celery_singleton import Singleton

log = get_logger("worker")

@celery.task(name="update_all")
def update_all():
    db: Session = get_session_local()
    servers: List[Server] = db.query(Server).all()
    for server in servers:
        update_info.delay(server.id)


@celery.task(name="update_info", base=Singleton, unique_on=['serverId', ])
def update_info(serverId: int):
    db: Session = get_session_local()
    server: Server = db.query(Server).get(serverId)
    try:
        log.info(f"{server.ip}:{server.port}")     
        server_info = SourceServer(f"{server.ip}:{server.port}").info
        server.hostname = server_info["name"]
        server.mapname = server_info["map"]
        server.players = int(server_info["players"])
        server.players_max = int(server_info["max_players"])       
        server.last_update = datetime.utcnow()
    finally:
        server.last_try = datetime.utcnow()
        db.commit()