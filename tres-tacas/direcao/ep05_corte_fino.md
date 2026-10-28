# Ep.05 "A revanche da Touriga": corte fino do YouTube

O corte atual (yt5) tem 14:55. Este corte fino fica em cerca de **10:05**, ou uns 10:12 se a reação do quiz voltar (ver Quiz).
Saem **166 de 382 frases** e **26 são aparadas**. Entram **22 notas de tela**. As 10 notas atuais que estavam mal ancoradas saem e voltam ancoradas por frase (2 com texto reescrito: "unha" e "menta").
Os índices de "aparar" são de palavras, contados a partir de 0 dentro do span de cada frase em `ep05_corte_atual.json`.

## Antes de tudo: 3 problemas que não dependem de cortar frase

1. **Notas caindo no teaser.** No `yt_ep.py`, quando o tempo-âncora de uma nota cai num buraco do corte, o código pega o primeiro trecho que começa depois dele na timeline. Esse trecho é o do **teaser** (1431 / 2452). Com isso, "Cor profunda descarta…", "Garrafa #21: muito carvalho", "menta = Touriga" e "No app, a #21 só contou a uva" aparecem todas entre 00:04 e 00:06, por cima da abertura. Por isso as notas agora são ancoradas por frase (`apos`), e não mais por tempo. Correção no render: na busca de fallback, ignorar os trechos do teaser (capítulo 0).
2. **Bordas que comem números** (são ajustes de trecho, não de frase):
   - **S007**: o trecho 271.0–274.3 corta o "nove" de 59, e ela fica dizendo "garrafinhas **cinquenta e**, vinte e um…". Estender o fim do trecho para **275.1** (pela energia do áudio, a voz vai até 275.0).
   - **S046**: o trecho 817.3–820.1 corta o "quatro" de 2024, e ela fica dizendo "**dois mil e vinte**". Estender para **820.8**.
   - Cortes que comem só o começo de uma palavra (pequenos, mas se ouvem): S036 começa em 645.6, S090 em 1229.7, S108 em 1346.3, S130 em 1698.2, S230 em 2324.6, S286 em 2561.4 e S309 em 2608.1.
3. **Quiz cortado em modo "energy".** Ele picou palavras no meio, e o que se ouve é "garrafinha V1", "39", "qual o corpo típico de um profissional?". Recortar em modo fala, com spans limpos (ver Quiz).

## Capítulos (tempos estimados no vídeo novo)

| Início | Frase | Título · sub |
|---|---|---|
| 0:04 | S001 | Abertura · a revanche da Touriga (sem cartão: é o teaser) |
| 0:16 | S006 | Três garrafinhas · #21 · #59 · #124 |
| 1:20 | S025 | Garrafa #21 · cor profunda, lágrima alta |
| 2:22 | S045 | Garrafa #59 · lágrima lenta, fruta negra |
| 3:39 | S078 | Garrafa #124 · a mais transparente |
| 4:14 | S090 | O nariz das três · todas se parecem |
| 4:47 | S110 | Garrafa #124 na boca · eu não posso errar |
| 5:49 | S142 | Garrafa #59 na boca · parece italiano |
| 6:37 | S173 | A dedução · mesma cor, outra madeira |
| 7:17 | S201 | Os chutes · começando pela #21 |
| 7:52 | S238 | A revelação · 3 de 3 uvas |
| 9:11 | S339 | Quiz · 9 de 10 |
| 9:27 | S358 | O que eu aprendi · Montepulciano × Sangiovese |

Os tempos são estimativa (±10 s). Depois do render, gere de novo o `youtube_ep05_capitulos.txt` a partir do plano.

---

## Abertura (teaser) · 12 s → 12 s
Mantido: S001–S005. A repetição dessas falas mais adiante é intencional, porque é teaser. Só precisa sair dali o empilhamento de notas (problema 1).

## Três garrafinhas · 1:31 → ~1:05
- **Cortadas:** S010 ("para não estar sempre provando vinho": a S011 diz o mesmo melhor); S012 ("Bom, vamos lá"); S013–S014 ("A garrafinha 21, vamos começar com ela": repete a S025, que já abre o capítulo da #21); S018–S020 (exceção "quando quero estudar mais…" e o fragmento "outras."); S023 ("o mais rápido que puder é o melhor": repete a S021).
- **Aparadas:** S006 sai o "Bom,"; S015 sai o "Mas" (a frase anterior foi cortada); S016 sai o "Sempre assim ó,".
- Fica a história completa: taça ISO, água e cuspideira, garrafinha de 30 ml / 15 ml por prova, metade aberta oxida, papel branco embaixo.
- A nota "Taça ISO" continua como está.

## Garrafa #21 · 1:37 → ~1:02
- **Cortadas:** S027 ("Já dá para sentir bastante coisa": é o resto da frase confusa dos "ésteres"); S029 (repete o teor da S030); S034 ("A gente deixa num aberto…": sem a frase anterior, não faz sentido); S041 ("rubi um pouco mais, digamos assim": incompleta, autocorreção).
- **Aparadas:** S025 sai o "Então,"; S032 sai o "muito," ("Não me parece com muita idade"); S033 sai o "Bom,"; S035 sai o "em específico,".
- **Notas:** "'Unha' é a borda…" depois da S030, chegando junto da fala dela. Dolcetto (ep.01 acertou, ep.02 era Cab Franc: confirmado nas decupagens) depois da S035, para a piada fazer sentido para quem chega agora. "Cor profunda descarta…" depois da S039. **"Dica: tire da geladeira…"** depois da S042, junto do "tô achando bem gelado". Hoje ela aparece na #59 sem motivo nenhum.

## Garrafa #59 · ~2:00 → ~1:17
- **Cortadas:** S044 (a S045 repete a cor; fica a S045, que é mais completa); S049–S050 e S052 (três voltas do "ainda está escorrendo"; fica a S051, a melhor); S055–S056 ("Entre 14 e 15", "E comparando as duas, eu diria…": hesitação); S058 (repete a S057); S060–S062 ("fruta vermelha… é uma fruta negra, quer dizer": autocorreção); S064 (repete a S073); S066 ("elas têm cores": incompleta); S068–S069 ("Ambas são rubi" aparece duas vezes; fica a S070).
- **Aparadas:** S045 sai "Bom, mas"; S071 sai "umas…" (emenda direto em "essas frutas"); S072 sai "nesse sentido"; S074 sai o "é…" final (emenda em "cassis").
- **S053 fica**: "Ela é uma lágrima lenta" justifica o 15%. Na S054 não se mexe: a palavra 0 tem o fim de "lenta" e o "Eu" juntos.
- **Notas:** "Lágrima é pista, não régua" depois da S059. Prepara o 13,5% da revelação sem entregar o resultado. "#21 rubi mais aberto / #59 mais escuro" depois da S075: hoje quem assiste não sabe qual taça é "essa daqui".

## Garrafa #124 · ~59 s → ~35 s
- **Cortadas:** S076–S077 (pensamento em voz alta, sem conclusão); S079 ("Ele não tá totalmente…"); S083–S087 (vai e volta 14 / 14,5 / 15 / "se essas duas forem 15…").
- **Aparadas:** S078 sai o "Bom,"; S080 sai "É, ele tem essa coisa,"; S082 sai "uma lágrima mais lenta" (contradiz o "mais rápida" logo antes); S088 fica só "eu vou colocar 14,5 nessas e 14 nessa". Esse é o teor que ela crava na revelação.
- **A S081 fica de propósito**: "me lembra muito o primeiro rubi" é a semente da dedução do capítulo 8.

## O nariz das três · ~59 s → ~33 s
- **Cortadas:** S089 ("Mesma coisa, frutas vermelhas": mesma coisa que quê?); **S093–S095 ("igual a de ontem… é um Barolo… esse é mais complexo")**: rodei o trecho de novo, sem prompt, no Whisper turbo e no small, com beam 1 e 5, e todos ouvem "**barulho**". A legenda põe "Barolo" na boca dela por causa de um FIX. Faz sentido com o ep.04 (Barolo acertado pela cor), mas na dúvida corta. **Se a Natalie confirmar que disse Barolo, volta, com a nota "Ep.04: acertei o Barolo só pela cor"**. S098–S099 ("Montepulciano é uma boa… uma boa ideia": repete a S097); S100–S102 (terceira vez do "todas se parecem"); S105 (repete o carvalho da S104).
- **Aparada:** S091 sai a parte confusa "tenho uma quantidade muito grande de garrafinhas de um mesmo sabor, então eu tento ir nessas, mas" e fica "tá confuso porque todas se parecem muito, todas as três".
- **Notas:** "Garrafa #21: muito carvalho" depois da S097. "#124, a terceira taça: notas de estábulo" depois da S107. Sem essa nota, "essa última" não diz qual garrafa é.

## Garrafa #124 na boca · ~1:16 → ~1:02
- **Cortadas:** S113 ("Então eu vou tentar nela": redundante); S116 ("Copinha"); S122 ("Ela tem uma menta": repete o "mentolado" da S118); S123–S124 ("Tiro da área de frutas as mais vermelhas. Opa!": incompreensível sem a tela); S134 ("Pra alto": fica a decisão "Vou colocar alto"); S136 e S138 ("E um corpo…", "Tem um bom corpo": embola com o "corpo médio", que é o que importa, porque é o erro do quiz); S139 ("Próximo").
- **Notas:** "Ordem de prova" passa para depois da S111, enquanto ela explica (hoje aparece 1 min depois). "Minha pista desde o ep.02: menta me lembra Touriga" depois da S117: a palavra é "pista", sem "=", porque a menta não é marcador clássico da Touriga (checagem do ep.04). **"Ep.01: o Governador me enganou / Ep.04: chutei Touriga num Gamay"** depois da S127: é isso que dá peso ao "não quero errar mais uma vez", e as duas coisas estão confirmadas nas decupagens.

## Garrafa #59 na boca · ~1:01 → ~48 s
- **Cortadas:** S141 ("Arterio", lixo de transcrição); S150 (a acidez repetida; fica a S149, que puxa o "Mas os taninos"); S154–S156 ("Com média… médio pra mais… um tanino": repete o tanino); S159–S160 ("Acidez de sabor. Médio": o certo era "intensidade de sabor", e a legenda ensina errado); S162–S163 ("Macio. Adstringente.": contraditório fora da ficha); **S170 ("Eu tenho já 19 garrafas cadastradas": o app mostra 22 vinhos ⚠️)**.
- **Aparadas:** S146 sai o "Bom,"; S151 sai "elas são bem…" ("Mas os taninos, são bem potentes"); S169 sai o "Assim,".
- **Nota:** "Transparência: eu conheço a minha adega" depois da S169.

## A dedução · ~54 s → ~40 s
- **Cortadas:** S174 (o segundo "Muita madeira"); S179 ("Não tô sentindo nada no aroma": parece que ela não sente cheiro nenhum); S182–S184, S187–S188 (falsos começos, "É…", "Com certeza não, né?"); S192 ("Não tem sido solto": incompreensível); S198–S199 ("Mas é isso. Vamos lá, bem.").
- **Aparadas:** S185 sai o "num…" (emenda em "Num Dolcetto nela"); S189 sai o "né?".
- **Notas:** o gráfico "#21 e #124: a mesma cor rubi. Só a #21 tem carvalho. Mesma uva?" depois da S180. "Agora, a #59 (a do meio): o que ela não é" depois da S181. Sem essa nota, o "nela" da S186 não tem dono.

## Os chutes · ~58 s → ~35 s
- **Cortadas:** S200 ("Então, primeiro"); S203 ("Uma menta": fica hortelã e eucalipto); S206 (repete o carvalho); S209–S212 ("que tá seco… típico da evolução… É seco": repete a S207 e confunde seco de tabaco com seco de açúcar); S213 ("Tensidade média": ninguém entende); S216, S218, S220, S221; **S224–S225 ("O país. Eu vou colocar…")**: o corte comeu o "Brasil" e ela parecia dizer que o país era "Rio Grande do Sul"; S227 ("Sub-região").
- **Notas:** "Tabaco: evolução ou barrica" depois da S207 (hoje cai numa frase cortada). **Cartão-resumo dos chutes** depois da S235. Ele substitui toda a digitação e devolve o "Brasil" e o "Touriga" da #124, que se perderam no corte.

## A revelação · ~2:10 → ~1:19
- **Cortadas:** S236–S237 ("Próxima. Concluir."); falsos começos S245–S246, S248, S250–S251, S254, S258–S268, S274, S276–S278, S283, S288, S294–S295; **S252 ("Eles usam muito a barrica"**: não confirmado para esta Touriga, ⚠️ na checagem); S292–S293 ("Não sei dizer. Vou pesquisar agora": a S285 já diz isso); S306–S308 ("fiquei sem na memória": não se entende); S311–S315 ("Como eu falei assim… ah… eu falei assim… tá…"); S323–S325 ("Pra não confundir Touriga Nacional com Touriga Franca…": solta, sem começo nem fim); S325 "Top" (fica o "Arrasamos").
- **Aparadas:** S253 sai o "Mas"; S255 sai o "da…" (emenda em "Da Touriga"); S280 sai o "os…" (emenda em "Os italianos"); S302 sai o "assim…" ("Não tinha como passar vergonha").
- Fica: tambores, a reação, "a gente bebeu na escola", "mentolado da Touriga / poderia ter confundido com Cabernet Franc", "13,5, caramba, eu coloquei 14,5", Montepulciano "foi um chute", "coisa molhada, funguinho" (prepara o fim), "sou ótima com teor alcoólico" (ironia), o Governador, "acabei a garrafinha pra testar" (fecha o S128), 14% e safra 2023 "eu sei" (transparência dita por ela mesma).
- **Notas:** "No app, a #21 só contou a uva" depois da S243. Gabarito da #21 depois da S249 (**"a mesma do ep.04"**, confirmado: era a #21 no ep.04). Gabarito da #59 depois da S275. **"#124: Governador 2023 · o mesmo que me enganou no ep.01"** depois da S301: é a explicação do "maldito".

## Quiz · ~34 s → ~11 s de fala (+ 5 s da tela 9/10)
- **Cortadas:** S329–S338 (perguntas picadas: "uma garrafa? 59. Hum… Era da… Qual era a uva? 39."); S341, S343–S344 ("Ela poderia ter sido uma Sangiovese mesmo" repete a S342); S348–S349 ("vermelho estomago/tomate": tomate é descritor de aroma, ⚠️); S350–S355 (ininteligível: "garrafinha V1", "Briga Nacional", "corpo típico de um profissional?", "O corpo não mais"). A pergunta da Sonora já tinha saído e continua fora.
- **Recorte limpo recomendado** (modo fala, sem "energy"): 2664.4–2670.0 · 2671.5–2673.5 · 2677.9–2684.6. A S346 hoje perde o "Ela".
- **Reinserção recomendada (fora dos ids):** **2738.9–2743.7 + 2744.7–2749.8**, "O corpo era um corpo médio, mas… que eu errei isso da outra vez. Ah! Oh, não! Encorpado?". É o melhor momento de humor do quiz e hoje não entra no corte. Se entrar, a nota da S347 vira só "Quiz: 9 de 10". Se não entrar, a nota fica como está.
- **Notas:** Sangiovese mais clara depois da S346. "9 de 10, só errei o corpo da Touriga: marquei médio+, ela é encorpada" depois da S347 (✅ Wine Folly: Touriga full body).

## O que eu aprendi · ~52 s → ~35 s
- **Cortadas:** S356–S357 ("Ver a ficha das uvas. Já o sistema te manda": leitura do app); S359 (repete a S358); S361–S364 ("Isso dela melhora. Ó… Importante. A Sangio…"); S368, S370, S372, S374–S375 (muletas); **S378–S379** (o corte comeu "pode ser até", e ficou "É que a Montepulciano tenha mais aromas…"; além disso, sugere que a ficha do app está incompleta sem mostrar isso); S381–S382.
- **Aparada:** S360 sai "os cheiros," ("Pra ver realmente os aromas que ela tem").
- Fecha com: comparação Montepulciano × Sangiovese → tomilho → "posso estar confundindo esse tempero com algo mais mineral" → "engraçado que terra molhada teve na Sangiovese" → "vou fazer uma pesquisa melhor". A pergunta fica em aberto e puxa o próximo episódio.

---

## O que ainda não funciona (e não se resolve só cortando frase)
- **Ritmo do meio:** os capítulos de boca (#124 e #59) continuam em formato de lista da ficha ("acidez média, tanino…"). Para ficarem vivos, mostrar a ficha do app recortada ao lado, preenchendo, com a fala por cima. Assim a lista vira imagem e a cabeça de quem assiste descansa.
- **Rosto pequeno da revelação em diante:** vale o layout da direção (card do app no meio, rosto em cartão com borda creme). A reação "Preciso beber um vinho agora" merece um zoom de no máximo 2×.
- **Excesso de notas:** são 22 em ~10 min. Se alguma tiver de sair, que seja "#124, a terceira taça" ou "Lágrima é pista". As de garrafa e de continuidade ficam.
