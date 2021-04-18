
class Region:
    
    def __init__(self, code,  name, port):
        self.code = code
        self.name = name
        self.port = port


class DynamoDB:

        def __init__(self, regions):
            self.regions = regions