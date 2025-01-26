class MagazinePage:
    def __init__(self, index: int, text: str):
        self.index = index
        self.text = text

    def __repr__(self):
        return f"MagazinePage(index={self.index}, text={self.text[:30]}...)"
