from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Tuple


class BaseQuery(BaseModel):
    query_id: int
    max_papers: Optional[int] = 100
    required_keywords: Optional[List[str]] = []
    countries: Optional[List[str]] = ['Russian Federation']
    years: Optional[List[int]] = [datetime.now().year]
    authors: Optional[List[str]] = []
    organizations: Optional[List[str]] = []
