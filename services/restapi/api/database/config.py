from pydantic import BaseModel, SecretStr


class PostgresqlDBConfig(BaseModel):
    """
    Configuration for MongoDB connection.
    """

    username: str
    password: SecretStr
    host: str
    port: int
    database: str

    def get_url(self) -> str:
        """
        Generate Postgresql connection URL.

        Returns:
            str: The Postgresql connection URL.
        """
        return f'postgresql://{self.username}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.database}'
