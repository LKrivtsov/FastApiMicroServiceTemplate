from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):    
  email: str
  # password: str
  middlename: Optional[str]
  firstname: Optional[str]
  lastname: Optional[str]
  is_email_confirmed: bool
  email_confirmed_at: Optional[datetime]
  phone: Optional[str]
  iin: Optional[str]
  is_active: bool
  is_admin: bool
  created_at: datetime
  last_seen_at: datetime
  id_card: Optional[str]
  is_phone_confirmed: bool
  phone_confirmed_at: Optional[datetime]


class UserInDb(User):
  id: int    

  class Config:
      orm_mode = True

class UserSession(BaseModel):
  session_id: str

class AuthorizationResponse(BaseModel):
  access_token: str
  token_type: str