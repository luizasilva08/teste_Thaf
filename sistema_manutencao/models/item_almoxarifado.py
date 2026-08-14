#class item_almoxarifado
class ItemAlmoxarifado:
    def __init__(self, id_ferramenta = None,
                 nome_ferramenta = "",
                 dimensao_ferramenta = None,
                 quantidade_atual = 0,
                 estoque_minimo = 1,
                 unidade_medida = "UN",
                 localizacao_gaveta = None):

        self.id_ferramenta = id_ferramenta
        self.nome_ferramenta = nome_ferramenta
        self.dimensao_ferramenta = dimensao_ferramenta
        self.quantidade_atual = quantidade_atual
        self.estoque_minimo = estoque_minimo
        self.unidade_medida = unidade_medida
        self.localizacao_gaveta = localizacao_gaveta

    def __str__(self):
        c1  = "\033[38;5;94m"
        c2  = "\033[38;5;130m"
        c3  = "\033[38;5;180m"
        reset = "\033[0m"

        return (
            f"{c1}=== ITEM DO ALMOXARIFADO ==={reset}\n"
            f"{c2}Nome:{reset} {self.nome_ferramenta}\n"
            f"{c3}Quantidade:{reset} {self.quantidade_atual} {self.unidade_medida} (mín. {self.estoque_minimo})\n"
            f"{c2}Localização:{reset} {self.localizacao_gaveta}\n"
            f"{c1}=========================={reset}"
        )
