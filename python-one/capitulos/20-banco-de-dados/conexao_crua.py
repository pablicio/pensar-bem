import psycopg

url = "postgresql://postgres:senha@localhost/catalogo"

with psycopg.connect(url) as conn:
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO produto (nome, preco) VALUES (%s, %s)",
            ("Cenoura", "5.25"),
        )
        cur.execute("SELECT id, nome, preco FROM produto")
        for linha in cur.fetchall():
            print(linha)
