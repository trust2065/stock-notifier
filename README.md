[雲端排程 (GitHub Actions / Server)] ──> [Python 腳本 (抓資料+算KD)] ──(觸發)──> [Line / Telegram API] ──> [手機彈出通知]

## Telegram creation
1. BotFather > Open > Create > get token
2. @userinfobot > choose the bot > get chat id
3. 新增一個channel
4. 把bot加入channel 給管理員權限, 權限UI要調成可以傳訊息

## Free cloud scheduling

The bot runs once each weekday on GitHub Actions at 09:00 Taiwan time
(UTC+8). GitHub Actions is free for public repositories and includes a monthly
allowance for private repositories.

1. Push this project to GitHub.
2. In the repository, open **Settings > Secrets and variables > Actions**.
3. Add repository secrets named `TELEGRAM_TOKEN` and `CHANNEL_ID`.
4. Open **Actions > Stock notifier** and use **Run workflow** to test it.

The scheduled workflow is in
[`.github/workflows/stock-notifier.yml`](.github/workflows/stock-notifier.yml).
