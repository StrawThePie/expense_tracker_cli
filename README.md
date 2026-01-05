## Expense Tracker (CLI + Filesystem)

A simple expense tracker built as a command-line application in Python that lets you add, update, delete, and view expenses.

All data is sstored as JSON files on the filesystem instead of using a database, which keeps the project lightweight and easy to understand.

Created for https://roadmap.sh/projects/expense-tracker

___

## Features 

- ### Expense management:

    - Add a new expense with amount, description, category, and date.
    - View a list of all recorded expenses.
    - Update an existing expense by its ID.
    - Delete an expense by its ID.
  
- ### Summaries:

    - Summary of all expenses  (total, count, average amount).
    - Monthly summary for a specific month of the current or given year. 
    - Category-based summary showing total and count for a category.

- ### Category filtering:

    - List only the expenses that belong to a specific category.

- ### Budget tracking:

    - Set a monthly budget for a given month and year.
    - View budget status for a month (total spent, budget, remaining).
    - Show a warning when the total spent exceeds the monthly budget.

- ### Export:

    - Export all expenses to a CSV file that can be opened in Excel or Google Sheets.

- ### File-based storage:

    - Expenses stored in ```expenses.json```.
    - Budgets stored in ```budgets.json```.

___

## Tech Stack

- ### Python 3
- ### Standard library only:
    
    - ```argparse``` for command-line parsing
    - ```json``` for data storage
    - ```os``` for filesystem checks
    - ```datetime``` for dates
    - ```csv``` for CSV export

___

## Project Structure

```text
project-root/
│
├── expense_tracker.py   # Main CLI application
├── expenses.json        # JSON data file storing all expenses
├── budgets.json         # JSON data file storing monthly budgets
└── README.md            # Project documentation
```

### Example ```expenses.json``` entry:

```text
[
  {
    "id": 1,
    "amount": 9.99,
    "description": "Coffee",
    "category": "Food",
    "date": "2026-01-05"
  }
]
```

### Example ```budgets.json```:

```text
{
  "2026-01": 500.0
}
```

___

## Getting Started

### Prerequisites

- Python 3 installed on your system

    Check with:
    ```text
    python --version
    ```
    or

    ```
    python3 --version  
    ```
### Installation

1. Clone the repository:
    ```text
    git clone https://github.com/StrawThePie/expense_tracker_cli.git
    cd expense_tracker_cli
    ```
2. Ensure the data files exist (they will be created automatically if missing):

    - ```expenses.json```
    - ```budgets.json```

No additional dependencies are required beyond the Python standard library.

___

### Commands

All commands are run from the project directory using:

```text
python expense_tracker.py <command> [options]
```

(Use ```python3``` instead of ```python``` if required by your environment)

#### Add an expense

```text
python expense_tracker.py add \
  --amount 12.50 \
  --description "Lunch" \
  --category Food \
  --date 2026-01-05
```

- ```--amount``` (required): Expense amount (must be positive).
- ```--description``` (required): Text description of the expense.
- ```--category``` (optional, default: ```"other"): Category label.
- ```--date``` (optional): Date in ```YYYY-MM--DD``` format. If omitted, today's date is used.

___

#### List all expenses

```text
python expense_tracker.py list
```

Prints each expense with its ID, amount, description, category, and date.

___

#### Update an expense

```text
python expense_tracker.py update <id> [--amount AMOUNT] [--description TEXT] [--category NAME] [--date YYYY-MM-DD]
```

Example:

```text
python expense_tracker.py update 1 --amount 15.00 --description "Dinner" --category Food
```

Only the fields provided are updated. The expense is looked up by its numeric ID.

___

#### Delete an expense

```text
python expense_tracker.py delete <id>
```

Example:

```text
python expense_tracker.py delete 1
```

Removes the expense with the specified ID if it exists.

___

#### Summary of all expenses

```text
python expense_tracker.py summary
```

Shows:

- Total spent.
- Number of expenses.
- Average expense amount.

___

#### Monthly summary

```text
python expense_tracker.py summary-month <month>
```

Examples:

```text
python expense_tracker.py summary-month 1
python expense_tracker.py summary-month 12
```

Uses the current year by default and shows:

- Total spent in that month.
- Number of expenses in that month.

___

#### Category summary

```text
python expense_tracker.py summary-category <category>
```

Example:

```text
python expense_tracker.py summary-category Food
```

Shows the total amount and count of expenses for the given category.

___

#### Filter expenses by category

```text
python expense_tracker.py filter-category <category>
```

Example:

```text
python expense_tracker.py filter-category Transportation
```

Prints only the expenses in the selected category.

___

#### Set a monthly budget

```text
python expense_tracker.py set-budget <month> <year> <amount>
```

Example:

```text
python expense_tracker.py set-budget 1 2026 500
```

Sets the budget for that month and year combination.

___

#### View budget status

```text
python expense_tracker.py budget-status <month> [--year YEAR]
```

Examples:

```text
python expense_tracker.py budget-status 1
python expense_tracker.py budget-status 1 --year 2026
```

Shows:

- Total spent in that month.
- Budget amount (if set).
- Remaining amount or a warning if the budget is exceeded.

___

#### Export expenses to CSV

```text
python expense_tracker.py export-csv [--filename NAME]
```

Examples:

```text
python expense_tracker.py export-csv
python expense_tracker.py export-csv --filename my_expenses.csv
```

Creates a CSV file with headers: ```id, amount, description, category, date```.

___

Author

StrawThePie