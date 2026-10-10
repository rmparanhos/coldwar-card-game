"""Roda partidas, séries e torneios entre estratégias e mostra estatísticas.

Exemplos:
    python -m guerrafria.simulador partida pomba falcao --semente 7
    python -m guerrafria.simulador duelo pomba oportunista --series 500
    python -m guerrafria.simulador torneio --series 200
"""

import argparse
import random
from collections import Counter
from itertools import combinations_with_replacement
from statistics import mean

from .bots import ESTRATEGIAS
from .config import Config
from .motor import LADOS, Partida

TIPOS = ("militar", "diplomatica", "tecnologica", "paz", "destruicao_mutua")


def jogar_serie(nome_a, nome_b, partidas, cfg, rng):
    """Série de partidas entre dois bots; quem começa alterna. Retorna a lista de resultados."""
    bots = [ESTRATEGIAS[nome_a](rng), ESTRATEGIAS[nome_b](rng)]
    resultados = []
    for i in range(partidas):
        for eu, bot in enumerate(bots):
            bot.inicio_partida(eu)
        r = Partida(bots, cfg, rng, primeiro=i % 2).jogar()
        for bot in bots:
            bot.fim_partida(r)
        resultados.append(r)
    return resultados


def _pct(n, total):
    return f"{100 * n / total:5.1f}%" if total else "  -  "


def relatorio(resultados, nome_a="A", nome_b="B"):
    total = len(resultados)
    tipos = Counter(r.tipo for r in resultados)
    linhas = [f"Partidas: {total}", "", "Resultados:"]
    for t in TIPOS:
        vit_a = sum(1 for r in resultados if r.tipo == t and r.vencedor == 0)
        vit_b = sum(1 for r in resultados if r.tipo == t and r.vencedor == 1)
        detalhe = f"  ({nome_a}: {vit_a}, {nome_b}: {vit_b})" if t not in ("paz", "destruicao_mutua") else ""
        linhas.append(f"  {t:<17} {_pct(tipos[t], total)}{detalhe}")

    decididas = [r for r in resultados if r.vencedor is not None]
    vit_primeiro = sum(1 for r in decididas if r.vencedor == r.primeiro_jogador)
    lancou = [r for r in resultados if r.primeiro_lancamento is not None]
    linhas += [
        "",
        f"Duração média: {mean(r.turnos for r in resultados) / 2:.1f} rodadas",
        f"Quem começa vence: {_pct(vit_primeiro, len(decididas))} das partidas com vencedor",
        f"Partidas com ICBM lançado: {_pct(len(lancou), total)}",
        f"Pontos médios por partida: {nome_a} {mean(r.pontos[0] for r in resultados):.2f}"
        f" | {nome_b} {mean(r.pontos[1] for r in resultados):.2f}",
    ]
    return "\n".join(linhas)


def cmd_partida(args, cfg):
    rng = random.Random(args.semente)
    bots = [ESTRATEGIAS[args.a](rng), ESTRATEGIAS[args.b](rng)]
    for eu, bot in enumerate(bots):
        bot.inicio_partida(eu)
    partida = Partida(bots, cfg, rng, log=True)
    r = partida.jogar()
    print(f"{LADOS[0]} = {args.a}  |  {LADOS[1]} = {args.b}\n")
    print("\n".join(partida.eventos))
    print(f"\nPontos: {LADOS[0]} {r.pontos[0]} x {r.pontos[1]} {LADOS[1]}")


def cmd_duelo(args, cfg):
    rng = random.Random(args.semente)
    resultados = []
    pontos_serie = [0, 0]
    for _ in range(args.series):
        serie = jogar_serie(args.a, args.b, args.partidas, cfg, rng)
        resultados += serie
        a = sum(r.pontos[0] for r in serie)
        b = sum(r.pontos[1] for r in serie)
        pontos_serie[0 if a > b else 1 if b > a else 0] += a != b
    print(f"Duelo: {args.a} x {args.b} ({args.series} séries de {args.partidas} partidas)\n")
    print(relatorio(resultados, args.a, args.b))
    print(f"Séries vencidas: {args.a} {pontos_serie[0]} | {args.b} {pontos_serie[1]}")


def torneio(cfg, series, partidas, rng, nomes=None):
    """Todas as estratégias contra todas. Retorna (pontos médios por série, todos os resultados)."""
    nomes = nomes or list(ESTRATEGIAS)
    media = {}
    todos = []
    for a, b in combinations_with_replacement(nomes, 2):
        pa, pb = [], []
        for _ in range(series):
            serie = jogar_serie(a, b, partidas, cfg, rng)
            todos += serie
            pa.append(sum(r.pontos[0] for r in serie))
            pb.append(sum(r.pontos[1] for r in serie))
        media[(a, b)] = mean(pa)
        media[(b, a)] = mean(pb) if a != b else mean(pa + pb)
    return media, todos


def cmd_torneio(args, cfg):
    rng = random.Random(args.semente)
    nomes = list(ESTRATEGIAS)
    media, todos = torneio(cfg, args.series, args.partidas, rng, nomes)

    print(f"Torneio: {args.series} séries de {args.partidas} partidas por confronto")
    print("Pontos médios por série da LINHA contra a COLUNA\n")
    largura = max(map(len, nomes)) + 1
    print(" " * largura + "".join(f"{n[:9]:>10}" for n in nomes) + f"{'MÉDIA':>10}")
    ranking = []
    for a in nomes:
        valores = [media[(a, b)] for b in nomes]
        ranking.append((mean(valores), a))
        print(f"{a:<{largura}}" + "".join(f"{x:>10.2f}" for x in valores) + f"{mean(valores):>10.2f}")
    print("\nClassificação:")
    for i, (m, a) in enumerate(sorted(ranking, reverse=True), 1):
        print(f"  {i}. {a:<{largura}} {m:.2f}")
    print("\nGeral:\n")
    print(relatorio(todos))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Simulador do jogo Guerra Fria")
    parser.add_argument("--semente", type=int, default=None, help="semente aleatória (reprodutível)")
    parser.add_argument("--defesa-cega", action="store_true", help="Defesa jogada no turno, procurando o míssil")
    parser.add_argument("--fim-limite", type=int, default=None, help="voltas do relógio até a paz")
    sub = parser.add_subparsers(dest="comando", required=True)

    estrategias = list(ESTRATEGIAS)
    p = sub.add_parser("partida", help="mostra uma partida narrada")
    p.add_argument("a", choices=estrategias)
    p.add_argument("b", choices=estrategias)

    d = sub.add_parser("duelo", help="várias séries entre duas estratégias")
    d.add_argument("a", choices=estrategias)
    d.add_argument("b", choices=estrategias)
    d.add_argument("--series", type=int, default=200)
    d.add_argument("--partidas", type=int, default=5)

    t = sub.add_parser("torneio", help="todas as estratégias contra todas")
    t.add_argument("--series", type=int, default=100)
    t.add_argument("--partidas", type=int, default=5)

    args = parser.parse_args(argv)
    cfg = Config(defesa_cega=args.defesa_cega)
    if args.fim_limite:
        cfg.fim_limite = args.fim_limite
    {"partida": cmd_partida, "duelo": cmd_duelo, "torneio": cmd_torneio}[args.comando](args, cfg)


if __name__ == "__main__":
    main()
