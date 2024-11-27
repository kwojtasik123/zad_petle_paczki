from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Import bazy danych i modeli
from app import db
from models import Pracownik, Punkty, Historia  # Zmień te importy na zgodne z twoją strukturą projektu, jeśli trzeba

# Obiekt konfiguracji Alembic, umożliwiający dostęp do wartości z pliku .ini
config = context.config

# Ustawienie konfiguracji dla logowania
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Ustawienie metadanych modeli
target_metadata = db.metadata


def run_migrations_offline() -> None:
    """Uruchom migracje w trybie 'offline'.

    W tym trybie konfigurujemy kontekst tylko z użyciem URL-a
    bez tworzenia obiektu Engine.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Uruchom migracje w trybie 'online'.

    W tym trybie tworzymy obiekt Engine i łączymy go z kontekstem.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# Decyduje, w którym trybie uruchomić migracje
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

