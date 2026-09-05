from functions_and_scraping import get_single_cost, clear_cache, get_cache
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

while True:
    inp = " ".join(input("Item name (in English) (type exit to quit): ").lower().split())
    if inp == 'exit':
        sys.exit(0)
    elif inp == "--cache c":
        clear_cache()
        continue
    elif inp == "--cache k":
        keep_cache = True
        continue
    elif inp == "--cache !k":
        keep_cache = False
        clear_cache()
        continue
    elif inp == "--cache s":
        max_len = len(max(get_cache().keys(), key=len)) if get_cache().keys() else 0
        print("{")
        for key, val in get_cache().items():
            print("    ", end = '')
            print(f"{key.ljust(max_len)} : {val}$")
        print("}")
        continue
    while True:
        n = input(f"Required quantity of {inp} (type exit to quit): ").strip().lower()
        if n == 'exit':
            sys.exit(0)
        try:
            n = int(n)
            if n > 64:
                print("Enter a value less than or equal to 64.")
                continue
            break
        except ValueError:
            print("The value entered is not a number, please try again.")

    print()
    price_found, not_included = get_single_cost(inp, n)
    print(f"Price found for crafting {inp} x {n}: {price_found[0]}$\n" + \
          ((f"(not including {' '.join(not_included)} (not found))") if not_included else ''))
    print()
    if not keep_cache:
        clear_cache()
