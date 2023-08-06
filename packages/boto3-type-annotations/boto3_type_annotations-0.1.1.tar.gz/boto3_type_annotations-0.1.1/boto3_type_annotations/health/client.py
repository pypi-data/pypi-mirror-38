from botocore.waiter import Waiter
from typing import Optional
from botocore.paginate import Paginator
from typing import List
from botocore.client import BaseClient
from typing import Dict
from typing import NoReturn
from typing import Union


class Client(BaseClient):
    def can_paginate(self, operation_name: str = None) -> NoReturn:
        pass

    def describe_affected_entities(self, filter: Dict, locale: str = None, nextToken: str = None, maxResults: int = None) -> Dict:
        pass

    def describe_entity_aggregates(self, eventArns: List = None) -> Dict:
        pass

    def describe_event_aggregates(self, aggregateField: str, filter: Dict = None, maxResults: int = None, nextToken: str = None) -> Dict:
        pass

    def describe_event_details(self, eventArns: List, locale: str = None) -> Dict:
        pass

    def describe_event_types(self, filter: Dict = None, locale: str = None, nextToken: str = None, maxResults: int = None) -> Dict:
        pass

    def describe_events(self, filter: Dict = None, nextToken: str = None, maxResults: int = None, locale: str = None) -> Dict:
        pass

    def generate_presigned_url(self, ClientMethod: str = None, Params: Dict = None, ExpiresIn: int = None, HttpMethod: str = None) -> NoReturn:
        pass

    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass
