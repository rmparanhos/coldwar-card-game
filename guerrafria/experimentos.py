"""Compara variantes de regra com torneios entre os bots.

    python -m guerrafria.experimentos --series 40
"""

import argparse
import random
from collections import Counter
from dataclasses import replace
from statistics import mean

from .cartas import Tipo
from .config import Config, _pontos_padrao
from .simulador import TIPOS, torneio

# Estratégias "sérias" (sem o bot aleatório, que distorce as médias).
NOMES = ["pomba", "cordeiro", "paranoico", "oportunista", "falcao", "olho_por_olho"]


def _com(cfg, **qtd):
    baralho = dict(cfg.baralho)
    for nome, n in qtd.items():
        baralho[Tipo[nome.upper()]] = n
    return baralho


def _mad_negativo():
    pontos = _pontos_padrao()
    pontos["destruicao_mutua"] = (-1, -1)
    return pontos


def variantes():
    base = Config()
    return {
        "atual": base,
        "tratado no meio": replace(base, tratado_no_meio=True),
        "tecnologia em ordem": replace(base, tecnologia_em_ordem=True),
        "1 cópia de cada tecnologia": replace(
            base, baralho=_com(base, sputnik=1, voo_tripulado=1, pouso_lua=1)
        ),
        "radar (2 cartas)": replace(base, radar=2),
        "1 Defesa": replace(base, baralho=_com(base, defesa=1)),
        "2 Defesas": replace(base, baralho=_com(base, defesa=2)),
        "destruição mútua = -1": replace(base, pontos=_mad_negativo()),
        "segundo ataque": replace(base, segundo_ataque=True),
        "COMBINADO A": replace(
            base,
            baralho=_com(base, defesa=2, sputnik=1, voo_tripulado=1, pouso_lua=1),
            tratado_no_meio=True,
        ),
        "COMBINADO B (A + radar)": replace(
            base,
            baralho=_com(base, defesa=2, sputnik=1, voo_tripulado=1, pouso_lua=1),
            tratado_no_meio=True,
            radar=2,
        ),
        "COMBINADO C (A, 1 Defesa)": replace(
            base,
            baralho=_com(base, defesa=1, sputnik=1, voo_tripulado=1, pouso_lua=1),
            tratado_no_meio=True,
        ),
        "COMBINADO D (A + 2º ataque)": replace(
            base,
            baralho=_com(base, defesa=2, sputnik=1, voo_tripulado=1, pouso_lua=1),
            tratado_no_meio=True,
            segundo_ataque=True,
        ),
        "COMBINADO E (D, tec 2 cópias)": replace(
            base,
            baralho=_com(base, defesa=2),
            tratado_no_meio=True,
            segundo_ataque=True,
        ),
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--series", type=int, default=40)
    parser.add_argument("--partidas", type=int, default=5)
    parser.add_argument("--semente", type=int, default=1)
    args = parser.parse_args(argv)

    abrev = {"militar": "milit", "diplomatica": "diplo", "tecnologica": "tecno",
             "paz": "paz", "destruicao_mutua": "mútua"}
    print(f"{'variante':<28}" + "".join(f"{abrev[t]:>7}" for t in TIPOS)
          + f"{'rodadas':>9}  oport×pomba  vencedor do torneio")
    for nome, cfg in variantes().items():
        media, todos = torneio(cfg, args.series, args.partidas, random.Random(args.semente), NOMES)
        tipos = Counter(r.tipo for r in todos)
        ranking = sorted(((mean(media[(a, b)] for b in NOMES), a) for a in NOMES), reverse=True)
        duelo = f"{media[('oportunista', 'pomba')]:.1f}×{media[('pomba', 'oportunista')]:.1f}"
        print(
            f"{nome:<28}"
            + "".join(f"{100 * tipos[t] / len(todos):6.1f}%" for t in TIPOS)
            + f"{mean(r.turnos for r in todos) / 2:9.1f}  {duelo:>11}  {ranking[0][1]} ({ranking[0][0]:.1f})"
        )


if __name__ == "__main__":
    main()
