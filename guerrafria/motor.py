"""Motor de regras: estado da partida e resolução das cartas.

O baralho é uma deque: índice 0 é o topo, o final é o fundo.
"""

import random
from collections import Counter, deque
from dataclasses import dataclass, field
from itertools import islice

from .cartas import CRISES, ORDEM_TECNOLOGIA, REACOES, TECNOLOGIAS, Carta, Tipo
from .config import Config

LADOS = ("EUA", "URSS")

# Estados do ICBM de um jogador.
MAO = "mao"
VOO = "voo"
INTERCEPTADO = "interceptado"
DETONADO = "detonado"
# Estado do ICBM do oponente quando não se sabe.
DESCONHECIDO = "desconhecido"


class FimDePartida(Exception):
    pass


@dataclass
class Jogada:
    carta: Carta
    secreta: bool = False
    # Desertor: carta entregue. Sabotagem: tecnologia do oponente.
    alvo: Carta | None = None


@dataclass
class Intel:
    """O que um jogador sabe sobre o ICBM do oponente."""

    estado: str = MAO
    # Jogadas secretas do oponente desde a última confirmação.
    secretas: int = 0


@dataclass
class Visao:
    """O que um jogador pode ver da partida."""

    eu: int
    mao: list
    mesa: list
    mesa_oponente: list
    n_mao_oponente: int
    tamanho_baralho: int
    meu_icbm: str
    icbm_oponente: str
    secretas_oponente: int
    meu_tratado_pendente: bool
    tratado_oponente_pendente: bool
    turno: int
    fim_contagem: int
    jogaveis: list
    cfg: Config


@dataclass
class Resultado:
    tipo: str
    vencedor: int | None
    turnos: int
    primeiro_jogador: int
    primeiro_lancamento: int | None
    pontos: tuple
    jogadas: Counter = field(default_factory=Counter)


class Partida:
    def __init__(self, bots, config=None, rng=None, primeiro=0, log=False):
        self.cfg = config or Config()
        self.rng = rng or random.Random()
        self.bots = bots
        self.primeiro = primeiro
        self.log = log
        self.eventos = []
        self.baralho = deque()
        self.maos = [[], []]
        self.mesas = [[], []]
        self.icbm = [MAO, MAO]
        self.intel = [Intel(), Intel()]
        self.fim_contagem = 0
        self.turno = 0
        self.compras_extras = [0, 0]
        self.primeiro_lancamento = None
        self.jogadas = Counter()
        self.resultado = None
        self._preparar()

    # ------------------------------------------------------------------ setup

    def _preparar(self):
        normais, crises, fim = [], [], []
        for tipo, qtd in self.cfg.baralho.items():
            for _ in range(qtd):
                carta = Carta(tipo)
                if tipo is Tipo.FIM:
                    fim.append(carta)
                elif tipo in CRISES:
                    crises.append(carta)
                else:
                    normais.append(carta)
        # A mão inicial nunca recebe crises nem o relógio.
        self.rng.shuffle(normais)
        for p in (0, 1):
            self.maos[p] = [Carta(Tipo.ICBM, dono=p)]
            self.maos[p] += [normais.pop() for _ in range(self.cfg.mao_inicial)]
        resto = normais + crises
        self.rng.shuffle(resto)
        # O relógio começa no fundo do baralho.
        self.baralho = deque(resto + fim)

    # ------------------------------------------------------------- utilidades

    def _registrar(self, msg):
        if self.log:
            self.eventos.append(f"[{self.turno:3}] {msg}")

    def _nome(self, p):
        return LADOS[p]

    def _encerrar(self, tipo, vencedor):
        vitoria, derrota = self.cfg.pontos[tipo]
        if vencedor is None:
            pontos = (vitoria, vitoria)
        else:
            pontos = (vitoria, derrota) if vencedor == 0 else (derrota, vitoria)
        self.resultado = Resultado(
            tipo=tipo,
            vencedor=vencedor,
            turnos=self.turno,
            primeiro_jogador=self.primeiro,
            primeiro_lancamento=self.primeiro_lancamento,
            pontos=pontos,
            jogadas=self.jogadas,
        )
        quem = "ninguém" if vencedor is None else self._nome(vencedor)
        self._registrar(f"FIM DE PARTIDA: {tipo} (vencedor: {quem})")
        raise FimDePartida

    def _tratado_pendente(self, dono):
        return any(c.tipo is Tipo.TRATADO and c.pendente and c.dono == dono for c in self.baralho)

    def _tem_tecnologia_completa(self, p):
        return TECNOLOGIAS <= {c.tipo for c in self.mesas[p]}

    def _sem_icbm(self, cartas):
        return [c for c in cartas if c.tipo is not Tipo.ICBM]

    def _tirar(self, p, tipo):
        carta = next((c for c in self.maos[p] if c.tipo is tipo), None)
        if carta is not None:
            self.maos[p].remove(carta)
        return carta

    def jogaveis(self, p):
        """Cartas da mão que podem ser jogadas abertas no turno."""
        mesa = {c.tipo for c in self.mesas[p]}
        oponente_tem_tec = any(c.tipo in TECNOLOGIAS for c in self.mesas[1 - p])
        resultado = []
        for c in self.maos[p]:
            t = c.tipo
            if t is Tipo.ICBM or t in REACOES:
                continue
            if t is Tipo.DEFESA and not self.cfg.defesa_cega:
                continue
            if t in TECNOLOGIAS and t in mesa:
                continue
            if t in TECNOLOGIAS and self.cfg.tecnologia_em_ordem:
                anteriores = ORDEM_TECNOLOGIA[: ORDEM_TECNOLOGIA.index(t)]
                if not all(a in mesa for a in anteriores):
                    continue
            if t is Tipo.SABOTAGEM and not oponente_tem_tec:
                continue
            resultado.append(c)
        return resultado

    def visao(self, p):
        o = 1 - p
        return Visao(
            eu=p,
            mao=list(self.maos[p]),
            mesa=list(self.mesas[p]),
            mesa_oponente=list(self.mesas[o]),
            n_mao_oponente=len(self.maos[o]),
            tamanho_baralho=len(self.baralho),
            meu_icbm=self.icbm[p],
            icbm_oponente=self.intel[p].estado,
            secretas_oponente=self.intel[p].secretas,
            meu_tratado_pendente=self._tratado_pendente(p),
            tratado_oponente_pendente=self._tratado_pendente(o),
            turno=self.turno,
            fim_contagem=self.fim_contagem,
            jogaveis=self.jogaveis(p),
            cfg=self.cfg,
        )

    def _revelar_para(self, observador):
        """O observador descobre a verdade sobre o ICBM do oponente."""
        estado = self.icbm[1 - observador]
        self.intel[observador].estado = estado if estado != DETONADO else VOO
        self.intel[observador].secretas = 0

    def _observar(self, p, cartas):
        if any(c.tipo is Tipo.ICBM and c.dono == 1 - p for c in cartas):
            self.intel[p].estado = VOO

    # ----------------------------------------------------------------- partida

    def jogar(self):
        p = self.primeiro
        try:
            while self.turno < self.cfg.max_turnos:
                self.turno += 1
                self._turno(p)
                p = 1 - p
            self._encerrar("paz", None)
        except FimDePartida:
            pass
        return self.resultado

    def _turno(self, p):
        jogada = self.bots[p].escolher_jogada(self.visao(p))
        if jogada is not None:
            self._executar(p, jogada)
        compras = 1 + self.compras_extras[p]
        self.compras_extras[p] = 0
        for _ in range(compras):
            self._comprar(p)
        self._limite_mao(p)
        self._radar()

    def _radar(self):
        """Mísseis perto do topo são detectados por todos."""
        for c in islice(self.baralho, self.cfg.radar):
            if c.tipo is Tipo.ICBM and self.intel[1 - c.dono].estado != VOO:
                self.intel[1 - c.dono].estado = VOO
                self._registrar(f"Radar de {self._nome(1 - c.dono)} detecta um ICBM chegando!")

    def _limite_mao(self, p):
        excesso = len(self.maos[p]) - self.cfg.limite_mao
        if excesso <= 0:
            return
        escolhidas = self.bots[p].descartar(self.visao(p), excesso)
        validas = [c for c in escolhidas if c in self.maos[p] and c.tipo is not Tipo.ICBM]
        for c in self._sem_icbm(self.maos[p]):
            if len(validas) >= excesso:
                break
            if c not in validas:
                validas.append(c)
        for c in validas[:excesso]:
            self.maos[p].remove(c)
            self.baralho.append(c)

    # ------------------------------------------------------------------ jogadas

    def _jogada_secreta(self, p, carta):
        self.baralho.append(carta)
        if carta.tipo is Tipo.ICBM:
            carta.dono = p
            self.icbm[p] = VOO
            if self.primeiro_lancamento is None:
                self.primeiro_lancamento = p
            self._registrar(f"{self._nome(p)} LANÇA o ICBM em segredo")
        else:
            self._registrar(f"{self._nome(p)} põe uma carta virada no fundo ({carta})")
        intel = self.intel[1 - p]
        intel.secretas += 1
        if intel.estado == MAO:
            intel.estado = DESCONHECIDO

    def _executar(self, p, jogada):
        carta = jogada.carta
        if carta not in self.maos[p]:
            raise ValueError(f"{carta} não está na mão de {self._nome(p)}")
        if jogada.secreta:
            self.maos[p].remove(carta)
            self._jogada_secreta(p, carta)
            return
        if carta not in self.jogaveis(p):
            raise ValueError(f"{carta} não pode ser jogada agora")
        self.maos[p].remove(carta)
        self.jogadas[(p, carta.tipo)] += 1
        self._registrar(f"{self._nome(p)} joga {carta}")
        if self._vetado(p, carta):
            self.baralho.append(carta)
            return
        self._efeito(p, carta, jogada.alvo)

    def _vetado(self, autor, carta):
        """Cadeia de Vetos: cada Veto inverte o resultado. Retorna se a carta foi cancelada."""
        vetado = False
        reagente = 1 - autor
        while True:
            if not any(c.tipo is Tipo.VETO for c in self.maos[reagente]):
                break
            if not self.bots[reagente].quer_vetar(self.visao(reagente), carta.tipo, autor):
                break
            self.baralho.append(self._tirar(reagente, Tipo.VETO))
            self.jogadas[(reagente, Tipo.VETO)] += 1
            vetado = not vetado
            self._registrar(f"{self._nome(reagente)} usa Veto na ONU contra {carta}")
            reagente = 1 - reagente
        return vetado

    def _efeito(self, p, carta, alvo):
        o = 1 - p
        t = carta.tipo

        if t in TECNOLOGIAS or t is Tipo.SUBMARINO:
            self.mesas[p].append(carta)
            if t in TECNOLOGIAS and self._tem_tecnologia_completa(p):
                self._encerrar("tecnologica", p)
            return

        if t is Tipo.TRATADO:
            carta.dono = p
            carta.pendente = True
            if self.cfg.tratado_no_meio:
                self.baralho.insert(len(self.baralho) // 2, carta)
            else:
                self.baralho.append(carta)
            return

        if t is Tipo.SATELITE:
            self._observar(p, list(islice(self.baralho, self.cfg.cartas_satelite)))

        elif t in (Tipo.SERVICO_SECRETO, Tipo.TELEFONE):
            self._revelar_para(p)

        elif t is Tipo.CORRIDA:
            self.baralho.append(carta)
            for q in (p, o):
                for _ in range(2):
                    self._comprar(q)
            return

        elif t is Tipo.BLOQUEIO:
            ponte = None
            if any(c.tipo is Tipo.PONTE_AEREA for c in self.maos[o]):
                if self.bots[o].usar_ponte_aerea(self.visao(o)):
                    ponte = self._tirar(o, Tipo.PONTE_AEREA)
                    self.jogadas[(o, Tipo.PONTE_AEREA)] += 1
                    self._registrar(f"{self._nome(o)} responde com Ponte aérea")
            if ponte is not None and not self._vetado(o, ponte):
                self.baralho.append(ponte)
            else:
                if ponte is not None:
                    self.baralho.append(ponte)
                self.compras_extras[o] += 1

        elif t is Tipo.DESINFORMACAO:
            n = min(self.cfg.cartas_desinformacao, len(self.baralho))
            topo = [self.baralho.popleft() for _ in range(n)]
            self._observar(p, topo)
            nova = self.bots[p].reordenar(self.visao(p), list(topo))
            if sorted(map(id, nova)) != sorted(map(id, topo)):
                nova = topo
            self.baralho.extendleft(reversed(nova))

        elif t is Tipo.AGENTE_DUPLO:
            candidatas = self._sem_icbm(self.maos[o])
            if candidatas:
                roubada = self.rng.choice(candidatas)
                self.maos[o].remove(roubada)
                self.maos[p].append(roubada)

        elif t is Tipo.DESERTOR:
            minhas = self._sem_icbm(self.maos[p])
            dele = self._sem_icbm(self.maos[o])
            if minhas and dele:
                entrega = alvo if alvo in minhas else minhas[0]
                recebe = self.rng.choice(dele)
                self.maos[p].remove(entrega)
                self.maos[o].remove(recebe)
                self.maos[o].append(entrega)
                self.maos[p].append(recebe)

        elif t is Tipo.SABOTAGEM:
            techs = [c for c in self.mesas[o] if c.tipo in TECNOLOGIAS]
            if techs:
                destruida = alvo if alvo in techs else techs[0]
                self.mesas[o].remove(destruida)
                self.baralho.append(destruida)

        elif t is Tipo.DEFESA:  # só no modo defesa_cega
            missil = next((c for c in self.baralho if c.tipo is Tipo.ICBM and c.dono == o), None)
            if missil is not None:
                self.baralho.remove(missil)
                self._interceptar(o)

        self.baralho.append(carta)

    # ------------------------------------------------------------------ compras

    def _comprar(self, p):
        if not self.baralho:
            return
        carta = self.baralho.popleft()
        t = carta.tipo

        if t is Tipo.ICBM:
            self._chegada_icbm(carta)
            return

        if t is Tipo.TRATADO and carta.pendente:
            carta.pendente = False
            if VOO not in self.icbm:
                self._registrar(f"Tratado de {self._nome(carta.dono)} volta ao topo em paz")
                self._encerrar("diplomatica", carta.dono)
            self._registrar(f"Tratado de {self._nome(carta.dono)} fracassa: há míssil em voo")

        elif t is Tipo.FIM:
            self.fim_contagem += 1
            self._registrar(f"Fim da Guerra Fria comprada ({self.fim_contagem}/{self.cfg.fim_limite})")
            self.baralho.append(carta)
            if self.fim_contagem >= self.cfg.fim_limite:
                self._encerrar("paz", None)
            return

        elif t in CRISES:
            self._registrar(f"{self._nome(p)} compra a crise {carta}")
            self._crise(p, carta)
            self.baralho.append(carta)
            return

        self.maos[p].append(carta)

    def _crise(self, p, carta):
        t = carta.tipo
        if t is Tipo.CRISE_MISSEIS:
            self._revelar_para(1 - p)
        elif t is Tipo.ALARME_FALSO:
            # Quem comprou põe uma carta virada no fundo: o ICBM ou outra (blefe).
            if self.icbm[p] == MAO and self.bots[p].alarme_lancar(self.visao(p)):
                self._jogada_secreta(p, self._tirar(p, Tipo.ICBM))
            else:
                outras = self._sem_icbm(self.maos[p])
                if outras:
                    escolhida = self.rng.choice(outras)
                    self.maos[p].remove(escolhida)
                    self._jogada_secreta(p, escolhida)
        elif t is Tipo.GOLPE:
            outras = self._sem_icbm(self.maos[p])
            if outras:
                perdida = self.rng.choice(outras)
                self.maos[p].remove(perdida)
                self.baralho.append(perdida)
        elif t is Tipo.ESCALADA:
            for c in self.baralho:
                if c.tipo is Tipo.TRATADO:
                    c.pendente = False

    # ---------------------------------------------------------------- ataques

    def _interceptar(self, atacante):
        self.icbm[atacante] = INTERCEPTADO
        self.intel[1 - atacante].estado = INTERCEPTADO
        self._registrar(f"ICBM de {self._nome(atacante)} INTERCEPTADO")

    def _chegada_icbm(self, missil):
        atacante = missil.dono
        alvo = 1 - atacante
        self._registrar(f"ICBM de {self._nome(atacante)} chega ao alvo")
        tem_defesa = any(c.tipo is Tipo.DEFESA for c in self.maos[alvo])
        if tem_defesa and not self.cfg.defesa_cega and self.bots[alvo].usar_defesa(self.visao(alvo)):
            defesa = self._tirar(alvo, Tipo.DEFESA)
            self.jogadas[(alvo, Tipo.DEFESA)] += 1
            self.baralho.append(defesa)
            if not self._vetado(alvo, defesa):
                self._interceptar(atacante)
                return
        self._impacto(alvo)

    def _impacto(self, alvo):
        atacante = 1 - alvo
        self.icbm[atacante] = DETONADO
        self._registrar(f"{self._nome(alvo)} é ATINGIDO")
        submarino = any(c.tipo is Tipo.SUBMARINO for c in self.mesas[alvo])
        if self.icbm[alvo] == MAO and (submarino or self.cfg.segundo_ataque):
            self._registrar(f"{self._nome(alvo)} retalia com o segundo ataque")
            missil = self._tirar(alvo, Tipo.ICBM)
            missil.dono = alvo
            self.icbm[alvo] = VOO
            self.baralho.append(missil)
        if self.icbm[alvo] == VOO:
            self._fase_final(atacante)
        self._encerrar("militar", atacante)

    def _fase_final(self, sobrevivente):
        """A retaliação já está em voo: só uma Defesa na mão do sobrevivente o salva."""
        if any(c.tipo is Tipo.DEFESA for c in self.maos[sobrevivente]):
            self.baralho.remove(next(c for c in self.baralho if c.tipo is Tipo.ICBM))
            self._interceptar(1 - sobrevivente)
            self._encerrar("militar", sobrevivente)
        self._registrar(f"{self._nome(sobrevivente)} é ATINGIDO pela retaliação")
        self._encerrar("destruicao_mutua", None)
