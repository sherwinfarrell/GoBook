from models.dynamodb import Region


MAX_TRIPS_PER_ROUTE = 10

ddb_local_host = 'http://localhost:'


ddb_regions = {
    'Ireland': Region('eu-west-1', 'Ireland', '8000'),
    'Frankfurt': Region('eu-central-1', 'Frankfurt', '8001'),
    'Stockholm': Region('eu-north-1', 'Stockholm', '8002')
}