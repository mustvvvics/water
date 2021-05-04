import os
import sys
import time
import json
import struct
import socket
import base64
import requests
from pathlib import Path
from base64 import b64encode

from tcpcommon import device, printT, bufferSize, getTime

def sendData(device, data, waitReply=False):
    payload = {
        'timestamp': getTime(),
        'source': socket.gethostname(),
        'data': data
    }
    payloadJson = json.dumps(payload).encode("utf-8")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5.0)
            # printT(f"Connecting to {device}.")
            s.connect(device)

            # printT("Sending json ...")
            s.sendall(struct.pack(">I", len(payloadJson)))  # send server the length of json
            s.sendall(payloadJson)                          # send server the json
            # printT("Send Success.")

            if waitReply:
                # printT("Waiting for reply...")
                try:
                    msg = s.recv(1024)
                    if not msg:
                        return "Received None."
                    return msg
                except:
                    # printT('Error: Timeout while waiting for replying!')
                    return False
            return True
    except socket.timeout:
        # printT("Error: Send timeout.")
        return "Error: Timeout"
    except KeyboardInterrupt:
        # printT("Terminated by user.")
        sys.exit()
    except:
        raise
