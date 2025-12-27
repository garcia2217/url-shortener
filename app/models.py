from sqlalchemy import BigInteger, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base
import datetime

class URL(Base):
    __tablename__ = "urls"

    # Use BigInteger for scalability (Phase 3 ready)
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    
    # The original long URL
    target_url: Mapped[str] = mapped_column(String, nullable=False, index=True)
    
    # The Base62 code (e.g., 'sG1')
    short_code: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )