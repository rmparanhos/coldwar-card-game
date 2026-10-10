"""Parâmetros ajustáveis do jogo. Mude aqui para testar variantes de regras."""

from dataclasses import dataclass, field

from .cartas import Tipo


def _baralho_padrao():
    return {
        Tipo.DEFESA: 3,
        Tipo.SUBMARINO: 1,
        Tipo.SATELITE: 3,
        Tipo.SERVICO_SECRETO: 2,
        Tipo.AGENTE_DUPLO: 2,
        Tipo.DESERTOR: 1,
        Tipo.SABOTAGEM: 2,
        Tipo.CORRIDA: 2,
        Tipo.BLOQUEIO: 2,
        Tipo.PONTE_AEREA: 1,
        Tipo.DESINFORMACAO: 2,
        Tipo.TRATADO: 3,
        Tipo.VETO: 3,
        Tipo.TELEFONE: 2,
        Tipo.SPUTNIK: 2,
        Tipo.VOO_TRIPULADO: 2,
        Tipo.POUSO_LUA: 2,
        Tipo.CRISE_MISSEIS: 1,
        Tipo.ALARME_FALSO: 1,
        Tipo.GOLPE: 1,
        Tipo.ESCALADA: 1,
        Tipo.FIM: 1,
    }


def _pontos_padrao():
    # (vencedor, perdedor)
    return {
        "militar": (5, 0),
        "diplomatica": (4, 1),
        "tecnologica": (4, 1),
        "paz": (3, 3),
        "destruicao_mutua": (0, 0),
    }


@dataclass
class Config:
    baralho: dict = field(default_factory=_baralho_padrao)
    mao_inicial: int = 4  # além do ICBM
    limite_mao: int = 7
    # A partida termina em paz quando "Fim da Guerra Fria" for comprada esta quantidade de vezes.
    fim_limite: int = 2
    cartas_satelite: int = 3
    cartas_desinformacao: int = 3
    # False: Defesa é usada quando o ICBM inimigo chega (como o "Defuse" do Exploding Kittens).
    # True: Defesa é jogada no próprio turno e procura um ICBM inimigo em voo no baralho.
    defesa_cega: bool = False
    pontos: dict = field(default_factory=_pontos_padrao)
    max_turnos: int = 400
