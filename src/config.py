from models.dynamodb import DynamoDB
from const import ddb_regions


ddb_config = DynamoDB([r for _, r in ddb_regions.items()])