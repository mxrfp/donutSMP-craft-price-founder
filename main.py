from functions_and_scraping import get_single_cost, clear_cache, get_cache
import sys

print("-"*100)
print()
print("TROVA PREZZO SU DONUTSMP.AUCTION".center(100))
print()
print("-"*100)
print()
print("[X] Digita il nome dell'item per trovare il prezzo del craft.")
print()
print("-"*100)

keep_cache = False

while True:
    inp = " ".join(input("Nome dell'item (in inglese) (exit per uscire): ").lower().split())
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
        n = input(f"Quantita' necessaria di {inp} (exit per uscire): ").strip().lower()
        if n == 'exit':
            sys.exit(0)
        try:
            n = int(n)
            if n > 64:
                print("Inserire un valore minore o uguale a 64.")
                continue
            break
        except ValueError:
            print("Il valore inserito non e' un numero, riprovare.")

    print()
    price_found, not_included = get_single_cost(inp, n)
    print(f"Prezzo trovato per il craft di {inp} x {n}: {price_found[0]}$\n" + \
          ((f"(non includendo {' '.join(not_included)} (non trovati/o))") if not_included else ''))
    print()
    if not keep_cache:
        clear_cache()
