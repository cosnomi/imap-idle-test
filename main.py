from imapclient import IMAPClient
import yaml

with open('config.yml') as f:
    data = yaml.load(f)
    HOST = data['HOST']
    USERNAME = data['USERNAME']
    PASSWORD = data['PASSWORD']

server = IMAPClient(HOST)
server.login(USERNAME, PASSWORD)
server.select_folder('INBOX')

timeout = 30
connection_refresh_sec = 60 * 10
while True:
    # Start IDLE mode
    server.idle()
    print("Connection is now in IDLE mode")
    try:
        for i in range(connection_refresh_sec//timeout):
                responses = server.idle_check(timeout=timeout)
                print("Server sent:", responses if responses else "nothing")
    except KeyboardInterrupt:
        break
    server.idle_done()
    print("Disconnected")

print("\nIDLE mode done")
server.logout()