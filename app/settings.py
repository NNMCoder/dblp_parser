from pydantic import BaseSettings

class Settings(BaseSettings):
    db_host: str 
    db_port: int 
    db_user: str 
    db_password: str 
    db_name: str 
    finish_end_point: str  



    class Config:
        env_file = '.env'
        env_prefix='exclusive_'