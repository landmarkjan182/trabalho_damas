from pecas import peca

class Tabuleiro:
    def __init__(self):
        self.tabuleiro = self.criar_tabuleiro()
        self.turno = "azul"
        self.contador_comidas_azul = 0
        self.contador_comidas_vermelho = 0

    def criar_tabuleiro(self):
        tab = [[None for _ in range(8)] for _ in range(8)]
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:
                    tab[i][j] = peca("vermelho")
        for i in range(5, 8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    tab[i][j] = peca("azul")
        return tab

    def mostrar(self):
        print("\n   A  B  C  D  E  F  G  H")
        for i, linha in enumerate(self.tabuleiro):
            print(f"{i + 1:<2}", end=" ")
            for j, peca in enumerate(linha):
                if peca:
                    print(str(peca), end=" ")
                else:
                    if (i + j) % 2 == 0:
                        print("⬜", end=" ")
                    else:
                        print("⬛", end=" ")
            print()
        print()
        print(f"Peças comidas - 🔵 Azul: {self.contador_comidas_azul} | 🔴 Vermelho: {self.contador_comidas_vermelho}\n")

    def converter_posicao(self, pos):
        letras = "ABCDEFGH"
        if len(pos) != 2:
            return None, None
        col = letras.find(pos[0].upper())
        try:
            row = int(pos[1]) - 1
        except:
            return None, None
        if 0 <= col <= 7 and 0 <= row <= 7:
            return row, col
        return None, None

    def mover(self, origem, destino):
        ol, oc = self.converter_posicao(origem)
        dl, dc = self.converter_posicao(destino)

        if None in [ol, oc, dl, dc]:
            print("Posição inválida.")
            return False

        peca = self.tabuleiro[ol][oc]
        if not peca:
            print("Não há peça nessa posição.")
            return False
        if peca.cor != self.turno:
            print(f"É a vez do jogador {self.turno}.")
            return False

        delta_l = dl - ol
        delta_c = dc - oc
        destino_vazio = self.tabuleiro[dl][dc] is None

        direcao = -1 if peca.cor == "azul" else 1

       
        if abs(delta_l) == 1 and abs(delta_c) == 1 and destino_vazio:
            if peca.dama or delta_l == direcao:
                self.fazer_movimento(ol, oc, dl, dc, peca)
                return True

        if abs(delta_l) == 2 and abs(delta_c) == 2:
            meio_l = ol + delta_l // 2
            meio_c = oc + delta_c // 2
            peca_meio = self.tabuleiro[meio_l][meio_c]

            if peca_meio and peca_meio.cor != peca.cor and destino_vazio:
                self.tabuleiro[meio_l][meio_c] = None
                self.atualizar_contador_comidas(peca_meio)
                self.fazer_movimento(ol, oc, dl, dc, peca)
                return True

        print("Movimento inválido.")
        return False

    def fazer_movimento(self, ol, oc, dl, dc, peca):
        self.tabuleiro[dl][dc] = peca
        self.tabuleiro[ol][oc] = None

      
        if (peca.cor == "azul" and dl == 0) or (peca.cor == "vermelho" and dl == 7):
            peca.dama = True

        self.trocar_turno()

    def trocar_turno(self):
        self.turno = "vermelho" if self.turno == "azul" else "azul"

    def atualizar_contador_comidas(self, peca_comida):
        if peca_comida.cor == "azul":
            self.contador_comidas_vermelho += 1
        else:
            self.contador_comidas_azul += 1

    def acabou(self):
        azuis = vermelhas = 0
        for linha in self.tabuleiro:
            for peca in linha:
                if peca:
                    if peca.cor == "azul":
                        azuis += 1
                    else:
                        vermelhas += 1
        if azuis == 0:
            print("🔴 Jogador VERMELHO venceu!")
            return True
        if vermelhas == 0:
            print("🔵 Jogador AZUL venceu!")
            return True
        return False


tabuleiro = Tabuleiro()

while True:
    tabuleiro.mostrar()
    if tabuleiro.acabou():
        break
    print(f"Vez do jogador: {tabuleiro.turno.upper()}")
    origem = input("Mover de (ex: B6): ").strip()
    destino = input("Para (ex: C5): ").strip()

    if origem.lower() == "sair" or destino.lower() == "sair":
        break

    tabuleiro.mover(origem, destino)
