from sqlalchemy.orm import raiseload

stmt = select(Produto).options(raiseload("*")).limit(100)
