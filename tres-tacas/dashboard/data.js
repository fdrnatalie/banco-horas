// Três Taças — base do painel. Mantido pelo estrategista. status: ideia | gravado | edicao | aprovacao | aprovado | programado | postado
// dono: quem precisa agir agora ("natalie" ou "equipe").
window.TT_DATA = {
  atualizado: "28/10/2026",
  pecas: [
    {id: "ep00-reels", ep: "00", rede: "instagram", formato: "reels", titulo: "Como eu estudo vinho", status: "aprovado", dono: "natalie",
     pendente: "Confirmar se já foi postado", img: "img/reels_ep00.jpg", arquivo: "reels_ep0_v8_envio.mp4", data: "", hora: "",
     notas: "Você ia cortar os 'eeee' por conta própria antes de postar."},
    {id: "ep01-reels", ep: "01", rede: "instagram", formato: "reels", titulo: "O intruso", status: "aprovado", dono: "natalie",
     pendente: "Confirmar se já foi postado", img: "img/reels_ep01.jpg", arquivo: "reels_ep1_v7_envio.mp4", data: "", hora: ""},
    {id: "ep01-yt", ep: "01", rede: "youtube", formato: "vídeo longo", titulo: "Qual é o intruso? · Três Taças nº 01", status: "aprovado", dono: "natalie",
     pendente: "Confirmar se já foi postado", img: "img/yt_ep01.jpg", arquivo: "youtube_ep01_leve.mp4", duracao: "~20 min", data: "", hora: ""},
    {id: "ep02-reels", ep: "02", rede: "instagram", formato: "reels", titulo: "A Touriga de novo (painéis)", status: "aprovacao", dono: "natalie",
     pendente: "Aprovar o Reels com os painéis de contexto", img: "img/reels_ep02.jpg", arquivo: "reels_ep2_v2.mp4", data: "", hora: "",
     legenda: "A Touriga Nacional me enganou de novo 🍷 Três taças às cegas: acertei o Barolo em cheio, confundi um Cabernet Franc brasileiro com Dolcetto e caí na mesma pegadinha do episódio 1. O aprendizado: quando vem menta, é Touriga. O episódio completo tá no YouTube (link na bio).\n\n#vinho #degustacaoascegas #touriganacional #barolo #estudodevinho"},
    {id: "ep02-quiz", ep: "02", rede: "instagram", formato: "quiz da taça", titulo: "Quiz da Taça · Touriga Nacional", status: "aprovado", dono: "equipe",
     img: "img/quiz_ep02.jpg", arquivo: "reels_quiz_touriga_v2.mp4", data: "", hora: "",
     legenda: "Quiz da Taça: 5 perguntas sobre a Touriga Nacional 🍷 Pausa no 3-2-1 e responde antes de ver. Comenta quantas você acertou! O app que eu uso tá no link da bio.\n\n#quizdevinho #touriganacional #vinhoportugues #vinho #degustacaoascegas"},
    {id: "ep02-yt", ep: "02", rede: "youtube", formato: "vídeo longo", titulo: "A Touriga Nacional me enganou DE NOVO · Três Taças nº 02", status: "aprovacao", dono: "natalie",
     pendente: "Aprovar e trocar [link do app] na descrição", img: "img/yt_ep02.jpg", arquivo: "youtube_ep02.mp4 + capa + SRT", duracao: "15 min", data: "", hora: "",
     legenda: "Três garrafinhas às cegas (#13, #43 e #134), uma degustação completa do visual à revelação e a mesma pegadinha do episódio 1: Primitivo ou Touriga Nacional?\n\nPlacar: 37/100 na degustação e 9/10 no quiz.\n\n00:00 Três garrafinhas às cegas\n00:11 Garrafa #13\n02:30 Garrafa #43\n04:58 Garrafa #134\n07:24 A revelação\n09:59 Quiz da degustação\n11:29 Comparando as uvas"},
    {id: "ep02-short", ep: "02", rede: "shorts", formato: "short", titulo: "A Touriga de novo (Short)", status: "aprovacao", dono: "natalie",
     pendente: "Mesmo arquivo do Reels: sai junto depois de aprovado", img: "img/reels_ep02.jpg", arquivo: "reels_ep2_v2.mp4", data: "", hora: ""},
    {id: "aromas-reels", ep: "extra", rede: "instagram", formato: "reels", titulo: "Teste de aromas às cegas", status: "aprovacao", dono: "natalie",
     pendente: "Aprovar a versão sem a cantoria (v3)", img: "img/aromas.jpg", arquivo: "ep03/teste_aromas_v3.mp4", data: "", hora: ""},
    {id: "aromas-short", ep: "extra", rede: "shorts", formato: "short", titulo: "Teste de aromas às cegas (Short)", status: "aprovacao", dono: "natalie",
     pendente: "Mesmo arquivo do Reels (1min46s, vertical): entra como Short", img: "img/aromas.jpg", arquivo: "ep03/teste_aromas_v3.mp4", data: "", hora: ""},
    {id: "ep04-raw", ep: "04", rede: "youtube", formato: "vídeo longo", titulo: "Ep. 04 · garrafinhas #21 e #41", status: "gravado", dono: "equipe",
     pendente: "Diretor criativo analisando; depois decupagem para aprovação", img: "img/raw_ep04.jpg", duracao: "bruto 35 min", data: "", hora: ""},
    {id: "ep05-raw", ep: "05", rede: "youtube", formato: "vídeo longo", titulo: "Ep. 05 · garrafinhas #21, #124 e #59", status: "gravado", dono: "equipe",
     pendente: "Diretor criativo analisando; depois decupagem para aprovação", img: "img/raw_ep05.jpg", duracao: "bruto 50 min", data: "", hora: ""}
  ]
};
