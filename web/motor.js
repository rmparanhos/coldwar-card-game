// Motor de regras do Guerra Fria (porte do guerrafria/motor.py para o navegador).
// O baralho é um array: índice 0 é o topo, o final é o fundo.
(function (raiz) {
  "use strict";

  const CARTAS = {
    ICBM: { curta: "Lance em segredo", nome: "ICBM", cat: "militar", desc: "Lance em segredo: vai virado para o fundo do baralho. Quando chegar ao topo, atinge o oponente." },
    DEFESA: { curta: "Intercepta um ICBM", nome: "Defesa antimíssil", cat: "militar", desc: "Reação: quando um ICBM inimigo chega ao topo, intercepte-o." },
    SUBMARINO: { curta: "Retaliação garantida", nome: "Submarino nuclear", cat: "militar", desc: "Fica na mesa. Se você for atingido com o ICBM ainda na mão, ele é lançado mesmo assim." },
    SATELITE: { curta: "Veja 3 do topo", nome: "Satélite", cat: "espionagem", desc: "Veja as 3 cartas do topo do baralho." },
    SERVICO_SECRETO: { curta: "Veja a mão dele", nome: "Serviço secreto", cat: "espionagem", desc: "Veja a mão do oponente." },
    AGENTE_DUPLO: { curta: "Roube 1 carta", nome: "Agente duplo", cat: "espionagem", desc: "Roube 1 carta aleatória da mão do oponente (nunca o ICBM)." },
    DESERTOR: { curta: "Troque 1 carta", nome: "Desertor", cat: "espionagem", desc: "Troque 1 carta sua por 1 carta aleatória do oponente (nunca o ICBM)." },
    SABOTAGEM: { curta: "Derrube 1 tecnologia", nome: "Sabotagem", cat: "espionagem", desc: "Mande 1 tecnologia da mesa do oponente para o fundo do baralho." },
    CORRIDA: { curta: "Todos compram 2", nome: "Corrida armamentista", cat: "tempo", desc: "Os dois jogadores compram 2 cartas: o tempo acelera." },
    BLOQUEIO: { curta: "Ele compra 2", nome: "Bloqueio de Berlim", cat: "tempo", desc: "O oponente compra 2 cartas no próximo turno." },
    PONTE_AEREA: { curta: "Anula o Bloqueio", nome: "Ponte aérea", cat: "tempo", desc: "Reação: anula um Bloqueio de Berlim jogado contra você." },
    DESINFORMACAO: { curta: "Reordene o topo", nome: "Desinformação", cat: "tempo", desc: "Veja as 3 cartas do topo e reordene como quiser." },
    TRATADO: { curta: "Vitória pela paz", nome: "Tratado", cat: "diplomacia", desc: "Vai ao fundo, à vista de todos. Se voltar ao topo sem nenhum ICBM em voo, você vence." },
    VETO: { curta: "Cancela 1 carta", nome: "Veto na ONU", cat: "diplomacia", desc: "Reação: cancela uma carta jogada aberta (inclusive outro Veto)." },
    TELEFONE: { curta: "Onde está o ICBM?", nome: "Telefone vermelho", cat: "diplomacia", desc: "O oponente diz a verdade: o ICBM dele está na mão, em voo ou fora de jogo?" },
    SPUTNIK: { curta: "Tecnologia 1 de 3", nome: "Sputnik", cat: "tecnologia", desc: "Fica na mesa. Junte as três tecnologias para vencer." },
    VOO_TRIPULADO: { curta: "Tecnologia 2 de 3", nome: "Voo tripulado", cat: "tecnologia", desc: "Fica na mesa. Junte as três tecnologias para vencer." },
    POUSO_LUA: { curta: "Tecnologia 3 de 3", nome: "Pouso na Lua", cat: "tecnologia", desc: "Fica na mesa. Junte as três tecnologias para vencer." },
    CRISE_MISSEIS: { curta: "Revele o ICBM", nome: "Crise dos Mísseis", cat: "crise", desc: "Quem comprou revela se ainda tem o ICBM na mão." },
    ALARME_FALSO: { curta: "Decida agora", nome: "Alarme falso", cat: "crise", desc: "Quem comprou põe agora uma carta virada no fundo: o ICBM ou outra (blefe)." },
    GOLPE: { curta: "Perca 1 carta", nome: "Golpe de Estado", cat: "crise", desc: "Quem comprou perde 1 carta aleatória da mão para o fundo do baralho." },
    ESCALADA: { curta: "Tratados caem", nome: "Escalada", cat: "crise", desc: "Todos os Tratados em curso são cancelados." },
    FIM: { curta: "Relógio da partida", nome: "Fim da Guerra Fria", cat: "relogio", desc: "Na segunda vez em que for comprada, a partida termina em paz." },
  };

  const ORDEM_TEC = ["SPUTNIK", "VOO_TRIPULADO", "POUSO_LUA"];
  const TECNOLOGIAS = new Set(ORDEM_TEC);
  const CRISES = new Set(["CRISE_MISSEIS", "ALARME_FALSO", "GOLPE", "ESCALADA"]);
  const REACOES = new Set(["VETO", "PONTE_AEREA"]);
  const LADOS = ["EUA", "URSS"];

  const MAO = "mao", VOO = "voo", INTERCEPTADO = "interceptado", DETONADO = "detonado", DESCONHECIDO = "desconhecido";

  function configPadrao() {
    return {
      baralho: {
        DEFESA: 3, SUBMARINO: 1, SATELITE: 3, SERVICO_SECRETO: 2, AGENTE_DUPLO: 2, DESERTOR: 1,
        SABOTAGEM: 2, CORRIDA: 2, BLOQUEIO: 2, PONTE_AEREA: 1, DESINFORMACAO: 2, TRATADO: 3,
        VETO: 3, TELEFONE: 2, SPUTNIK: 2, VOO_TRIPULADO: 2, POUSO_LUA: 2,
        CRISE_MISSEIS: 1, ALARME_FALSO: 1, GOLPE: 1, ESCALADA: 1, FIM: 1,
      },
      maoInicial: 4,
      limiteMao: 7,
      fimLimite: 2,
      cartasSatelite: 3,
      cartasDesinformacao: 3,
      tecnologiaEmOrdem: false,
      tratadoNoMeio: false,
      radar: 0,
      segundoAtaque: false,
      pontos: {
        militar: [5, 0], diplomatica: [4, 1], tecnologica: [4, 1], paz: [3, 3], destruicao_mutua: [0, 0],
      },
      maxTurnos: 400,
    };
  }

  let proximoId = 1;
  function carta(tipo, dono = null) {
    return { id: proximoId++, tipo, dono, pendente: false };
  }

  class FimDePartida extends Error {}

  function embaralhar(arr, rng) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(rng() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  // Jogadores (humano ou bot) implementam, todos podendo devolver Promises:
  //   escolherJogada(v) -> {carta, secreta, alvo} | null
  //   querVetar(v, tipo, autor), usarDefesa(v), usarPonteAerea(v), alarmeLancar(v) -> bool
  //   reordenar(v, cartas) -> cartas, descartar(v, n) -> cartas
  //   observar(v, evento) -> informação privada (opcional)
  // ouvinte.evento(texto, privado) é chamado a cada acontecimento;
  // `privado` = {jogador, texto}: versão que só aquele jogador pode ver.
  class Partida {
    constructor(jogadores, cfg, opcoes = {}) {
      this.cfg = cfg || configPadrao();
      this.rng = opcoes.rng || Math.random;
      this.jogadores = jogadores;
      this.primeiro = opcoes.primeiro || 0;
      this.ouvinte = opcoes.ouvinte || null;
      this.baralho = [];
      this.maos = [[], []];
      this.mesas = [[], []];
      this.icbm = [MAO, MAO];
      this.intel = [{ estado: MAO, secretas: 0 }, { estado: MAO, secretas: 0 }];
      this.fimContagem = 0;
      this.turno = 0;
      this.vez = this.primeiro;
      this.comprasExtras = [0, 0];
      this.primeiroLancamento = null;
      this.lancamentos = [];
      this.resultado = null;
      this._preparar();
    }

    _preparar() {
      const normais = [], crises = [], fim = [];
      for (const [tipo, qtd] of Object.entries(this.cfg.baralho)) {
        for (let i = 0; i < qtd; i++) {
          const c = carta(tipo);
          if (tipo === "FIM") fim.push(c);
          else if (CRISES.has(tipo)) crises.push(c);
          else normais.push(c);
        }
      }
      embaralhar(normais, this.rng);
      for (const p of [0, 1]) {
        this.maos[p] = [carta("ICBM", p)];
        for (let i = 0; i < this.cfg.maoInicial; i++) this.maos[p].push(normais.pop());
      }
      const resto = embaralhar(normais.concat(crises), this.rng);
      this.baralho = resto.concat(fim);
    }

    // ---------------------------------------------------------------- utilidades

    _evento(texto, privado = null) {
      if (this.ouvinte) this.ouvinte.evento(texto, privado);
    }

    async _pausa() {
      if (this.ouvinte && this.ouvinte.pausa) await this.ouvinte.pausa();
    }

    _encerrar(tipo, vencedor) {
      const [vit, der] = this.cfg.pontos[tipo];
      let pontos;
      if (vencedor === null) pontos = [vit, vit];
      else pontos = vencedor === 0 ? [vit, der] : [der, vit];
      this.resultado = {
        tipo, vencedor, turnos: this.turno, primeiroJogador: this.primeiro,
        primeiroLancamento: this.primeiroLancamento, lancamentos: this.lancamentos.slice(), pontos,
      };
      throw new FimDePartida();
    }

    _tratadoPendente(dono) {
      return this.baralho.some((c) => c.tipo === "TRATADO" && c.pendente && c.dono === dono);
    }

    _semIcbm(cartas) {
      return cartas.filter((c) => c.tipo !== "ICBM");
    }

    _tirar(p, tipo) {
      const i = this.maos[p].findIndex((c) => c.tipo === tipo);
      return i < 0 ? null : this.maos[p].splice(i, 1)[0];
    }

    _remover(lista, c) {
      const i = lista.indexOf(c);
      if (i >= 0) lista.splice(i, 1);
    }

    _escolher(lista) {
      return lista[Math.floor(this.rng() * lista.length)];
    }

    jogaveis(p) {
      const mesa = new Set(this.mesas[p].map((c) => c.tipo));
      const oponenteTemTec = this.mesas[1 - p].some((c) => TECNOLOGIAS.has(c.tipo));
      return this.maos[p].filter((c) => {
        const t = c.tipo;
        if (t === "ICBM" || REACOES.has(t) || t === "DEFESA") return false;
        if (TECNOLOGIAS.has(t)) {
          if (mesa.has(t)) return false;
          if (this.cfg.tecnologiaEmOrdem) {
            const anteriores = ORDEM_TEC.slice(0, ORDEM_TEC.indexOf(t));
            if (!anteriores.every((a) => mesa.has(a))) return false;
          }
        }
        if (t === "SABOTAGEM" && !oponenteTemTec) return false;
        return true;
      });
    }

    visao(p) {
      const o = 1 - p;
      return {
        eu: p,
        mao: this.maos[p].slice(),
        mesa: this.mesas[p].slice(),
        mesaOponente: this.mesas[o].slice(),
        nMaoOponente: this.maos[o].length,
        tamanhoBaralho: this.baralho.length,
        meuIcbm: this.icbm[p],
        icbmOponente: this.intel[p].estado,
        secretasOponente: this.intel[p].secretas,
        meuTratadoPendente: this._tratadoPendente(p),
        tratadoOponentePendente: this._tratadoPendente(o),
        turno: this.turno,
        fimContagem: this.fimContagem,
        jogaveis: this.jogaveis(p),
        cfg: this.cfg,
      };
    }

    _revelarPara(observador) {
      const estado = this.icbm[1 - observador];
      this.intel[observador].estado = estado === DETONADO ? VOO : estado;
      this.intel[observador].secretas = 0;
      return this.intel[observador].estado;
    }

    _observar(p, cartas) {
      if (cartas.some((c) => c.tipo === "ICBM" && c.dono === 1 - p)) this.intel[p].estado = VOO;
    }

    async _avisar(p, evento) {
      const j = this.jogadores[p];
      if (j.observar) await j.observar(this.visao(p), evento);
    }

    // ------------------------------------------------------------------ partida

    async jogar() {
      let p = this.primeiro;
      try {
        while (this.turno < this.cfg.maxTurnos) {
          this.turno++;
          this.vez = p;
          await this._turno(p);
          p = 1 - p;
        }
        this._encerrar("paz", null);
      } catch (e) {
        if (!(e instanceof FimDePartida)) throw e;
      }
      return this.resultado;
    }

    async _turno(p) {
      const jogada = await this.jogadores[p].escolherJogada(this.visao(p));
      if (jogada) await this._executar(p, jogada);
      const compras = 1 + this.comprasExtras[p];
      this.comprasExtras[p] = 0;
      for (let i = 0; i < compras; i++) await this._comprar(p);
      await this._limiteMao(p);
      this._radar();
      await this._pausa();
    }

    _radar() {
      for (const c of this.baralho.slice(0, this.cfg.radar)) {
        if (c.tipo === "ICBM" && this.intel[1 - c.dono].estado !== VOO) {
          this.intel[1 - c.dono].estado = VOO;
          this._evento(`Radar de ${LADOS[1 - c.dono]} detecta um ICBM chegando!`);
        }
      }
    }

    async _limiteMao(p) {
      const excesso = this.maos[p].length - this.cfg.limiteMao;
      if (excesso <= 0) return;
      const escolhidas = (await this.jogadores[p].descartar(this.visao(p), excesso)) || [];
      const validas = escolhidas.filter((c) => this.maos[p].includes(c) && c.tipo !== "ICBM");
      for (const c of this._semIcbm(this.maos[p])) {
        if (validas.length >= excesso) break;
        if (!validas.includes(c)) validas.push(c);
      }
      for (const c of validas.slice(0, excesso)) {
        this._remover(this.maos[p], c);
        this.baralho.push(c);
      }
      this._evento(`${LADOS[p]} descarta ${excesso} carta(s) para o fundo (limite de mão)`);
    }

    // ------------------------------------------------------------------ jogadas

    _jogadaSecreta(p, c) {
      this.baralho.push(c);
      if (c.tipo === "ICBM") {
        c.dono = p;
        this.icbm[p] = VOO;
        if (this.primeiroLancamento === null) this.primeiroLancamento = p;
        this.lancamentos.push({ jogador: p, turno: this.turno });
        this._evento(`${LADOS[p]} põe uma carta virada no fundo do baralho`, {
          jogador: p, texto: `Você LANÇA o seu ICBM em segredo`,
        });
      } else {
        this._evento(`${LADOS[p]} põe uma carta virada no fundo do baralho`, {
          jogador: p, texto: `Você põe ${CARTAS[c.tipo].nome} virada no fundo (blefe)`,
        });
      }
      const intel = this.intel[1 - p];
      intel.secretas++;
      if (intel.estado === MAO) intel.estado = DESCONHECIDO;
    }

    async _executar(p, jogada) {
      const c = jogada.carta;
      if (!this.maos[p].includes(c)) throw new Error("carta fora da mão");
      if (jogada.secreta) {
        this._remover(this.maos[p], c);
        this._jogadaSecreta(p, c);
        return;
      }
      if (!this.jogaveis(p).includes(c)) throw new Error("carta não jogável");
      this._remover(this.maos[p], c);
      this._evento(`${LADOS[p]} joga ${CARTAS[c.tipo].nome}`);
      if (await this._vetado(p, c)) {
        this.baralho.push(c);
        return;
      }
      await this._efeito(p, c, jogada.alvo || null);
    }

    async _vetado(autor, c) {
      let vetado = false;
      let reagente = 1 - autor;
      for (;;) {
        if (!this.maos[reagente].some((x) => x.tipo === "VETO")) break;
        if (!(await this.jogadores[reagente].querVetar(this.visao(reagente), c.tipo, autor))) break;
        this.baralho.push(this._tirar(reagente, "VETO"));
        vetado = !vetado;
        this._evento(`${LADOS[reagente]} usa Veto na ONU contra ${CARTAS[c.tipo].nome}`);
        reagente = 1 - reagente;
      }
      if (vetado) this._evento(`${CARTAS[c.tipo].nome} foi cancelada`);
      return vetado;
    }

    async _efeito(p, c, alvo) {
      const o = 1 - p;
      const t = c.tipo;

      if (TECNOLOGIAS.has(t) || t === "SUBMARINO") {
        this.mesas[p].push(c);
        if (TECNOLOGIAS.has(t) && ORDEM_TEC.every((x) => this.mesas[p].some((m) => m.tipo === x))) {
          this._evento(`${LADOS[p]} completa a corrida espacial!`);
          this._encerrar("tecnologica", p);
        }
        return;
      }

      if (t === "TRATADO") {
        c.dono = p;
        c.pendente = true;
        if (this.cfg.tratadoNoMeio) this.baralho.splice(Math.floor(this.baralho.length / 2), 0, c);
        else this.baralho.push(c);
        return;
      }

      if (t === "SATELITE") {
        const topo = this.baralho.slice(0, this.cfg.cartasSatelite);
        this._observar(p, topo);
        await this._avisar(p, { tipo: "topo", cartas: topo });
      } else if (t === "SERVICO_SECRETO") {
        this._revelarPara(p);
        await this._avisar(p, { tipo: "mao", cartas: this.maos[o].slice() });
      } else if (t === "TELEFONE") {
        const estado = this._revelarPara(p);
        await this._avisar(p, { tipo: "estado", estado });
      } else if (t === "CORRIDA") {
        this.baralho.push(c);
        for (const q of [p, o]) for (let i = 0; i < 2; i++) await this._comprar(q);
        return;
      } else if (t === "BLOQUEIO") {
        let ponte = null;
        if (this.maos[o].some((x) => x.tipo === "PONTE_AEREA") && (await this.jogadores[o].usarPonteAerea(this.visao(o)))) {
          ponte = this._tirar(o, "PONTE_AEREA");
          this._evento(`${LADOS[o]} responde com Ponte aérea`);
        }
        if (ponte && !(await this._vetado(o, ponte))) {
          this.baralho.push(ponte);
        } else {
          if (ponte) this.baralho.push(ponte);
          this.comprasExtras[o]++;
        }
      } else if (t === "DESINFORMACAO") {
        const n = Math.min(this.cfg.cartasDesinformacao, this.baralho.length);
        const topo = this.baralho.splice(0, n);
        this._observar(p, topo);
        let nova = await this.jogadores[p].reordenar(this.visao(p), topo.slice());
        const mesmo = nova && nova.length === topo.length && topo.every((x) => nova.includes(x));
        if (!mesmo) nova = topo;
        this.baralho.unshift(...nova);
      } else if (t === "AGENTE_DUPLO") {
        const cand = this._semIcbm(this.maos[o]);
        if (cand.length) {
          const roubada = this._escolher(cand);
          this._remover(this.maos[o], roubada);
          this.maos[p].push(roubada);
          this._evento(`${LADOS[p]} rouba uma carta de ${LADOS[o]}`, {
            jogador: p, texto: `Você rouba ${CARTAS[roubada.tipo].nome} de ${LADOS[o]}`,
          });
          this._evento("", { jogador: o, texto: `${LADOS[p]} roubou a sua ${CARTAS[roubada.tipo].nome}` });
        }
      } else if (t === "DESERTOR") {
        const minhas = this._semIcbm(this.maos[p]);
        const dele = this._semIcbm(this.maos[o]);
        if (minhas.length && dele.length) {
          const entrega = minhas.includes(alvo) ? alvo : minhas[0];
          const recebe = this._escolher(dele);
          this._remover(this.maos[p], entrega);
          this._remover(this.maos[o], recebe);
          this.maos[o].push(entrega);
          this.maos[p].push(recebe);
          this._evento(`${LADOS[p]} troca uma carta com ${LADOS[o]}`, {
            jogador: p, texto: `Você entrega ${CARTAS[entrega.tipo].nome} e recebe ${CARTAS[recebe.tipo].nome}`,
          });
          this._evento("", {
            jogador: o, texto: `Você perde ${CARTAS[recebe.tipo].nome} e recebe ${CARTAS[entrega.tipo].nome}`,
          });
        }
      } else if (t === "SABOTAGEM") {
        const techs = this.mesas[o].filter((x) => TECNOLOGIAS.has(x.tipo));
        if (techs.length) {
          const destruida = techs.includes(alvo) ? alvo : techs[0];
          this._remover(this.mesas[o], destruida);
          this.baralho.push(destruida);
          this._evento(`${CARTAS[destruida.tipo].nome} de ${LADOS[o]} é sabotado`);
        }
      }
      this.baralho.push(c);
    }

    // ------------------------------------------------------------------ compras

    async _comprar(p) {
      if (!this.baralho.length) return;
      const c = this.baralho.shift();
      const t = c.tipo;

      if (t === "ICBM") {
        await this._chegadaIcbm(c);
        return;
      }
      if (t === "TRATADO" && c.pendente) {
        c.pendente = false;
        if (!this.icbm.includes(VOO)) {
          this._evento(`O Tratado de ${LADOS[c.dono]} volta ao topo em paz`);
          this._encerrar("diplomatica", c.dono);
        }
        this._evento(`O Tratado de ${LADOS[c.dono]} fracassa`);
      } else if (t === "FIM") {
        this.fimContagem++;
        this._evento(`Fim da Guerra Fria comprada (${this.fimContagem}/${this.cfg.fimLimite})`);
        this.baralho.push(c);
        if (this.fimContagem >= this.cfg.fimLimite) this._encerrar("paz", null);
        return;
      } else if (CRISES.has(t)) {
        this._evento(`CRISE! ${LADOS[p]} compra ${CARTAS[t].nome}`);
        await this._crise(p, c);
        this.baralho.push(c);
        return;
      }
      this.maos[p].push(c);
      this._evento("", { jogador: p, texto: `Você compra ${CARTAS[t].nome}` });
    }

    async _crise(p, c) {
      const t = c.tipo;
      if (t === "CRISE_MISSEIS") {
        const tem = this.icbm[p] === MAO;
        this._revelarPara(1 - p);
        this._evento(`${LADOS[p]} revela: o ICBM ${tem ? "ainda está na mão" : "NÃO está na mão"}`);
      } else if (t === "ALARME_FALSO") {
        if (this.icbm[p] === MAO && (await this.jogadores[p].alarmeLancar(this.visao(p)))) {
          this._jogadaSecreta(p, this._tirar(p, "ICBM"));
        } else {
          const outras = this._semIcbm(this.maos[p]);
          if (outras.length) {
            const escolhida = this._escolher(outras);
            this._remover(this.maos[p], escolhida);
            this._jogadaSecreta(p, escolhida);
          }
        }
      } else if (t === "GOLPE") {
        const outras = this._semIcbm(this.maos[p]);
        if (outras.length) {
          const perdida = this._escolher(outras);
          this._remover(this.maos[p], perdida);
          this.baralho.push(perdida);
          this._evento(`${LADOS[p]} perde uma carta no golpe`, {
            jogador: p, texto: `Você perde ${CARTAS[perdida.tipo].nome} no golpe`,
          });
        }
      } else if (t === "ESCALADA") {
        for (const x of this.baralho) if (x.tipo === "TRATADO") x.pendente = false;
        this._evento("Todos os Tratados em curso foram cancelados");
      }
    }

    // ------------------------------------------------------------------ ataques

    _interceptar(atacante) {
      this.icbm[atacante] = INTERCEPTADO;
      this.intel[1 - atacante].estado = INTERCEPTADO;
      this._evento(`O ICBM de ${LADOS[atacante]} foi INTERCEPTADO`);
    }

    async _chegadaIcbm(missil) {
      const atacante = missil.dono;
      const alvo = 1 - atacante;
      this._evento(`☢ O ICBM de ${LADOS[atacante]} chega ao alvo!`);
      if (this.maos[alvo].some((x) => x.tipo === "DEFESA") && (await this.jogadores[alvo].usarDefesa(this.visao(alvo)))) {
        const defesa = this._tirar(alvo, "DEFESA");
        this.baralho.push(defesa);
        this._evento(`${LADOS[alvo]} usa Defesa antimíssil`);
        if (!(await this._vetado(alvo, defesa))) {
          this._interceptar(atacante);
          return;
        }
      }
      this._impacto(alvo);
    }

    _impacto(alvo) {
      const atacante = 1 - alvo;
      this.icbm[atacante] = DETONADO;
      this._evento(`${LADOS[alvo]} é ATINGIDO`);
      const submarino = this.mesas[alvo].some((x) => x.tipo === "SUBMARINO");
      if (this.icbm[alvo] === MAO && (submarino || this.cfg.segundoAtaque)) {
        this._evento(`${LADOS[alvo]} retalia com o segundo ataque`);
        const missil = this._tirar(alvo, "ICBM");
        missil.dono = alvo;
        this.icbm[alvo] = VOO;
        this.baralho.push(missil);
      }
      if (this.icbm[alvo] === VOO) {
        // A retaliação já está em voo: só uma Defesa na mão do sobrevivente o salva.
        if (this.maos[atacante].some((x) => x.tipo === "DEFESA")) {
          this._remover(this.baralho, this.baralho.find((x) => x.tipo === "ICBM"));
          this._interceptar(alvo);
          this._encerrar("militar", atacante);
        }
        this._evento(`A retaliação de ${LADOS[alvo]} atinge ${LADOS[atacante]}`);
        this._encerrar("destruicao_mutua", null);
      }
      this._encerrar("militar", atacante);
    }
  }

  // --------------------------------------------------------------------- bots

  const VALOR = {
    DEFESA: 9, VETO: 8, SUBMARINO: 8, SPUTNIK: 6, VOO_TRIPULADO: 6, POUSO_LUA: 6, TRATADO: 6,
    SABOTAGEM: 5, SERVICO_SECRETO: 5, TELEFONE: 4, SATELITE: 4, AGENTE_DUPLO: 4, PONTE_AEREA: 3,
    DESINFORMACAO: 3, DESERTOR: 2, BLOQUEIO: 2, CORRIDA: 1,
  };

  class Estrategista {
    // primeiroAtaque: "nunca" | "oportunista" | "sempre"
    constructor({ primeiroAtaque = "nunca", retalia = true, paranoia = 0, blefe = 0.1, rng = Math.random } = {}) {
      Object.assign(this, { primeiroAtaque, retalia, paranoia, blefe, rng });
    }

    inicioPartida(eu) {
      this.eu = eu;
      this.secretasVistas = 0;
      this.suspeita = false;
    }

    fimPartida() {}

    _oponenteAtacou(v) {
      if (v.icbmOponente === VOO) return true;
      if (v.secretasOponente > this.secretasVistas) {
        const novas = v.secretasOponente - this.secretasVistas;
        this.secretasVistas = v.secretasOponente;
        for (let i = 0; i < novas; i++) if (this.rng() < this.paranoia) this.suspeita = true;
      } else if (v.secretasOponente < this.secretasVistas) {
        this.secretasVistas = v.secretasOponente;
      }
      return this.suspeita && v.icbmOponente === DESCONHECIDO;
    }

    _querLancar(v) {
      if (v.meuIcbm !== MAO) return false;
      if (this.retalia && this._oponenteAtacou(v)) return true;
      if (this.primeiroAtaque === "sempre") return true;
      if (this.primeiroAtaque === "oportunista") {
        const temDefesa = v.mao.some((c) => c.tipo === "DEFESA");
        const semResposta = v.icbmOponente === INTERCEPTADO;
        const naMao = v.icbmOponente === MAO && v.secretasOponente === 0;
        return semResposta || (temDefesa && naMao);
      }
      return false;
    }

    escolherJogada(v) {
      if (this._querLancar(v)) return { carta: v.mao.find((c) => c.tipo === "ICBM"), secreta: true };
      const por = {};
      for (const c of v.jogaveis) if (!por[c.tipo]) por[c.tipo] = c;
      const j = (t, extra = {}) => Object.assign({ carta: por[t], secreta: false }, extra);

      for (const t of ORDEM_TEC) if (por[t]) return j(t);
      if (por.SUBMARINO && v.meuIcbm === MAO) return j("SUBMARINO");
      const techsOp = v.mesaOponente.filter((c) => TECNOLOGIAS.has(c.tipo));
      if (por.SABOTAGEM && techsOp.length >= 2) return j("SABOTAGEM", { alvo: techsOp[0] });
      if (v.icbmOponente === DESCONHECIDO) {
        for (const t of ["SERVICO_SECRETO", "TELEFONE", "SATELITE"]) if (por[t]) return j(t);
      }
      if (por.TRATADO && !v.meuTratadoPendente && v.meuIcbm === MAO) return j("TRATADO");
      if (por.AGENTE_DUPLO && v.nMaoOponente > 1) return j("AGENTE_DUPLO");
      if (por.DESINFORMACAO && v.icbmOponente === VOO) return j("DESINFORMACAO");
      if (por.BLOQUEIO) return j("BLOQUEIO");
      if (por.DESERTOR) {
        const outras = v.mao.filter((c) => c !== por.DESERTOR && c.tipo !== "ICBM");
        if (outras.length) {
          const pior = outras.reduce((a, b) => ((VALOR[a.tipo] || 0) <= (VALOR[b.tipo] || 0) ? a : b));
          return j("DESERTOR", { alvo: pior });
        }
      }
      if (this.rng() < this.blefe) {
        const fracas = v.mao.filter((c) => c.tipo !== "ICBM" && (VALOR[c.tipo] || 0) <= 3);
        if (fracas.length) return { carta: fracas[Math.floor(this.rng() * fracas.length)], secreta: true };
      }
      return null;
    }

    querVetar(v, tipo, autor) {
      if (autor === v.eu) return TECNOLOGIAS.has(tipo) || ["DEFESA", "TRATADO", "SABOTAGEM"].includes(tipo);
      if (tipo === "DEFESA" || tipo === "SABOTAGEM") return true;
      if (TECNOLOGIAS.has(tipo)) return v.mesaOponente.some((c) => TECNOLOGIAS.has(c.tipo));
      if (["TRATADO", "SERVICO_SECRETO", "TELEFONE"].includes(tipo)) return v.meuIcbm === VOO;
      return false;
    }

    usarDefesa() { return true; }
    usarPonteAerea() { return true; }

    alarmeLancar(v) {
      if (!this.retalia) return false;
      return (v.icbmOponente === VOO || v.icbmOponente === DESCONHECIDO) && this.rng() < Math.max(this.paranoia, 0.2);
    }

    reordenar(v, cartas) {
      const chave = (c) => {
        if (c.tipo === "ICBM") return c.dono !== v.eu ? 2 : -1;
        if (c.tipo === "TRATADO" && c.pendente && c.dono === v.eu) return -1;
        if (c.tipo === "DEFESA") return 0;
        return 1;
      };
      return cartas.slice().sort((a, b) => chave(a) - chave(b));
    }

    descartar(v, n) {
      return v.mao.filter((c) => c.tipo !== "ICBM").sort((a, b) => (VALOR[a.tipo] || 0) - (VALOR[b.tipo] || 0)).slice(0, n);
    }
  }

  class OlhoPorOlho extends Estrategista {
    constructor(op = {}) {
      super(Object.assign({}, op, { primeiroAtaque: "nunca" }));
      this.traido = false;
    }
    inicioPartida(eu) {
      super.inicioPartida(eu);
      this.primeiroAtaque = this.traido ? "sempre" : "nunca";
    }
    fimPartida(r) {
      this.traido = r.primeiroLancamento !== null && r.primeiroLancamento !== this.eu;
    }
  }

  const ESTRATEGIAS = {
    pomba: { nome: "Pomba", desc: "Nunca ataca primeiro; retalia se descobrir um lançamento.", criar: (rng) => new Estrategista({ rng }) },
    oportunista: { nome: "Oportunista", desc: "Ataca primeiro quando acha que sai impune.", criar: (rng) => new Estrategista({ primeiroAtaque: "oportunista", rng }) },
    falcao: { nome: "Falcão", desc: "Lança o ICBM logo no início.", criar: (rng) => new Estrategista({ primeiroAtaque: "sempre", rng }) },
    paranoico: { nome: "Paranoico", desc: "Desconfia de toda jogada secreta e retalia por precaução.", criar: (rng) => new Estrategista({ paranoia: 0.3, rng }) },
    olho_por_olho: { nome: "Olho por olho", desc: "Pacífico, até ser atacado primeiro numa partida anterior.", criar: (rng) => new OlhoPorOlho({ rng }) },
  };

  const api = {
    CARTAS, ORDEM_TEC, TECNOLOGIAS, CRISES, LADOS, MAO, VOO, INTERCEPTADO, DETONADO, DESCONHECIDO,
    configPadrao, Partida, Estrategista, OlhoPorOlho, ESTRATEGIAS,
  };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else raiz.GuerraFria = api;
})(typeof window !== "undefined" ? window : globalThis);
