from enum import Enum, unique
from typing import List


FloatVector = List[float]
IntegerVector = List[int]
StringVector = List[str]
Float2DVector = List[List[float]]


@unique
class ElasticSearchStatusCode(Enum):
  YELLOW = 'yellow'
  GREEN = 'green'
  RED = 'red'