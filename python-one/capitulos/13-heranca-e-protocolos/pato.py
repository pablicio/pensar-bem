class Email:
    def enviar(self, texto):
        print(f"e-mail: {texto}")


class SMS:
    def enviar(self, texto):
        print(f"sms: {texto}")


def notificar(canal, texto):
    canal.enviar(texto)
