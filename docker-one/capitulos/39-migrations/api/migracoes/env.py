import os
config.set_main_option("sqlalchemy.url", os.environ["DATABASE_URL"])
