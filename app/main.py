from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .database import get_db
from .models import URL
from .schemas import URLCreate, URLInfo
from .services import URLShortenerService

app = FastAPI()

@app.post("/shorten", response_model=URLInfo)
async def create_short_url(
    payload: URLCreate, 
    db: AsyncSession = Depends(get_db)
):
    # 1. Create a new URL entry (without short_code yet)
    # We save first to let Postgres generate the unique ID
    new_url = URL(target_url=str(payload.target_url), short_code="temp")
    
    db.add(new_url)
    await db.flush()  # 'flush' pushes data to DB and gets back the ID without closing the transaction

    # 2. Use our Service to turn that ID into a Base62 string
    short_code = URLShortenerService.encode(new_url.id)
    
    # 3. Update the record with the real code
    new_url.short_code = short_code
    
    await db.commit()   # Save everything permanently
    await db.refresh(new_url) # Refresh to get the latest state from DB
    
    return new_url


@app.get("/{short_code}")
async def redirect_to_target(
    short_code: str, 
    db: AsyncSession = Depends(get_db)
):
    """
    Look up the short_code in the DB and redirect the user.
    """
    # 1. Database Lookup
    query = select(URL).where(URL.short_code == short_code)
    result = await db.execute(query)
    url_entry = result.scalar_one_or_none()

    # 2. Handle "Not Found"
    if url_entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found"
        )

    # 3. Perform the Redirect
    # Use 302 (Temporary Redirect) so browsers don't cache the link forever.
    # This is important for Phase 4 (Analytics) later!
    return RedirectResponse(url=url_entry.target_url)