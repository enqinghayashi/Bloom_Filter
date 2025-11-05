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
        self.m = self._optimal_bit_size()
        self.k = self._optimal_hash_count()
        self.bits = bytearray((self.m + 7) // 8)

    def _optimal_bit_size(self) -> int:
        return math.ceil(-(self.n * math.log(self.p)) / (math.log(2) ** 2))

    def _optimal_hash_count(self) -> int:
        return max(1, math.ceil((self.m / self.n) * math.log(2)))

    def _hashes(self, item: ItemType) -> Iterable[int]:
        if isinstance(item, str):
            data = item.encode("utf-8")
        elif isinstance(item, (bytes, bytearray)):
            data = bytes(item)
        else:
            data = str(item).encode("utf-8")
        digest = hashlib.sha256(data).digest()
        h1 = int.from_bytes(digest[:16], "big")
        h2 = int.from_bytes(digest[16:], "big") or 1
        for i in range(self.k):
            yield (h1 + i * h2) % self.m

    def add(self, item: ItemType) -> None:
        for idx in self._hashes(item):
            self.bits[idx // 8] |= 1 << (idx % 8)

    def might_contain(self, item: ItemType) -> bool:
        return all(
            self.bits[idx // 8] & (1 << (idx % 8))
            for idx in self._hashes(item)
        )

    def check_in_and_sign(self, item: ItemType) -> bool:
        if self.might_contain(item):
            return False
        self.add(item)
        return True

if __name__ == "__main__":
    bf = BloomFilter(expected_items=100_000_000, false_positive_rate=0.01)
    ids = sys.argv[1:]
    if not ids:
        ids = []
        print("Enter IDs(letters+numbers)* one per line (type 'confirm' to finish):")
        try:
            while True:
                entry = input("ID> ").strip()
                if entry.lower() == "confirm":
                    break
                if entry:
                    ids.append(entry)
        except KeyboardInterrupt:
            print("\nInput cancelled; exiting.")
            sys.exit(1)
        if not ids:
            print("No IDs provided; exiting.")
            sys.exit(1)
    for uid in ids:
        print(f"{uid}: {'checked in' if bf.check_in_and_sign(uid) else 'already present'}")