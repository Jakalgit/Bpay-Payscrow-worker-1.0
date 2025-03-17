import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "transactions.db")


def get_connection():
    """Создает и возвращает соединение с базой данных."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Возвращает данные в виде словаря
    return conn


def create_tables():
    """Создает таблицу транзакций, если она не существует."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT NOT NULL UNIQUE,
            amount REAL CHECK(amount >= -1),
            appeal_id TEXT DEFAULT NULL UNIQUE,
            external_id TEXT NULL UNIQUE,
            chat_id TEXT NOT NULL,
            message_id TEXT NOT NULL,
            provider TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def add_transaction(token, amount, appeal_id, external_id, chat_id, message_id, provider):
    """Добавляет новую транзакцию в базу данных."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO transactions (token, amount, appeal_id, external_id, chat_id, message_id, provider) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (token, amount, appeal_id, external_id, chat_id, message_id, provider))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Ошибка добавления транзакции: {e}")
        conn.rollback()
    finally:
        conn.close()


def row_to_dict(row):
    """Преобразует sqlite3.Row в обычный словарь."""
    return dict(row) if row else None


def get_transaction_by_token(token):
    """Получает транзакцию по token (возвращает словарь)."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions WHERE token = ?", (token,))
    transaction = cursor.fetchone()

    conn.close()
    return row_to_dict(transaction)


def get_transaction_by_appeal_id(appeal_id):
    """Получает транзакцию по appeal_id (возвращает словарь или None)."""
    if appeal_id is None:
        return None

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions WHERE appeal_id = ?", (appeal_id,))
    transaction = cursor.fetchone()

    conn.close()
    return row_to_dict(transaction)


def get_transaction_by_order_id(external_id):
    """Получает транзакцию по order_id (возвращает словарь)."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions WHERE order_id = ?", (external_id,))
    transaction = cursor.fetchone()

    conn.close()
    return row_to_dict(transaction)


def update_transaction_field(token, field, value):
    """Обновляет указанное поле транзакции по token."""
    valid_fields = ['token', 'amount', 'appeal_id', 'order_id', 'source_chat_id', 'source_message_id', 'source', 'result', 'handled']

    if field not in valid_fields:
        return

    conn = get_connection()
    cursor = conn.cursor()

    # Формируем SQL-запрос для обновления
    cursor.execute(f"""
        UPDATE transactions
        SET {field} = ?
        WHERE token = ?
    """, (value, token))

    conn.commit()

def delete_transaction(token: str):
    """Удаляет транзакцию по уникальному токену из таблицы."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Удаляем транзакцию с указанным token
        cursor.execute("""
            DELETE FROM transactions WHERE token = ?
        """, (token,))

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Ошибка при удалении транзакции: {e}")


# Создание таблицы при первом запуске
create_tables()