"""Ponto de entrada do Sistema de Gerenciamento de Manutenção (CTW)."""

from dotenv import load_dotenv

import menu

load_dotenv()


def main():
    print("=== SISTEMA DE GERENCIAMENTO DE MANUTENÇÃO ===")
    tentativas = 3
    while tentativas > 0:
        if menu.fazer_login():
            menu.menu_principal()
            return
        tentativas -= 1
        print(f"Tentativas restantes: {tentativas}")
    print("Número máximo de tentativas excedido.")


if __name__ == "__main__":
    main()
