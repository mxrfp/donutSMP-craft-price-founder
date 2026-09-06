from functions_and_scraping import get_single_cost, clear_cache, get_cache, items, v
import sys

print("-"*100)
print()
print("FIND PRICE ON DONUTSMP.AUCTION".center(100))
print()
print("-"*100)
print()
print("[X] Type the name of the item to find the crafting price.")
print()
print("-"*100)

keep_cache = False
deep_search = True

while True:
    inp = " ".join(input("Item name (type exit to quit): ").lower().split())
    match inp:
        case 'exit':
            sys.exit(0)
        case "--cache c":
            clear_cache()
            continue
        case "--cache k":
            keep_cache = True
            continue
        case "--cache !k":
            keep_cache = False
            clear_cache()
            continue
        case "--cache s":
            max_len = len(max(get_cache().keys(), key=len)) if get_cache().keys() else 0
            print("{")
            for key, val in get_cache().items():
                print("    ", end = '')
                print(f"{key.ljust(max_len)} : {val}$")
            print("}")
            continue
        case "--search q":
            deep_search = False
            continue
        case "--search d":
            deep_search = True
            continue
        case "--version":
            print(f"current version: {v}")
            continue
    if f"minecraft:{inp}".replace(" ", "_") not in items:
        print("Item not found in shop.")
        continue
    while True:
        n = input(f"Required quantity of {inp} (type exit to quit): ").strip().lower()
        if n == 'exit':
            sys.exit(0)
        try:
            n = int(n)
            if  n > 64 or n < 1:
                print("Enter a value less than or equal to 64.")
                continue
            break
        except ValueError:
            print("The value entered is not a number, please try again.")

    print()
    price_found = get_single_cost(inp, n, deep_search=deep_search)
    print(f"Total price: {price_found[0][0]}$")
    print()
    print(f"Items used for crafting: ")
    for i in price_found[1:][0]:
        name, cost, found, quant = i
        print(f"    item: {name} x {quant}, price: {cost}$ ({'found' if found else 'not found'})")
    print()
    if not keep_cache:
        clear_cache()
