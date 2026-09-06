import re
from playwright.sync_api import sync_playwright, TimeoutError
import urllib.request
import json
from collections import Counter
from typing import Dict, List, Tuple, Union
import threading
import time
import sys
import os
import requests

if getattr(sys, 'frozen', False):
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = os.path.join(sys._MEIPASS, "ms-playwright") #type: ignore

def get_latest_supported_minecraft_data_version() -> str:

    versions_url = "https://raw.githubusercontent.com/PrismarineJS/minecraft-data/master/data/pc/common/versions.json"
    
    try:
        response = requests.get(versions_url, timeout=5)
        response.raise_for_status()
        supported_versions = response.json()
        
     
        return supported_versions[-1]
    except Exception:
  
        return "1.20"

v = get_latest_supported_minecraft_data_version()

def parse_remote_minecraft_recipes(version: str = v) -> Dict[str, List[Union[Tuple[str, int], int]]]:
  
    data_url = f"https://raw.githubusercontent.com/PrismarineJS/minecraft-data/master/data/pc/{version}"
    

    items_request = urllib.request.urlopen(f"{data_url}/items.json")
    items_catalog = json.loads(items_request.read().decode('utf-8'))
    id_map = {item['id']: f"minecraft:{item['name']}" for item in items_catalog}
    
    recipes_request = urllib.request.urlopen(f"{data_url}/recipes.json")
    raw_recipes = json.loads(recipes_request.read().decode('utf-8'))
    
    parsed_dictionary: Dict[str, List[Union[Tuple[str, int], int]]] = {}
    
    for target_id_str, recipe_options in raw_recipes.items():
        target_id = int(target_id_str)
        target_name = id_map.get(target_id, f"minecraft:unknown_{target_id}")
        
        for recipe in recipe_options:
            extracted_ingredients = []
            yield_count = 1
            
     
            if "result" in recipe and isinstance(recipe["result"], dict):
                yield_count = recipe["result"].get("count", 1)
            
      
            if "inShape" in recipe:
                for row in recipe["inShape"]:
                    for cell in row:
                        if cell is not None and cell in id_map:
                            extracted_ingredients.append(id_map[cell])
            
         
            elif "ingredients" in recipe:
                for ingredient in recipe["ingredients"]:
                    if isinstance(ingredient, int) and ingredient in id_map:
                        extracted_ingredients.append(id_map[ingredient])
                    elif isinstance(ingredient, dict) and "id" in ingredient and ingredient["id"] in id_map:
                        extracted_ingredients.append(id_map[ingredient["id"]])
            
  
            if extracted_ingredients:
                counts = Counter(extracted_ingredients)
                recipe_value: List[Union[Tuple[str, int], int]] = [(name, count) for name, count in counts.items()]
       
                recipe_value.append(yield_count)
                
                if target_name not in parsed_dictionary:
                    parsed_dictionary[target_name] = recipe_value
                    
    return parsed_dictionary

def get_prices(browser, item: str) -> list[str]:
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 720}
    )
    page = context.new_page()
    
    page.goto("https://donut.auction/", wait_until="domcontentloaded")
    
    search_input = page.get_by_role("combobox", name="Search auction items...")
    search_input.fill(item)
    
    page.get_by_role("option", name=re.compile(rf"^{re.escape(item)}\s+\$", re.IGNORECASE)).click(force=True, timeout=4000)

    locator_rows = page.locator('tbody[data-slot="table-body"] tr[data-slot="table-row"]')
    locator_rows.first.wait_for(state="attached", timeout=7000)

    rows = locator_rows.all()
    data = [row.inner_text().split("\t") for row in rows]

    context.close()
    return data

stop_event = threading.Event()
estimate = 2.7

def print_loading_bar(item_name, lenght=20):
    print(f"Searching price for {item_name}...")
    interval = estimate/lenght
    complete = "".join(["—" for _ in range(lenght)])
    state = [" " for _ in range(lenght)]
    time1 = time.perf_counter()
    print("\r|", end="", flush=True)
    indx = 0
    while not stop_event.is_set():
        state[indx] = "—"
        indx += 1
        state_string = "".join(state)
        time.sleep(interval)
        print(f"\r|{state_string}| {(round(time.perf_counter() - time1, 1))}", end="", flush=True)
        if indx == lenght:
            break
    print(f"\r|{complete}| {(round(time.perf_counter() - time1, 1))}", end="", flush=True)



def stop_thread(th: threading.Thread, s_e):
    s_e.set()
    th.join()
    s_e.clear()

items = parse_remote_minecraft_recipes()

def expand_craft(craft, name, visited = None, needed = 1):
    if visited is None:
        visited = set()
    extended_name = f"minecraft:{name.lower().replace(' ', '_')}"
    if isinstance(craft, list):
        normalized = [(i[0].replace("minecraft:", "").replace("_", " "), i[1]/craft[-1]) for i in craft[:-1:]]
        return [expand_craft((i[0], i[1]*needed), i[0], visited=visited.copy()) for i in normalized]
    elif isinstance(craft, tuple):
        if items.get(extended_name) and craft not in visited:
            visited.add(craft)
            return expand_craft(items.get(extended_name), name, visited=visited.copy(), needed=craft[1])
        else:
            return craft

def flatten(lst) -> list:
    if not isinstance(lst, list):
        return [lst]
    if not lst:
        return []
    return flatten(lst[0]) + flatten(lst[1:])

cache = {}

def clear_cache():
    global cache
    cache = {}

def get_cache():
    global cache
    return cache

wood_logs = {

    "oak log",
    "spruce log",
    "birch log",
    "jungle log",
    "acacia log",
    "dark oak log",
    "mangrove log",
    "cherry log",
    "pale oak log",

}

def get_dict(price_list):
    price_dict = {}
    for i in price_list:
        name, cost, found = i
        if found:
            price_dict[cost] = [name, found]
    if not price_dict:
        price_dict[price_list[0][1]] = [price_list[[0][0]], False]
    return price_dict

def get_price(name, quantity, _check = True, deep_search = True):
    found = True
    if deep_search:
        if name in wood_logs and _check:
            price_list = [get_price(i, quantity, _check=False) for i in wood_logs]
            price_dict = get_dict(price_list)
            min_found = min(price_dict.keys())
            return [price_dict[min_found][0], min_found, price_dict[min_found][1]]
        elif name in {'coal', 'charcoal'} and _check:
            price_dict = {get_price(i, quantity, _check=False)[1]:i for i in {'coal', 'charcoal'}}
            min_found = min(price_dict.keys())
            return [price_dict[min_found], min_found, found]
    item_thread = threading.Thread(target=print_loading_bar, args=(name,))
    item_thread.start()
    cost = float('inf')
    item_data = []
    if name in cache:
        cost = cache[name]
    else:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                item_data = get_prices(browser, name)
                browser.close()
        except TimeoutError:
            stop_thread(item_thread, stop_event)
            print(f"\nYou cannot buy {name} (not present in the shop).")
            found = False
            cost = 0

        for element in item_data:
            cost = min(cost, int(element[1].strip().replace(",", ""))/int(element[2]))
            cache[name] = cost
            
    stop_thread(item_thread, stop_event)
    print(f"\nPrice for {name} found. ({round(cost * quantity, 1)}$ x {quantity})\n")
    return [name, cost, found]


def get_single_cost(item, needed = 1, deep_search = True):
    global_name = f"minecraft:{item.lower().replace(' ', '_')}"
    if not items.get(global_name):
        item_craft = [(item, 1)]
    else:
        item_craft = flatten(expand_craft(items.get(global_name), item))
    price = 0
    ingrediens_used = []
    for ingredient in item_craft:
        name, quant = ingredient
        result = get_price(name, quant, deep_search=deep_search)
        price += result[1]
        ingrediens_used.append(result + [quant])

    return [[round(price * needed, 1)], ingrediens_used]

