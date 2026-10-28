app = FastAPI(
    title="Catálogo Sabiá",
    version="1.3.0",
    summary="Catálogo de produtos da Cooperativa Sabiá.",
    description=(
        "API REST do catálogo. Autenticação por token Bearer; "
        "peça o seu em `POST /auth/login`.\n\n"
        "Preços viajam como **texto** para preservar a "
        "precisão decimal."
    ),
    contact={
        "name": "Time de tecnologia",
        "email": "dev@sabia.coop",
    },
    license_info={"name": "Uso interno"},
    openapi_tags=[
        {
            "name": "produtos",
            "description": "Cadastro e consulta do catálogo.",
        },
        {
            "name": "auth",
            "description": "Login e renovação de token.",
        },
    ],
)
