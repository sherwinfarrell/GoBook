from models.dynamodb import DynamoDB, Region
from const import ddb_regions


ddb_config = DynamoDB([
    Region('eu-west-1', 'Ireland', '8000'),
    Region('eu-central-1', 'Frankfurt', '8001'),
    Region('eu-north-1', 'Stockholm', '8002')
])