from fastapi.responses import JSONResponse as FasAPI_JSONResponse
from fastapi.encoders import jsonable_encoder
from functools import lru_cache
import typing, json

class JSONResponse(FasAPI_JSONResponse):
    """
    JSON response class for sending indent-ed JSON strings.

    @note Routes `/docs` and `/redoc` didn't work without this class,
          but thanks to `jsonable_encoder()` helper, all related errors
          gone.
    """
    def __init__(self, status: int, content: typing.Any = None, indent: int = 2):
        """
        Use just status & content for simplicity,
        and keep indent option for `render()` calls.
        @override
        """
        self.indent = indent

        super().__init__(status_code=status, content=jsonable_encoder(content))

    def render(self, content: typing.Any) -> bytes:
        """
        Render given content as JSON string.
        @override
        """
        return json.dumps(content, indent=self.indent).encode("utf-8")

@lru_cache()
def parse_dotenv():
    """
    Parse .env file.
    """
    options = {}

    with open(".env") as file:
        for line in file:
            line = line.strip()
            if not line.startswith("#"):
                key, value = line.split("=")
                options[key.strip()] = value.strip()

    return options
