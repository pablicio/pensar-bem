from sqlalchemy import func

termo = f"%{filtro.q}%"
stmt = stmt.where(
    func.unaccent(Produto.nome).ilike(func.unaccent(termo))
)
