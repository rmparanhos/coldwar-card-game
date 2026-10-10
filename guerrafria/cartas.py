"""Definição dos tipos de carta."""

from dataclasses import dataclass
from enum import Enum


class Tipo(Enum):
    # Militar
    ICBM = "ICBM"
    DEFESA = "Defesa antimíssil"
    SUBMARINO = "Submarino nuclear"
    # Espionagem
    SATELITE = "Avião espião / Satélite"
    SERVICO_SECRETO = "Serviço secreto"
    AGENTE_DUPLO = "Agente duplo"
    DESERTOR = "Desertor"
    SABOTAGEM = "Sabotagem"
    # Tempo
    CORRIDA = "Corrida armamentista"
    BLOQUEIO = "Bloqueio de Berlim"
    PONTE_AEREA = "Ponte aérea"
    DESINFORMACAO = "Desinformação"
    # Diplomacia
    TRATADO = "Tratado"
    VETO = "Veto na ONU"
    TELEFONE = "Telefone vermelho"
    # Tecnologia
    SPUTNIK = "Sputnik"
    VOO_TRIPULADO = "Voo tripulado"
    POUSO_LUA = "Pouso na Lua"
    # Crises (resolvidas ao serem compradas)
    CRISE_MISSEIS = "Crise dos Mísseis"
    ALARME_FALSO = "Alarme falso"
    GOLPE = "Golpe de Estado"
    ESCALADA = "Escalada"
    # Relógio
    FIM = "Fim da Guerra Fria"

    def __str__(self):
        return self.value


TECNOLOGIAS = frozenset({Tipo.SPUTNIK, Tipo.VOO_TRIPULADO, Tipo.POUSO_LUA})
CRISES = frozenset({Tipo.CRISE_MISSEIS, Tipo.ALARME_FALSO, Tipo.GOLPE, Tipo.ESCALADA})
# Cartas que só podem ser usadas como reação, fora da jogada normal do turno.
REACOES = frozenset({Tipo.VETO, Tipo.PONTE_AEREA})


@dataclass(eq=False)
class Carta:
    tipo: Tipo
    # ICBM: quem lançou. Tratado: quem propôs.
    dono: int | None = None
    # Tratado jogado e aguardando voltar ao topo.
    pendente: bool = False

    def __repr__(self):
        return str(self.tipo)
