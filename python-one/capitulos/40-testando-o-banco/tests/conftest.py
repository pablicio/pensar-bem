from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def engine():
    with PostgresContainer("postgres:16") as pg:
        eng = create_engine(pg.get_connection_url())
        Base.metadata.create_all(eng)
        yield eng
