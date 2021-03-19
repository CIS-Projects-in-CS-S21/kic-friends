import asyncio
import os
import logging

from friends.data.friendslist.mongo_repository import MongoRepository
from friends.server import FriendsService
from grpclib.server import Server


async def main(*, host='0.0.0.0', port=50051):
    if os.getenv("PROD") is None:
        db_name = "kic-friends-test"
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(lineno)d %(levelname)s:%(message)s')
        logger = logging.getLogger(__name__)
        logger.info("Running test")
    else:
        db_name = "kic-friends-prod"
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(lineno)d %(levelname)s:%(message)s')
        logger = logging.getLogger(__name__)
    db = MongoRepository(
        db_name
    )

    logger.info("Starting server")
    server = Server([FriendsService(db)])
    await server.start(host, port)
    await server.wait_closed()


if __name__ == '__main__':
    desired_port = int(os.getenv("PORT"))
    asyncio.run(main(port=desired_port))
