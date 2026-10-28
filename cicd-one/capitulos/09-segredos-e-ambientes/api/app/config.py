class Config(BaseSettings):
    database_url: PostgresDsn
    redis_url: RedisDsn
    gateway_pagamento_token: SecretStr
    ambiente: Literal["dev", "homologacao", "producao"]
