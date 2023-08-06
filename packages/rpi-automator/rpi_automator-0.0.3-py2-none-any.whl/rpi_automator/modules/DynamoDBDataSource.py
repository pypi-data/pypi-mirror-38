from modules.BaseModule import BaseModule
from dto.ModuleResult import ModuleResult
import boto3
import logging
import time
logger = logging.getLogger()


class DynamoDBDataSource(BaseModule):

    def __init__(self, config):
        BaseModule.__init__(self, config)
        self.reset(config)

    def run(self, module_result):

        if module_result.data is None:
            logger.info("Received empty data for %s", module_result.module)
            return ModuleResult(self)

        data = {
            'created': module_result.timestamp.isoformat(),
            'module_name': module_result.module.name
        }
        data.update(vars(module_result.data))

        updates = {k: {'Action': 'PUT', 'Value': v} for k, v in data.items()}
        epoch = int(time.mktime(module_result.timestamp.timetuple()))

        self.table.update_item(Key={'module_type': module_result.module.__class__.__name__,
                                    'epoch': epoch},
                               AttributeUpdates=updates)

        return ModuleResult(self)

    def write_item(self, data):
        self.table.put_item(Item=data)

    def reset(self, config):
        self.dynamodb = boto3.resource('dynamodb',
                                       region_name=config['region'],
                                       endpoint_url=config['endpoint_url'] if 'endpoint_url' in config else None)

        self.table = self.dynamodb.Table(config['table'])
