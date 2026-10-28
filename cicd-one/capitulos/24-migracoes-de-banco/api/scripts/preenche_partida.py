while True:
    n = db.execute(text("""
        UPDATE viagens SET partida_em = calcula_partida(id)
        WHERE id IN (SELECT id FROM viagens
                     WHERE partida_em IS NULL LIMIT 5000)
    """)).rowcount
    db.commit()
    if n == 0:
        break
    time.sleep(0.2)
