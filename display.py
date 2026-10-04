RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"

def print_table(items):
    if not items:
        print(f"{YELLOW} No items to display. {RESET}")
        return

    headers = ['ID', 'Name', 'Brand', 'Price', 'Stock']
    rows = [
        [
            str(i.get("id", "-")),
            str(i.get("product_name", ""))[:25],
            str(i.get("brands", ""))[:15],
            f"${float(i.get('price', 0)):.2f}",
            str(i.get("stock", 0)),
        ]
        for i in items
    ]

    widths = [max(len(h), *(len(r[c]) for r in rows)) for c, h in enumerate(headers)]
    fmt = " | ".join(f"{{:<{w}}}" for w in widths)
    separator = "-+-".join("-" * w for w in widths)

    print (f"{BOLD}{CYAN}{fmt.format(*headers)}{RESET}")
    print (separator)
    for row in rows:
        print (fmt.format(*row))

def print_item(item):
    """Pretty-print a single item as key/value pairs."""
    if not item:
        print(f"{YELLOW}No item to display.{RESET}")
        return

    print(f"\n{BOLD}{CYAN}--- Item Details ---{RESET}")
    for key, value in item.items():
        print(f"{BOLD}{key:>18}{RESET}: {value}")
    print()


def success(msg):
    print(f"\n{GREEN}{BOLD}[OK]{RESET} {msg}\n")


def error(msg):
    print(f"\n{RED}{BOLD}[ERROR]{RESET} {msg}\n")
