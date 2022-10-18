from pydantic import BaseSettings

class Settings(BaseSettings):
    db_host: str = 'localhost'
    db_port: int = 3306
    db_user: str = 'root'
    db_password: str = 'csv16xp'
    db_name: str = 'exclusive'



    class Config:
        env_file = '../.env'
        env_prefix='exclusive_'