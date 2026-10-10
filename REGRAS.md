# Guerra Fria — Regras (v0, rascunho)

Documento vivo. Cada regra tem uma marcação:

- ✅ **Confirmado**: veio do design original.
- 💡 **Proposta**: sugestão para preencher lacunas; pode mudar.
- ❓ **Dúvida**: ainda precisa de decisão.

Inspirações: *Exploding Kittens* (comprar cartas como risco, cartas de reação) e a
**dissuasão nuclear** (destruição mútua assegurada).

---

## 1. Ideia central: o baralho é o tempo ✅

- Há **um baralho compartilhado** entre os jogadores. ✅
- Em toda rodada, cada jogador **compra uma carta** do topo. ✅
- Uma carta usada vai para o **fundo do baralho**. ✅
- Por isso, o que é jogado agora "volta" no futuro. O baralho funciona como uma
  linha do tempo, e o **tamanho do baralho define quanto tempo as coisas levam**. ✅

Consequência: um ICBM lançado vai para o fundo e precisa percorrer o baralho até
"chegar ao alvo". Enquanto isso, o oponente tem tempo para **retaliar** ou se
**defender**. ✅

## 2. Jogadores 💡

- v0: **2 jogadores** (EUA × URSS). 💡
- ❓ Suporte a 3 ou mais jogadores no futuro?

## 3. Preparação 💡

- Embaralhar o baralho (composição inicial na seção 8). 💡
- Cada jogador compra **5 cartas**. 💡
- Inserir a carta **"Fim da Guerra Fria"** (relógio da partida) no fundo do baralho. 💡

## 4. Turno 💡

1. **Jogar** até 1 carta da mão (opcional). 💡
2. **Comprar** 1 carta do topo. ✅
3. Limite de mão: **7 cartas**; se passar, descarta para o fundo. 💡

Cartas de **reação** (ex.: Defesa antimíssil) podem ser jogadas fora do próprio
turno, em resposta a algo. 💡

## 5. Cartas "ativas" no baralho 💡

Algumas cartas, quando jogadas, vão ao fundo **ativas**: no jogo físico, são postas
**giradas 90°** para indicar que estão "em curso". 💡

- Quando uma carta **ativa** chega ao topo e é comprada, ela **se resolve**
  (ex.: o ICBM detona).
- Quando uma carta **inativa** é comprada, vai para a mão normalmente.
- Depois de resolvida, a carta vira inativa e volta ao fundo.

❓ As cartas ativas ficam **visíveis** para todos (lançamento público) ou
**escondidas** (o oponente precisa "perceber" com espionagem)? A simulação pode
testar as duas variantes.

## 6. Cartas conhecidas

| Carta | Efeito | Status |
|---|---|---|
| **ICBM** | Lança um míssil contra o oponente: vai ao fundo **ativo**. Quando chega ao topo, atinge o alvo. | ✅ ideia / 💡 detalhes |
| **Defesa antimíssil** | Desativa um ICBM em curso que tenha você como alvo. | ✅ |
| **Avião espião / Satélite** | Olhe as próximas cartas do baralho (💡 3 cartas). | ✅ |
| **Polícia / Serviço secreto** | Olhe a mão do oponente. | ✅ |
| **Guerra por procuração (proxy war)** | ❓ Efeito esquecido. | ❓ |
| **Crises** | Cartas para "agitar" a partida. Efeitos a definir. | ✅ ideia / ❓ efeitos |
| **Tratado / Conferência de Paz** | Caminho da vitória diplomática (seção 7). | 💡 |
| **Tecnologia** (Sputnik, Voo tripulado, Pouso na Lua) | Caminho da vitória tecnológica (seção 7). | 💡 |
| **Fim da Guerra Fria** | Relógio da partida (seção 7). | 💡 |

### Detalhes do ICBM 💡

- O alvo do ICBM é o oponente, **não quem o compra**: se o próprio atacante
  comprar seu ICBM ativo, ele detona no alvo do mesmo jeito. 💡
- **Retaliação**: enquanto um ICBM está em curso, o alvo pode lançar o próprio ICBM.
  Ele entra no fundo, *depois* do primeiro, então ambos acabam chegando:
  **destruição mútua**. ✅
- ❓ Um ICBM desativado pela Defesa volta ao fundo como carta inativa (reutilizável)
  ou sai do jogo?

### Ideias de Crises 💡 (aguardando as suas lembranças)

São resolvidas imediatamente ao serem compradas, como o gatinho do *Exploding Kittens*.

- **Crise dos Mísseis**: cada jogador deve descartar um ICBM da mão para o fundo, ou
  o outro jogador olha a sua mão.
- **Corrida armamentista**: cada jogador compra 2 cartas (o tempo acelera).
- **Alarme falso**: o jogador que comprou embaralha as próximas N cartas.

## 7. Formas de vencer ✅ (militar, diplomática, tecnológica)

Inspirado em *Civilization*: vários caminhos para a vitória. ✅

### ☢️ Militar ✅

O seu ICBM atinge o oponente, e ele não tem nenhum ICBM em curso contra você
(não conseguiu retaliar nem se defender).

### 🕊️ Diplomática 💡

Você joga **Tratado**, que vai ao fundo **ativo**. Se ele voltar ao topo **sem que
nenhum ICBM tenha sido lançado nesse intervalo**, você vence pela diplomacia.

Isso cria tensão: para impedir a paz, o oponente precisa escalar. Ao escalar,
dá a você motivo e tempo para retaliar.

### 🚀 Tecnológica 💡

Cartas de tecnologia, ao serem jogadas, **ficam na mesa** à sua frente (não vão
ao fundo). Quem completar **Sputnik + Voo tripulado + Pouso na Lua** vence.

Efeito colateral interessante: cada tecnologia na mesa **encurta o baralho**, e
o tempo passa mais rápido para todos.

### ⏳ Fim do tempo: paz 💡

Quando a carta **Fim da Guerra Fria** for comprada pela **2ª vez** (ou seja,
depois de o baralho dar duas voltas), a partida termina em **paz** se ninguém
venceu antes.

## 8. Pontuação: teoria dos jogos ✅ ideia / 💡 valores

A ideia original: ✅

- Se ambos escolhem **não se destruir**, ambos ganham pontos.
- Se um lança e o outro não retalia nem se protege, o **lançador ganha mais** do que
  ganharia na paz, e o atingido ganha **zero**.
- Se ambos lançam, **ninguém ganha**.

Proposta de valores por partida, para jogar em **séries de várias partidas**: 💡

| Resultado | Vencedor | Perdedor |
|---|---|---|
| Vitória militar | **5** | 0 |
| Vitória diplomática | 4 | 1 |
| Vitória tecnológica | 4 | 1 |
| Paz (fim do tempo) | 3 | 3 |
| Destruição mútua | ❓ 0 ou −1 | ❓ 0 ou −1 |

### Nota de teoria dos jogos

Com **T** = atacar sem resposta (5), **R** = paz (3), **S** = ser atingido (0) e
**P** = destruição mútua:

- Se **P > S** (destruição mútua menos ruim que ser atingido), é o **Dilema do
  Prisioneiro**.
- Se **P < S** (destruição mútua é o pior de tudo), é o **Jogo do Covarde
  (Chicken)**, que é o modelo clássico da dissuasão nuclear.
- Com **P = S = 0**, fica exatamente na fronteira entre os dois.

Jogar em **séries** (várias partidas seguidas, somando pontos) transforma o jogo
num **dilema repetido**. Aí entram reputação, retaliação e estratégias como
*olho por olho* (tit-for-tat). Os bots da simulação podem testar isso, num estilo
de torneio de Axelrod.

❓ Uma partida isolada também deve valer, ou o jogo é pensado em séries?

## 9. Composição inicial do baralho 💡

Ponto de partida para a simulação; os números serão ajustados.

| Carta | Qtd |
|---|---|
| ICBM | 6 |
| Defesa antimíssil | 4 |
| Avião espião / Satélite | 4 |
| Serviço secreto | 4 |
| Tratado | 3 |
| Sputnik | 3 |
| Voo tripulado | 3 |
| Pouso na Lua | 3 |
| Crises | 4 |
| Fim da Guerra Fria | 1 |
| **Total** | **35** |

Com 35 cartas e 2 jogadores, uma carta jogada leva cerca de **17 rodadas** para
voltar ao topo (menos as cartas que estão nas mãos).

## 10. O que a simulação deve medir

- Taxa de vitória por tipo (militar / diplomática / tecnológica / paz / destruição mútua).
- Vantagem de quem começa.
- Duração média das partidas.
- Frequência de ICBM "sem resposta possível" (sinal de desequilíbrio).
- Impacto do **tamanho do baralho** (tempo de voo) em tudo acima.
- Valor de guardar um ICBM na mão como **ameaça** versus lançá-lo logo.
- Estratégias em séries de partidas (cooperar, trair, olho por olho...).

## Dúvidas em aberto ❓

1. O lançamento de ICBM é público ou escondido?
2. ICBM desativado volta ao baralho ou sai do jogo?
3. O que fazia a **proxy war**?
4. Quais eram as **Crises**?
5. Valor da destruição mútua: 0 ou negativo?
6. Partida isolada ou séries de partidas?
