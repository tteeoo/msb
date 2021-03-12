# For interactions with the minecraft server.

import os
from json import loads, dumps
from socket import AF_INET, socket, SOCK_STREAM

BUFSIZ = 1024
host = os.environ["MSB_HOST"]
port = int(os.environ["MSB_PORT"])

def make(payload):
    return bytes([len(payload)] + payload)

def deserialize(resp):
    for i in range(len(resp)):
        try:
            return loads(str(resp[i:].decode('utf8')))
        except:
            pass

# Should work for 1.7+ (TODO: older versions)
# Pass a bool to return json
def list_ping(return_json):
    pinger = socket(AF_INET, SOCK_STREAM)
    try:
        pinger.connect((host, port))
        # pid, protocol version, host, port (2 bytes), next state
        pinger.send(make([0, 1, len(host)] + [ord(c) for c in host] + [0, 1, 1]))
        pinger.send(make([0]))
        j = deserialize(pinger.recv(BUFSIZ))
        pinger.close()
        if return_json: return j
        return True
    except Exception as e:
        pinger.close()
        print('server down:', e)
        if return_json: return None
        return False
