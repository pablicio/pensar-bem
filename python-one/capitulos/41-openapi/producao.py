config = get_config()
interno = config.app_ambiente != "producao"

app = FastAPI(
    docs_url="/docs" if interno else None,
    redoc_url=None,
    openapi_url="/openapi.json" if interno else None,
)
