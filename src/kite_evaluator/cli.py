import argparse
import json
from pathlib import Path

from .engine import evaluate


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a Kite x402 service manifest")
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    findings = evaluate(json.loads(args.manifest.read_text()))
    if findings:
        for finding in findings:
            print(f"{finding.level.upper():5} {finding.code}: {finding.message}")
        return 1
    print("PASS manifest is ready for service integration")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
