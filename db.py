import aiosqlite as sql


class Database:
    async def __aenter__(self):
        self.db = await sql.connect('base.db')
        self.cursor = await self.db.cursor()
        await self.create_table()
        return self
        
    async def __aexit__(self, *args):
        await self.cursor.close()
        await self.db.close()
    
    async def create_table(self):
        await self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS
            tasks(
                task_id INTEGER PRIMARY KEY,
                prompt TEXT NOT NULL,
                product_id INTEGER NOT NULL,
                operations INTEGER
            )
        """)
        await self.db.commit()
        
    async def add(self, data: tuple):
        await self.cursor.execute("""
            INSERT INTO 
            tasks (prompt, product_id, operations)
            VALUES (?, ?, ?)
        """, data)
        await self.db.commit()
    
    
    async def get_all(self):
        result = await self.cursor.execute("""
            SELECT * FROM tasks
        """)
        all = await result.fetchall()
        return all
        
    async def get_one(self, id: int):
        result = await self.cursor.execute(f"""
            SELECT * FROM tasks
            WHERE task_id = ?
        """, (id, ))
        one = await result.fetchone()
        return one
        
    async def delete(self, id_: int):
        await self.cursor.execute(f"""
            DELETE FROM tasks
            WHERE task_id = ?
        """, tuple(id_))
        await self.db.commit()
