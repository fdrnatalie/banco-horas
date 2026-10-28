# Ep. 04 · YouTube · corte fino ("Tirei zero: a Touriga ao contrário")

Arquivo de decisões: `ep04_corte_fino.json`. Os ids vêm de `ep04_corte_atual.md`. Os índices de palavra são 0-based, dentro do span de cada frase.
Para conferir, retranscrevi o corte atual inteiro e 30 trechos do bruto com o Whisper large-v3-turbo e o espectro de energia (os arquivos estão em `scratchpad/ep04/fino/`).

**Resultado:** saem 109 de 265 frases e 19 são aparadas. A duração estimada fica em **≈ 7:25–7:30** (431 s de fala a 1.1x, mais cerca de 6 s das bordas corrigidas e 10 s de cartelas). O corte atual tem 10:02.

---

## 0. Antes de tudo: o problema que gera a maior parte das "frases sem sentido"

A Natalie tem razão, mas o maior culpado não é a fala dela. **O fim de vários trechos corta a última palavra.** As bordas do `cuts_ep04.py` saíram da minha decupagem anterior, que usou tempos de palavra do Whisper adiantados 0,2–0,6 s. Por isso:
- "Touriga Nacional" vira "Por quê?" / "Tô ligando" (S046)
- "Talvez estejamos falando da mesma uva" vira "…do mesmo" (S132)
- "Mas ele tem bons taninos" vira "Ele tem um bom…" (S138, e também no teaser S003)
- "Eu vou no Touriga também" vira "Eu vou no Tori" (S148)
- "Essa aqui que é a pegadinha" vira "É essa aqui que abriu" (S146)

**A virada inteira da #107 está inaudível no corte atual.**

O corte fino conta com estas correções de borda. Os tempos são do bruto e foram conferidos palavra por palavra com o turbo:

| # | Trecho atual (fim) | Novo | O que volta | Frase | Obrigatória? |
|---|---|---|---|---|---|
| 1 | início 34.3 | **35.75** | tira o resto de "…escolher, é o" antes de "eu dou preferência" | S004 | sim |
| 2 | 596.2 | **596.45** | "Touriga **Nacional**" | S046 | **sim** |
| 3 | 713.9 | **715.45** | "um pouco mais **adocicado**" | S057 | sim |
| 4 | 726.4 | **726.9** | "um Touriga aqui **do Brasil**" | S060 | sim |
| 5 | 1297.21 (cuts: 1297.5) | **1298.15** | "da **mesma uva**" | S133 (palavra 0 = "da mesma") | **sim** |
| 6 | 1365.4 | **1366.0** | "bons **taninos**" | S138 | **sim** |
| 7 | 1437.98–1438.7 | **1437.85–1439.3** | "**Essa** aqui que é a **pegadinha**" | S146 | **sim** |
| 8 | 1459.6 | **1460.0** | "Touriga **também**" | S148 | **sim** |
| 9 | 1569.0 | **1569.45** | "acertei duas **uvas**" | S157 | sim |
| 10 | 1615.2 | **1616.1** | "dúvida sobre o **Gamay**" | S165 | sim |
| 11 | 1712.4 | **1712.8** | "com o primeiro, **que é um Touriga**" | S187 | sim |
| 12 | 1723.6 | **1723.9** | "bem **mais**" | S188 | sim |
| 13 | 1793.9 | **1794.2** | "e o que eu **errei**" | S203 | sim |
| 14 | 1918.4 | **1919.05** | "na parte sul da **Borgonha**" (hoje soa "da França") | S247 | sim |
| 15 | 2052.1 | **2052.85** | "ela é muito **complexa**" | S257 | sim |
| 16 | 2059.5 | **2060.05** | "um dos principais **da Itália**" | S258 | sim |
| 17 | 2093.8 | **2094.85** | "me pareceu taninoso, **mas não era realmente**" | S265 | recomendada |

Regra para o pipeline daqui em diante: a borda final é o fim da última palavra **pelo turbo + 0,15 s**, conferida pela energia. Não usar o tempo do transcript antigo.

**Se as bordas 2, 5, 6, 7 e 8 não puderem ser corrigidas, corte S046, S133, S137–S138, S146 e S148.** Mas aí o capítulo da #107 perde a virada. Prefiro corrigir.

Outros dois pontos de pipeline (fora do JSON):
- **Gancho.** Hoje o vídeo abre com 4 s de cartela de capítulos, antes de qualquer fala. Isso quebra a regra do gancho em 2 s. Coloque o teaser ("O último eu errei tudo. Tirei exatamente zero.") **antes** da cartela.
- **Legenda.** S133 tem o texto "Ele" no JSON, mas o áudio é "da mesma". A legenda tem que sair da retranscrição do corte novo, nunca do texto destas frases. Corrigir também "barriga" → **barrica** e "Gouge Blanca" → **Gouais Blanc**.

---

## 1. Três garrafinhas às cegas (teaser + preparo) · antes 1:10 · agora ≈ 1:01 (57 s de fala + 4 s de cartela)

**Saem:**
- **S003** (teaser do Gamay). É a mesma fala de 5:51 (S135–S138). Sem contexto ela não se entende ("morango… valoração… Gamay") e, com o fim cortado, ainda termina em "bom escolher". O teaser fica só com o zero, que se entende sozinho.
- **S007** "Começar com as…": frase cortada no meio.
- **S010–S011**: a lavagem das garrafinhas. É uma tangente que segura a entrada no vinho, e S011 tem autocorreção ("coloco na água fervendo, coloco a água fervendo nele"). Rende um story à parte.
- **S015** "Poder enxergar": é a emenda de "coloração" cortada com o "enxergar" de outro momento. Não existe como frase.

**Aparadas:**
- S001 [0] ("Porque": o gancho começa limpo em "O último eu errei tudo").
- S004 [0–1] ("é o…").
- S006 [12–13] (o "a 21" repetido).
- S013 [3–5] ("tá, tipo assim"), [15–19] ("então acaba não sendo tão", que termina truncado).
- S014 [1–2], [11–21]: fica "Mas é incrível como você consegue diferenciar algumas castas". O resto termina em "só por causa da…", com a palavra cortada.

**Nota nova** (depois de S005): *"Sorteio do dia: #21, #41 e #107. / Provadas na ordem dos números."* Ela dá o contexto que faltava e prepara a lição da ordem das taças no fim.

## 2. Garrafa #21 · antes 2:27 · agora ≈ 2:06

**Saem:**
- **S018** "Pra não…": o "influenciar" foi cortado.
- **S028**: "quer dizer que você não sentiu esse…". O "ésteres" foi cortado, então a nota sobre ésteres aparecia sem que ninguém tivesse dito a palavra. **A nota também sai.**
- **S032** "um morango mais…": truncada.
- **S033** "Vou colocar um fio": leitura do app, truncada.
- **S043** "Por exemplo, o eucalipto". Repete a ideia: a frase seguinte, "menta, de eucalipto", é a percepção real e fica.
- **S050–S052** "um bom… / às vezes colocar média pra mais / ou álcool": a ladainha de médio/médio+ com as palavras cortadas.
- **S053** "Vou inicialmente colocar um…": repete a hipótese Touriga, já dita em S046.
- **S055** "Eu vou…": falso começo.
- **S061** "Teor alcoólico, eu vou colocar o próximo": é a emenda de "14 %" com "o próximo" e não faz sentido.

**Aparadas:**
- S016 [9–11]: o "preferencialmente branca" repetia a frase seguinte. Fica "tem que ter uma luz. Eu odeio luz branca, mas…precisa ser branca", que é humor com ensinamento.
- S019 [4] ("é").
- S020 [10] (o "muito" duplicado), [14–15] ("um pouco", autocorreção). Fica "tá muito jovem".
- S022 [0], [7–11]: "mais profundo, rubi no nariz" é ela lendo campos da ficha.
- S029 [0–1] ("É isso,").
- S031 [8–12]: "porque ele não tem essa…" terminava truncada. Fica "Não iria numa fruta muito fresca, tipo morango". Isso funciona como ironia, já que o morango volta na #107.

**Ficam** porque ensinam:
- a luz branca;
- a borda e a idade;
- a dica da cereja ("se não tá vindo, não tem problema");
- "frutas voltadas na coloração";
- o "álcool que não é álcool, é algo fresco";
- a menta e a Touriga (a continuidade da série);
- o raciocínio "Douro não, mais adocicado, Novo Mundo, Brasil".

Com as bordas 2, 3 e 4 corrigidas, a hipótese fica completa e honesta: "como eu sei que eu tenho um Touriga aqui do Brasil".

**Notas:**
- A nota "A borda da cor…" sai do início do capítulo, onde caía sobre a luz branca. Ela volta depois de S019, quando ela fala da "unha".
- Nova, depois de S060: *"Hipótese da #21: Touriga Nacional / do Brasil (Bento Gonçalves, RS)"*. Confere com a tela f_760.
- A nota "A pista dela: menta = Touriga…" fica.

## 3. Garrafa #41 · antes 1:18 · agora ≈ 0:47

Era o capítulo com mais repetição: 27 de 47 frases saem.

**Saem:**
- **S063–S064** "esse daqui é o mais rápido possível": repete o "muito fácil".
- **S065**: o primeiro "Por que um Barolo?". Ela pergunta duas vezes e fica a segunda, que vem depois de "poderia ser Pinot Noir, Gamay" e tem mais força.
- **S067** "Média": órfã, porque o "transparência" estava cortado.
- **S069, S070, S073**: "É… / Mas assim…".
- **S078** "que não é o laranjada granada": confusa.
- **S080** "É um vermelho-laranja": repete o "laranja tomate", que é a frase de efeito.
- **S081–S083**: "Essa… essa é a coloração que eu sinto. Então assim…".
- **S089–S090** "Então… é só por essa": truncada.
- **S091–S092**: "límpido / testagem é a cor média", leitura da ficha com erro de reconhecimento.
- **S095**: "algo tipo…", com a pimenta cortada.
- **S096–S101**: a ladainha "acidez média+ / taninos médios / álcool médio / um cor… / quase um médio para mais / nas coisas, assim", com palavras cortadas.
- **S106–S108**: "intensidade do sabor é… média. Macio".

**Aparadas:**
- S062 [12] ("assim").
- S066 [6–11]: fica "Não sei se vocês conseguem ver," e emenda em S068, "Você consegue enxergar facilmente do outro lado do teu dedo". A frase se explica sozinha e dispensa a borda do "transparência".
- S074 [1]: fica "Mas" e em seguida "por que um Barolo?".

**Fica:** "Esse aqui é muito fácil… Barolo → dá pra ver o dedo → poderia ser um Pinot Noir, um Gamay → mas por que um Barolo? → coloração mais alaranjada, laranja tomate → me parece um Nebbiolo → e Barolo porque eu tenho cadastrado Barolo." Essa última é a transparência que a gente combinou manter. Depois vem "Morango. Framboesa." (o mesmo par da #107, porque o espectador atento percebe) e "ótima acidez, bom álcool, bom tanino → corpo médio+".

**Nota:** "Nebbiolo: cor clara…" sai do início do capítulo e volta depois de S085, como *"Nebbiolo: cor clara e borda alaranjada / mesmo jovem. É a uva do Barolo."*

## 4. Garrafa #107 · antes 1:30 · agora ≈ 1:04 (com as bordas)

**Saem:**
- **S113–S114** "Mas vamos lá. Coloração".
- **S117** "Ele é médio".
- **S119** "médio para profundo": contradiz o "não me parece muito escuro" e a própria ficha, que diz rubi médio.
- **S120–S121**: "Um pouco turvo, médio… o rubi", repetição.
- **S123** "Ele me dá muito mais…": a "geleia" foi cortada.
- **S124** "Não sei como é mexer": é "um figo seco, uma ameixa seca" cortado e fica incompreensível.
- **S125**: "tem alguma coisa de especiaria, mas não tô conseguindo sentir". Logo depois de ela nomear pimenta-do-reino, soa contraditório.
- **S126** "algo também de vácio": emenda de "alcaçuz" com "herbáceo", as duas cortadas.
- **S134** "Morango": o morango se repete na frase seguinte.
- **S139–S145**: "o que me faz pensar é o seco / desmédia / os médio-altos / bom cor / presidência média", a ladainha da ficha com emendas.
- **S153–S154**: "Poderia ser em 2022 / Pronto", pensamento em voz alta.

**Aparadas:**
- S129 [0] ("Mais" duplicado).
- S132 [3–4]: "do mesmo…" é autocorreção. Fica "Talvez estejamos falando" + S133[0] = "da mesma uva".
- S133 [1–4] ("Ele me trouxe algo de…", repetição).
- S146 [0–1] ("É macio" emendado).

**Arco que fica:** "Nossa! Esse aqui me deu um cheiro inicial de defumado → rubi, turbidez, não muito escuro → pimenta-do-reino → *essas aqui se parecem muito… talvez estejamos falando da mesma uva* → *morango, framboesa… eu poderia até ir para um Gamay. Mas ele tem bons taninos* → *essa aqui que é a pegadinha* → Velho Mundo → *Touriga também* → safra pela borda mais aberta."

O espectador sabe antes dela. Esse é o coração do episódio, e hoje ele está mudo.

Mantive S149–S152 (a safra pela borda) porque aplicam a lição do capítulo #21. Se precisar ganhar mais 12 s, eles são os próximos a sair.

## 5. A revelação · antes 1:04 · agora ≈ 0:37

Ela começa em S155, "Vamos revelar os vinhos". Mantenha o inserto do placar 67/100 (1590–1594).

**Saem:**
- **S156, S158, S162, S166**: "Bom." soltos.
- **S163–S164** "O primeiro… hum…".
- **S169–S170**: "pode ser influência dos vinhos anteriores / pode ser". É a mesma ideia que ela desenvolve inteira logo depois (S191–S196), e fica a versão completa.
- **S173** "Mas…".
- **S175**: "Não tinha bons taninos". Repete S176, que é mais clara.
- **S177–S179**: "Vou confirmar essa informação / mas é bom para os próximos / assim, não é…". Quem confirma agora é a nota na tela.
- **S186** "Então…".

**Aparada:** S174 [4], [7]. Fica "Eu tinha na cabeça que Gamay" + S176 "tinha praticamente nada de tanino".

**Problema de ordem da história:** ela comenta o tanino do Gamay **antes** do momento "era um Gamay" (S228), que só vem em "Vinho a vinho". Hoje o espectador ouve "os Beaujolais são conhecidos por…" sem saber que a #107 era Beaujolais. A costura é uma nota depois de S161: *"No placar, a #107 era um Gamay: / a uva que ela cogitou e descartou."* Ela entrega a uva e preserva a piada do zero ("o último eu errei tudo… eu falei que era um Touriga"). Com a borda 10, S165 ("fiquei bem nessa dúvida sobre o Gamay") também ajuda.

## 6. O que a Gamay me ensinou (antes: o fim da revelação + "A ordem das taças") · antes 0:25 + parte da revelação · agora ≈ 0:29

O capítulo vai de S180 a S196: "não é que ele não tenha tanino, é que não tem **tanto** tanino" → teste da língua → "a Touriga é bem mais" → a ordem das taças.

**Saem:**
- **S189–S190**: "uma melhoria para fazer no aplicativo… deixar a ordem dos vinhos como deveriam ser". A frase é truncada e soa como pedido de suporte no meio da aula. O conteúdo vai para a nota da ordem clássica, e o pedido continua no item 8 da lista do app.
- **S195, S197–S201**: "Então… / porque… / experimentei anteriormente vinhos mais taninosos / então… acabou que passou pra ele / alguma coisa nesse…". É a terceira vez que ela diz a mesma coisa.

**Notas:**
- Depois de S181: *"Gamay: tanino baixo, acidez alta. / Baixo, mas presente."*
- Depois de S196: *"Ordem clássica de prova: / do mais leve ao mais encorpado e tânico."* A versão antiga sai e é reposicionada.

## 7. Vinho a vinho · antes 0:42 · agora ≈ 0:33

**Saem:**
- **S205**: "É realmente o Touriga", repetição.
- **S209–S210**: "Vocês deveriam comprar, porque é muito bom". "Super recomendo" já diz tudo, e isso soa como publi.
- **S215** "Ele tem…".
- **S217–S219**: "Ele é muito bom. Muito… muito maravilhoso", o terceiro elogio seguido.
- **S231** "12…": o ",5" foi cortado.
- **S232**: "não parecia muito…", com o "alcoólico" cortado.

**Fica:**
- "Agora eu vou ver o que eu acertei e o que eu errei" (borda 13);
- Touriga da Iribarrem, maravilhoso, super recomendo, barrica presente, muita fruta, uma coisa fresca;
- Barolo 100;
- **"Oh, é engraçado. Ah, tá. É por isso que eu tirei 67. Porque o último eu errei tudo. Tirei exatamente zero. Eu falei que era um Touriga. Era um Gamay. De Beaujolais. Da França."**

Nos momentos fortes, nada sai.

**Notas:**
- "Barolo nunca é jovem" sai porque caía em cima da fala sobre a Touriga, e "nunca é jovem" é absoluto demais. Volta depois de S221: *"Barolo envelhece no mínimo 38 meses: / uma safra 2024 só chega à venda em 2028."* Fonte: Disciplinare DOCG Barolo, 38 meses a partir de 1º/nov da colheita e venda a partir de 1º/jan do 4º ano.
- "Gamay: tanino baixo…" sai daqui porque já foi dita no capítulo 6. Fica *"Beaujolais: sul da Borgonha, / ao norte de Lyon. A casa da Gamay."* depois de S230.

## 8. Quiz da degustação · antes 1:16 · agora ≈ 0:47 + tela 8/10

**Saem:**
- **S233** "Bom, é isso" (fica "Tá aí mais uma degustação").
- **S236**: "Fazer quiz desse", repetição.
- **S237**: "Eu vou sugerir essa modificação". Ela se refere ao pedido que saiu.
- **S238–S240**: "De qual era a garrafinha 41? É… a 41 era…", com a resposta truncada.
- **S241–S242**: "Vou solicitar melhoria nesse quiz / não tem que decorar número de garrafinha". É crítica ao app que ela recomenda e destoa da voz da marca. O pedido já está no item 7 do Wine Study Lab.
- **S244** "Vamos lá".
- **S249** "Hum…".
- **S251**: "O Pinot Noir e a Guj…". O nome sai truncado e mal pronunciado, e a nota substitui.
- **S253**: "Essa aqui não é importante". Soa como desprezo pela pergunta.
- **S261** "Hum…".
- **S263** "Os sabores principais": leitura solta.
- **S264**: "Então o tanino do Barolo é…". Fica o "É alto." de S262, que é a reação dela ao ver a resposta.

**Fica:** países da Gamay (Borgonha → Beaujolais → sul da Borgonha, borda 14), DNA ("eu iria no Pinot Noir"), Nebbiolo, a lista de aromas, "muito complexa, por isso o Barolo é um dos principais da Itália" (bordas 15–16), tanino do Barolo "médio+… é alto" e o fecho do arco, "por isso que quando eu fui pra Gamay me pareceu taninoso, mas não era realmente" (borda 17).

**Notas:**
- "A Suíça também é resposta certa…" fica.
- Nova, depois de S250: *"Pinot Noir × Gouais Blanc: / os mesmos pais da Chardonnay."* Fonte: Bowers et al., *Science* 285, 1999.
- Nova, depois de S265: *"Quiz: 8 de 10. / Os dois erros foram sobre a Nebbiolo."* As perguntas 6 e 8 conferem com z_2107.

---

## Capítulos novos

| Início | Título | Sub | Duração estimada |
|---|---|---|---|
| S001 | Três garrafinhas às cegas | #21 · #41 · #107 | ≈ 1:01 |
| S016 | Garrafa #21 | a menta de novo | ≈ 2:06 |
| S062 | Garrafa #41 | o Barolo pela cor | ≈ 0:47 |
| S109 | Garrafa #107 | a pegadinha | ≈ 1:04 |
| S155 | A revelação | 67 de 100 | ≈ 0:37 |
| S180 | O que a Gamay me ensinou | tanino baixo, mas presente | ≈ 0:29 |
| S202 | Vinho a vinho | o que era cada um | ≈ 0:33 |
| S234 | Quiz da degustação | 8 de 10 | ≈ 0:47 + cartela final 6 s |
| | **Total** | | **≈ 7:25–7:30** |

## Notas removidas (por texto)

"A borda da cor", "Ésteres", "Nebbiolo:", "Ordem clássica de prova:", "Barolo nunca é jovem:" e "Gamay: tanino baixo, acidez alta."

Quatro delas voltam reposicionadas pelo `notas_tela`. As outras duas, "Ésteres" e a antiga "Gamay…", não voltam.

Todas as notas novas cabem no cartão de 1100 px: a maior mede 713 px.

## Checagem técnica das notas novas

- ✅ Ordem de prova: do mais leve ao mais tânico. É a prática WSET e de concursos.
- ✅ Gamay com tanino baixo e acidez alta (Wine Folly; WSET L3).
- ✅ Beaujolais fica ao sul da Borgonha, ao norte de Lyon.
- ✅ Pinot Noir × Gouais Blanc também são os pais da Chardonnay (Bowers 1999).
- ✅ Barolo: 38 meses de envelhecimento mínimo, venda a partir do 4º ano (Disciplinare).
- ✅ Nebbiolo: cor clara e borda alaranjada cedo (*Wine Grapes*).
- ✅ Hipótese da #21: Brasil, Bento Gonçalves (tela f_760).
- ⚠️ Percepção dela, mantida como percepção: S102–S105, "ótima acidez, bom álcool, bom tanino → corpo médio+". Tecnicamente, o corpo vem de álcool, tanino e extrato, e a acidez não soma corpo. Como é a ficha dela e não uma afirmação de regra, fica sem nota.
