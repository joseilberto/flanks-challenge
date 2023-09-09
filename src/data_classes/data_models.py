"""File containing all the model data classes we need"""

from datetime import datetime
from typing import Dict, List, NamedTuple, Optional, TypeAlias, TypedDict, Union

QueryDict: TypeAlias = Dict[str, Union[str, List[str], Dict[str, str]]]


class ContentTypes(NamedTuple):
    """
    Named tuple for the content of each pagination
    """

    next_page: str = ""
    urls: List[str] = []


class DataTypes(NamedTuple):
    """NamedTuple for the MongoClientBase params"""

    nombre: str
    numero_registro: str
    fecha_registro: str
    isin: str
    domicilio: Optional[str] = None
    capital_inicial: Optional[float] = None
    capital_maximo: Optional[float] = None
    fecha_ultimo_folleto: Optional[str] = None


class DocumentType(TypedDict):
    """
    Document entry type for the database
    """

    nombre: str
    numero_registro: str
    fecha_registro: str
    isin: str
    domicilio: str
    capital_inicial: float
    capital_maximo: float
    fecha_ultimo_folleto: str
    last_update: str
    write_date: datetime
    updates: Dict[str, Dict[str, Union[str, float]]]


class KeyDocumentType(TypedDict):
    """
    Key document entry type for the database
    """

    nombre: str
    numero_registro: str
    fecha_registro: str
    isin: str
