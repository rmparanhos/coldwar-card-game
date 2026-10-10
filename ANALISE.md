# Análise de balanceamento

Torneios entre 6 estratégias automáticas (pomba, cordeiro, paranoico, oportunista,
falcão, olho por olho), em séries de 5 partidas, com 60 séries por confronto
(≈ 6.300 partidas por variante). Para reproduzir:

```bash
python3 -m guerrafria.experimentos --series 60
```

Os bots são simples e não pensam em pontos. Os números mostram tendências das
regras, não o jogo ideal de pessoas.

## Resultados por variante

| Variante | Militar | Diplom. | Tecnol. | Paz | Destr. mútua | Rodadas | Oportunista × Pomba |
|---|---|---|---|---|---|---|---|
| Regras atuais | 18% | **0%** | **48%** | 33% | 1% | 19,3 | 14,2 × 11,6 |
| Tratado no meio do baralho | 17% | 37% | 35% | 10% | 1% | 14,8 | 13,8 × 11,6 |
| Tecnologias em ordem | 19% | 0% | 46% | 34% | 1% | 19,6 | 14,4 × 11,8 |
| 1 cópia de cada tecnologia | 30% | 0% | 8% | 60% | 2% | 21,4 | 14,4 × 11,8 |
| Radar (2 cartas) | 18% | 0% | 48% | 33% | 1% | 19,3 | 14,4 × 11,5 |
| 2 Defesas | 22% | 0% | 47% | 30% | 2% | 18,4 | 14,9 × 10,7 |
| 1 Defesa | 23% | 0% | 46% | 25% | 6% | 17,2 | 14,5 × 10,1 |
| Destruição mútua = −1 | 18% | 0% | 48% | 33% | 1% | 19,3 | 14,2 × 11,4 |
| Segundo ataque | 18% | 0% | 48% | 33% | 1% | 19,3 | 14,2 × 11,6 |
| Segundo ataque + 1 Defesa | 22% | 0% | 46% | 25% | 7% | 17,2 | 14,5 × 10,1 |
| **Segundo ataque + 0 Defesa** | **0%** | 0% | 47% | 30% | **24%** | 16,8 | 14,1 × 13,2 |
| 2º ataque + 1 Defesa + Tratado no meio | 20% | 42% | 30% | 1% | 6% | 12,6 | 13,8 × 9,4 |

## Conclusões

1. **A vitória diplomática não existe nas regras atuais.** O Tratado leva o baralho
   inteiro para voltar, e até lá alguém já completou as tecnologias. Colocar o
   Tratado **no meio do baralho** resolve: a diplomacia passa a 37–50%.

2. **A tecnologia está fácil.** Com 2 cópias de cada, ela decide quase metade das
   partidas. Com 1 cópia, cai para 8%. Jogar em ordem quase não muda nada.

3. **A Defesa antimíssil quebra a dissuasão.** Em cerca de 80% dos impactos, o
   atacante tem uma Defesa na mão. Quem ataca segurando uma Defesa intercepta a
   retaliação e fica imune. Por isso, o segundo ataque e o radar não mudam nada
   enquanto houver 3 Defesas.

4. **Sem Defesas e com segundo ataque, a dissuasão funciona como na teoria.**
   Nenhum ataque compensa (0% de vitórias militares) e o falcão vira de longe a
   pior estratégia (4,1 pontos por série, contra 11–12 das outras). Foi a mesma
   lógica do **Tratado ABM de 1972**, que limitou os escudos antimísseis
   justamente para manter a destruição mútua assegurada.

5. **O valor da destruição mútua (0 ou −1) não muda nada nos bots**, porque eles
   não calculam pontos. Para testar isso, precisamos de bots que escolham pela
   pontuação esperada, ou de partidas entre pessoas.

6. **Quem começa vence cerca de 50%** em todas as variantes: não há vantagem de
   primeiro jogador.

## Perguntas de design que surgiram

- A Defesa deve existir? Uma alternativa temática é ela ser uma carta de mesa
  (um sistema instalado, à vista), que pode ser alvo de Sabotagem e que a carta
  "Tratado ABM" remove.
- Se a dissuasão funcionar bem demais, a militar some (0%). Quanto de vitória
  militar o jogo deve ter? Algum caminho para um ataque bem-sucedido é desejável
  (por exemplo, o oponente ter perdido o ICBM).
