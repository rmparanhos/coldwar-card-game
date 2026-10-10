# Guerra Fria — Regras (v0.1, rascunho)

Documento vivo. Cada regra tem uma marcação:

- ✅ **Confirmado**: veio do design original ou foi decidido.
- 💡 **Proposta**: sugestão para preencher lacunas; pode mudar.
- ❓ **Dúvida**: ainda precisa de decisão.

Inspirações: *Exploding Kittens* (comprar cartas como risco, cartas de reação),
*Civilization* (vários caminhos para a vitória) e a **dissuasão nuclear**
(destruição mútua assegurada).

Estas regras estão implementadas no simulador (`guerrafria/`). Os números
ajustáveis ficam em `guerrafria/config.py`.

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

## 2. Jogadores

- **2 jogadores** (EUA × URSS). 💡
- O jogo é disputado em **séries de várias partidas**, somando pontos. ✅
  Quem começa alterna a cada partida. 💡

## 3. Preparação

1. Cada jogador começa com **1 ICBM na mão**. O ICBM **não faz parte do baralho**. ✅
2. Separe as **Crises** e o **Fim da Guerra Fria**. Embaralhe o resto e dê
   **4 cartas** a cada jogador (mão inicial: ICBM + 4). 💡
3. Junte as Crises às cartas que sobraram e embaralhe. 💡
4. Coloque o **Fim da Guerra Fria** no **fundo** do baralho. 💡

## 4. Turno 💡

1. **Jogar** até 1 carta da mão (opcional): **aberta** ou **secreta** (seção 5).
2. **Comprar** 1 carta do topo. ✅
3. Limite de mão: **7 cartas**. O excesso vai para o fundo do baralho (o ICBM
   nunca pode ser descartado).

**Cartas de reação** (Veto na ONU, Ponte aérea, Defesa antimíssil) são usadas
fora do próprio turno, em resposta a algo.

## 5. Lançamento escondido e jogadas secretas

- O lançamento do ICBM é **escondido**: o oponente precisa *perceber*. ✅
- Como o ICBM só entra no baralho quando é lançado, **todo ICBM comprado do
  baralho está em voo** e detona. 💡
- **Jogada secreta** 💡: em vez de jogar uma carta aberta, o jogador põe
  **1 carta virada para baixo no fundo** do baralho. Pode ser o ICBM (o único jeito
  de lançá-lo) ou qualquer outra carta, sem efeito (**blefe**). O oponente vê que
  houve uma jogada secreta, mas não sabe qual carta foi.

Para perceber um lançamento, o jogador conta com:

- **Avião espião / Satélite**: vê as próximas cartas do topo, então só detecta o
  míssil quando ele já está **perto de chegar** (detecção tardia).
- **Serviço secreto**: vê a mão do oponente. Se o ICBM **sumiu da mão**, ele foi
  lançado.
- **Telefone vermelho** e **Crise dos Mísseis** (seção 6).
- **Leitura do oponente**: houve jogada secreta. Foi míssil ou blefe?

## 6. Cartas

### ☢️ Militar

| Carta | Qtd | Efeito |
|---|---|---|
| **ICBM** | 1 por jogador | Começa na mão. Lançado com uma jogada secreta. Quando chega ao topo, atinge o oponente (não importa quem o comprou). ✅ |
| **Defesa antimíssil** | 3 | **Reação:** quando um ICBM inimigo chega, intercepte-o. O míssil sai do jogo. ✅ ideia / 💡 momento de uso |
| **Submarino nuclear** | 1 | Fica na mesa. Se você for atingido com o ICBM ainda na mão, ele é lançado mesmo assim (**retaliação garantida**). 💡 |

### 🕵️ Espionagem

| Carta | Qtd | Efeito |
|---|---|---|
| **Avião espião / Satélite** | 3 | Olhe as 3 cartas do topo do baralho. ✅ |
| **Serviço secreto** | 2 | Olhe a mão do oponente. ✅ |
| **Agente duplo** | 2 | Roube 1 carta aleatória da mão do oponente (nunca o ICBM). 💡 |
| **Desertor** | 1 | Troque 1 carta da sua mão por 1 aleatória da mão do oponente (nunca o ICBM). 💡 |
| **Sabotagem** | 2 | Mande 1 tecnologia da mesa do oponente para o fundo do baralho. 💡 |

### ⏳ Tempo

| Carta | Qtd | Efeito |
|---|---|---|
| **Corrida armamentista** | 2 | Os dois jogadores compram 2 cartas: o tempo acelera. 💡 |
| **Bloqueio de Berlim** | 2 | O oponente compra 2 cartas no próximo turno. 💡 |
| **Ponte aérea** | 1 | **Reação:** anula um Bloqueio de Berlim jogado contra você. 💡 |
| **Desinformação** | 2 | Olhe as 3 cartas do topo e reordene como quiser. 💡 |

### 🕊️ Diplomacia

| Carta | Qtd | Efeito |
|---|---|---|
| **Tratado** | 3 | Vai ao fundo do baralho, aberto e girado 90°. Se voltar ao topo **sem nenhum ICBM em voo**, quem o jogou vence. 💡 |
| **Veto na ONU** | 3 | **Reação:** cancela qualquer carta jogada aberta, inclusive uma Defesa ou outro Veto (cadeia, como o *Nope*). 💡 |
| **Telefone vermelho** | 2 | O oponente diz a verdade: o ICBM dele está na mão, em voo ou fora de jogo? 💡 |

### 🚀 Tecnologia

| Carta | Qtd | Efeito |
|---|---|---|
| **Sputnik** | 2 | Fica na sua mesa. 💡 |
| **Voo tripulado** | 2 | Fica na sua mesa. 💡 |
| **Pouso na Lua** | 2 | Fica na sua mesa. Quem tiver as três tecnologias vence. 💡 |

### ⚠️ Crises

Resolvidas **ao serem compradas** (como o gatinho do *Exploding Kittens*), depois
vão para o fundo. Nunca ficam na mão.

| Carta | Qtd | Efeito |
|---|---|---|
| **Crise dos Mísseis** | 1 | Quem comprou revela se ainda tem o ICBM na mão. 💡 |
| **Alarme falso** | 1 | "O radar indica um ataque!" Quem comprou põe **agora** uma carta virada no fundo: o ICBM (lançamento) ou outra (blefe). 💡 |
| **Golpe de Estado** | 1 | Quem comprou manda 1 carta aleatória da mão para o fundo (nunca o ICBM). 💡 |
| **Escalada** | 1 | Todos os Tratados em curso são cancelados. 💡 |

### ⏳ Relógio

| Carta | Qtd | Efeito |
|---|---|---|
| **Fim da Guerra Fria** | 1 | Começa no fundo. Ao ser comprada, volta para o fundo. Na **2ª vez**, a partida termina em paz. 💡 |

**Total no baralho: 40 cartas** (mais os 2 ICBMs, que começam nas mãos).

### ❓ Guerra por procuração (proxy war)

Fazia parte do jogo original, mas o efeito foi esquecido.

## 7. Ataque, retaliação e defesa

- Cada jogador tem **um único ICBM por partida**. ✅
- **Retaliação**: enquanto um ICBM está em voo, o alvo pode lançar o próprio ICBM.
  Ele entra no fundo, *depois* do primeiro. ✅
- Quando um ICBM atinge o alvo e há um **míssil de retaliação já em voo**, o
  resultado é **destruição mútua: ninguém ganha**. ✅ A única salvação é o
  sobrevivente já ter uma **Defesa antimíssil na mão**. 💡
- Quem é atingido **antes** de lançar o seu ICBM não retalia mais, a não ser que
  tenha um **Submarino nuclear** na mesa. 💡
- Um ICBM interceptado pela Defesa **sai do jogo**. Como cada jogador só tem um,
  quem foi interceptado perdeu a sua arma. 💡

## 8. Formas de vencer ✅ (militar, diplomática, tecnológica)

| Vitória | Como |
|---|---|
| ☢️ **Militar** ✅ | O seu ICBM atinge o oponente e não há retaliação a caminho. |
| 🕊️ **Diplomática** 💡 | O seu Tratado volta ao topo sem nenhum ICBM em voo. |
| 🚀 **Tecnológica** 💡 | Ter Sputnik + Voo tripulado + Pouso na Lua na mesa. |
| ⏳ **Paz** 💡 | O Fim da Guerra Fria é comprado pela 2ª vez e ninguém venceu. |

## 9. Pontuação: teoria dos jogos

A ideia original: ✅

- Se ambos escolhem **não se destruir**, ambos ganham pontos.
- Se um lança e o outro não retalia nem se protege, o **lançador ganha mais** do que
  ganharia na paz, e o atingido ganha **zero**.
- Se ambos lançam, **ninguém ganha**.

Valores por partida (somados ao longo da série): 💡

| Resultado | Vencedor | Perdedor |
|---|---|---|
| Vitória militar | **5** | 0 |
| Vitória diplomática | 4 | 1 |
| Vitória tecnológica | 4 | 1 |
| Paz (fim do tempo) | 3 | 3 |
| Destruição mútua | 0 (❓ ou −1) | 0 (❓ ou −1) |

### Nota de teoria dos jogos

Com **T** = atacar sem resposta (5), **R** = paz (3), **S** = ser atingido (0) e
**P** = destruição mútua:

- Se **P > S** (destruição mútua menos ruim que ser atingido), é o **Dilema do
  Prisioneiro**.
- Se **P < S** (destruição mútua é o pior de tudo), é o **Jogo do Covarde
  (Chicken)**, que é o modelo clássico da dissuasão nuclear.
- Com **P = S = 0**, fica exatamente na fronteira entre os dois.

Jogar em **séries** transforma o jogo num **dilema repetido**: entram reputação,
retaliação e estratégias como *olho por olho* (tit-for-tat).

## Dúvidas em aberto ❓

1. O que fazia a **proxy war**?
2. Destruição mútua vale 0 ou negativo?
3. A Defesa antimíssil é usada **na chegada** do míssil (padrão, como o *Defuse*)
   ou **às cegas** no seu turno? O simulador testa as duas (`--defesa-cega`).

### Decididas

- ✅ Lançamento do ICBM é **escondido**.
- ✅ **1 ICBM por jogador**, começando na mão.
- ✅ O jogo é disputado em **séries**.
- ✅ Vitórias: militar, diplomática e tecnológica.
- ✅ Cartas novas aprovadas: Corrida armamentista, Bloqueio de Berlim, Ponte aérea,
  Desinformação, Agente duplo, Desertor, Sabotagem, Veto na ONU, Telefone vermelho,
  Submarino nuclear e as Crises.
