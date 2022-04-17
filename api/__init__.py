from fastapi import FastAPI

app = FastAPI()


from api.routes.servers import servers_route

app.include_router(servers_route)