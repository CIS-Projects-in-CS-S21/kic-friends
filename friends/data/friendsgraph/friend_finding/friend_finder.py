import logging
from friends.data.friendsgraph.friend_finding.priority_queue import HeapQueue

from friends.data.friendsgraph.repository import Repository

logger = logging.getLogger(__name__)


class FriendFinder:

    def __init__(self, graph: Repository):
        self.graph = graph

    def _dijkstra_loop(self, priority_q: HeapQueue, distances: dict):
        dist, cur_id = priority_q.remove_top()
        current_neighbors = self.graph.get_friends(cur_id)
        for neighbor in current_neighbors:
            conn_weight = self.graph.get_connection(cur_id, neighbor)
            # not a novel node, need to check if this path is actually an improvement
            if neighbor in distances:
                dist_with_cur = dist + conn_weight
                if dist_with_cur < distances[neighbor]:
                    distances[neighbor] = dist_with_cur
                    priority_q.decrease_weight(neighbor, dist_with_cur)
            # novel node, any path length is better than infinity, also need to insert into queue rather than
            # decrease weight
            else:
                dist_with_cur = dist + conn_weight
                distances[neighbor] = dist_with_cur
                priority_q.insert(neighbor, dist_with_cur)

    def dijkstra(self, starting_node_id: int):
        # map user id to distance, also seconds as a set to let us know if
        # we have found a new node
        distances = {
            starting_node_id: 0
        }

        # currently just a heap queue, technically fibonacci is faster but that's only with a large number of
        # nodes since it has a lot of overhead... also programming time is a cost
        priority_q = HeapQueue()

        priority_q.insert(starting_node_id, 0)

        while len(priority_q) > 0:
            self._dijkstra_loop(priority_q, distances)

        return distances

    def get_recommendations(self, num_recommendations: int, target_uid: int):
        distances = self.dijkstra(target_uid)

        # I assume this can be done better than a sort with DP but that's an optimization for later
        # if this is an issue
        nodes = list(distances.keys())
        nodes.sort(key=lambda x: distances[x], reverse=True)

        recs = list()
        while len(recs) < num_recommendations and len(nodes) > 0:
            user_id = nodes.pop()
            # check if the node is either the target or they are already friends
            if not (target_uid == user_id or self.graph.get_connection(target_uid, user_id) is not None):
                recs.append(user_id)
        return recs


