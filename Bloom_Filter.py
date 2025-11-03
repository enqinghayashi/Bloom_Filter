import math
import hashlib
import sys
from typing import Iterable, Union

ItemType = Union[str, bytes, bytearray]

class BloomFilter:
    def __init__(self, expected_items: int, false_positive_rate: float) -> None:
        if expected_items <= 0 or not (0 < false_positive_rate < 1):
            raise ValueError("Invalid Bloom filter parameters.")
        self.n = expected_items
        self.p = false_positive_rate







