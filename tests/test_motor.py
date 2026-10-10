import random
import unittest
from collections import deque

from guerrafria.bots import ESTRATEGIAS, Bot
from guerrafria.cartas import Carta, Tipo
from guerrafria.config import Config
from guerrafria.motor import INTERCEPTADO, VOO, Jogada, Partida

class Roteiro(Bot):
    """Bot que executa jogadas pré-definidas, uma por turno."""

    def __init__(self, jogadas=(), veta=False, defende=True, alarme=False):
        super().__init__(random.Random(0))
        self.jogadas = list(jogadas)
        self.veta = veta
        self.defende = defende
        self.alarme = alarme

    def escolher_jogada(self, v):
        if not self.jogadas:
            return None
        tipo, secreta = self.jogadas.pop(0)
        if tipo is None:
            return None
        carta = next(c for c in v.mao if c.tipo is tipo)
        return Jogada(carta, secreta=secreta)

    def quer_vetar(self, v, tipo, autor):
        return self.veta

    def usar_defesa(self, v):
        return self.defende

    def alarme_lancar(self, v):
        return self.alarme

def montar(bots, maos, baralho, mesas=((), ()), **cfg):
    """Partida com mãos e baralho definidos (o topo é o primeiro da lista)."""
    p = Partida(bots, Config(**cfg), random.Random(0))
    for i in (0, 1):
        p.maos[i] = [Carta(Tipo.ICBM, dono=i)] + [Carta(t) for t in maos[i]]
        p.mesas[i] = [Carta(t) for t in mesas[i]]
    p.baralho = deque(Carta(t) for t in baralho)
    return p

ENCHIMENTO = [Tipo.CORRIDA] * 0 + [Tipo.DESERTOR] * 20

class TestMotor(unittest.TestCase):
    def test_icbm_sem_resposta_e_vitoria_militar(self):
        bots = [Roteiro([(Tipo.ICBM, True)]), Roteiro()]
        p = montar(bots, [[], []], [Tipo.DESERTOR] * 3)
        r = p.jogar()
        self.assertEqual(r.tipo, "militar")
        self.assertEqual(r.vencedor, 0)
        self.assertEqual(r.primeiro_lancamento, 0)
        self.assertEqual(r.pontos, (5, 0))

    def test_retaliacao_em_voo_e_destruicao_mutua(self):
        bots = [Roteiro([(Tipo.ICBM, True)]), Roteiro([(Tipo.ICBM, True)])]
        p = montar(bots, [[], []], [Tipo.DESERTOR] * 3)
        r = p.jogar()
        self.assertEqual(r.tipo, "destruicao_mutua")
        self.assertIsNone(r.vencedor)

    def test_defesa_intercepta_na_chegada(self):
        bots = [Roteiro([(Tipo.ICBM, True)]), Roteiro()]
        p = montar(bots, [[], [Tipo.DEFESA]], [Tipo.DESERTOR] * 3, max_turnos=10)
        r = p.jogar()
        self.assertEqual(p.icbm[0], INTERCEPTADO)
        self.assertEqual(r.tipo, "paz")

    def test_veto_cancela_a_defesa(self):
        bots = [Roteiro([(Tipo.ICBM, True)], veta=True), Roteiro()]
        p = montar(bots, [[Tipo.VETO], [Tipo.DEFESA]], [Tipo.DESERTOR] * 3)
        r = p.jogar()
        self.assertEqual((r.tipo, r.vencedor), ("militar", 0))

    def test_contra_veto_restaura_a_defesa(self):
        bots = [Roteiro([(Tipo.ICBM, True)], veta=True), Roteiro(veta=True)]
        p = montar(bots, [[Tipo.VETO], [Tipo.DEFESA, Tipo.VETO]], [Tipo.DESERTOR] * 3, max_turnos=10)
        r = p.jogar()
        self.assertEqual(p.icbm[0], INTERCEPTADO)
        self.assertEqual(r.tipo, "paz")

    def test_submarino_garante_retaliacao(self):
        bots = [Roteiro([(Tipo.ICBM, True)]), Roteiro()]
        p = montar(bots, [[], []], [Tipo.DESERTOR] * 3, mesas=((), (Tipo.SUBMARINO,)))
        r = p.jogar()
        self.assertEqual(r.tipo, "destruicao_mutua")

    def test_atacante_com_defesa_sobrevive_a_retaliacao(self):
        bots = [Roteiro([(Tipo.ICBM, True)]), Roteiro([(Tipo.ICBM, True)])]
        p = montar(bots, [[Tipo.DEFESA], []], [Tipo.DESERTOR] * 3)
        bots[0].defende = False  # não usa a Defesa contra o 1º míssil (ele nem é contra ele)
        r = p.jogar()
        self.assertEqual((r.tipo, r.vencedor), ("militar", 0))

    def test_tratado_volta_em_paz_e_vence(self):
        bots = [Roteiro([(Tipo.TRATADO, False)]), Roteiro()]
        p = montar(bots, [[Tipo.TRATADO], []], [Tipo.DESERTOR] * 4)
        r = p.jogar()
        self.assertEqual((r.tipo, r.vencedor), ("diplomatica", 0))

    def test_tratado_fracassa_com_missil_em_voo(self):
        bots = [Roteiro([(Tipo.TRATADO, False)]), Roteiro([(Tipo.ICBM, True)])]
        p = montar(bots, [[Tipo.TRATADO], [Tipo.DEFESA]], [Tipo.DESERTOR] * 3)
        bots[0].jogadas.append((Tipo.ICBM, True))
        r = p.jogar()
        self.assertNotEqual(r.tipo, "diplomatica")

    def test_escalada_cancela_tratados(self):
        bots = [Roteiro([(Tipo.TRATADO, False)]), Roteiro()]
        p = montar(bots, [[Tipo.TRATADO], []], [Tipo.DESERTOR, Tipo.ESCALADA] + [Tipo.FIM] * 4)
        r = p.jogar()
        self.assertEqual(r.tipo, "paz")

    def test_tecnologia_completa_vence(self):
        bots = [Roteiro([(Tipo.POUSO_LUA, False)]), Roteiro()]
        p = montar(bots, [[Tipo.POUSO_LUA], []], [Tipo.DESERTOR] * 3, mesas=((Tipo.SPUTNIK, Tipo.VOO_TRIPULADO), ()))
        r = p.jogar()
        self.assertEqual((r.tipo, r.vencedor), ("tecnologica", 0))

    def test_fim_da_guerra_fria_encerra_em_paz(self):
        p = montar([Roteiro(), Roteiro()], [[], []], [Tipo.FIM, Tipo.DESERTOR], fim_limite=2)
        r = p.jogar()
        self.assertEqual(r.tipo, "paz")
        self.assertEqual(r.pontos, (3, 3))

    def test_bloqueio_faz_oponente_comprar_duas(self):
        bots = [Roteiro([(Tipo.BLOQUEIO, False)]), Roteiro()]
        p = montar(bots, [[Tipo.BLOQUEIO], []], [Tipo.DESERTOR] * 10)
        p.turno = 1
        p._turno(0)
        p._turno(1)
        self.assertEqual(len(p.maos[1]), 1 + 2)

    def test_ponte_aerea_anula_bloqueio(self):
        bots = [Roteiro([(Tipo.BLOQUEIO, False)]), Roteiro()]
        p = montar(bots, [[Tipo.BLOQUEIO], [Tipo.PONTE_AEREA]], [Tipo.DESERTOR] * 10)
        p._turno(0)
        p._turno(1)
        self.assertEqual(len(p.maos[1]), 1 + 1)

    def test_jogada_secreta_esconde_o_lancamento(self):
        bots = [Roteiro([(Tipo.ICBM, True)]), Roteiro()]
        p = montar(bots, [[], []], [Tipo.DESERTOR] * 10)
        p._turno(0)
        self.assertEqual(p.icbm[0], VOO)
        self.assertEqual(p.visao(1).icbm_oponente, "desconhecido")
        self.assertEqual(p.visao(1).secretas_oponente, 1)

    def test_servico_secreto_revela_lancamento(self):
        bots = [Roteiro([(Tipo.ICBM, True)]), Roteiro([(Tipo.SERVICO_SECRETO, False)])]
        p = montar(bots, [[], [Tipo.SERVICO_SECRETO]], [Tipo.DESERTOR] * 10)
        p._turno(0)
        p._turno(1)
        self.assertEqual(p.visao(1).icbm_oponente, VOO)

    def test_satelite_ve_missil_perto_do_topo(self):
        bots = [Roteiro(), Roteiro([(Tipo.SATELITE, False)])]
        p = montar(bots, [[], [Tipo.SATELITE]], [Tipo.DESERTOR] * 2)
        p.baralho.insert(1, Carta(Tipo.ICBM, dono=0))
        p.icbm[0] = VOO
        p.maos[0] = [c for c in p.maos[0] if c.tipo is not Tipo.ICBM]
        p._turno(1)
        self.assertEqual(p.visao(1).icbm_oponente, VOO)

    def test_alarme_falso_forca_jogada_secreta(self):
        bots = [Roteiro(alarme=True), Roteiro()]
        p = montar(bots, [[Tipo.SATELITE], []], [Tipo.ALARME_FALSO] + [Tipo.DESERTOR] * 5)
        p._turno(0)
        self.assertEqual(p.icbm[0], VOO)

    def test_icbm_nunca_e_roubado(self):
        bots = [Roteiro([(Tipo.AGENTE_DUPLO, False)]), Roteiro()]
        p = montar(bots, [[Tipo.AGENTE_DUPLO], []], [Tipo.DESERTOR] * 5)
        p._turno(0)
        self.assertTrue(any(c.tipo is Tipo.ICBM for c in p.maos[1]))
        self.assertEqual(sum(c.tipo is Tipo.ICBM for c in p.maos[0]), 1)

class TestSimulacao(unittest.TestCase):
    def test_partidas_aleatorias_terminam_e_conservam_cartas(self):
        for defesa_cega in (False, True):
            cfg = Config(defesa_cega=defesa_cega)
            total = sum(cfg.baralho.values()) + 2
            rng = random.Random(42)
            nomes = list(ESTRATEGIAS)
            for i in range(400):
                bots = [ESTRATEGIAS[rng.choice(nomes)](rng) for _ in range(2)]
                for eu, b in enumerate(bots):
                    b.inicio_partida(eu)
                p = Partida(bots, cfg, rng, primeiro=i % 2)
                r = p.jogar()
                self.assertIsNotNone(r)
                if r.tipo in ("paz", "tecnologica", "diplomatica"):
                    em_jogo = len(p.baralho) + sum(map(len, p.maos)) + sum(map(len, p.mesas))
                    fora = sum(e == INTERCEPTADO for e in p.icbm)
                    self.assertEqual(em_jogo + fora, total)

if __name__ == "__main__":
    unittest.main()
