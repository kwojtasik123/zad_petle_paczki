import os
import sys
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from aplikacja_webowa_program_ksiegowy_bd.models import db
from aplikacja_webowa_program_ksiegowy_bd.models import Saldo, Magazyn, Historia



# Konfiguracja Alembic
config = context.config

# Logowanie (opcjonalne)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata aplikacji
target_metadata = db.Model.metadata

# Funkcje migracji
def run_migrations_offline():
    """Uruchamia migracje w trybie offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Uruchamia migracje w trybie online."""
    connectable = create_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

