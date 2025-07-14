from logging.config import fileConfig
from sqlalchemy import pool, create_engine
from alembic import context
from sqlmodel import SQLModel
from app.models import Post
from app.config import settings
from urllib.parse import quote_plus

# 🔐 encode password
encoded_password = quote_plus(settings.database_password)

# ✅ Choose the correct DB URL based on environment (test or dev)
DATABASE_URL = (
    f"postgresql+psycopg://{settings.database_username}:{encoded_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

# ✅ Use this database URL for Alembic
config = context.config
# 📋 logging config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ point to all models' metadata (required for autogenerate)
target_metadata = SQLModel.metadata

# ✅ create DB engine
connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

def run_migrations_offline() -> None:
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
