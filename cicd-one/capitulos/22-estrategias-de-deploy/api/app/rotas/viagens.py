if flags.ligada("aviso_atraso", usuario=usuario):
    resposta["aviso"] = calcula_aviso_atraso(viagem)
