v1 = APIRouter(prefix="/v1")
v1.include_router(produtos.router)

app.include_router(v1)
