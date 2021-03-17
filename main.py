from friends.server import FriendsService
from grpclib.server import Server


HOST = "0.0.0.0"
PORT = 50051
server = Server([FriendsService()])
await server.start(HOST, PORT)
await server.serve_forever()