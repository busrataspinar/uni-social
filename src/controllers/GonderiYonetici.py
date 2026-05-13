import random
from datetime import datetime
from models.Gonderi import Gonderi
from utils.JsonIsleyicisi import JsonIsleyicisi


class GonderiYonetici:
    """
    Gönderi iş mantığını yöneten Controller sınıfı.
    Veriler bellekte liste olarak tutulur; her işlemde
    JsonIsleyicisi aracılığıyla gonderiler.json'a yazılır.
    """

    def __init__(self):
        self._json = JsonIsleyicisi()
        # JSON'dan gelen dict listesini Gonderi nesnelerine çevir
        self.gonderiler: list[Gonderi] = self._json_to_gonderiler(
            self._json.oku("gonderiler")
        )
