from botocore.waiter import Waiter
from typing import Optional
from botocore.paginate import Paginator
from botocore.client import BaseClient
from typing import Dict
from typing import NoReturn
from typing import Union


class Client(BaseClient):
    def can_paginate(self, operation_name: str = None) -> NoReturn:
        pass

    def create_cluster(self, name: str, roleArn: str, resourcesVpcConfig: Dict, version: str = None, clientRequestToken: str = None) -> Dict:
        pass

    def delete_cluster(self, name: str) -> Dict:
        pass

    def describe_cluster(self, name: str) -> Dict:
        pass

    def generate_presigned_url(self, ClientMethod: str = None, Params: Dict = None, ExpiresIn: int = None, HttpMethod: str = None) -> NoReturn:
        pass

    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    def list_clusters(self, maxResults: int = None, nextToken: str = None) -> Dict:
        pass
