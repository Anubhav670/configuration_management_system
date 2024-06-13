from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError, OperationalError
from . import models, schemas

def get_configurations(db: Session, country_code: str):
    try:
        return db.query(models.Configuration).filter(models.Configuration.country_code == country_code).all()
    except ProgrammingError:
        # Handle the specific error when the table does not exist
        raise
    except OperationalError:
        # Handle database connection errors
        raise

def get_configuration(db: Session, country_code: str, business_name: str):
    return db.query(models.Configuration).filter(models.Configuration.country_code == country_code, models.Configuration.business_name == business_name).first()

def create_configuration(db: Session, configuration: schemas.ConfigurationCreate):
    db_configuration = models.Configuration(**configuration.dict())
    db.add(db_configuration)
    db.commit()
    db.refresh(db_configuration)
    return db_configuration

def update_configuration(db: Session, configuration: schemas.ConfigurationUpdate):
    db_configuration = get_configuration(db, configuration.country_code, configuration.business_name)
    if db_configuration:
        db_configuration.requirements = configuration.requirements
        db.commit()
        db.refresh(db_configuration)
    return db_configuration



def delete_configuration(db: Session, country_code: str, business_name: str):
    configuration = get_configuration(db, country_code, business_name)
    if configuration:
        db.delete(configuration)
        db.commit()
    return configuration



def delete_configurations_by_country(db: Session, country_code: str):
    configurations = db.query(models.Configuration).filter_by(country_code=country_code).all()
    if configurations:
        for config in configurations:
            db.delete(config)
        db.commit()
    return configurations
