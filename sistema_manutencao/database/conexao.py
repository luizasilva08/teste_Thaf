import os

import mysql.connector
from mysql.connector import pooling

_POOL = None


def _config():
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "ctw_manutencao"),
    }


def _pool():
    global _POOL
    if _POOL is None:
        _POOL = pooling.MySQLConnectionPool(
            pool_name="ctw_pool", pool_size=5, **_config()
        )
    return _POOL


def obter_conexao():
    """Retorna uma conexão do pool. Chamador é responsável por fechar (with)."""
    return _pool().get_connection()
