from functools import lru_cache
import sys

@lru_cache(maxsize=None)
def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    return 1 if n <= 1 else n * factorial(n - 1)

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print(f"factorial({n}) = {factorial(n)}")

if __name__ == "__main__":
    main()
