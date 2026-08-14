def gradiente_texto(texto, cor_inicio, cor_fim):
    """Aplica um gradiente de cor a uma linha de texto usando ANSI truecolor."""
    r1, g1, b1 = cor_inicio
    r2, g2, b2 = cor_fim
    tamanho = len(texto)
    resultado = ""
    for i, char in enumerate(texto):
        if tamanho <= 1:
            t = 0
        else:
            t = i / (tamanho - 1)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        resultado += f"\033[38;2;{r};{g};{b}m{char}"
    resultado += "\033[0m"
    return resultado
