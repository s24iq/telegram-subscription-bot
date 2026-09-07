# Telegram Channel Subscription Management Bot

An automated access-control system built with **Python 3** and **aiogram 3** to manage private Telegram channel memberships, dynamic single-use invitations, and time-based access revocation.

## Architecture & Flowchart

```text
[ User / Client ] 
       │
       │  1. /start & Request Access
       ▼
[ Telegram Bot (aiogram 3) ] ─── 2. Generate Single-Use Link ───► [ Private Channel ]
       │                                                                  ▲
       │  3. Delivers Exclusive Invite Link                               │
       ▼                                                                  │
[ User Joins Channel ] ───────────────────────────────────────────────────┘

[ Background Scheduler ]
       │
       │  4. Scans Active Subscriptions (Every hour)
       ▼
[ If Expired ] ─── 5. Ban & Unban (Revoke Access) ───► [ Kicked from Channel ]
       │
       └─────────► 6. Send Renewal Notification to User
```
## Features

* **Dynamic Single-Use Invite Links**: Generates exclusive invite links via Telegram Bot API with a strict member usage limit (`member_limit=1`) to prevent unauthorized link sharing.
* **Automated Expiry & Access Revocation**: Background asynchronous scheduler tracks active subscription periods and automatically removes expired users (`ban_chat_member` / `unban_chat_member`).
* **Self-Service Member Portal**: Inline interactive keyboard for members to verify remaining membership days and initiate renewals directly.
* **Asynchronous Architecture**: High-concurrency runtime powered by `asyncio` and non-blocking I/O.

## Tech Stack

* **Language**: Python 3.10+
* **Framework**: aiogram 3.x
* **Network & Concurrency**: asyncio, aiohttp

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/telegram-subscription-bot.git](https://github.com/your-username/telegram-subscription-bot.git)
   cd telegram-subscription-bot

1. Set up a virtual environment:

python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

2. Install dependencies:

pip install -r requirements.txt

3. Configuration:

Assign your Telegram bot token to BOT_TOKEN.

Set your private channel ID in CHANNEL_ID.

Ensure the bot has administrative permissions in the target channel (Invite Users via Links, Ban Users).

4. Run the bot:
python bot.py
