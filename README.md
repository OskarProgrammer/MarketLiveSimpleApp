# Market Monitor

A simple desktop application built with PySide6 for monitoring stock prices in real-time. This tool allows you to add stock symbols and view their current price, daily change, and percentage change. The data is automatically refreshed at a set interval.

## Features

-   **Real-time price monitoring:** Fetches and displays the current stock price, last close price, and currency for a given symbol.
-   **Daily performance:** Calculates and shows the price difference and percentage change from the previous day's close.
-   **Visual feedback:** Labels for each stock symbol are color-coded to indicate performance:
    -   **Green:** The stock price has increased since the last close.
    -   **Red:** The stock price has decreased since the last close.
    -   **Gray:** The stock price has not changed or data is unavailable.
-   **Auto-refresh:** Prices are automatically updated every 15 seconds. A countdown timer in the window title shows when the next refresh will occur.
-   **Persistent symbols:** All symbols you add are saved to a `symbols.txt` file, so they will be loaded automatically the next time you run the application.

## Prerequisites

To run this application, you need to have Python and the following libraries installed:

-   `PySide6`
-   `yfinance`

You can install these dependencies using pip:

```bash
pip install PySide6 yfinance
```

## How to Use

1.  **Run the application:**
    Simply double-click the **`run.bat`** file. This will automatically execute the **`main.py`** script and launch the application.

2.  **Add stock symbols:**
    In the application window, type a stock symbol (e.g., `AAPL`, `GOOGL`, `MSFT`) into the input field and click the **"Add symbol"** button. The new symbol will appear in the list, and its data will be displayed.

3.  **Monitor the prices:**
    The application will automatically refresh the prices for all added symbols every 15 seconds. The window title will show a countdown to the next refresh.

## Project Structure

```
├── Icons/
│   └── appIcon.ico
│   └── source.txt
├── source/
│   ├── main.py
│   └── gettingData.py
├── .gitignore
├── LICENSE
├── README.md
├── run.bat
└── symbols.txt
```


-   **`source/main.py` (Main Application File):**
    -   Initializes the main application window and its user interface.
    -   Handles user input for adding new symbols.
    -   Manages the timer for periodic price updates.
    -   Reads and writes stock symbols from a `symbols.txt` file to ensure persistence.
    -   Dynamically creates and updates the labels displaying stock data.

-   **`source/gettingData.py`:**
    -   Contains the `getData()` function, which uses the `yfinance` library to fetch stock information for a given symbol.
    -   Retrieves the current price, last close price, and currency.
    -   Includes error handling to gracefully manage cases where a symbol's data cannot be retrieved.

-   **`run.bat`:**
    -   A batch script located in the project root that provides a convenient way to start the application with a double-click. It likely calls `python source/main.py`.

-   **`symbols.txt`:**
    -   A plain text file where the application stores the stock symbols you've added.
    -   Each symbol is saved on a new line.

### Alias Support for Stock Symbols

The application now allows you to assign custom, more readable names (aliases) to stock symbols. Instead of only seeing the symbol, you can define how it should be displayed.

#### How to Use Aliases

1. In the text input field for adding symbols, type the symbol followed by a space and then the alias (e.g., `CDR.WA CDProjekt`).
2. Click the **"Add symbol"** button.

The application will remember the alias and will display the data in the format: **`Alias(Symbol): current price | difference | percentage change`**.

**Example:**

After entering `CDR.WA CDProjekt`, the application will display:

`CDProjekt(CDR.WA): 120.50 PLN | +2.30 | +1.95 %`

The alias is saved in the `symbols.txt` file along with the symbol and will be loaded automatically each time you run the application.