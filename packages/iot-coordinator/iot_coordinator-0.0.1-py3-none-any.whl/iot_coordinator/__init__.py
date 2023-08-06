from . import coordinator_pb2
from . import coordinator_pb2_grpc
import grpc
import queue
import ed25519
import base64
import time
import os
from threading import Thread

AUTH_SIGN_PREFIX = "IC_NODE_AUTH_"

def build_auth_info(private_key, grant_info):
    global AUTH_SIGN_PREFIX

    current_time = int(time.time() * 1000)
    payload = (AUTH_SIGN_PREFIX + str(current_time)).encode()

    #print("sign payload: " + str(payload))
    sig = private_key.sign(payload) # sha512 by default?
    #print(sig)

    return coordinator_pb2.AuthInfo(
        grant_info = grant_info,
        time = current_time,
        sig = sig,
    )

class UpMessageQueue:
    def __init__(self, private_key, grant_info):
        self.is_first = True
        self.private_key = private_key
        self.grant_info = grant_info
        self.q = queue.Queue()

    def __iter__(self):
        return self

    def __next__(self):
        item = self.q.get()
        if self.is_first:
            self.is_first = False
            item.auth.CopyFrom(build_auth_info(self.private_key, self.grant_info))
            
        return item

    def put(self, m):
        self.q.put(m)

class PersistentRecvIterator:
    def __init__(self, service, private_key, grant_info, tags):
        self.service = service
        self.private_key = private_key
        self.grant_info = grant_info
        self.tags = tags
        self.recv_iter = self._begin_recv()

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            try:
                return self.recv_iter.__next__()
            except:
                time.sleep(5)
                self.recv_iter = self._begin_recv()

    def _begin_recv(self):
        return self.service.ReceiveMessage(coordinator_pb2.RecvConf(
            tags = self.tags,
            auth = build_auth_info(self.private_key, self.grant_info),
        ))

class Session:
    def __init__(self, remote, private_key, grant_info):
        self.remote = remote
        self.channel = None
        self.service = None
        self.private_key = ed25519.SigningKey(base64.b64decode(private_key))
        self.grant_info = grant_info
        self.up_queue = UpMessageQueue(self.private_key, self.grant_info)

    def start(self):
        self.channel = grpc.insecure_channel(self.remote)
        self.service = coordinator_pb2_grpc.CoordinatorStub(self.channel)
        Thread(target = self._always_submit_message, args = []).start()

    def _always_submit_message(self):
        while True:
            try:
                self.service.SubmitMessage(self.up_queue)
            except Exception as e:
                print(e)

            self.up_queue.is_first = True
            time.sleep(5)

    def submit_message(self, recipient, tag, body):
        self.up_queue.put(coordinator_pb2.UpMessage(
            recipient = recipient,
            tag = tag,
            body = body,
        ))

    def receive_message(self, tags):
        return PersistentRecvIterator(self.service, self.private_key, self.grant_info, tags)
