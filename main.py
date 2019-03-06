from imapclient import IMAPClient
import yaml
from datetime import datetime, timedelta
from last_fetched_uid_mock import get_last_fetched_uid, set_last_fetched_uid

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
            responses = server.idle_check(timeout=timeout)
            if responses:
                print("Server sent:", responses if responses else "nothing")
                server.idle_done()
                print('last uid: {}'.format(get_last_fetched_uid()))
                messages = server.search(
                    ['UID', str(get_last_fetched_uid() + 1) + ':*'])
                print('mes: {}'.format(messages))
                if len(messages) == 0:
                    continue
                set_last_fetched_uid(messages[-1])
                res = server.fetch(messages, ['BODY.PEEK[TEXT]'])
                print(res)
                server.idle()
    except KeyboardInterrupt:
        break
    server.idle_done()
    print("Disconnected")

print("\nIDLE mode done")
server.logout()