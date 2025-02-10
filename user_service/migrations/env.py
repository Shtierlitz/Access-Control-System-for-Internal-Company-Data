import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool, text
from sqlalchemy import engine_from_config
from app.models import User  # Импорт моделей
from app.database import Base, engine  # Импорт `Base` и `engine`
from dotenv import load_dotenv

load_dotenv()

# Схема, в которой создаются таблицы
SCHEMA = os.getenv("DB_SCHEMA", "user_service")

config = context.config

config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Запуск миграций в offline-режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema="public"  # <-- Это фикс, указываем схему public
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
