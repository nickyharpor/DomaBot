# Doma Bot

A Telegram bot to monitor and manage all activities on Doma Testnet.
Get all info you need about listings, offers, tokens, and orders.
Interact and manage notification subscriptions.

## Features

- Multilingual design that easily expands to new languages
- Intuitive UX makes it easy to use by everyone
- Domain name search and event subscription made easy
- Implements a service layer on Doma Multi-Chain Subgraph
- Makes full use of Poll API and Orderbook API

## Requirements

- Python 3.12 or above
- MongoDB
- Telegram bot token

## Installation
Create a `.env` file and set the `ENV` variable to one of the following:
  - `test`
  - `dev`
  - `live`

Setting the environment tells the bot which config to use:
  - `config_test.py`
  - `config_dev.py`
  - `config_live.py`

Fill in the config file with the appropriate values.

Create a virtual environment and install dependencies:

`uv sync`

Run `python bot.py`