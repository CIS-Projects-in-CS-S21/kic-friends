import sys
import asyncio

from grpclib.client import Channel

from proto.common_pb2 import Date
from proto.users_grpc import UsersStub
from proto.users_pb2 import AddUserRequest


async def main():
    location = "test.api.keeping-it-casual.com"

    if len(sys.argv) > 1:
        location = sys.argv[1]

    async with Channel(location, 50051) as channel:
        users_client = UsersStub(channel)
        res = await users_client.AddUser(
            AddUserRequest(
                email="testuser@gmail.com",
                desiredUsername="testuser",
                desiredPassword="testpass",
                birthday=Date(
                    year=1998,
                    month=8,
                    day=21,
                ),
                city="test"
            )
        )

        print(res)

        res = await users_client.AddUser(
            AddUserRequest(
                email="testuser1@gmail.com",
                desiredUsername="testuser1",
                desiredPassword="testpass",
                birthday=Date(
                    year=1998,
                    month=8,
                    day=21,
                ),
                city="test"
            )
        )

        print(res)

        res = await users_client.AddUser(
            AddUserRequest(
                email="testuser2@gmail.com",
                desiredUsername="testuser2",
                desiredPassword="testpass",
                birthday=Date(
                    year=1998,
                    month=8,
                    day=21,
                ),
                city="test"
            )
        )

        print(res)

        res = await users_client.AddUser(
            AddUserRequest(
                email="testuser3@gmail.com",
                desiredUsername="testuser3",
                desiredPassword="testpass",
                birthday=Date(
                    year=1998,
                    month=8,
                    day=21,
                ),
                city="test"
            )
        )

        print(res)

if __name__ == '__main__':
    asyncio.run(main())
