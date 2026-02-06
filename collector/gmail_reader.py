# Gmail reader (placeholder)
import csv
import argparse

def load_companies(csv_path: str):
    companies = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("status", "").strip().lower() != "active":
                continue
            domain = (row.get("domain") or "").strip()
            if not domain:
                continue
            companies.append({
                "company_id": (row.get("company_id") or "").strip(),
                "company_name": (row.get("company_name") or "").strip(),
                "domain": domain,
            })
    return companies

def build_gmail_query(domain: str) -> str:
    return f'(from:@{domain} OR to:@{domain})'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--companies", default="config/companies.csv")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    companies = load_companies(args.companies)
    print(f"Loaded {len(companies)} companies")

    for c in companies:
        q = build_gmail_query(c["domain"])
        name = c["company_name"] or c["company_id"]
        print(f"- {name}: {q}")

    if args.dry_run:
        print("\nDry-run mode: Gmail API not called.")

if __name__ == "__main__":
    main()
