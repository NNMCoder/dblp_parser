from pydantic import BaseSettings

class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str = 'exclusive'
    scopus_apikey: str
    entry_point_url: str
    scopus_url: str
    scopus_metrix_url: str
    yandex_folder_id: str
    yandex_api_key: str


    class Config:
        env_file = '.env'
        env_prefix='exclusive_'