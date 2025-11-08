import sys
from pathlib import Path

def fib(n: int) -> list[int]:
    a, b = 0, 1
    out = []
    for _ in range(n):
        out.append(a)
        a, b = b, a + b
    return out

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    seq = fib(n)
    print("Fibonacci:", seq)

    # write a quick report
    report = Path("fib_report.txt")
    report.write_text(
        "Fibonacci Report\n"
        f"N = {n}\n"
        f"Sequence = {seq}\n"
        f"Sum = {sum(seq)}\n"
        f"Last = {seq[-1] if seq else None}\n"
    )
    print(f"Wrote {report.resolve()}")

if __name__ == "__main__":
    main()
