from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError, OperationalError
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.post("/create_configuration", response_model=schemas.Configuration)
def create_configuration(configuration: schemas.ConfigurationCreate, db: Session = Depends(get_db)):
    db_configuration = crud.get_configuration(db, configuration.country_code, configuration.business_name)
    if db_configuration:
        raise HTTPException(status_code=400, detail="Configuration already exists for this business")
    return crud.create_configuration(db, configuration)



@router.get("/get_configurations/{country_code}", response_model=List[schemas.Configuration])
def get_configurations(country_code: str, db: Session = Depends(get_db)):
    try:
        configurations = crud.get_configurations(db, country_code)
        if not configurations:
             raise HTTPException(status_code=404, detail="No configurations found for the given country code")
        return configurations
    except ProgrammingError:
        raise HTTPException(status_code=500, detail="Database error: The configuration table does not exist. Please ensure the table is created.")
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database error: Unable to connect to the database. Please ensure the database is running.")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/get_configuration/{country_code}/{business_name}", response_model=schemas.Configuration)
def get_configuration(country_code: str, business_name: str, db: Session = Depends(get_db)):
    db_configuration = crud.get_configuration(db, country_code, business_name)
    if not db_configuration:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return db_configuration

@router.post("/update_configuration", response_model=schemas.Configuration)
def update_configuration(configuration: schemas.ConfigurationUpdate, db: Session = Depends(get_db)):
    db_configuration = crud.get_configuration(db, configuration.country_code, configuration.business_name)
    if not db_configuration:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return crud.update_configuration(db, configuration)



@router.delete("/delete_configuration/{country_code}/{business_name}", response_model=schemas.Configuration)
def delete_configuration(country_code: str, business_name: str, db: Session = Depends(get_db)):
    try:
        db_configuration = crud.get_configuration(db, country_code, business_name)
        if not db_configuration:
             raise HTTPException(status_code=404, detail="No configurations found for the given country code or Business name")
        return crud.delete_configuration(db, country_code, business_name)
    except ProgrammingError:
        raise HTTPException(status_code=500, detail="Database error: The configuration table does not exist. Please ensure the table is created.")
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database error: Unable to connect to the database. Please ensure the database is running.")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")



@router.delete("/delete_configurations/{country_code}", response_model=List[schemas.Configuration])
def delete_configurations_by_country(country_code: str, db: Session = Depends(get_db)):
    try:
        configurations = crud.delete_configurations_by_country(db, country_code)
        if not configurations:
             raise HTTPException(status_code=404, detail="No configurations found for the given country code")
        return configurations
    except ProgrammingError:
        raise HTTPException(status_code=500, detail="Database error: The configuration table does not exist. Please ensure the table is created.")
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database error: Unable to connect to the database. Please ensure the database is running.")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")