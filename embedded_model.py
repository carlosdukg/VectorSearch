from pydantic import BaseModel
from typing import List, Optional

class embedded_request(BaseModel):
    SR: str = ''
    Title: str = ''
    Customer: str = ''
    Description: str = ''
    sr_embedding: Optional[List[float]]
    title_embedding: Optional[List[float]]
    customer_embedding: Optional[List[float]]
    description_embedding: Optional[List[float]]

class request_search(BaseModel):
    SR: str = ''
    Title: str = ''
    Customer: str = ''
    Description: str = ''
    Score: float = 0.0