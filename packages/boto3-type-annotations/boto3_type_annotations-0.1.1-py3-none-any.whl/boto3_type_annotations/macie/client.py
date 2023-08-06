from botocore.waiter import Waiter
from typing import Optional
from botocore.paginate import Paginator
from typing import List
from botocore.client import BaseClient
from typing import Dict
from typing import NoReturn
from typing import Union


class Client(BaseClient):
    def associate_member_account(self, memberAccountId: str) -> NoReturn:
        pass

    def associate_s3_resources(self, s3Resources: List, memberAccountId: str = None) -> Dict:
        pass

    def can_paginate(self, operation_name: str = None) -> NoReturn:
        pass

    def disassociate_member_account(self, memberAccountId: str) -> NoReturn:
        pass

    def disassociate_s3_resources(self, associatedS3Resources: List, memberAccountId: str = None) -> Dict:
        pass

    def generate_presigned_url(self, ClientMethod: str = None, Params: Dict = None, ExpiresIn: int = None, HttpMethod: str = None) -> NoReturn:
        pass

    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    def list_member_accounts(self, nextToken: str = None, maxResults: int = None) -> Dict:
        pass

    def list_s3_resources(self, memberAccountId: str = None, nextToken: str = None, maxResults: int = None) -> Dict:
        pass

    def update_s3_resources(self, s3ResourcesUpdate: List, memberAccountId: str = None) -> Dict:
        pass
