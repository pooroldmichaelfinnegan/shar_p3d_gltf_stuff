import numpy as np
from mat import *

class Chunk:
    def __init__(self, chunk_body: list[dict, list]):
        self.body: list = chunk_body
        self.data: dict = chunk_body[0]
        self.child: list = chunk_body[1]
