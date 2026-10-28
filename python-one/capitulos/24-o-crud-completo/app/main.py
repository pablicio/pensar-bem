from app.database import Base, engine
from app.models import produto as _  # registra o modelo

Base.metadata.create_all(engine)
