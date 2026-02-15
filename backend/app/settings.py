class Settings:
    NAME: str = "iivko Super Bank - FastAPI"
    DESCRIPTION: str = "Fully feaured banking API"

    VERSION: str = ""

    DEBUG: bool = False

    def __str__(self):
        return self.NAME
