from turtle import showturtle
from api.model.server import Server
from valve.source.master_server import MasterServerQuerier


from api.db import get_session_local

def _update_list():
    ms = MasterServerQuerier()
    servers = ms.find(region='all',
        gamedir="tf",        
    )
    db = get_session_local()
    for host, port in servers:
        c = db.query(Server).filter((Server.ip == host) & (Server.port == port)).count()
        should_skip = False
        if c != 0:
            should_skip=True
        if host is None or port is None:
            should_skip=True
        if should_skip:
            print(f"skiping {host}:{port}")
            continue
        print(f"adding {host}:{port}")
        new_server = Server()
        new_server.ip = host
        new_server.port = port
        db.add(new_server)
    db.commit()
    ms.close()