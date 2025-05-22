# IntelLive Pro 🌍

Real-time Geostrategic Intelligence Platform with Telegram Integration and 3D Visualization


## Key Features 🔑
- 🕵️ Real-time monitoring of strategic Telegram channels
- 🌍 Automatic geolocation using NLP and geocoding
- 🗺️ Interactive 3D visualization with PyDeck/Mapbox
- 📊 Automated report generation with Plotly
- 📌 Critical point marking and selection system
- 🖼️ Media attachment support (images/videos)
- ⚡ Auto-refresh every 60 seconds

## Requirements 📋
- Python 3.10+
- Telegram account with [API ID/HASH](https://core.telegram.org/api/obtaining_api_id)
- (Optional) [Mapbox Access Token](https://docs.mapbox.com/help/getting-started/access-tokens/) for premium styles

## Installation 🚀

### 1. Clone Repository
```bash
git clone https://github.com/your-username/IntelMap.git
cd IntelMap




Telegram Listener Configuration Guide
1. Create a Telegram Application
Go to https://my.telegram.org/auth

Log in with your Telegram account

Click "API development tools"

Fill in the form:

App title: IntelLivePro

Short name: intel_pro

Click "Create application"

Save your credentials:

ini
API_ID = 1234567
API_HASH = 0123456789abcdef0123456789abcdef
2. Configure .env File
Create .env file in project root with:

ini
API_ID=your_api_id_from_step_1
API_HASH=your_api_hash_from_step_1
3. Channel Configuration
For Public Channels:
Add your account to the target channel as admin

Get channel username (e.g., @geopoliticalwatch)

Update config.py:

python
CHANNELS = [
    "geopoliticalwatch",
    "UkraineNewsLive",
    -1001234567890  # For private channels
]
For Private Channels:
Get channel ID:

Forward a message from the channel to @username_to_id_bot

You'll receive format like -100XXXXXXXXXX

Add this ID to CHANNELS in config.py

4. Setup Monitoring Group
Create a new private Telegram group

Add @userinfobot to the group to get group ID

Update MONITOR_GROUP in config.py:

python
MONITOR_GROUP = -1001234567890  # Your group ID
5. Authorization Process
When first running telegram_listener.py:

bash
python telegram_listener.py
You'll be prompted to:

Enter your Telegram phone number (with country code)

Enter verification code sent to Telegram

For 2FA accounts: Enter password (if enabled)

A session file (intel_map_session.session) will be created for future logins.

Required Permissions
Ensure your Telegram account has:

Access to all configured channels/groups

Admin privileges in monitored channels (if restricted)

Message reading permissions in target channels

Troubleshooting Common Issues
1. "Channel Private" Error
log
telethon.errors.rpcerrorlist.ChannelPrivateError
Solution:

Add your account to the private channel as member/admin

For channels you own: Update privacy settings to "Public"

2. FloodWaitError
log
telethon.errors.rpcerrorlist.FloodWaitError: 
A wait of 86000 seconds is required
Solution:

Wait the specified time (24 hours in this example)

Reduce number of channel joins in short periods

3. Message Forwarding Failure
Ensure:

Your account is member of both source channel and target group

The target group allows message forwarding

No content restrictions in group settings

Security Considerations
Use a dedicated Telegram account for monitoring

Never share intel_map_session.session file

Store credentials in .env (not in code)

Use read-only permissions where possible

Final Checklist
API credentials in .env

Channels configured in config.py

Monitoring group ID set

Account added to all channels/groups

Session file generated

Required permissions verified

After completing these steps, the listener should successfully:

Monitor configured channels

Store messages in SQLite database

Forward messages to monitoring group

Process geolocation data

Start the listener with:

bash
python telegram_listener.py
You should see real-time logging of processed messages:

log
2024-03-15 14:30:45 - TelegramListener - INFO - New message from -100123456789
2024-03-15 14:30:47 - TelegramListener - INFO - Message 123 saved to DB
2024-03-15 14:30:49 - TelegramListener - INFO - Found 2 locations in message
