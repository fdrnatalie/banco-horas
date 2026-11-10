// Três Taças — base do painel. Mantido pelo estrategista.
// status (o que o index.html lê): ideia | gravado | edicao | aprovacao | aprovado | programado | postado
// etapa (o que a Natalie vê no plano): fazer | editar | aprovar | agendado | postado | confirmar
//   fazer = ideia/gravado · editar = edicao · aprovar = aprovacao · agendado = programado · confirmar = não sabemos se já foi ao ar
// dono: quem precisa agir agora ("natalie" ou "equipe"). data: AAAA-MM-DD · hora: HH:MM (Brasília). pendente = próximo passo.
// Regra: só vira "programado/agendado" peça com arquivo final aprovado e já agendada na ferramenta.
// Regra das IG que apontam para o YouTube: só saem no dia em que o episódio já está no ar (ou depois).
// Plano completo: tres-tacas/plano_estrategia.md
// Grade: YouTube qui 18:00 · IG qui 19:30 (gancho) · IG sáb 11:00 (quiz) · IG ter 19:00 (curiosidade) · Shorts sex 12:00 · dom 19:00 só bônus.
window.TT_DATA = {
  atualizado: "10/11/2026",
  cadencia: {
    padrao: "1 YouTube + 3 Instagram + 1 Short por semana",
    minimo: "1 YouTube + 2 Instagram (gancho de quinta + quiz de sábado) + 1 Short",
    semanaCheia: "Natalie não faz nada na semana: a fila agendada roda sozinha; aprovações novas passam para a sessão seguinte",
    sessaoSemanal: "1 sessão fixa de 30 min por semana (sugestão: segunda 20:00) para aprovar e agendar tudo das próximas 2 semanas",
    fila: "Sempre 2 semanas de posts aprovados e agendados. Se a fila cair abaixo de 1 semana, a semana seguinte entra no mínimo."
  },

  // Material bruto que chegou (Drive / editor). status: novo, a analisar | em análise | em edição | editado | arquivado
  material: [
    {pasta: "9-11 (Drive)", gravado: "2026-11-09", subiu: "até 10/11 (data exata: conferir no Drive)",
     arquivos: ["IMG_2392.MOV", "IMG_2393.MOV", "IMG_2394.MOV", "IMG_2395.MOV", "gravação de tela do app (~750 MB, nome a conferir)"],
     tamanho: "~4,3 GB de câmera + ~750 MB de tela", status: "novo, a analisar", destino: "ep.06 (provável)", dono: "equipe",
     proximo: "Baixar, transcrever e mapear até 16/11: quantas degustações há nos 4 arquivos (1 episódio em partes ou mais de um?), vinhos, placar, momentos curiosos para o Instagram e erros do app na tela. Natalie confirma os vinhos do gabarito se a tela do app não mostrar.",
     notas: "4 arquivos de ~1 GB cada podem ser uma degustação dividida ou mais de uma. Se houver 2 ou mais, o ep.07 já está gravado e a fila de dezembro fica garantida."},
    {pasta: "raw/ep05.mov", gravado: "2026-10-27", subiu: "até 28/10", arquivos: ["ep05.mov (bruto 50 min)"],
     status: "em edição", destino: "ep.05", dono: "natalie",
     proximo: "Roteiro v3 por temas (13 blocos, ~8:13) aguardando aprovação dela. Aprovando, o editor renderiza e o diretor confere.",
     notas: "Reels do ep.05 já postado (~28/10). O JSON de tempos do diretor se perdeu; ele regera a partir dos slides ao aprovar (roteiros/ep05_v3/LEIA.md)."},
    {pasta: "raw/ep04.mov", gravado: "2026-10-27", subiu: "até 28/10", arquivos: ["ep04.mov (bruto 35 min)"],
     status: "editado", destino: "ep.04", dono: "natalie",
     proximo: "YouTube v2 (7:12) entregue. Decidir: publicar a v2 como está ou refazer por temas como o ep.05.",
     notas: "Reels, quiz Gamay e corte extra do ep.04 entregues para aprovação."}
  ],

  pecas: [
    // ───────── Já no ar ou a confirmar (antes de 11/11) ─────────
    {id: "ep00-reels", ep: "00", rede: "instagram", formato: "reels", titulo: "Como eu estudo vinho", status: "aprovado", etapa: "confirmar", confirmar: true, dono: "natalie",
     pendente: "Confirmar até 11/11: já foi ao ar? Qual versão (v8, 1min34, ou v9, 32 s)? Se ainda não saiu, vira bônus de domingo em dezembro.",
     img: "img/reels_ep00.jpg", arquivo: "reels_ep0_v8_envio.mp4 (ou v9)", data: "2026-10-29", hora: "19:30",
     legenda: "Esse é o meu jeito de estudar vinho: garrafinha às cegas, ficha completa e quiz no final.\n\nTrês taças por episódio, do visual à revelação. Errar faz parte do método: é assim que a uva fica na memória.\n\nEpisódios completos no YouTube (link na bio).\n\n#vinho #degustacaoascegas #estudodevinho #sommelier #trestacas"},
    {id: "ep00-short", ep: "00", rede: "shorts", formato: "short", titulo: "Como eu estudo vinho (Short)", status: "aprovado", etapa: "confirmar", confirmar: true, dono: "natalie",
     pendente: "Confirmar até 11/11 se já subiu como Short",
     img: "img/reels_ep00.jpg", arquivo: "reels_ep0_v8_envio.mp4 (ou v9)", data: "2026-10-30", hora: "12:00"},
    {id: "ep01-yt", ep: "01", rede: "youtube", formato: "vídeo longo", titulo: "Qual é o intruso? · Três Taças nº 01", status: "aprovado", etapa: "confirmar", confirmar: true, dono: "natalie",
     pendente: "Confirmar até 11/11 se está no canal. Se ainda não está, ele ocupa a quinta 12/11 e o calendário inteiro anda uma semana.",
     img: "img/yt_ep01.jpg", arquivo: "youtube_ep01_leve.mp4", duracao: "11 min", data: "2026-10-31", hora: "10:00",
     notas: "Se já está no ar, trocar o [link do app] da descrição pelo link definitivo com UTM (utm_campaign=ep01) e acrescentar a linha de transparência."},
    {id: "ep01-reels", ep: "01", rede: "instagram", formato: "reels", titulo: "O intruso", status: "aprovado", etapa: "confirmar", confirmar: true, dono: "natalie",
     pendente: "Confirmar até 11/11 se já foi ao ar",
     img: "img/reels_ep01.jpg", arquivo: "reels_ep1_v7_envio.mp4", data: "2026-10-31", hora: "11:00"},
    {id: "ep01-short", ep: "01", rede: "shorts", formato: "short", titulo: "O intruso (Short)", status: "aprovado", etapa: "confirmar", confirmar: true, dono: "natalie",
     pendente: "Confirmar até 11/11 se já subiu como Short",
     img: "img/reels_ep01.jpg", arquivo: "reels_ep1_v7_envio.mp4", data: "2026-11-01", hora: "12:00"},
    {id: "ep05-reels", ep: "05", rede: "instagram", formato: "reels", titulo: "A revanche da Touriga", status: "postado", etapa: "postado", dono: "natalie",
     pendente: "Confirmar a data exata (~28/10). Em 26/11, quando o ep.05 sair no YouTube, repostar este Reels nos Stories com o link do episódio.",
     img: "img/reels_ep05.jpg", arquivo: "reels_ep5_v3.mp4", data: "2026-10-28", hora: "",
     notas: "A legenda manda para o episódio completo no YouTube, que ainda não saiu. Por isso o ep.05 tem prioridade no YouTube logo depois do ep.04."},

    // ───────── Semana 1 (11–15/11) · volta com o ep.02 ─────────
    {id: "ep02-yt", ep: "02", rede: "youtube", formato: "vídeo longo", titulo: "A Touriga Nacional me enganou DE NOVO · Três Taças nº 02", status: "aprovacao", etapa: "aprovar", dono: "natalie",
     pendente: "Até qua 11/11 22:00: aprovar o vídeo e mandar o link definitivo do app. Depois: agendar no YouTube Studio para qui 12/11 18:00.",
     img: "img/yt_ep02.jpg", arquivo: "youtube_ep02.mp4 + capa + SRT", duracao: "15 min", data: "2026-11-12", hora: "18:00",
     notas: "Diretor criativo: conferir a frase sobre a pista da menta (é a pista dela, sem virar regra da uva).",
     legenda: "TÍTULO\nA Touriga Nacional me enganou DE NOVO | 3 vinhos às cegas · Três Taças nº 02\n\nDESCRIÇÃO\nTrês garrafinhas às cegas (#13, #43 e #134), uma degustação completa do visual à revelação e a mesma pegadinha do episódio 1: Primitivo ou Touriga Nacional? Acertei um Barolo em cheio, confundi um Cabernet Franc brasileiro com Dolcetto e anotei a pista que me faltava para a Touriga.\n\nPlacar: 37/100 na degustação e 9/10 no quiz.\n\nEu estudo com o Wine Study Lab, o app que eu uso para registrar as degustações, fazer o quiz e comparar as uvas: [link do app]?utm_source=youtube&utm_medium=descricao&utm_campaign=ep02\n[linha de transparência]\n\n00:00 Três garrafinhas às cegas\n00:11 Garrafa #13\n02:30 Garrafa #43\n04:58 Garrafa #134\n07:24 A revelação\n09:59 Quiz da degustação\n11:29 Comparando as uvas\n\nVinhos do episódio:\n#13 Basco Loco Cabernet Franc 2023 · Vale dos Vinhedos (RS)\n#43 Barolo Morello · Nebbiolo · Piemonte\n#134 Governador 2023 · Touriga Nacional · Douro\n\nNo Instagram tem o Quiz da Taça da Touriga. Quantas você acerta?\n\n#vinho #degustacaoascegas #touriganacional #barolo #cabernetfranc #estudodevinho"},
    {id: "ep02-reels", ep: "02", rede: "instagram", formato: "reels", titulo: "A Touriga de novo", status: "aprovacao", etapa: "aprovar", dono: "natalie",
     pendente: "Até qua 11/11: aprovar. Depois: agendar para qui 12/11 19:30 (1h30 depois do YouTube).",
     img: "img/reels_ep02.jpg", arquivo: "reels_ep2_v2.mp4", data: "2026-11-12", hora: "19:30",
     legenda: "Mesmo vinho, mesma pegadinha: a Touriga Nacional me pegou de novo.\n\nTrês taças às cegas: acertei o Barolo em cheio, confundi um Cabernet Franc brasileiro com Dolcetto e saí com uma pista nova para a Touriga, a menta.\n\nEpisódio completo no YouTube (link na bio).\n\n#vinho #degustacaoascegas #touriganacional #barolo #cabernetfranc #estudodevinho"},
    {id: "ep02-short", ep: "02", rede: "shorts", formato: "short", titulo: "A Touriga de novo (Short)", status: "aprovacao", etapa: "aprovar", dono: "natalie",
     pendente: "Sai com a aprovação do Reels (mesmo arquivo). Agendar no YouTube Studio para sex 13/11 12:00, ligado ao vídeo longo do ep.02.",
     img: "img/reels_ep02.jpg", arquivo: "reels_ep2_v2.mp4", data: "2026-11-13", hora: "12:00",
     legenda: "TÍTULO\nA Touriga Nacional me enganou de novo\n\nDESCRIÇÃO\nMesma pegadinha do ep.01, agora com a pista da menta. Episódio completo no canal: Três Taças nº 02.\n#shorts #vinho #touriganacional"},
    {id: "ep02-quiz", ep: "02", rede: "instagram", formato: "quiz da taça", titulo: "Quiz da Taça · Touriga Nacional", status: "aprovacao", etapa: "aprovar", dono: "natalie",
     pendente: "Até qua 11/11: aprovar a v3 (pergunta da Touriga Franca reescrita, diretor confere antes). Depois: agendar para sáb 14/11 11:00.",
     img: "img/quiz_ep02.jpg", arquivo: "reels_quiz_touriga_v3.mp4", data: "2026-11-14", hora: "11:00",
     legenda: "5 perguntas sobre a Touriga Nacional. Quantas você acerta?\n\nQuiz da Taça: pausa no 3-2-1 e responde antes de ver. É a uva que me enganou duas vezes no YouTube.\n\nComenta o seu placar.\n\n#quizdevinho #touriganacional #vinhoportugues #degustacaoascegas #vinho"},

    // ───────── Semana 2 (16–22/11) · ep.04 ─────────
    {id: "aromas-reels", ep: "extra", rede: "instagram", formato: "reels", titulo: "Teste de aromas às cegas", status: "aprovacao", etapa: "confirmar", confirmar: true, dono: "natalie",
     pendente: "Confirmar até 11/11 se já foi ao ar. Se não: aprovar a v3 até seg 16/11 e agendar para ter 17/11 19:00. Se já saiu, o slot vira Story.",
     img: "img/aromas.jpg", arquivo: "ep03/teste_aromas_v3.mp4", data: "2026-11-17", hora: "19:00",
     notas: "1min46 é longo para Reels. Funciona se o desafio aparecer já no 1º segundo; senão, cartão de abertura do editor.",
     legenda: "Doce de leite ou manteiga? Chocolate ou coco queimado?\n\nTeste de aromas às cegas em casa: cheira e responde na hora. Acertei doce de leite, canela e pêssego; o coco queimado virou chocolate.\n\nQuantos você acertaria? Conta aqui.\n\n#aromasdovinho #degustacaoascegas #estudodevinho #vinho #sommelier"},
    {id: "ep04-yt", ep: "04", rede: "youtube", formato: "vídeo longo", titulo: "A Touriga me enganou AO CONTRÁRIO · Três Taças nº 04", status: "aprovacao", etapa: "aprovar", dono: "natalie",
     pendente: "DECISÃO até seg 16/11: publicar a v2 (7:12) como está em 19/11, ou refazer por temas (aí o ep.04 vai para 03/12 e o ep.05 assume 19/11). Aprovando a v2: mandar link do app e agendar.",
     img: "img/yt_ep04.jpg", arquivo: "youtube_ep04_v2.mp4 (corte fino do diretor) + capa + SRT + descrição", duracao: "7:12", data: "2026-11-19", hora: "18:00",
     notas: "Conferir a descrição contra o corte v2: 'Neste episódio' cita o teste da língua e a ordem das taças; sai o que não estiver no corte. Capítulos vêm do arquivo entregue.",
     legenda: "TÍTULO\nA Touriga me enganou AO CONTRÁRIO | 3 vinhos às cegas · Três Taças nº 04\n\nDESCRIÇÃO\nTrês garrafinhas às cegas (#21, #41 e #107). Depois de dois episódios caindo na Touriga Nacional, agora eu reconheço a uva pela menta… e passo a enxergá-la em todas as taças. Acertei o Barolo pela cor, cheguei a dizer Gamay e mudei de ideia. Tirei zero nessa.\n\nPlacar: 67/100 na degustação e 8/10 no quiz.\n\nEu estudo com o Wine Study Lab, o app que eu uso para registrar as degustações, fazer o quiz e comparar as uvas: [link do app]?utm_source=youtube&utm_medium=descricao&utm_campaign=ep04\n[linha de transparência]\n\n[capítulos: do arquivo v2]\n\nVinhos do episódio:\n#21 Reserva Touriga Nacional 2022 · Bodega Iribarrem · Vale dos Vinhedos, Bento Gonçalves (RS)\n#41 Barolo Morello · Nebbiolo · Piemonte\n#107 Beaujolais · Gamay · França\n\nNo Instagram tem o Quiz da Taça da Gamay. Quantas você acerta?\n\n#vinho #degustacaoascegas #touriganacional #gamay #barolo #estudodevinho"},
    {id: "ep04-reels", ep: "04", rede: "instagram", formato: "reels", titulo: "Tirei zero numa taça", status: "aprovacao", etapa: "aprovar", dono: "natalie",
     pendente: "Aprovar até seg 16/11 e agendar para qui 19/11 19:30. Só sai se o YouTube do ep.04 sair no mesmo dia.",
     img: "img/reels_ep04.jpg", arquivo: "reels_ep4_v2.mp4", data: "2026-11-19", hora: "19:30",
     legenda: "Tirei exatamente zero numa das taças. E a culpa foi da Touriga.\n\nNa #21 senti menta e fui de Touriga Nacional: acertei. Na #41 a cor me levou direto ao Barolo. Na #107 cheguei a pensar em Gamay… e fui de Touriga de novo. Era Gamay, de Beaujolais. Lição do dia: tanino baixo é diferente de tanino zero.\n\nEpisódio completo no YouTube (link na bio).\n\n#vinho #degustacaoascegas #touriganacional #gamay #beaujolais #barolo"},
    {id: "ep04-short", ep: "04", rede: "shorts", formato: "short", titulo: "Tirei zero numa taça (Short)", status: "aprovacao", etapa: "aprovar", dono: "natalie",
     pendente: "Sai com a aprovação do Reels (mesmo arquivo). Sexta 20/11 é feriado (Consciência Negra): mais tempo de tela.",
     img: "img/reels_ep04.jpg", arquivo: "reels_ep4_v2.mp4", data: "2026-11-20", hora: "12:00",
     legenda: "TÍTULO\nTirei ZERO numa taça de vinho às cegas\n\nDESCRIÇÃO\nA Touriga me enganou ao contrário. Episódio completo no canal: Três Taças nº 04.\n#shorts #vinho #degustacaoascegas"},
    {id: "ep04-quiz", ep: "04", rede: "instagram", formato: "quiz da taça", titulo: "Quiz da Taça · Gamay", status: "aprovacao", etapa: "aprovar", dono: "natalie",
     pendente: "Aprovar até seg 16/11 e agendar para sáb 21/11 11:00",
     img: "img/quiz_ep04.jpg", arquivo: "quiz_gamay_v1.mp4", data: "2026-11-21", hora: "11:00",
     notas: "Perguntas checadas na direção (Bowers 1999; Swiss Wine). Distratores sem Canadá e EUA.",
     legenda: "A uva que me deu zero. Você acerta 5 de 5?\n\nQuiz da Taça: Gamay. Pausa no 3-2-1 e responde antes de ver. A degustação inteira está no YouTube (link na bio).\n\nComenta o seu placar.\n\n#quizdevinho #gamay #beaujolais #vinhofrances #degustacaoascegas"},
    {id: "carrossel-governador", ep: "05", rede: "instagram", formato: "carrossel", titulo: "O vinho que me enganou duas vezes (bônus)", status: "ideia", etapa: "fazer", dono: "equipe",
     pendente: "Bônus: só entra se a fila estiver com 2 semanas prontas em 16/11. Equipe monta com quadros do ep.01 (#125) e ep.02 (#134) até 19/11; aprovação até 21/11.",
     img: "", data: "2026-11-22", hora: "19:00",
     notas: "Confirmado nas decupagens: o Governador deu 12 pontos no ep.01 e 12 no ep.02. Último slide sem spoiler: 'quinta ele volta'. Se não couber, vira Story.",
     legenda: "Doze pontos. Duas vezes. Sempre o mesmo vinho.\n\nO Governador, uma Touriga Nacional do Douro, me enganou no ep.01 e no ep.02. Quinta ele volta no YouTube.\n\nAposta aqui: dessa vez eu acerto?\n\n#touriganacional #douro #degustacaoascegas #vinhoportugues #estudodevinho"},

    // ───────── Semana 3 (23–29/11) · ep.05 ─────────
    {id: "ep04-extra", ep: "04", rede: "instagram", formato: "corte extra", titulo: "O teste da língua", status: "aprovacao", etapa: "aprovar", dono: "natalie",
     pendente: "Aprovar até seg 16/11 (junto do pacote ep.04) e agendar para ter 24/11 19:00",
     img: "img/extra_ep04.jpg", arquivo: "reels_ep4_extra_v2.mp4", data: "2026-11-24", hora: "19:00",
     legenda: "Um teste de 5 segundos para sentir o tanino.\n\nDepois do gole, passa a língua no céu da boca: boca seca é tanino. Fiz com a Gamay e com a Touriga, lado a lado, e a diferença aparece na hora.\n\nA degustação completa está no YouTube (link na bio).\n\n#tanino #dicadevinho #gamay #touriganacional #estudodevinho"},
    {id: "ep05-yt", ep: "05", rede: "youtube", formato: "vídeo longo", titulo: "A revanche da Touriga · Três Taças nº 05", status: "edicao", etapa: "editar", dono: "natalie",
     pendente: "Natalie: aprovar o roteiro v3 por temas até sex 13/11 (inclui decidir o palavrão do B03). Depois: editor renderiza até 19/11, diretor confere, Natalie aprova o vídeo até seg 23/11 e agenda.",
     img: "img/yt_ep05.jpg", arquivo: "roteiro v3 (roteiros/ep05_v3) · vídeo a renderizar", duracao: "~8:13", data: "2026-11-26", hora: "18:00",
     notas: "Já existe uma v2 (10:47) do corte fino. O v3 reorganiza por temas. Cortar a pergunta 'Sonora'; número principal: 3 de 3 uvas (o 99 do app está inflado). Diretor confere as faixas de álcool no cartão do WSET.",
     legenda: "TÍTULO\nA revanche da Touriga: 3 de 3 às cegas · Três Taças nº 05\n\nDESCRIÇÃO\nO Governador me enganou nos episódios 1 e 2. Hoje ele voltou, junto com outra Touriga e um italiano que eu provei pela primeira vez.\n\nTrês garrafinhas às cegas (#21, #59 e #124): visual, nariz, boca, a dedução das duas taças de mesma cor e a revelação. Eu conheço a minha adega, e isso entra no raciocínio: faz parte do jogo.\n\nPlacar: 3 de 3 uvas certas e 9/10 no quiz.\n\nEu estudo com o Wine Study Lab, o app que eu uso para registrar as degustações, fazer o quiz e comparar as uvas: [link do app]?utm_source=youtube&utm_medium=descricao&utm_campaign=ep05\n[linha de transparência]\n\n[capítulos: entram com o arquivo final]\n\nVinhos do episódio:\n#21 Reserva Touriga Nacional 2022 · Bodega Iribarrem · Vale dos Vinhedos, Bento Gonçalves (RS) · 13,5%\n#59 Montepulciano d'Abruzzo · Duca di Saragnano · Abruzzo · 13,5%\n#124 Governador 2023 · Touriga Nacional · Douro · 14%\n\nNo Instagram tem o Quiz da Taça da Montepulciano. Quantas você acerta?\n\n#vinho #degustacaoascegas #touriganacional #montepulciano #douro #estudodevinho"},
    {id: "ep05-extra", ep: "05", rede: "instagram", formato: "corte extra", titulo: "A lágrima mentiu", status: "aprovacao", etapa: "aprovar", dono: "natalie",
     pendente: "Aprovar até seg 23/11 e agendar para qui 26/11 19:30. É o gancho do ep.05 no Instagram (o Reels do episódio já saiu em 28/10).",
     img: "img/extra_ep05.jpg", arquivo: "reels_ep5_extra_v2.mp4", data: "2026-11-26", hora: "19:30",
     legenda: "A lágrima me disse 15%. O rótulo disse 13,5%.\n\nLágrima é pista: o álcool divide a cena com o açúcar, a temperatura e até a taça. Na #124 eu cravei, 14%.\n\nA revanche inteira está no YouTube (link na bio).\n\n#lagrimadovinho #teoralcoolico #dicadevinho #degustacaoascegas #estudodevinho"},
    {id: "ep05-short", ep: "05", rede: "shorts", formato: "short", titulo: "A revanche da Touriga (Short)", status: "aprovacao", etapa: "confirmar", confirmar: true, dono: "natalie",
     pendente: "Confirmar até 11/11 se o Reels do ep.05 também subiu como Short. Se não: agendar para sex 27/11 12:00, ligado ao vídeo longo.",
     img: "img/reels_ep05.jpg", arquivo: "reels_ep5_v3.mp4", data: "2026-11-27", hora: "12:00",
     legenda: "TÍTULO\nO vinho que me enganou duas vezes voltou\n\nDESCRIÇÃO\nTerceira chance com o Governador, às cegas. Episódio completo no canal: Três Taças nº 05.\n#shorts #vinho #touriganacional"},
    {id: "ep05-quiz", ep: "05", rede: "instagram", formato: "quiz da taça", titulo: "Quiz da Taça · Montepulciano", status: "aprovacao", etapa: "aprovar", dono: "natalie",
     pendente: "Diretor confere os disciplinari (Vino Nobile, Conero) até 20/11 → Natalie aprova até seg 23/11 → agendar para sáb 28/11 11:00",
     img: "img/quiz_ep05.jpg", arquivo: "quiz_monte_v1.mp4", data: "2026-11-28", hora: "11:00",
     legenda: "Montepulciano é uva ou cidade? As duas.\n\nQuiz da Taça: a uva que eu acertei no chute. 5 perguntas, pausa no 3-2-1 e responde antes de ver.\n\nComenta o seu placar.\n\n#quizdevinho #montepulciano #abruzzo #vinhoitaliano #degustacaoascegas"},

    // ───────── Semana 4 (30/11–06/12) · ep.06 (pasta 9-11) ─────────
    {id: "ep06-teaser", ep: "06", rede: "instagram", formato: "curiosidade", titulo: "Ep.06 · curiosidade 1 (puxa a quinta)", status: "gravado", etapa: "fazer", dono: "equipe",
     pendente: "Sai da análise da pasta 9-11 (até 16/11): escolher o momento mais curioso. Corte até 25/11, aprovação até 30/11.",
     img: "", data: "2026-12-01", hora: "19:00"},
    {id: "ep06-yt", ep: "06", rede: "youtube", formato: "vídeo longo", titulo: "Três Taças nº 06", status: "gravado", etapa: "fazer", dono: "equipe",
     pendente: "Análise até 16/11 → roteiro por temas até 20/11 → Natalie aprova o roteiro até 23/11 → render + diretor até 27/11 → Natalie aprova o vídeo até 30/11.",
     img: "", arquivo: "Drive 9-11: IMG_2392–2395.MOV + tela do app", data: "2026-12-03", hora: "18:00"},
    {id: "ep06-reels", ep: "06", rede: "instagram", formato: "reels", titulo: "Ep.06 · Reels gancho", status: "gravado", etapa: "fazer", dono: "equipe",
     pendente: "Junto do roteiro do ep.06; aprovação até 30/11", img: "", data: "2026-12-03", hora: "19:30"},
    {id: "ep06-short", ep: "06", rede: "shorts", formato: "short", titulo: "Ep.06 · Short", status: "gravado", etapa: "fazer", dono: "equipe",
     pendente: "Mesmo arquivo do Reels", img: "", data: "2026-12-04", hora: "12:00"},
    {id: "ep06-quiz", ep: "06", rede: "instagram", formato: "quiz da taça", titulo: "Ep.06 · Quiz da Taça", status: "gravado", etapa: "fazer", dono: "equipe",
     pendente: "Diretor checa as perguntas; aprovação até 30/11", img: "", data: "2026-12-05", hora: "11:00"},

    // ───────── Semana 5 (07–13/12) · ep.07 ─────────
    {id: "ep06-extra", ep: "06", rede: "instagram", formato: "curiosidade", titulo: "Ep.06 · curiosidade 2", status: "gravado", etapa: "fazer", dono: "equipe",
     pendente: "Corte junto do pacote ep.06; aprovação até 07/12", img: "", data: "2026-12-08", hora: "19:00"},
    {id: "ep07-yt", ep: "07", rede: "youtube", formato: "vídeo longo", titulo: "Três Taças nº 07", status: "ideia", etapa: "fazer", dono: "natalie",
     pendente: "Gravar até sex 27/11 (ou já está na pasta 9-11, se ela tiver mais de uma degustação). Roteiro até 01/12, aprovação do vídeo até 07/12.",
     img: "", data: "2026-12-10", hora: "18:00"},
    {id: "ep07-reels", ep: "07", rede: "instagram", formato: "reels", titulo: "Ep.07 · Reels gancho", status: "ideia", etapa: "fazer", dono: "equipe",
     pendente: "Depende da gravação do ep.07", img: "", data: "2026-12-10", hora: "19:30"},
    {id: "ep07-short", ep: "07", rede: "shorts", formato: "short", titulo: "Ep.07 · Short", status: "ideia", etapa: "fazer", dono: "equipe",
     pendente: "Depende da gravação do ep.07", img: "", data: "2026-12-11", hora: "12:00"},
    {id: "ep07-quiz", ep: "07", rede: "instagram", formato: "quiz da taça", titulo: "Ep.07 · Quiz da Taça", status: "ideia", etapa: "fazer", dono: "equipe",
     pendente: "Depende da gravação do ep.07", img: "", data: "2026-12-12", hora: "11:00"},

    // ───────── Semana 6 (14–20/12) · ep.08 ─────────
    {id: "ep07-extra", ep: "07", rede: "instagram", formato: "curiosidade", titulo: "Ep.07 · curiosidade", status: "ideia", etapa: "fazer", dono: "equipe",
     pendente: "Depende da gravação do ep.07", img: "", data: "2026-12-15", hora: "19:00"},
    {id: "ep08-yt", ep: "08", rede: "youtube", formato: "vídeo longo", titulo: "Três Taças nº 08", status: "ideia", etapa: "fazer", dono: "natalie",
     pendente: "Gravar até sex 27/11, na mesma sessão do ep.07. Roteiro até 08/12, aprovação do vídeo até 14/12.",
     img: "", data: "2026-12-17", hora: "18:00"},
    {id: "ep08-reels", ep: "08", rede: "instagram", formato: "reels", titulo: "Ep.08 · Reels gancho", status: "ideia", etapa: "fazer", dono: "equipe",
     pendente: "Depende da gravação do ep.08", img: "", data: "2026-12-17", hora: "19:30"},
    {id: "ep08-short", ep: "08", rede: "shorts", formato: "short", titulo: "Ep.08 · Short", status: "ideia", etapa: "fazer", dono: "equipe",
     pendente: "Depende da gravação do ep.08", img: "", data: "2026-12-18", hora: "12:00"},
    {id: "ep08-quiz", ep: "08", rede: "instagram", formato: "quiz da taça", titulo: "Ep.08 · Quiz da Taça", status: "ideia", etapa: "fazer", dono: "equipe",
     pendente: "Depende da gravação do ep.08", img: "", data: "2026-12-19", hora: "11:00"}
  ]
};
