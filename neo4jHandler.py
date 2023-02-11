import logging
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable


class App:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

        """
            * cypher function has only query objects.
            * can handle the cypher query in the "Utils" class
        """
    def cypher(self, param):
        with self.driver.session() as session:
            res_node = session.execute_read(self._cypher, param)
            _utill_class_obj = Utils(res_node)
            _utill_class_obj.extract_properties_name()

    @staticmethod
    def _cypher(tx, params):
        result = tx.run(params)
        result_list = []
        for data in result:
            result_list.append(data)
        return result_list  # list


class Utils:
    def __init__(self, params: list):
        self.res_node = params

    # print to properties from cypher
    def extract_properties_name(self):
        json_version = {}
        for node_data in self.res_node:
            # for items in node_data.items():
            #     json_version[items[0]] = items[1]
            for key, values in node_data.items():
                print(key, values, end="\n")
            print('├──────────────────────────────────────────────────────────────────────┤')
    
    
    def print_query(self):
        for node_data in self.res_node:
            # for items in node_data.items():
            #     json_version[items[0]] = items[1]
            for key, values in node_data.items():
                print(key, values, end="\n")
            print('├──────────────────────────────────────────────────────────────────────┤')


if __name__ == '__main__':
    from config import connectionInfo
    
    url, user, password = connectionInfo()
    app = App(url, user, password)
    query = "match (n) " \
            "RETURN n limit 25"
            
    app.cypher(query)
    app.close()