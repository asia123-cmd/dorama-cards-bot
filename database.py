import aiosqlite

DB_NAME = "dorama_cards.db"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS collection (
                user_id INTEGER NOT NULL,
                card_id INTEGER NOT NULL,
                count INTEGER NOT NULL DEFAULT 1,
                PRIMARY KEY (user_id, card_id)
            )
        """)

        await db.commit()


async def add_card(user_id: int, card_id: int) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (user_id,),
        )

        cursor = await db.execute(
            """
            SELECT count
            FROM collection
            WHERE user_id = ? AND card_id = ?
            """,
            (user_id, card_id),
        )

        row = await cursor.fetchone()

        if row:
            await db.execute(
                """
                UPDATE collection
                SET count = count + 1
                WHERE user_id = ? AND card_id = ?
                """,
                (user_id, card_id),
            )

            await db.commit()
            return False

        await db.execute(
            """
            INSERT INTO collection (user_id, card_id, count)
            VALUES (?, ?, 1)
            """,
            (user_id, card_id),
        )

        await db.commit()
        return True


async def get_collection(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT card_id, count
            FROM collection
            WHERE user_id = ?
            ORDER BY card_id
            """,
            (user_id,),
        )

        return await cursor.fetchall()


async def get_user_total_cards(user_id: int) -> int:
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT COALESCE(SUM(count), 0)
            FROM collection
            WHERE user_id = ?
            """,
            (user_id,),
        )

        row = await cursor.fetchone()
        return row[0]


async def get_user_unique_cards(user_id: int) -> int:
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT COUNT(*)
            FROM collection
            WHERE user_id = ?
            """,
            (user_id,),
        )

        row = await cursor.fetchone()
        return row[0]


async def get_top_players(limit: int = 10):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT user_id, SUM(count) AS total
            FROM collection
            GROUP BY user_id
            ORDER BY total DESC
            LIMIT ?
            """,
            (limit,),
        )

        return await cursor.fetchall()
