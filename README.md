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

1. Start PostgreSQL server

2. Create database and tables

```shell
psql postgresuser
CREATE DATABASE database_name;
\c databasename postgres_user
\i init.sql

\l
\dt
```

3. Create `config.ini`

```ini
[Postgres]
host = 127.0.0.1
port = 5432
dbname = database_name
dbuser = postgres_user
dbpassword = postgres_password

[csv]
currency_symbol = $
item_column = Item
value_column = Value
skip_item = Total

[General]
portfolio_account_name = Account
```

4. Start Application

