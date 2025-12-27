from pydantic import BaseModel, HttpUrl

class URLBase(BaseModel):
    target_url: HttpUrl

class URLCreate(URLBase):
    pass

class URLInfo(URLBase):
    short_code: str

    class Config:
        from_attributes = True # Allows Pydantic to read SQLAlchemy models