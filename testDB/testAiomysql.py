'''
import asyncio
import aiomysql
from dotenv import load_dotenv
import os
from time import time

load_dotenv('.env.database')

DATABASE_DB = os.getenv("DATABASE_DB")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PWD = os.getenv("DATABASE_PWD")
DATABASE_PORT = int(os.getenv("DATABASE_PORT"))
DATABASE_SERVER = os.getenv("DATABASE_SERVER")

async def main():
    # 비동기 DB 연결 설정
    pool = await aiomysql.create_pool(
        host='localhost', port=3306,
        user='your_username', password='your_password',
        db='your_database', loop=loop)
    
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # 쿼리 실행
            await cur.execute("SELECT * FROM your_table")
            
            # 결과 가져오기
            rows = await cur.fetchall()
            for row in rows:
                print(row)

    pool.close()
    await pool.wait_closed()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
'''