# Stock Notifier

Stock Notifier is a small Python service that retrieves market data, calculates
the latest stochastic oscillator values, and delivers a concise notification
to one or more Telegram chats. It can be run locally or dispatched on a
schedule through GitHub Actions.

## How it works

```text
External scheduler
        |
        v
GitHub Actions  --->  bot.py  --->  yfinance
                           |
                           v
                    Telegram Bot API
```

The default configuration monitors `0050.TW` using six months of weekly data.
The notification includes the most recent `%K` and `%D` values.

## Features

- Downloads historical prices with [`yfinance`](https://github.com/ranaroussi/yfinance)
- Calculates a smoothed stochastic oscillator
- Sends notifications to multiple Telegram chats or channels
- Fails explicitly when configuration or market data is unavailable
- Runs manually or from an external weekday scheduler through GitHub Actions

## Requirements

- Python 3.12 or later
- A Telegram bot token
- A Telegram chat ID or channel username
- A GitHub repository if you want scheduled execution

## Installation

```bash
git clone https://github.com/trust2065/stock-notifier.git
cd stock-notifier

python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Telegram configuration

1. Create a bot with [@BotFather](https://t.me/BotFather) and copy its token.
2. Obtain the destination chat ID. You can use a bot such as
   [@userinfobot](https://t.me/userinfobot), or use a channel username.
3. If you are sending to a channel, add your bot as an administrator with
   permission to post messages.

Create a `.env` file in the project root for local execution:

```dotenv
TELEGRAM_TOKEN=123456789:replace-with-your-bot-token
CHANNEL_ID=@your_channel
```

`CHANNEL_ID` may contain multiple comma-separated destinations:

```dotenv
CHANNEL_ID=@market_alerts,-1001234567890
```

Do not commit `.env` or expose your bot token. The included `.gitignore` is
configured for local environment files.

## Run locally

Run the notifier with:

```bash
python bot.py
```

To send a basic connectivity test without fetching market data:

```bash
python send_message.py
```

## Customize the monitored stock

The symbol, data period, and interval are defined in
[`bot.py`](bot.py):

```python
stock = fetch_stock_information("0050.TW")
```

The fetcher currently defaults to:

| Setting | Default |
| --- | --- |
| Symbol | `0050.TW` |
| Historical period | `6mo` |
| Data interval | `1wk` |

Pass a Yahoo Finance symbol supported by `yfinance` to monitor another
instrument. For example, `AAPL` monitors Apple on the US market.

## GitHub Actions scheduling

The workflow in
[`.github/workflows/stock-notifier.yml`](.github/workflows/stock-notifier.yml)
is intentionally configured with `workflow_dispatch`. GitHub Actions scheduled
workflows may be delayed, so an external scheduler can trigger it reliably.

### Configure repository secrets

In **Settings > Secrets and variables > Actions**, add:

| Secret | Value |
| --- | --- |
| `TELEGRAM_TOKEN` | Telegram bot token |
| `CHANNEL_ID` | Chat ID, channel username, or comma-separated destinations |

### Configure an external scheduler

Using a service such as [cron-job.org](https://cron-job.org/), create a
weekday `POST` request at the desired time. For 09:01 Taiwan time, use the
`Asia/Taipei` timezone and send the request to:

```text
https://api.github.com/repos/trust2065/stock-notifier/actions/workflows/stock-notifier.yml/dispatches
```

Include these headers:

```text
Accept: application/vnd.github+json
X-GitHub-Api-Version: 2022-11-28
Authorization: Bearer <GITHUB_TOKEN>
```

The GitHub token must be a fine-grained token with **Actions: Read and write**
permission for this repository. The request body can be:

```json
{"ref":"main"}
```

Before relying on the scheduler, open **Actions > Stock notifier** and use
**Run workflow** to verify the workflow and repository secrets.

## Project structure

| File | Purpose |
| --- | --- |
| [`bot.py`](bot.py) | Application entry point; fetches data and sends the notification |
| [`fetch_stock.py`](fetch_stock.py) | Downloads prices and calculates stochastic `%K` and `%D` |
| [`send_message.py`](send_message.py) | Sends messages through the Telegram Bot API |
| [`get_env.py`](get_env.py) | Loads and validates Telegram configuration |
| [`requirements.txt`](requirements.txt) | Python dependencies |
| [`.github/workflows/stock-notifier.yml`](.github/workflows/stock-notifier.yml) | Manual GitHub Actions workflow |

## Troubleshooting

- **Missing environment variable:** Confirm that `TELEGRAM_TOKEN` and
  `CHANNEL_ID` are set in `.env` locally or as GitHub Actions secrets.
- **Telegram send failure:** Verify the destination ID and confirm that the bot
  can post to the target channel or chat.
- **No stock data found:** Check the Yahoo Finance symbol and try again later.
- **Workflow does not start:** Confirm the workflow file is on the selected
  branch and that the GitHub token has Actions write permission.
