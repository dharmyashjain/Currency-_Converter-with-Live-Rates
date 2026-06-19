# Currency Converter with Live Rates
# Fetches live exchange rates from a free API and lets you convert
# between any two currencies. Supports batch conversion and shows
# a mini rate table for popular currencies.
#
# Install: pip install requests rich
# Usage:   python currency.py 100 USD INR
#          python currency.py --table USD

import requests
import argparse
import sys
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()
# Open Exchange Rates free API — no API key required
API = "https://open.er-api.com/v6/latest"
POPULAR = ["USD", "EUR", "GBP", "JPY", "INR", "CAD", "AUD", "SGD", "AED", "CHF"]

def get_rates(base="USD"):
    # Fetch all exchange rates relative to the base currency
    r = requests.get(f"{API}/{base}", timeout=8)
    r.raise_for_status()
    data = r.json()
    if data["result"] != "success":
        console.print("[red]API error. Try again later.[/red]")
        sys.exit(1)
    return data["rates"], data["time_last_update_utc"]

def convert(amount, from_cur, to_cur):
    rates, updated = get_rates(from_cur.upper())
    to_cur = to_cur.upper()
    if to_cur not in rates:
        console.print(f"[red]Currency '{to_cur}' not found.[/red]")
        sys.exit(1)
    result = amount * rates[to_cur]
    console.print(f"\n[bold]{amount:,.2f} {from_cur.upper()}[/bold] = [green]{result:,.4f} {to_cur}[/green]")
    console.print(f"[dim]Rate: 1 {from_cur.upper()} = {rates[to_cur]:.6f} {to_cur} | Updated: {updated}[/dim]")

def show_table(base="USD"):
    # Display a rate comparison table for popular world currencies
    rates, updated = get_rates(base.upper())
    table = Table(box=box.SIMPLE_HEAD)
    table.add_column("Currency")
    table.add_column(f"1 {base.upper()} =", justify="right")
    for cur in POPULAR:
        if cur in rates and cur != base.upper():
            table.add_row(cur, f"{rates[cur]:,.4f}")
    console.print(f"\n[bold]Exchange rates vs {base.upper()}[/bold] [dim]({updated})[/dim]")
    console.print(table)

def main():
    parser = argparse.ArgumentParser(description="Live currency converter")
    parser.add_argument("amount", type=float, nargs="?", help="Amount to convert")
    parser.add_argument("from_cur", nargs="?", help="From currency (e.g. USD)")
    parser.add_argument("to_cur", nargs="?", help="To currency (e.g. INR)")
    parser.add_argument("--table", metavar="BASE", help="Show rate table for a base currency")
    args = parser.parse_args()

    if args.table:
        show_table(args.table)
    elif args.amount and args.from_cur and args.to_cur:
        convert(args.amount, args.from_cur, args.to_cur)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
