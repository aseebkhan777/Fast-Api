from typing import List
import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import models as _models
import schemas as _schemas
import services as _services
from services import get_db



app = _fastapi.FastAPI()


#endpoint for creating user
@app.post("/api/users")
async def create_user(user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = await _services.get_user_by_email(user.email, db)
    if db_user:
        raise _fastapi.HTTPException(status_code=400 , detail= "Email Already Exists")
    
    created_user = await _services.create_user(user,db)
    
    return await _services.create_token(created_user)

#endpoint for generating token
@app.post("/api/token")
async def generate_token(form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(), db : _orm.Session = _fastapi.Depends(_services.get_db)):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")
    
    return await _services.create_token(user)

#endpoint for retrieving the user
@app.get("/api/users/me", response_model= _schemas.User,  )
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user

#CRUD#
#endpoint for create lead (post)  --(Create-op)
@app.post("/api/leads", response_model=_schemas.Lead)
async def create_lead(lead: _schemas.LeadCreate, user: _schemas.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.create_lead(user=user, db= db, lead=lead)

#endpoint for returning all our leads --(Read-op)
@app.get("/api/leads", response_model=List[_schemas.Lead])
async def get_leads( user: _schemas.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_leads(user=user, db=db)

#endpoint for getting a specific lead 
@app.get("/api/leads/{lead_id}", status_code=200)
async def get_lead( lead_id: int,user: _schemas.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_lead(lead_id, user, db)

#endpoint for delete operation --(Delete-op)
@app.delete("/api/leads/{lead_id}", status_code=204)
async def delete_lead(lead_id: int,user: _schemas.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    await _services.delete_lead(lead_id,user,db)

    return{"message", "Sucessfully Deleted"}

#endpoint for update(put) operation --(Update-op)
@app.put("/api/leads/{lead_id}", status_code=200)
async def update_lead(lead_id: int, lead:_schemas.LeadCreate, user: _schemas.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    await _services.update_leaad(lead_id, lead, user, db)

    return{"message", "Sucessfully Updated"}


#endpoint to test frontend is connecting with the backend
@app.get("/api")
async def root():
    return {"message": "Leads Manager"}