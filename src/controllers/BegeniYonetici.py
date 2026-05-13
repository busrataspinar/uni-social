from models.Begeni import Begeni
from utils.JsonIsleyicisi import JsonIsleyicisi

class BegeniYonetici:
    """
    Gönderilere yapılan beğenilerin yönetimini sağlayan Controller sınıfı.
    Bellekte beğeni nesnelerini tutar, JSON ile kalıcılığı sağlar.
    """

    BEGENI_DOSYA = "data/begeniler.json"

    def __init__(self) -> None:
        self.json = JsonIsleyicisi()
        self.begeniler: list[Begeni] = []
        # ileride _verileri_yukle() fonksiyonu eklenecek
