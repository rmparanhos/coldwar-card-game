# Guerra Fria — jogo de cartas

Jogo de cartas sobre a Guerra Fria, com regras em [`REGRAS.md`](REGRAS.md), e um
simulador em Python para validar regras e balanceamento com partidas automáticas.

## Versão jogável

Abra `web/index.html` num navegador (ou sirva a pasta `web/`) para jogar contra um
bot, com placar de série e as variantes de regra em teste.

## Como rodar o simulador

Requer Python 3.10+ e nenhuma dependência externa.

```bash
# Uma partida narrada entre duas estratégias
python3 -m guerrafria.simulador --semente 7 partida pomba falcao

# Várias séries entre duas estratégias
python3 -m guerrafria.simulador duelo pomba oportunista --series 500

# Todas as estratégias contra todas
python3 -m guerrafria.simulador torneio --series 100

# Variantes de regra
python3 -m guerrafria.simulador --defesa-cega --fim-limite 3 torneio

# Comparar todas as variantes (resultados em ANALISE.md)
python3 -m guerrafria.experimentos --series 60

# Testes
python3 -m unittest
```

## Estrutura

| Arquivo | Conteúdo |
|---|---|
| `guerrafria/cartas.py` | Tipos de carta |
| `guerrafria/config.py` | Composição do baralho, pontuação e variantes de regra |
| `guerrafria/motor.py` | Motor de regras: turno, efeitos, vitórias |
| `guerrafria/bots.py` | Estratégias automáticas |
| `guerrafria/simulador.py` | Partidas, duelos, torneios e relatórios |
| `guerrafria/experimentos.py` | Comparação de variantes de regra |
| `web/motor.js` | O mesmo motor de regras, em JavaScript |
| `web/index.html` | Versão jogável no navegador |

## Estratégias (bots)

| Nome | Postura |
|---|---|
| `pomba` | Nunca ataca primeiro; retalia quando descobre um lançamento. |
| `cordeiro` | Nunca ataca, nem em retaliação. |
| `paranoico` | Como a pomba, mas trata jogadas secretas do oponente como possível ataque. |
| `oportunista` | Ataca primeiro quando acha que sai impune (tem Defesa ou o oponente perdeu o ICBM). |
| `falcao` | Lança o ICBM logo no início. |
| `olho_por_olho` | Na série, só passa a atacar primeiro se o oponente atacou primeiro antes. |
| `aleatorio` | Jogadas aleatórias (referência). |
