async function programacao(palco, dia) {
  const chave = `prog:${palco}:${dia}`;
  const guardada = await redis.get(chave);
  if (guardada) return JSON.parse(guardada);

  const { rows } = await db.query(
    "SELECT * FROM shows WHERE palco = $1 AND dia = $2",
    [palco, dia]);
  await redis.set(chave, JSON.stringify(rows), { EX: 60 });
  return rows;
}
