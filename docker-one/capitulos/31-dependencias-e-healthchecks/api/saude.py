import sys
import urllib.request

URL = "http://localhost:8000/saude"
try:
    r = urllib.request.urlopen(URL, timeout=2)
    sys.exit(0 if r.status == 200 else 1)
except Exception as erro:
    print(erro, file=sys.stderr)
    sys.exit(1)
