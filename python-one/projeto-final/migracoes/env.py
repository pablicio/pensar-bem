from app.config import get_config
from app.database import Base
from app.models import produto, produtor  # registra os modelos

config.set_main_option(
    "sqlalchemy.url", get_config().database_url
)
target_metadata = Base.metadata
