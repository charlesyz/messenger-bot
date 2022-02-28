# Facebook Messenger reminder bot

Simple messenger reminder bot that sends periodic messages from a facebook page. 

Currently configured to send a message at 12:30 every day. If the message fails to send (or the computer is offline), the bot will continue to re-attempt until either midnight or the message is sent successfully

## Getting Started

1. Create a `config.py` file in the same folder as `charles_bot.py` with the following information:
```python
PSID="<PSID>"                   # PSID (Page Scoped ID) of the intended recipient
ACCESS_TOKEN="<ACCESS_TOKEN>"   # Access token of the source page
LOG_FILE="log.json"             # the log file where we keep track of the last 50 message requests
MESSAGE = "<MESSAGE>"           # The message to send
```
2. Set up the chrontab
```
crontab -e
*/30 * * * * cd <PATH_TO_DIR>/charles-bot && python3 charles_bot.py
```

This crontab will run the script once every thirty minutes. On every run, the script will:
1. If this is the first time the script was run, send a message and log when it was sent
2. If no message was sent today and it is past 12:29, send a message and log that it was sent
3. If the last message sent today failed, re-try it.

You can change the time that the message is sent at `config.py:52` 
```py
if now.time().hour >= 12 and now.time().minute >= 29:
```

## Setting up the Facebook page & App

1. Enroll as a FB developer: https://developers.facebook.com
2. Set up your Facebook App & Page: https://developers.facebook.com/docs/messenger-platform/getting-started/app-setup
    - The Facebook page can be unpublished
    - Note that you do not need a webhook for this app
    - Take note of the messenger access token that you create in step 3 and save it in the `config.py`
3. Have the intended recipient message your facebook page. One way you can do this is by creating a `Send Message` button on your page and then clicking `Test Button`
    - Note that if your page/app is unpublished, the recipient must be an Editor on your private page **and** must be an Admin, Developer, or Tester of your FB app. Edit roles on your [app dashboard](https://developers.facebook.com/apps)
4. Find the `PSID` of the intended message recipient
    - Get your Page ID from the [messenger settings in your app dashboard](https://developers.facebook.com/apps). Eg: `108593488762456`
    - Go to the [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
    - On the right hand side, select your facebook app and select a page access token for your page (under `user or page`)
    - Retrieve the list of conversations: `GET` -> `<PAGE_ID>?fields=conversations`
    - Given the desired conversation id (eg: `t_000000000000000`), find the list of participants: `GET` -> `<CONVERSATION_ID>?fields=participants` 
    - The result of the query will have the PSID of the conversation participants in the `ID` field. Record this in `config.py`

**FB API Resources**:
- Send Messages API: https://developers.facebook.com/docs/messenger-platform/send-messages
- About PSID: https://developers.facebook.com/docs/messenger-platform/introduction/integration-components
- Conversations Graph API: https://developers.facebook.com/docs/graph-api/reference/v13.0/conversation
- Graph API Explorer: https://developers.facebook.com/tools/explorer
