import os

class Settings:
    app_name: str = os.getenv("APP_NAME", "Ecommerce Docker Platform")
    environment: str = os.getenv("APP_ENV", "development")

settings = Settings()
