# The Swamp — Horde WoW Forever Discord

Python `discord.py` bot for creating the guild server layout, self-assigning **main class / spec / raid role**, and managing raid signups.

## 1. Create the Discord server

In Discord, click **Add a Server → Create My Own**, name it **The Swamp**, and choose a region-independent voice setup (Discord handles voice regions automatically). Keep the server owner account secure with 2FA.

## 2. Create and invite the bot

1. Open https://discord.com/developers/applications and select **New Application**. Name it **Swamp Keeper**.
2. On the **Bot** page, create/reset a bot token and copy it securely. **Never post or commit the token.**
3. Under **Bot → Privileged Gateway Intents**, enable **Server Members Intent**.
4. In **Installation** (or OAuth2 URL Generator), choose guild installation and the scopes **bot** and **applications.commands**. Give the bot **Manage Roles**, **Manage Channels**, **View Channels**, **Send Messages**, **Embed Links**, and **Read Message History**. It also needs **Manage Messages** if you want to expand moderation later. Invite it to your server.
5. In **Server Settings → Roles**, drag the **Swamp Keeper** bot role **above all class, spec, and raid-role roles**. Keep it below officer roles. The bot must not be granted Administrator.
6. Enable **Developer Mode** in Discord Advanced settings, right-click the server icon, choose **Copy Server ID**.

## 3. Install Python dependencies

Requires Python 3.11+.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and replace the placeholders with your **bot token** and **server ID**.

```bash
python bot.py
```

**Keep the bot running** on your own computer, a small VPS, or another always-on Python host for signups to work.

## 4. Run initial setup

In your server, type `/swamp_setup` from an account with **Administrator** permissions. This creates categories, channels, guild roles, and the registration panel in `#choose-your-roles`. It can be run again to add missing items without intentionally deleting existing content.

The `Swamp Council` and `Raid Leader` roles are created but must be **assigned manually** by the server owner. The owner can also rename the top role to `Swamp Lord` if desired.

## 5. Register and create raids

Members use the dropdown in `#choose-your-roles` to choose their **main** class, spec, and one role (Tank / Healer / DPS / Flex). This implementation supports **one main character profile per Discord account**; multi-character alt profiles are not yet implemented.

An officer with `Swamp Council` or `Raid Leader` role can create a raid using:

`/raid_create name:Molten Core starts_at:2026-11-15 01:00 capacity:40`

**Important:** `starts_at` is UTC, not local time. Discord will display the converted local time for each member. For example, 01:00 UTC on Nov 15 is 8:00 PM Eastern on Nov 14.

Members click **Going**, **Tentative**, or **Decline**. The bot shows confirmed players, first-come-first-served waitlist, and tentative players, including class/spec/role. The roster is updated when someone clicks a signup button.

Other commands:

- `/raid_roster raid_id:1` — view a current roster privately
- `/raid_cancel raid_id:1` — officer-only cancellation

## Permissions and operational notes

- **Do not share** `.env`, your bot token, or `swamp.sqlite3` publicly. Back up the SQLite file periodically.
- The bot does not automatically assign officer privileges. Officer access is controlled by manually assigned roles.
- The private officer category is hidden from `@everyone` and shown to `Swamp Council` and `Raid Leader`.
- Discord channel permissions should be reviewed after setup, especially if other roles already existed.
- The signup display is limited by Discord's embed field length; a full 40-person roster may be truncated visually. The database still retains all signups.
- No automated raid reminders, recurring event creation, calendar sync, automatic class-role validation, alt profiles, or signup closing deadlines are included in this initial version. These are possible future upgrades.
- The server setup is idempotent for roles and channel names. Re-running it does not intentionally delete content, but if the role panel is older than the last 100 messages it may post a new panel.
