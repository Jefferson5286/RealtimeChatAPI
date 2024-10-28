from fastapi import APIRouter
from typing import List

import apps.authentication.routes


routes: List[APIRouter] = [
    apps.authentication.routes.route,
]