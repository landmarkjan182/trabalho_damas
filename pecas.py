class peca:
    def __init__(self, cor, dama=False):
        self.cor = cor
        self.dama = dama

    def __str__(self):
        if self.cor == "azul":
            return "🔵" if not self.dama else "💙"
        else:
            return "🔴" if not self.dama else "💖"