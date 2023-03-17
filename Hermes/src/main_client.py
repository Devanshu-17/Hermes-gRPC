import grpc

import main_pb2
import main_pb2_grpc


class ChatClient:
    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = main_pb2_grpc.ChatServiceStub(self.channel)

    def send_message(self, username, content):
        message = main_pb2.Message(
            username=username,
            content=content
        )
        response = self.stub.SendMessage(message)
        return response

    def receive_messages(self):
        message = main_pb2.Message(username="", content="")
        messages = self.stub.ReceiveMessage(message)
        for message in messages:
            yield f"{message.username}: {message.content}"
