# Donut SMP Auction Crafting Calculator

A command-line interface (CLI) tool developed in Python to calculate the total crafting cost of any Minecraft item in real-time, based on the economy prices of the Donut SMP server (donut.auction). 

The real strength of this project? It was created to solve the problem of the recent shutdown of the Donut SMP public API. 
While other calculators have stopped working, this script operates completely independently by extracting prices directly from web pages via Web Scraping, making craft calculations convenient and automatic again for all players.

## Main Features

* Post-API Solution: The program does not need the official API to work. It autonomously reads data from the site by simulating a normal user, ensuring calculations continue to work despite server-side blocks.
* Recursive Recipe Resolution: Automatically calculates the entire crafting tree of an item down to the base materials, interfacing with the official PrismarineJS datasets.
* Real-time Web Scraping: Uses Playwright (headless Chromium) to navigate the donut.auction site and extract the updated minimum prices.
* Multithreading: Implements an asynchronous interface with a visual loading bar that does not block the execution of network requests.
* Cache Management: Optimizes execution times and network resources by storing the prices of items already searched during the session.

## Basic Usage (For those who just want to use the program)

If you are not a developer and just want to have a working calculator again:
1. Go to the "Releases" section on the right side of this GitHub page.
2. Download the latest version of the available `.zip` file.
3. Extract the entire folder contained in the ZIP file to your desktop (or wherever you prefer).
4. Enter the extracted folder, launch the `.exe` file, and follow the on-screen instructions. No complex configuration is required.

## Developer Installation (From source code)

To run the Python code directly or to compile it, you need to have Python 3.8+ installed.

1. Clone the repository:
   git clone https://github.com/mxrfp/donutSMP-craft-price-founder.git
   cd donutSMP-craft-price-founder

2. Install the required libraries:
   pip install playwright

3. Install browsers for Playwright:
   playwright install chromium

4. Run the main script:
   python main.py

## CLI Commands and Cache Management

The application includes a caching system to avoid searching for the same item on the internet multiple times. By default, the cache is cleared after each new search, but it can be managed using specific commands.

Warning: Commands must be entered when the item NAME is requested, not the quantity.

* --cache c : Completely clears the current cache.
* --cache k : Tells the script to keep the cache at the end of the search. Useful if you need to search for multiple items in a row that share the same materials (e.g., iron sword and iron pickaxe).
* --cache !k : Disables cache keeping (returns to the default behavior of clearing it at the end of the search).
* --cache s : Displays the current contents of the cache and the saved prices on the screen.
* exit : Safely closes the program.

## Execution Example

----------------------------------------------------------------------------------------------------
                                FIND PRICE ON DONUTSMP.AUCTION
----------------------------------------------------------------------------------------------------

[X] Type the name of the item to find the crafting price.

----------------------------------------------------------------------------------------------------
Item name (exit to quit): diamond pickaxe
Required quantity of diamond pickaxe (exit to quit): 1

Searching for the price of stick...
|————————————————————| 2.7
Price of stick found. (0.5$ x 2)

Searching for the price of diamond...
|————————————————————| 2.7
Price of diamond found. (150.0$ x 3)

Price found for crafting diamond pickaxe x 1: 451.0$

## Disclaimer

This tool was created for purely educational purposes, to help players following the removal of the API. It is in no way affiliated with, authorized by, or supported by Donut SMP, donut.auction, or Mojang AB. The software simply simulates normal web browsing to extract public information.
