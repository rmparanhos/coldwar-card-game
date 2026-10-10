"""Jogadores automáticos (estratégias)."""

import random

from .cartas import TECNOLOGIAS, Tipo
from .motor import DESCONHECIDO, INTERCEPTADO, MAO, VOO, Jogada


class Bot:
    nome = "base"

    def __init__(self, rng=None):
        self.rng = rng or random.Random()

    # Ciclo de vida da série
    def inicio_partida(self, eu):
        self.eu = eu

    def fim_partida(self, resultado):
        pass

    # Decisões
    def escolher_jogada(self, v):
        return None

    def quer_vetar(self, v, tipo, autor):
        return False

    def usar_defesa(self, v):
        return True

    def usar_ponte_aerea(self, v):
        return True

    def alarme_lancar(self, v):
        return False

    def reordenar(self, v, cartas):
        return cartas

    def descartar(self, v, n):
        return []


class Aleatorio(Bot):
    """Faz escolhas aleatórias entre as jogadas válidas."""

    nome = "aleatorio"

    def escolher_jogada(self, v):
        opcoes = [None] + [Jogada(c) for c in v.jogaveis] + [Jogada(c, secreta=True) for c in v.mao]
        jogada = self.rng.choice(opcoes)
        if jogada and not jogada.secreta:
            if jogada.carta.tipo is Tipo.SABOTAGEM:
                techs = [c for c in v.mesa_oponente if c.tipo in TECNOLOGIAS]
                jogada.alvo = self.rng.choice(techs)
            elif jogada.carta.tipo is Tipo.DESERTOR:
                outras = [c for c in v.mao if c is not jogada.carta and c.tipo is not Tipo.ICBM]
                jogada.alvo = self.rng.choice(outras) if outras else None
        return jogada

    def quer_vetar(self, v, tipo, autor):
        return self.rng.random() < 0.5

    def alarme_lancar(self, v):
        return self.rng.random() < 0.5

    def reordenar(self, v, cartas):
        self.rng.shuffle(cartas)
        return cartas

    def descartar(self, v, n):
        return self.rng.sample([c for c in v.mao if c.tipo is not Tipo.ICBM], n)


# Valor aproximado de cada carta, usado para descartar e para decidir Vetos.
VALOR = {
    Tipo.DEFESA: 9,
    Tipo.VETO: 8,
    Tipo.SUBMARINO: 8,
    Tipo.SPUTNIK: 6,
    Tipo.VOO_TRIPULADO: 6,
    Tipo.POUSO_LUA: 6,
    Tipo.TRATADO: 6,
    Tipo.SABOTAGEM: 5,
    Tipo.SERVICO_SECRETO: 5,
    Tipo.TELEFONE: 4,
    Tipo.SATELITE: 4,
    Tipo.AGENTE_DUPLO: 4,
    Tipo.PONTE_AEREA: 3,
    Tipo.DESINFORMACAO: 3,
    Tipo.DESERTOR: 2,
    Tipo.BLOQUEIO: 2,
    Tipo.CORRIDA: 1,
}


class Estrategista(Bot):
    """Bot com heurísticas, parametrizado pela postura nuclear.

    primeiro_ataque:
        "nunca"       - só lança o ICBM em retaliação.
        "oportunista" - ataca primeiro quando acha que pode sair impune.
        "sempre"      - lança o ICBM logo no primeiro turno.
    retalia: lança o ICBM ao saber (ou desconfiar) de um ataque.
    paranoia: chance de tratar uma jogada secreta do oponente como ataque.
    """

    nome = "estrategista"

    def __init__(self, rng=None, primeiro_ataque="nunca", retalia=True, paranoia=0.0, blefe=0.1):
        super().__init__(rng)
        self.primeiro_ataque = primeiro_ataque
        self.retalia = retalia
        self.paranoia = paranoia
        self.blefe = blefe

    def inicio_partida(self, eu):
        super().inicio_partida(eu)
        self._secretas_vistas = 0
        self._suspeita = False

    # --------------------------------------------------------------- ataques

    def _oponente_atacou(self, v):
        if v.icbm_oponente == VOO:
            return True
        # Cada nova jogada secreta pode ser um lançamento.
        if v.secretas_oponente > self._secretas_vistas:
            novas = v.secretas_oponente - self._secretas_vistas
            self._secretas_vistas = v.secretas_oponente
            if any(self.rng.random() < self.paranoia for _ in range(novas)):
                self._suspeita = True
        elif v.secretas_oponente < self._secretas_vistas:
            self._secretas_vistas = v.secretas_oponente
        return self._suspeita and v.icbm_oponente == DESCONHECIDO

    def _quer_lancar(self, v):
        if v.meu_icbm != MAO:
            return False
        if self.retalia and self._oponente_atacou(v):
            return True
        if self.primeiro_ataque == "sempre":
            return True
        if self.primeiro_ataque == "oportunista":
            tem_defesa = any(c.tipo is Tipo.DEFESA for c in v.mao)
            sem_resposta = v.icbm_oponente == INTERCEPTADO
            confirmado_na_mao = v.icbm_oponente == MAO and v.secretas_oponente == 0
            return sem_resposta or (tem_defesa and confirmado_na_mao)
        return False

    # --------------------------------------------------------------- turno

    def escolher_jogada(self, v):
        if self._quer_lancar(v):
            icbm = next(c for c in v.mao if c.tipo is Tipo.ICBM)
            return Jogada(icbm, secreta=True)

        por_tipo = {}
        for c in v.jogaveis:
            por_tipo.setdefault(c.tipo, c)

        def tem(t):
            return t in por_tipo

        # Tecnologia: completar a coleção.
        for t in (Tipo.SPUTNIK, Tipo.VOO_TRIPULADO, Tipo.POUSO_LUA):
            if tem(t):
                return Jogada(por_tipo[t])

        if tem(Tipo.SUBMARINO) and v.meu_icbm == MAO:
            return Jogada(por_tipo[Tipo.SUBMARINO])

        techs_oponente = [c for c in v.mesa_oponente if c.tipo in TECNOLOGIAS]
        if tem(Tipo.SABOTAGEM) and len(techs_oponente) >= 2:
            return Jogada(por_tipo[Tipo.SABOTAGEM], alvo=techs_oponente[0])

        if tem(Tipo.DEFESA):  # modo defesa_cega
            if v.icbm_oponente in (VOO, DESCONHECIDO):
                return Jogada(por_tipo[Tipo.DEFESA])

        # Espionagem quando há dúvida sobre o ICBM do oponente.
        if v.icbm_oponente == DESCONHECIDO:
            for t in (Tipo.SERVICO_SECRETO, Tipo.TELEFONE, Tipo.SATELITE):
                if tem(t):
                    return Jogada(por_tipo[t])

        if tem(Tipo.TRATADO) and not v.meu_tratado_pendente and v.meu_icbm == MAO:
            return Jogada(por_tipo[Tipo.TRATADO])

        if tem(Tipo.AGENTE_DUPLO) and v.n_mao_oponente > 1:
            return Jogada(por_tipo[Tipo.AGENTE_DUPLO])

        if tem(Tipo.DESINFORMACAO) and v.icbm_oponente == VOO:
            return Jogada(por_tipo[Tipo.DESINFORMACAO])

        if tem(Tipo.BLOQUEIO):
            return Jogada(por_tipo[Tipo.BLOQUEIO])

        if tem(Tipo.DESERTOR):
            outras = [c for c in v.mao if c is not por_tipo[Tipo.DESERTOR] and c.tipo is not Tipo.ICBM]
            if outras:
                pior = min(outras, key=lambda c: VALOR.get(c.tipo, 0))
                return Jogada(por_tipo[Tipo.DESERTOR], alvo=pior)

        # Blefe: põe uma carta fraca virada no fundo.
        if self.rng.random() < self.blefe:
            fracas = [c for c in v.mao if c.tipo is not Tipo.ICBM and VALOR.get(c.tipo, 0) <= 3]
            if fracas:
                return Jogada(self.rng.choice(fracas), secreta=True)
        return None

    # -------------------------------------------------------------- reações

    def quer_vetar(self, v, tipo, autor):
        if autor == v.eu:
            # Contra-veto para salvar a própria carta.
            return tipo in TECNOLOGIAS or tipo in (Tipo.DEFESA, Tipo.TRATADO, Tipo.SABOTAGEM)
        if tipo is Tipo.DEFESA:
            return True  # não deixar interceptarem o meu míssil
        if tipo in TECNOLOGIAS:
            techs = {c.tipo for c in v.mesa_oponente if c.tipo in TECNOLOGIAS}
            return len(techs) >= 1
        if tipo is Tipo.SABOTAGEM:
            return True
        if tipo is Tipo.TRATADO:
            return v.meu_icbm == VOO
        if tipo in (Tipo.SERVICO_SECRETO, Tipo.TELEFONE):
            return v.meu_icbm == VOO
        return False

    def alarme_lancar(self, v):
        if not self.retalia:
            return False
        return v.icbm_oponente in (VOO, DESCONHECIDO) and self.rng.random() < max(self.paranoia, 0.2)

    def reordenar(self, v, cartas):
        # Empurra o míssil inimigo para o fim e traz Defesas para perto.
        def chave(c):
            if c.tipo is Tipo.ICBM:
                return 2 if c.dono != v.eu else -1
            if c.tipo is Tipo.TRATADO and c.pendente and c.dono == v.eu:
                return -1
            if c.tipo is Tipo.DEFESA:
                return 0
            return 1

        return sorted(cartas, key=chave)

    def descartar(self, v, n):
        candidatas = [c for c in v.mao if c.tipo is not Tipo.ICBM]
        candidatas.sort(key=lambda c: VALOR.get(c.tipo, 0))
        return candidatas[:n]


class OlhoPorOlho(Estrategista):
    """Na série: começa pacífico e passa a atacar primeiro se o oponente atacou primeiro antes."""

    nome = "olho_por_olho"

    def __init__(self, rng=None, **kw):
        super().__init__(rng, primeiro_ataque="nunca", **kw)
        self._traido = False

    def inicio_partida(self, eu):
        super().inicio_partida(eu)
        self.primeiro_ataque = "sempre" if self._traido else "nunca"

    def fim_partida(self, resultado):
        lancador = resultado.primeiro_lancamento
        self._traido = lancador is not None and lancador != self.eu


ESTRATEGIAS = {
    "aleatorio": lambda rng: Aleatorio(rng),
    "pomba": lambda rng: _nomeado(Estrategista(rng, "nunca", retalia=True), "pomba"),
    "cordeiro": lambda rng: _nomeado(Estrategista(rng, "nunca", retalia=False), "cordeiro"),
    "paranoico": lambda rng: _nomeado(Estrategista(rng, "nunca", retalia=True, paranoia=0.3), "paranoico"),
    "oportunista": lambda rng: _nomeado(Estrategista(rng, "oportunista", retalia=True), "oportunista"),
    "falcao": lambda rng: _nomeado(Estrategista(rng, "sempre", retalia=True), "falcao"),
    "olho_por_olho": lambda rng: OlhoPorOlho(rng),
}


def _nomeado(bot, nome):
    bot.nome = nome
    return bot
