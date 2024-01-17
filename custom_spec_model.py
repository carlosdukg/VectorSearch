
from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class service_request(BaseModel):
    SR: str
    Title: str
    Customer: str
    Description: str