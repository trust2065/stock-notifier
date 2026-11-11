[雲端排程 (GitHub Actions / Server)] ──> [Python 腳本 (抓資料+算KD)] ──(觸發)──> [Line / Telegram API] ──> [手機彈出通知]

## Telegram creation
1. BotFather > Open > Create > get token
2. @userinfobot > choose the bot > get chat id
3. 新增一個channel
4. 把bot加入channel 給管理員權限, 權限UI要調成可以傳訊息

## Free cloud scheduling

The workflow is triggered by an external cron service at 09:01 Taiwan time
(UTC+8) on weekdays. GitHub Actions' built-in scheduled workflows can be
delayed or skipped, so this repository keeps only `workflow_dispatch`.

1. Push this project to GitHub.
2. In the repository, open **Settings > Secrets and variables > Actions**.
3. Add repository secrets named `TELEGRAM_TOKEN` and `CHANNEL_ID`.
4. Configure cron-job.org to send a `POST` request on weekdays at 09:01 in
   the `Asia/Taipei` timezone to:
   `https://api.github.com/repos/trust2065/stock-notifier/actions/workflows/stock-notifier.yml/dispatches`
5. Add an `Authorization` header using the Bearer scheme and your GitHub
   fine-grained token. The token needs **Actions: Read and write** permission
   for this repository.
6. Add `Accept: application/vnd.github+json` and
   `X-GitHub-Api-Version: 2022-11-28` request headers.
7. Open **Actions > Stock notifier** and use **Run workflow** to test it.

The workflow is in
[`.github/workflows/stock-notifier.yml`](.github/workflows/stock-notifier.yml).
