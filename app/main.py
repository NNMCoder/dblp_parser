from fastapi import FastAPI
from uvicorn import run

from app.routes.dblp_route import dblp_router

app = FastAPI(
    title="DBLP parser",
    description="",
)
app.include_router(dblp_router, prefix='/dblp')


@app.get('/')
def index():
    return {'test_route': 'test message'}


def main() -> None:
    run(
        app,
        host='127.0.0.1',
        port=8089
    )