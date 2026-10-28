@time_machine.travel("2027-07-09 22:30:00-03:00", tick=False)
def test_aviso_de_atraso_perto_da_meia_noite():
    partida = agora() + timedelta(hours=2)
    viagem = cria_viagem(partida_em=partida)
    assert aviso_para(viagem).dia == date(2027, 7, 10)
