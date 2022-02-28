from re import I
import requests
import json
from datetime import datetime
from config import PSID, ACCESS_TOKEN, LOG_FILE, MESSAGE

def send(message: str, id: str, access_token: str) -> bool:
    msgObj = {
        "messaging_type": "MESSAGE_TAG",
        "tag": "ACCOUNT_UPDATE",
        "recipient": { "id": id },
        "message": { "text": message }
    }
    headers = {'content-type':  'application/json'}
    url = "https://graph.facebook.com/v13.0/me/messages?access_token={}".format(access_token)
    response = requests.post(url, data=json.dumps(msgObj), headers=headers)
    return response

def read_log(filename: str):
    # Read & return a JSON file. Create the file if it doesn't exist.
    data = None
    try:
        with open(filename, 'r') as json_file:
            json_file.seek(0)
            data = json.load(json_file)
    except:
        write_log(filename, [])
        return read_log(filename)
    return data

def write_log(filename, data):
    # Write a json dictionary to file
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def main():
    log = read_log(LOG_FILE)
    now = datetime.now()

    def send_and_log(message=MESSAGE):
        r = send(message, PSID, ACCESS_TOKEN)    
        success = "message_id" in r.json()
        log.append({
            "timestamp": now.isoformat(),
            "success": success,
            "response": r.text
        })

    if not log:
        # Fresh start
        send_and_log()
    elif datetime.fromisoformat(log[-1]['timestamp']).date() != now.date():
        # Send notice on new day at the right time
        if now.time().hour >= 12 and now.time().minute >= 29:
            send_and_log()
    elif log[-1]['success'] == False:
        # Retry after failure
        send_and_log() 

    if len(log) > 50:
        # Trim log
        log = [log[-1]]

    write_log(LOG_FILE, log)


if __name__ == "__main__":
    main()
