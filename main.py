from imapclient import IMAPClient
import yaml
from datetime import datetime, timedelta

with open('config.yml') as f:
    data = yaml.load(f)
    HOST = data['HOST']
    USERNAME = data['USERNAME']
    PASSWORD = data['PASSWORD']

server = IMAPClient(HOST, use_uid=True)
server.login(USERNAME, PASSWORD)
server.select_folder('INBOX')

timeout = 30
connection_refresh_sec = 60 * 10
while True:
    # Start IDLE mode
    server.idle()
    print("Connection is now in IDLE mode")
    try:
        for i in range(connection_refresh_sec // timeout):
            last_check_datetime = datetime.now() - timedelta(minutes=5)
            # The delay of push notification from the server is larger than timeout (30sec), so you have to subtract several minutes.
            responses = server.idle_check(timeout=timeout)
            if responses:
                server.idle_done()
                messages = server.search(['SINCE', last_check_datetime])
                print(messages)
                fetched_messages_meta_dict = server.fetch(
                    messages, ['INTERNALDATE'])
                to_fetch_body_messages_list = []
                for key, meta in fetched_messages_meta_dict.items():
                    print(meta)
                    if meta[b'INTERNALDATE'] >= last_check_datetime:
                        print('added')
                        to_fetch_body_messages_list.append(key)
                res = server.fetch(to_fetch_body_messages_list,
                                   ['BODY.PEEK[TEXT]'])
                print(res)
                server.idle()
            print("Server sent:", responses if responses else "nothing")
    except KeyboardInterrupt:
        break
    server.idle_done()
    print("Disconnected")

print("\nIDLE mode done")
server.logout()