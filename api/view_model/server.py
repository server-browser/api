from datetime import datetime
from typing import Optional
from api.view_model.base_view_model import BaseView

class ServerView(BaseView):
    hostname: Optional[str]
    ip: str
    port: int
    mapname: Optional[str]
    players: Optional[int]
    players_max: Optional[int]
    region: Optional[str]
    last_update: Optional[datetime]
