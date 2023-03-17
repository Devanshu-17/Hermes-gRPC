import grpc
import time

from concurrent import futures
import main_pb2
import main_pb2_grpc


class ChatService(main_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.messages = []

    def SendMessage(self, request, context):
        message = main_pb2.Message(
            username=request.username,
            content=request.content
        )
        self.messages.append(message)
        return message

    def ReceiveMessage(self, request, context):
        for message in self.messages:
            yield message


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    main_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
