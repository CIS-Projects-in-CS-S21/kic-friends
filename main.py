import asyncio
import os
import logging

from neomodel import config
from grpclib.server import Server

from friends.data.friendslist.mongo_repository import MongoRepository
from friends.server import FriendsService
from friends.data.friendsgraph.neo4j_repository import Neo4jRepository


async def main(*, host='0.0.0.0', port=50051):
    # only one possible neo4j db at a time, will need to share for prod and test
    config.DATABASE_URL = f"bolt://neo4j:{os.environ['NEO4J_PASSWORD']}@graph-neo4j:7687"

    # USE THIS FOR INTEGRATION TEST
    #config.DATABASE_URL = f"bolt://neo4j:test@graph:7687"

    if os.getenv("PROD") is None:
        db_name = "kic-friends-test"
        users_service_url = "test.api.keeping-it-casual.com"
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(lineno)d %(levelname)s:%(message)s')
    else:
        db_name = "kic-friends-prod"
        users_service_url = "api.keeping-it-casual.com"
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(lineno)d %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)
    db = MongoRepository(
        db_name
    )
    rep = Neo4jRepository()

    logger.info("Starting server")
    friends_service = FriendsService(
        db,
        rep,
        users_service_url
    )
    server = Server([friends_service])
    await server.start(host, port)
    await server.wait_closed()


if __name__ == '__main__':
    desired_port = int(os.getenv("PORT"))
    asyncio.run(main(port=desired_port))
