from botocore.waiter import Waiter
from datetime import datetime
from typing import Optional
from botocore.paginate import Paginator
from typing import List
from botocore.client import BaseClient
from typing import Dict
from typing import NoReturn
from typing import Union


class Client(BaseClient):
    def batch_meter_usage(self, UsageRecords: List, ProductCode: str) -> Dict:
        pass

    def can_paginate(self, operation_name: str = None) -> NoReturn:
        pass

    def generate_presigned_url(self, ClientMethod: str = None, Params: Dict = None, ExpiresIn: int = None, HttpMethod: str = None) -> NoReturn:
        pass

    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    def meter_usage(self, ProductCode: str, Timestamp: datetime, UsageDimension: str, UsageQuantity: int, DryRun: bool) -> Dict:
        pass

    def resolve_customer(self, RegistrationToken: str) -> Dict:
        pass
