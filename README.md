# haibun

Python Dash + PostgreSQL Web Application for visualizing your finances.

# Features

- List Expenses

- Visualize Subscription (Bar)

- Visualize the value of each account (Stacked Bar Plot)

- Import CSV of Portfolio and Visualize (Treemap and Bar)

| Item | Value |
|---|---|
| Item 1 | 10 |
| Item 2 | 20 |
| Total  | 30 |


# Set up

Create `config.ini`

```ini
[Postgres]
host = 127.0.0.1
port = 5432
dbname = database_name
dbuser = postgres_user
dbpassword = postgres_password

[General]
portfolio_account_name = Account
portfolio_account_type = Portfolio
```
