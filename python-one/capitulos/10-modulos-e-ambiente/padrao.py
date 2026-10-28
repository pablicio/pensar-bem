from datetime import datetime, timezone
from pathlib import Path

agora = datetime.now(timezone.utc)
arquivo = Path("dados") / "catalogo.json"

print(agora.isoformat())
print(arquivo.exists())
