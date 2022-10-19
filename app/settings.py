from pydantic import BaseSettings

class Settings(BaseSettings):
    db_host: str = 'localhost'
    db_port: int = 3306
    db_user: str = 'root'
    db_password: str = ''
    db_name: str = 'exclusive'
    finish_end_point: str  = 'http://localhost:8089'



    class Config:
        env_file = '../.env'
        env_prefix='exclusive_'