import asyncio
from sqlalchemy import update
from .database import SessionLocal 
from .redis_client import redis_client
from .models import URL

async def sync_all_clicks():
    async with SessionLocal() as db:
        # 1. Get all "clicks:" keys from Redis
        # Note: In production with millions of keys, use SCAN instead of KEYS
        keys = await redis_client.keys("clicks:*")
        
        for key in keys:
            short_code = key.split(":")[1]
            count = await redis_client.get(key)
            
            if count:
                # 2. Update Postgres
                query = (
                    update(URL)
                    .where(URL.short_code == short_code)
                    .values(clicks=int(count))
                )
                await db.execute(query)
        
        await db.commit()
        print(f"Synced {len(keys)} links to the database.")

async def main():
    while True:
        await sync_all_clicks()
        # Wait 60 seconds before the next sync
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())