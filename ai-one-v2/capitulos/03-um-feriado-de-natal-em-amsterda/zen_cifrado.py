import codecs
import contextlib
import io

with contextlib.redirect_stdout(io.StringIO()):
    import this

print(this.s[:24])
print(codecs.decode(this.s, "rot13")[:24])
