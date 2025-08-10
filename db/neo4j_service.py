class Neo4jService:
    def __init__(self,driver):
        self.driver = driver

    def close(self):
        self.driver.close()
    
    def run_query_for_videos(self,query,list_of_entities:dict,channelId:str):
        with self.driver.session() as session:
            result = session.run(query,
                    {"list_of_entities": list_of_entities,
                     "channelId": channelId
                    })
            for res in result:
                print(res)

    def run_query(self, query: str, kwargs: dict = None, list_of_entities: list = None):
        parameters = {}

        if kwargs:
            parameters.update(kwargs)
        if list_of_entities:
            parameters["list_of_entities"] = list_of_entities

        with self.driver.session() as session:
            if parameters:
                session.run(query, parameters)
            else:
                session.run(query)
    
