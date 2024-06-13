from sqlalchemy import Column, Integer, String, JSON, UniqueConstraint
from .database import Base

class Configuration(Base):
    __tablename__ = 'configurations'
    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String, index=True)
    business_name = Column(String, index=True)
    requirements = Column(JSON)
    
    __table_args__ = (UniqueConstraint('country_code', 'business_name', name='_country_business_uc'),)
