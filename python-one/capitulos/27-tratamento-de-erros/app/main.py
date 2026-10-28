from app.errors import registrar_tratadores

app = FastAPI(title=config.app_nome)
registrar_tratadores(app)
