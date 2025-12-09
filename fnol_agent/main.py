import argparse
import json

from .extractor import extract_from_file
from .routing import decide_route


def build_response(fields, missing, route, reason):
    return {
        "extractedFields": fields,
        "missingFields": missing,
        "recommendedRoute": route,
        "reasoning": reason,
    }


def main():
    parser = argparse.ArgumentParser(description="FNOL Claims Processing Agent")
    parser.add_argument("input_file", help="Path to a FNOL PDF or TXT file")
    parser.add_argument("--pretty", action="store_true", help="Pretty print JSON")

    args = parser.parse_args()

    fields, missing = extract_from_file(args.input_file)
    route, reason = decide_route(fields, missing)
    result = build_response(fields, missing, route, reason)

    if args.pretty:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result))


if __name__ == "__main__":
    main()
