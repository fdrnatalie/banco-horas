# Três Taças nº 04 · roteiro v3 por temas: "A Touriga ao contrário"

O montador lê `roteiro.json`, nesta mesma pasta. Este arquivo é a versão para ler e aprovar, com o porquê de cada bloco.
Todos os tempos são **segundos do bruto** (`raw/ep04.mov`, 2117 s).

**Duração estimada: ≈ 7:25** (482 s de fala limpa ÷ 1,1 = 7:18, mais 6 s do cartão final). A conta usa o mesmo `cleanfala.Cleaner` do montador, mas sem o arquivo de hesitações. Com o `F_ep04.json`, o vídeo deve encurtar mais uns 10–20 s, porque saem os 'ééé' escondidos dentro de palavras esticadas.
**14 blocos, 41 telas, 139 falas.**

## A história em uma linha
A Natalie já reconhece a Touriga pela menta (a pista do ep. 02) e acerta a #21. Acerta o Barolo pela cor. Na #107 ela chega a dizer Gamay, descarta pelo tanino e chuta Touriga de novo. Era Gamay, e a nota dela nessa garrafa é zero. A explicação vem no fim: ela provou a Gamay depois de dois tintos de tanino alto.

## Ordem dos temas
| Bloco | Capítulo | Tema | Fala limpa (a 1,1x) |
|---|---|---|---|
| B00 | Abertura · a Touriga ao contrário | Gancho: o zero da #107, antes de qualquer contexto. Depois, a capa. | 5 s |
| B01 | Três garrafinhas às cegas · #21 · #41 · #107 | Como eu escolho e cuido das garrafinhas, a ordem da prova e por que a cor às vezes já me dá a resposta. | 36 s |
| B02 | Garrafa #21 · a cor · luz branca, rubi e a unha | Como ler a cor: luz neutra, intensidade, tom e a unha (borda) como pista de idade. | 32 s |
| B03 | Garrafa #21 · o nariz · fruta negra, violeta e madeira | Como eu procuro aromas (pensar numa fruta e ir atrás dela), a fruta que combina com a cor e o que a madeira deixa. | 44 s |
| B04 | Garrafa #21 · a menta · a pista que eu aprendi no ep. 02 | Continuidade da série: o 'álcool que não é álcool' vira menta, e a menta me leva à Touriga. Logo depois, o que a Touriga é de fato. | 32 s |
| B05 | Garrafa #21 · a hipótese · Douro ou Brasil? | A estrutura na boca e o raciocínio da região, com a transparência de que ela sabe o que tem na adega. | 34 s |
| B06 | Garrafa #41 · a cor · dá pra ver o dedo | A cor separa as uvas de casca fina; o laranja da borda aponta Nebbiolo. A Gamay entra aqui como candidata de cor clara: semente da virada. | 32 s |
| B07 | Garrafa #41 · nariz e boca · fruta vermelha e o tanino que eu marquei | Ficha curta do Barolo. O tanino 'médio' que ela marca volta no quiz e explica o erro da #107. | 9 s |
| B08 | Garrafa #107 · a cor · essas duas se parecem muito | Primeiras impressões da #107 e a comparação de cor com a #21, que planta a ideia de 'mesma uva'. | 46 s |
| B09 | Garrafa #107 · a pegadinha · eu cheguei a dizer Gamay | A virada: ela nomeia a Gamay e descarta pelo tanino. O espectador sabe antes dela. | 29 s |
| B10 | A revelação · 67 de 100 | O placar e o gabarito vinho a vinho, até o zero da #107. | 41 s |
| B11 | O que a Gamay me ensinou · pouco tanino não é tanino zero | Por que ela descartou a Gamay: a ideia de 'tanino zero'. O teste da língua compara as duas taças. | 40 s |
| B12 | Quiz da degustação · 8 de 10 | O quiz do app fixa o que ela aprendeu sobre Gamay e Nebbiolo. Os dois erros são sobre a Nebbiolo, e o do tanino prepara o fecho. | 40 s |
| B13 | O que eu aprendi · a ordem das taças | Fecho: o tanino alto do Barolo, provado antes, fez a Gamay parecer tânica. A lição é a ordem de prova. | 18 s |

Na ordem original, o vídeo ia do sorteio ao quiz. Agora segue a pergunta do episódio: como eu leio uma taça (B01–B05), a cor que acerta (B06–B07), a cor que engana (B08–B09), o resultado (B10) e por que eu errei (B11–B13). A revelação vem **antes** da aula de tanino da Gamay. No bruto era o contrário, e quem assistia ouvia 'os Beaujolais não são tão taninosos' sem saber que a #107 era Beaujolais.

## Regras de corte usadas
- `a` é o início da primeira palavra e `b` é o fim da última + 0,15 s, pela `T_ep04.json`.
- Quando a palavra seguinte começa antes desses 0,15 s, `b` para no início dela, para a palavra que saiu não vazar. Essas falas estão marcadas com ✂ abaixo.
- Seis falas têm borda manual (marcadas com ✎). Nelas, a transcrição esticou uma palavra por cima de um começo falso ou de uma repetição. Retranscrevi esses trechos com o turbo e a borda nova está em `nota` no JSON.
- Começo falso, repetição e autocorreção saem quebrando a frase em duas falas. Por exemplo: 'falando | da mesma uva', 'Eu tinha na cabeça | que Gamay | tinha praticamente nada de tanino'.
- O montador tira 'ééé', 'hum', tosse e pausa de mais de 0,32 s dentro de cada fala.

---

## B00 · Abertura · *a Touriga ao contrário*

**Tema:** Gancho: o zero da #107, antes de qualquer contexto. Depois, a capa.

**Por quê:** O zero se entende sozinho e abre a pergunta do episódio: em qual taça e por quê? Em 3 s ela já disse a frase. A capa entra em seguida, sobre o 'Começar uma nova degustação', porque o montador só mantém uma tela no ar enquanto houver fala. A tela do gancho mostra o 0 da #107 sem dizer a uva.

**Tela 1 · PLACAR · 67 / 100** (falas 0–0)  
#21 · 100 pontos / #41 · 100 pontos / #107 · 0 pontos  
<small>Fonte: tela Resultado do app (1596 s e 1847 s do bruto)</small>

0. `1840.40–1843.93` “O último eu errei tudo. Tirei exatamente zero.”

**Tela 2 · AULA · capa** (falas 1–1)  
três taças · nº 04 / A Touriga ao contrário / três garrafinhas às cegas  
<small>Fonte: identidade da série</small>

1. `31.48–33.57` “Começar uma nova degustação.”

---

## B01 · Três garrafinhas às cegas · *#21 · #41 · #107*

**Tema:** Como eu escolho e cuido das garrafinhas, a ordem da prova e por que a cor às vezes já me dá a resposta.

**Por quê:** Antes era uma tangente cortada. Agora ensina o cuidado com a garrafinha aberta (oxidação) e deixa registrada a ordem da prova ('ordem sequencial'), que é a lição do fim. A fala da amostragem curta é a transparência que a gente combinou manter, e o 'diferenciar castas só pela cor' prepara as duas pontas do episódio: o Barolo acertado e a #107 errada justamente pela cor.

**Tela 1 · AULA · Garrafinha aberta** (falas 0–3)  
Uso primeiro as que abri há pouco. / Ar dentro da garrafinha = oxigênio: o vinho oxida e perde fruta. / Meu jeito de reaproveitar: água fervendo, um pouco de álcool, deixar secar.  
<small>Fonte: Linhas 1 e 3: o método dela. Linha 2: WSET Level 2, conservação do vinho aberto.</small>

0. `35.18–46.56` ✂ “Eu dou preferência aos que já abri recentemente, porque como tem ar dentro, né, oxigênio, se eu deixar muito tempo as garrafinhas, elas acabam oxidando.”
1. `94.74–97.83` “Quando acaba, o que eu faço é lavar.”
2. `98.04–99.65` “Coloco na água fervendo,”
3. `101.28–106.73` “depois um pouquinho de álcool e deixo evaporar tudo.”

**Tela 2 · COMPARACAO · Sorteio do dia** (falas 4–4)  
#21 · 1ª taça / #41 · 2ª taça / #107 · 3ª taça  
<small>Fonte: tela Nova degustação do app (60–90 s). Ela fala '141' no sorteio: o número sai do áudio.</small>

4. `60.48–64.31` “Como sempre, fica na ordem sequencial.”

**Tela 3 · AULA · A cor como primeira pista** (falas 5–8)  
Minha adega de garrafinhas é pequena: eu já conheço as cores dela. / A cor ajuda a separar uvas, mas sozinha não fecha a resposta.  
<small>Fonte: Linha 1: transparência dela. Linha 2: WSET L3 (a cor é uma pista entre várias).</small>

5. `111.76–115.11` “Tem alguns que eu consigo já saber pela cor.”
6. `122.12–126.66` ✂ “Uma amostragem curta, né? Eu não tenho tantos rótulos.”
7. `129.38–134.06` ✂ “Mas é realmente incrível como você consegue diferenciar algumas castas”
8. `138.70–141.37` “só por causa da coloração.”

---

## B02 · Garrafa #21 · a cor · *luz branca, rubi e a unha*

**Tema:** Como ler a cor: luz neutra, intensidade, tom e a unha (borda) como pista de idade.

**Por quê:** Esta é a aula de cor. A retranscrição achou uma fala que a transcrição tinha engolido: 'Um papelzinho branco pra poder enxergar' (fundo branco). Ficou fora o trecho de 279–303 s, porque a turbidez não indica safra e o tanino não se vê na taça. O palpite de safra pela unha fica, e o rótulo (2022) volta no B10.

**Tela 1 · AULA · Como eu leio a cor** (falas 0–2)  
Luz branca e fundo branco: a cor aparece sem desvio. / Intensidade: pálida · média · profunda. / Tom: púrpura · rubi · granada · atijolado. / Unha = a borda, com a taça inclinada: pista de idade.  
<small>Fonte: WSET Level 3, Systematic Approach to Tasting Wine (SAT) (aparência: intensidade, cor; borda indica evolução).</small>

0. `236.78–242.57` “Um papelzinho branco pra poder enxergar. A gente coloca assim, tem que ter uma luz.”
1. `244.36–250.59` “Eu odeio luz branca, mas para realmente fazer uma análise visual do vinho precisa ser branca.”
2. `251.68–253.39` “Para não influenciar.”

**Tela 2 · APP · #21 · eu vi** (falas 3–5)  
rubi, médio para profundo · unha média / meu palpite pela unha: 2024 ou 2025  
<small>Fonte: percepção dela; tela Visual do app</small>

3. `256.62–265.60` ✂ “Ele é um rubi, médio para profundo, de intensidade de cor.”
4. `265.60–273.11` “Tem uma unha média, não acho que é um vinho muito, muito velho, tampouco muito jovem.”
5. `273.80–278.70` ✂ “Eu chutaria algo em torno de 2024 ou 25.”

---

## B03 · Garrafa #21 · o nariz · *fruta negra, violeta e madeira*

**Tema:** Como eu procuro aromas (pensar numa fruta e ir atrás dela), a fruta que combina com a cor e o que a madeira deixa.

**Por quê:** É um método que dá para repetir em casa: pensar numa fruta e ir atrás dela, e 'se não vem, tudo bem'. A ligação entre fruta e cor é pista dela e aparece assim na tela. O 'morango, porque ele não tem essa coloração' é ironia plantada, porque o morango volta na #107. A violeta fica, porque é a marca da Touriga (B04).

**Tela 1 · APP · #21 · eu senti** (falas 0–2)  
fruta madura, banana, compota, geleia / violeta  
<small>Fonte: percepção dela; tela Nariz do app</small>

0. `309.42–311.29` “Ele puxa muito uma fruta madura.”
1. `328.94–335.75` “Ele já está me passando uma banana, mas é mais uma fruta em compota, geleia, uma fruta cozida talvez.”
2. `351.70–353.97` “Eu sinto algo de violeta também nele.”

**Tela 2 · AULA · Como eu procuro um aroma** (falas 3–8)  
Penso numa fruta e vou atrás dela na taça. / Não veio? Tudo bem: passo para a próxima. / Eu senti: fruta negra (cassis, mirtilo, ameixa), como a cor profunda. Pista minha, não regra.  
<small>Fonte: método dela; famílias de fruta do WSET Level 3, Systematic Approach to Tasting Wine (SAT)</small>

3. `369.54–375.85` “O legal de você ir vendo quais frutas é que você pensa assim: ah, cereja vermelha tem?”
4. `379.02–384.15` “Aí você puxa para ver se está vindo alguma coisa de cereja vermelha.”
5. `384.54–387.09` “Se não está vindo, não tem problema.”
6. `406.44–411.67` “Aqui tá me passando um cassis, um mirtilo, uma ameixa.”
7. `413.06–416.42` ✂ “Frutas mais voltadas na coloração dele mesmo.”
8. `416.86–421.77` “Não ia numa fruta muito fresca, tipo morango, porque ele não tem essa coloração.”

**Tela 3 · AULA · O que a madeira deixa** (falas 9–12)  
Carvalho traz aromas como cravo, baunilha, tosta, cedro e defumado. / A 'caixa de charuto' lembra o cedro. / Eu senti: alcaçuz, carvalho, defumado, caixa de charuto.  
<small>Fonte: WSET Level 3, Systematic Approach to Tasting Wine (SAT), léxico de aromas de carvalho</small>

9. `452.36–454.25` “Tem algo de especiaria.”
10. `456.46–457.33` “Alcaçuz.”
11. `479.96–483.45` “Talvez tem algo de madeira.”
12. `485.95–494.25` ✎ “Tem um carvalho, uma defumada, uma caixa de charuto.”  
   <small>começa no 2º 'tem' (o 1º é gaguejado); conferido no turbo: 'Tem... tem um carvalho... uma defumada... uma caixa de charuto'</small>

---

## B04 · Garrafa #21 · a menta · *a pista que eu aprendi no ep. 02*

**Tema:** Continuidade da série: o 'álcool que não é álcool' vira menta, e a menta me leva à Touriga. Logo depois, o que a Touriga é de fato.

**Por quê:** É o coração da continuidade. No ep. 02 ela aprendeu que, quando parece álcool, pode ser menta, e aqui aplica a pista sem ninguém pedir. Depois do 'Touriga Nacional' entra o fato: o que a uva é segundo as fontes, ligado à violeta que ela sentiu. A menta continua como pista dela.

**Tela 1 · AULA · Minha pista desde o ep. 02** (falas 0–4)  
Ep. 01 e 02: a Touriga Nacional me enganou. / Ep. 02: aprendi que o 'álcool' no nariz pode ser menta. / Menta me leva à Touriga. É pista minha, não regra.  
<small>Fonte: ep. 01 e ep. 02 da série (T_ep02, 2327–2342 s)</small>

0. `524.76–532.81` “Na boca ele me trouxe algo verde, inclusive eu posso voltar e ver se esse verde ainda permanece no nariz.”
1. `551.32–553.14` ✂ “No primeiro momento,”
2. `556.62–560.49` ✎ “quando você sente um álcool no nariz bem forte,”  
   <small>tira o começo falso 'eu senti um…' (553,7–556,6 s, conferido no turbo)</small>
3. `560.54–571.27` “mas eu já entendi que muitas vezes quando eu sinto esse álcool, não seja álcool, poderia ser uma coisa tão fresca que remete ao álcool, por exemplo, o eucalipto.”
4. `584.20–588.05` “Ele me dá alguma coisa de menta, de eucalipto.”

**Tela 2 · AULA · Touriga Nacional** (falas 5–5)  
Marca registrada: violeta, que eu senti nesta taça. / Fruta negra (amora, mirtilo, ameixa) e bergamota; menta aparece em alguns. / Tinto encorpado, de tanino alto. A uva símbolo do Douro e do Dão.  
<small>Fonte: Robinson, Harding & Vouillamoz, Wine Grapes (2012); Wines of Portugal; Wine Folly, Touriga Nacional</small>

5. `588.24–596.51` “Eu vou na menta, porque agora eu tô começando a achar que é o que eu erro sempre: Touriga Nacional.”

---

## B05 · Garrafa #21 · a hipótese · *Douro ou Brasil?*

**Tema:** A estrutura na boca e o raciocínio da região, com a transparência de que ela sabe o que tem na adega.

**Por quê:** Sai a ladainha de 'médio, médio pra mais, médio pra alto' (625–684 s) e fica uma frase de estrutura. O raciocínio da região fica inteiro e honesto: 'adocicado → Novo Mundo → como eu sei que tenho uma Touriga do Brasil'. A tela explica a pista de clima sem transformar em regra.

**Tela 1 · APP · #21 na boca · eu senti** (falas 0–2)  
seco · acidez média · tanino médio+ / bom corpo · macio  
<small>Fonte: percepção dela; tela Boca do app</small>

0. `604.16–610.83` “Na boca ele é seco, ele tem uma acidez média, ele tem taninos médios pra mais.”
1. `635.02–637.11` “E ele tem um bom corpo.”
2. `675.86–676.87` “Ele é macio.”

**Tela 2 · AULA · Fruta madura, clima mais quente** (falas 3–5)  
Fruta bem madura, com sensação adocicada, costuma apontar para clima mais quente. / É uma pista de estilo, não um mapa: serve como hipótese. / E eu sei que tenho uma Touriga do Brasil na adega.  
<small>Fonte: Linhas 1–2: WSET Level 3, Systematic Approach to Tasting Wine (SAT) (efeito do clima na fruta). Linha 3: transparência dela.</small>

3. `703.95–715.36` ✎ “Eu não vou colocar um Touriga do Douro, porque ele me parece um pouco mais adocicado.”  
   <small>tira 'hum… a região… eu vou,' (começo falso; no turbo, 2º 'eu' em 704,14 s)</small>
4. `715.36–722.11` “Então, eu iria mais pra uma região do Novo Mundo.”
5. `722.20–726.97` “Então, eu vou colocar, como eu sei que eu tenho um Touriga aqui do Brasil,”

**Tela 3 · PLACAR · Minha hipótese da #21** (falas 6–7)  
Touriga Nacional / Bento Gonçalves (RS) · Brasil / safra 2024 · 14%  
<small>Fonte: tela Hipótese do app (760 s)</small>

6. `738.20–740.71` “Bento Gonçalves.”
7. `775.36–779.23` “Teor alcoólico, eu vou colocar um 14%.”

---

## B06 · Garrafa #41 · a cor · *dá pra ver o dedo*

**Tema:** A cor separa as uvas de casca fina; o laranja da borda aponta Nebbiolo. A Gamay entra aqui como candidata de cor clara: semente da virada.

**Por quê:** Acerto por competência visual, com aula de tintos claros. A fala 'poderia ser um Pinot Noir, um Gamay' é a semente da virada, porque ela mesma põe a Gamay entre as uvas de cor clara. A transparência do acervo ('tenho cadastrado Barolo') e a continuidade com o ep. 02 (mesmo Barolo Morello) ficam na tela.

**Tela 1 · APP · #41 · eu vi** (falas 0–3)  
transparência média: dá pra ver o dedo / borda alaranjada: 'laranja tomate'  
<small>Fonte: percepção dela; tela Visual do app</small>

0. `796.84–802.83` “Esse aqui é muito fácil, porque já a cor dele me remete, assim, rapidamente a um Barolo.”
1. `814.44–816.22` ✂ “Não sei se vocês conseguem ver,”
2. `819.94–824.11` “transparência, digamos assim, média.”
3. `824.72–828.87` “Você consegue enxergar facilmente do outro lado do teu dedo.”

**Tela 2 · AULA · Tintos claros** (falas 4–9)  
Pinot Noir, Gamay e Nebbiolo têm casca fina: dão tintos claros, transparentes. / A Nebbiolo ganha borda granada, puxando ao laranja, mesmo jovem. / É a uva do Barolo, no Piemonte.  
<small>Fonte: Robinson, Harding & Vouillamoz, Wine Grapes (2012); WSET Level 3, Systematic Approach to Tasting Wine (SAT)</small>

4. `831.42–834.85` “Poderia ser um Pinot Noir, por exemplo, um Gamay.”
5. `836.94–837.95` “Por que um Barolo?”
6. `838.16–840.10` ✂ “Eu sinto que tem”
7. `841.86–844.65` “uma coloração mais alaranjada.”
8. `847.54–849.87` “É um laranja tomate.”
9. `856.80–860.93` “Já observando ele, me parece que é um Nebbiolo.”

**Tela 3 · APP · Transparência** (falas 10–10)  
o Barolo está cadastrado na minha adega / no ep. 02 eu provei esse mesmo Barolo  
<small>Fonte: adega do app; ep. 02 (#43 Barolo Morello)</small>

10. `861.72–866.33` “E Barolo porque eu tenho cadastrado Barolo.”

---

## B07 · Garrafa #41 · nariz e boca · *fruta vermelha e o tanino que eu marquei*

**Tema:** Ficha curta do Barolo. O tanino 'médio' que ela marca volta no quiz e explica o erro da #107.

**Por quê:** É curto de propósito. Morango e framboesa são as mesmas frutas que ela vai sentir na #107. O 'taninos médios' que ela marca no Barolo é o fio do episódio: o quiz mostra que o Barolo tem tanino alto, e é esse tanino que contamina a Gamay (B13).

**Tela 1 · APP · #41 · eu senti** (falas 0–2)  
morango, framboesa, geleia / guarde estas duas frutas: elas voltam na #107  
<small>Fonte: percepção dela; tela Nariz do app</small>

0. `896.16–897.43` “Morango.”
1. `899.42–900.75` “Framboesa.”
2. `908.23–908.97` “Geleia.”

**Tela 2 · APP · #41 na minha ficha** (falas 3–7)  
acidez média+ · tanino médio · corpo médio+ / o tanino 'médio' volta no quiz  
<small>Fonte: tela Confirmação do app (1060 s)</small>

3. `958.38–959.89` “Taninos médios.”
4. `976.68–977.99` “Tem uma ótima acidez.”
5. `978.40–979.58` ✂ “Um bom álcool.”
6. `979.58–980.49` “Um bom tanino.”
7. `981.84–983.84` ✂ “Vou colocar um corpo médio pra mais.”

---

## B08 · Garrafa #107 · a cor · *essas duas se parecem muito*

**Tema:** Primeiras impressões da #107 e a comparação de cor com a #21, que planta a ideia de 'mesma uva'.

**Por quê:** Mostra a ordem dos sentidos (cor, nariz) e a comparação de cor com a #21, que planta 'a mesma uva'. Saem a ladainha de 'médio/médio pra profundo/rubi' e os 77 s de silêncio. As emendas 'toquezinho | mais de vermelho' e 'falando | da mesma uva' tiram as autocorreções.

**Tela 1 · APP · #107 · eu senti** (falas 0–7)  
rubi, não muito escuro, um pouco turvo / defumado, pimenta-do-reino, geleia, herbáceo  
<small>Fonte: percepção dela; telas Visual e Nariz do app</small>

0. `1068.54–1072.68` ✂ “E agora, a última.”
1. `1072.68–1074.03` “Nossa!”
2. `1077.68–1085.01` “Essa aqui me deu um cheiro inicial de defumado.”
3. `1089.12–1091.87` “É um rubi. Tem uma turbidez.”
4. `1097.44–1099.71` “Ele não me parece muito escuro.”
5. `1134.02–1137.29` “Ele me dá muito uma pimenta-do-reino.”
6. `1147.96–1149.71` “Ele me dá muito uma geleia.”
7. `1253.66–1263.63` “Ele tem algo também de herbáceo, de frescor.”

**Tela 2 · COMPARACAO · Mesma uva?** (falas 8–14)  
#21 · rubi · um toque mais vermelho · um pouco mais escura · madeira / #107 · rubi · mais clara · defumado e geleia  
<small>Fonte: percepção dela (1268–1298 s)</small>

8. `1268.88–1273.47` “Engraçado que se eu comparar as cores, essas aqui se parecem muito,”
9. `1273.74–1278.30` ✂ “mas a primeira, ela tem um toquezinho”
10. `1284.52–1286.73` “mais de vermelho.”
11. `1288.72–1291.05` “Um pouquinho mais escura.”
12. `1291.66–1293.41` “Talvez incidência da barrica.”
13. `1293.64–1295.04` ✂ “Talvez estejamos falando”
14. `1295.88–1298.21` “da mesma uva.”

---

## B09 · Garrafa #107 · a pegadinha · *eu cheguei a dizer Gamay*

**Tema:** A virada: ela nomeia a Gamay e descarta pelo tanino. O espectador sabe antes dela.

**Por quê:** É a virada. Ela diz Gamay e descarta pelo tanino, e o espectador já viu o B06 e o B07. A safra pela unha fica porque aplica a aula do B02, e a tela corrige o exagero ('a unha dá uma faixa, não o ano').

**Tela 1 · APP · #107 na boca · eu senti** (falas 0–3)  
morango, framboesa · cor clara: 'poderia ser Gamay' / tanino médio+: descartei  
<small>Fonte: percepção dela; tela Boca do app</small>

0. `1356.56–1361.26` ✂ “Pelo morango, framboesa que me dá na boca e pela coloração, eu poderia até ir para um Gamay.”
1. `1361.26–1366.03` “Mas ele tem bons taninos.”
2. `1400.28–1401.67` “Ele é seco.”
3. `1430.56–1431.33` “Bom corpo.”

**Tela 2 · PLACAR · Minhas hipóteses** (falas 4–6)  
#21 · Touriga Nacional · Brasil / #41 · Nebbiolo · Barolo, Itália / #107 · Touriga Nacional · Douro, Portugal  
<small>Fonte: telas Hipótese do app (760, 1060 e 1560 s)</small>

4. `1437.76–1439.39` “Essa aqui que é a pegadinha.”
5. `1448.88–1453.09` “Eu vou no Velho Mundo, nessa daqui.”
6. `1457.18–1460.09` “Eu vou no Touriga também.”

**Tela 3 · APP · #107 · safra** (falas 7–9)  
unha mais aberta: chutei 2023, um pouco mais velho / a unha dá uma faixa de idade, não o ano  
<small>Fonte: Linha 1: percepção dela. Linha 2: WSET Level 3, Systematic Approach to Tasting Wine (SAT) (a borda indica evolução, sem datar o vinho)</small>

7. `1521.64–1522.81` “Por que eu coloquei 2023?”
8. `1523.30–1526.97` “Porque a unha dele é mais aberta.”
9. `1527.16–1534.67` “Então, como a unha acaba representando muito a idade do vinho, eu coloquei um pouquinho mais velho.”

---

## B10 · A revelação · *67 de 100*

**Tema:** O placar e o gabarito vinho a vinho, até o zero da #107.

**Por quê:** O placar e o gabarito, um vinho por vez. O 'acertei duas uvas' fica uma vez só (a segunda leitura, de 1600 s, sai). Na tela do Barolo entra a nota dos 38 meses, porque ela marcou safra 2024. O zero vem no fim do bloco e fecha o gancho.

**Tela 1 · PLACAR · 67 / 100** (falas 0–2)  
3 vinhos às cegas / uvas: 2 de 3  
<small>Fonte: tela Resultado do app (1596 s)</small>

0. `1557.14–1559.11` “Vamos revelar os vinhos.”
1. `1568.44–1571.13` “Acertei duas uvas. Ai, meu Deus.”
2. `1603.80–1606.59` “Uma região apenas. E um país.”

**Tela 2 · APP · #21 · Touriga Nacional ✓** (falas 3–8)  
Reserva Touriga Nacional 2022 · Bodega Iribarrem / Bento Gonçalves (RS) · 13,5% · pela unha eu chutei 2024  
<small>Fonte: gabarito do app (1797–1800 s)</small>

3. `1790.66–1794.29` “E agora eu vou ver o que eu acertei e o que eu errei.”
4. `1799.12–1803.29` “É aquele Touriga da Iribarrem, que é maravilhoso.”
5. `1803.42–1804.87` “Eu super recomendo esse vinho.”
6. `1813.70–1817.95` “O aroma de barrica é muito presente.”
7. `1819.08–1822.33` “Mas ele não só a barrica tem, ele tem muita fruta.”
8. `1822.56–1826.27` “Ele tem uma coisa fresca também.”

**Tela 3 · APP · #41 · Barolo ✓** (falas 9–9)  
Nebbiolo · Piemonte, Itália · 14% / Barolo envelhece no mínimo 38 meses: safra 2024 só sai em 2028  
<small>Fonte: gabarito do app (1825 s); Disciplinare DOCG Barolo: 38 meses (18 em madeira), venda a partir de 1º/jan do 4º ano após a colheita</small>

9. `1832.96–1836.11` “O próximo é o Barolo, que eu acertei também, 100.”

**Tela 4 · PLACAR · #107 · 0 pontos** (falas 10–17)  
Era Gamay · Beaujolais, França · 12,5% / Eu marquei: Touriga Nacional · Douro · 14%  
<small>Fonte: gabarito do app (1847–1851 s)</small>

10. `1836.32–1837.77` “Oh, é engraçado. Ah, tá.”
11. `1838.08–1839.63` “É por isso que eu tirei 67.”
12. `1840.18–1843.93` “Porque o último eu errei tudo. Tirei exatamente zero.”
13. `1844.44–1845.65` “Eu falei que era um Touriga,”
14. `1845.88–1847.42` ✎ “era um Gamay,”  
   <small>tira 'era um…' repetido; 'Gamay' termina em 1847,46 s no turbo, depois do fim da transcrição</small>
15. `1847.98–1849.87` ✎ “de Beaujolais, da França.”  
   <small>tira o 'é do…' (autocorreção)</small>
16. `1850.26–1851.83` “12,5.”
17. `1859.18–1861.63` “Ele realmente não parecia muito alcoólico.”

---

## B11 · O que a Gamay me ensinou · *pouco tanino não é tanino zero*

**Tema:** Por que ela descartou a Gamay: a ideia de 'tanino zero'. O teste da língua compara as duas taças.

**Por quê:** Na ordem original, ela comentava o tanino da Gamay antes de dizer que a #107 era Gamay. O B10 agora vem antes, e o B11 explica o erro: a ideia de que Gamay tem tanino zero, a frase de efeito ('não é que não tenha tanino, é que não tem tanto') e o teste da língua, com a Touriga como comparação.

**Tela 1 · APP · #107 era Gamay** (falas 0–3)  
a uva que eu cogitei e descartei / pelo tanino  
<small>Fonte: gabarito do app (1847 s)</small>

0. `1612.98–1616.19` “Eu fiquei bem nessa dúvida sobre o Gamay.”
1. `1620.72–1624.15` “Nossa, mas esse aqui é um Gamay com bastante tanino, por quê?”
2. `1637.32–1644.73` “Se não me engano, os Beaujolais são conhecidos por vinhos não tão taninosos.”
3. `1645.44–1647.67` “Esse daqui tem um tanino médio.”

**Tela 2 · AULA · Gamay** (falas 4–9)  
Casca fina: cor clara e transparente. / Fruta vermelha: morango, framboesa, cereja. / Acidez alta, tanino baixo. Baixo, não zero. / A uva do Beaujolais, logo ao sul da Borgonha, ao norte de Lyon.  
<small>Fonte: Robinson, Harding & Vouillamoz, Wine Grapes (2012); Wine Folly, Gamay e Beaujolais; WSET Level 3, Systematic Approach to Tasting Wine (SAT)</small>

4. `1655.66–1658.07` “Ele não me pareceu um Gamay, inicialmente.”
5. `1658.24–1665.13` “Eu cheguei a falar sobre ele, porque ele realmente puxa essa coisa do morango, de uma framboesa.”
6. `1668.32–1669.58` ✂ “Eu tinha na cabeça”
7. `1669.78–1670.84` ✂ “que Gamay”
8. `1673.60–1675.51` “tinha praticamente nada de tanino.”
9. `1688.84–1691.99` “Talvez não é que ele não tenha tanino, mas é que ele não tenha tanto tanino.”

**Tela 3 · AULA · O teste da língua** (falas 10–13)  
Tanino se sente como secura: gengiva e céu da boca ásperos. / Depois do gole, passe a língua no céu da boca: quanto mais seco, mais tanino. / Compare duas taças lado a lado.  
<small>Fonte: WSET Level 3, Systematic Approach to Tasting Wine (SAT) (tanino: sensação de secura e aspereza). O teste é prática dela.</small>

10. `1692.76–1694.76` ✂ “Por exemplo, agora fiz o teste da língua, né?”
11. `1694.76–1696.13` “Passei a língua no céu da boca.”
12. `1702.90–1704.23` “Me deixa a boca seca.”
13. `1705.60–1707.09` “Tá bem astringente.”

**Tela 4 · COMPARACAO · Tanino · eu senti × típico da uva** (falas 14–15)  
#107 Gamay · eu senti: médio · típico: baixo / #21 Touriga · eu senti: bem mais seco · típico: alto  
<small>Fonte: percepção dela; Robinson, Harding & Vouillamoz, Wine Grapes (2012)</small>

14. `1709.12–1712.87` “Vou testar a mesma coisa com o primeiro, com o Touriga.”
15. `1722.44–1724.01` “Claro que o Touriga é bem mais.”

---

## B12 · Quiz da degustação · *8 de 10*

**Tema:** O quiz do app fixa o que ela aprendeu sobre Gamay e Nebbiolo. Os dois erros são sobre a Nebbiolo, e o do tanino prepara o fecho.

**Por quê:** O quiz vira revisão. Entram onde a Gamay brilha (com a Suíça e a história de 1395 na tela), a família da Gamay e os aromas da Nebbiolo. Saem as críticas ao quiz e as perguntas pelo número da garrafinha, e esses pedidos foram para a lista do app. O bloco termina no 'eu acho que é um médio mais', e o placar 8/10 mostra que o erro foi o tanino da Nebbiolo.

**Tela 1 · APP · —** (falas 0–1)  
(tela do app, sem nota)  
<small>Fonte: tela do quiz no app (1903 s)</small>

0. `1870.74–1873.11` “Agora eu vou para o meu quiz de degustação.”
1. `1901.46–1905.31` “Em quais desses países a uva Gamay tem presença importante?”

**Tela 2 · AULA · Onde a Gamay brilha** (falas 2–5)  
França: Beaujolais, logo ao sul da Borgonha. / Suíça: uma das tintas mais plantadas (Valais, Vaud, Genebra). / Em 1395, Filipe, o Audaz, duque da Borgonha, mandou arrancá-la para proteger a Pinot Noir.  
<small>Fonte: Wine Folly, Beaujolais; swisswine.com, Gamay; Wine Spectator, 'The Exile of Burgundy'</small>

2. `1912.52–1916.07` “A Gamay é muito famosa em Borgonha, né?”
3. `1916.08–1917.13` “Na Beaujolais.”
4. `1917.14–1918.98` ✂ “Na parte sul da Borgonha.”
5. `1930.62–1931.87` “Ah, é França, né?”

**Tela 3 · AULA · A família da Gamay** (falas 6–7)  
Pelo DNA: Pinot Noir × Gouais Blanc. / Os mesmos pais da Chardonnay.  
<small>Fonte: Bowers et al., Science 285 (1999), 'Historical genetics: the parentage of Chardonnay, Gamay, and other wine grapes of northeastern France'</small>

6. `1936.70–1940.75` “Pela análise de DNA, qual dessas uvas é a mãe e pai da Gamay?”
7. `1943.02–1944.29` “Eu ia no Pinot Noir.”

**Tela 4 · AULA · Nebbiolo** (falas 8–9)  
Rosa e alcatrão: a assinatura clássica. / Cor clara, mas acidez e tanino altos. / É a uva do Barolo e do Barbaresco.  
<small>Fonte: Robinson, Harding & Vouillamoz, Wine Grapes (2012); WSET Level 3, Systematic Approach to Tasting Wine (SAT)</small>

8. `2035.64–2052.93` “Olha que interessante: a Nebbiolo tem como aromas típicos a rosa, o couro, anis, alcatrão, violeta, framboesa, trufa, tabaco, ameixa seca. Então ela é muito complexa,”
9. `2054.68–2060.43` “por isso que o Barolo é um dos principais da Itália.”

**Tela 5 · PLACAR · Quiz: 8 de 10** (falas 10–11)  
os dois erros foram na Nebbiolo / aroma: framboesa (marquei figo seco) / tanino: alto (marquei médio+)  
<small>Fonte: tela do quiz no app (2015, 2078 e 2106 s)</small>

10. `2068.20–2070.40` ✂ “Tanino típico de um Barolo.”
11. `2070.40–2072.32` ✂ “Eu acho que é um médio mais.”

---

## B13 · O que eu aprendi · *a ordem das taças*

**Tema:** Fecho: o tanino alto do Barolo, provado antes, fez a Gamay parecer tânica. A lição é a ordem de prova.

**Por quê:** O fecho junta o que estava espalhado em 1759 s e 2077–2095 s numa conclusão só: o Barolo tem tanino alto, ele veio antes, e a Gamay pareceu tânica. A lição prática é provar do mais leve ao mais tânico. O CTA retoma a série.

**Tela 1 · COMPARACAO · A ordem desta prova** (falas 0–1)  
1ª · #21 Touriga · tanino típico: alto / 2ª · #41 Barolo · tanino típico: alto / 3ª · #107 Gamay · tanino típico: baixo  
<small>Fonte: ordem do sorteio; perfis de tanino: Robinson, Harding & Vouillamoz, Wine Grapes (2012)</small>

0. `2077.28–2080.03` “O tanino do Barolo é alto.”
1. `2090.04–2095.13` “Por isso que quando eu fui para a Gamay, me pareceu taninoso, mas não era realmente.”

**Tela 2 · AULA · Ordem de prova** (falas 2–3)  
Do mais leve ao mais tânico. / A secura do tanino se acumula de um gole para o outro. / Na próxima, a Gamay vem primeiro.  
<small>Fonte: prática do WSET e de concursos; Guinard, Pangborn & Lewis, Am. J. Enol. Vitic. 37:184 (1986), adstringência em goles repetidos</small>

2. `1759.94–1766.44` ✂ “Talvez tenha influenciado, na minha percepção, eu ter tomado vinhos mais tânicos antes.”
3. `1766.44–1770.75` “E o Beaujolais, ele não é muito tânico.”

**Tela 3 · AULA · Qual uva te engana sempre?** (falas 4–4)  
Ep. 01 e 02: a Touriga me enganou. / Ep. 04: eu vi Touriga onde era Gamay. / Conta nos comentários.  
<small>Fonte: continuidade da série</small>

4. `1869.14–1870.63` “Tá aí mais uma degustação.”

---

## Checagem técnica (tudo o que vai ao ar)

**Percepção dela.** Pode ir ao ar, e na tela aparece como "eu senti / eu vi": a fruta que combina com a cor, a menta como pista da Touriga, o "adocicado → Novo Mundo", "a primeira é um pouco mais escura, talvez pela barrica", o tanino "médio" que ela sentiu na #107 e no Barolo, e o "ele realmente não parecia muito alcoólico".

| Afirmação | Onde | Status | Fonte / ação |
|---|---|---|---|
| Garrafinha aberta oxida por causa do ar dentro | B01 | ✅ | WSET Level 2, conservação do vinho aberto |
| Luz branca e fundo branco para a análise visual | B02 | ✅ | WSET L3 SAT, aparência |
| A unha (a borda) dá pista de idade | B02, B09 | ✅ com ressalva | WSET L3 SAT. A borda indica evolução, mas não data o vinho. A tela do B09 diz "uma faixa, não o ano" |
| Turbidez indica safra · tanino "pelo visual" · lágrimas | 279–303 s | ❌ | **Cortado.** Turbidez é limpidez. Tanino se sente na boca. Lágrima tem a ver com álcool e açúcar |
| Ésteres = os aromas de cereja | 387–395 s | ⚠️ | **Cortado** (fala incompleta, e ela mesma pergunta "falei certo?") |
| Carvalho dá cravo, baunilha, tosta, cedro, defumado | tela B03 | ✅ | WSET L3, léxico de aromas de carvalho |
| Touriga: violeta, fruta negra, bergamota; menta em alguns; tinto encorpado, tanino alto; Douro e Dão | tela B04 | ✅ | Robinson/Harding/Vouillamoz, *Wine Grapes*; Wines of Portugal; Wine Folly |
| Menta = Touriga | B04 | ⚠️ como regra | Fica como **pista dela**, e a tela diz isso |
| Fruta madura e adocicada sugere clima mais quente | tela B05 | ✅ como pista | WSET L3, efeito do clima. A tela chama de hipótese. Não diz que a Serra Gaúcha é quente |
| Pinot Noir, Gamay e Nebbiolo dão tintos claros | B06 | ✅ | *Wine Grapes*; WSET L3 |
| Nebbiolo ganha borda granada/alaranjada cedo | B06 | ✅ | *Wine Grapes* |
| Safra 2024 para um Barolo | ficha #41 | ❌ → nota | Disciplinare DOCG Barolo: mínimo de 38 meses (18 em madeira), venda a partir de 1º/jan do 4º ano após a colheita. Uma safra 2024 só chega ao mercado em 2028. Fica como nota na tela do B10 |
| "Talvez incidência da barrica" | B08 | ✅ como percepção | A legenda corrige "barriga" para **barrica** |
| Gamay: casca fina, fruta vermelha, acidez alta, tanino baixo | B11 | ✅ | *Wine Grapes*; Wine Folly; WSET L3 |
| Beaujolais conhecido por vinhos pouco tânicos | B11 | ✅ | idem |
| Teste da língua no céu da boca | B11 | ✅ como prática | O tanino é sentido como secura e aspereza (WSET L3). O teste em si é dela |
| "A Gamay é famosa em Borgonha… na parte sul da Borgonha" | B12 | ⚠️ | O Beaujolais costuma ser tratado como região própria, **logo ao sul** da Borgonha. A tela diz isso, sem contradizer a fala |
| Suíça também é país importante da Gamay | tela B12 | ✅ | swisswine.com: cerca de 1.000 ha, entre as tintas mais plantadas (Valais, Vaud, Genebra) |
| 1395: Filipe, o Audaz, mandou arrancar a Gamay | tela B12 | ✅ | Ordenança de 31/jul/1395 (Wine Spectator, "The Exile of Burgundy"; The Drinks Business). Na tela fica só "para proteger a Pinot Noir", sem "exilou para o Beaujolais", que é discutido |
| Gamay = Pinot Noir × Gouais Blanc, os mesmos pais da Chardonnay | tela B12 | ✅ | Bowers et al., *Science* 285 (1999) |
| Nebbiolo: rosa, alcatrão…; acidez e tanino altos | B12 | ✅ | *Wine Grapes*; WSET L3 |
| "Ela é muito complexa, por isso o Barolo é um dos principais da Itália" | B12 | ✅ como opinião | O Barolo é DOCG e referência italiana. O "por isso" é raciocínio dela |
| Tanino do Barolo é alto | B13 | ✅ | WSET L3; quiz do app |
| A adstringência se acumula de um gole para o outro; ordem do mais leve ao mais tânico | B13 | ✅ | Guinard, Pangborn & Lewis, *Am. J. Enol. Vitic.* 37:184 (1986); prática de prova WSET e de concursos |
| Gamay 12,5% = álcool médio | B10 | ✅ | SAT: médio = 11–13,9% |
| Bodega Iribarrem, Bento Gonçalves (RS), "super recomendo" | B10 | ✅ como opinião | Gabarito do app. **Sem @ até confirmar o perfil oficial** |

## O que ainda não funciona (crítica)

- **A imagem.** A câmera dela é uma janelinha de cerca de 450×600 px. Nas telas AULA e PLACAR o rosto entra num cartão de 640×480, ampliado 1,4×, no limite do que essa janela aguenta. Não dá para ampliar mais. Nas telas APP o iPad fica inteiro e a nota vai para a metade sem rosto.
- **B07 é fino** (9 s). Ela fala do Barolo quase só lendo a ficha. Se a Natalie quiser mais, a única fala boa que sobra é "É quase um médio pra mais porque ele entrega tanto nas coisas" (972–976 s). Eu deixei fora porque repete a ladainha.
- **B08 tem 45 s de nariz e cor da #107** antes da comparação. Se o ritmo pesar, saem "É um rubi. Tem uma turbidez." e "Ele tem algo também de herbáceo" (−9 s).
- **"Combinar as cores" (1270 s).** As duas transcrições ouvem "combinar", não "comparar". Mantive a palavra dela na legenda.
- **Pedidos ao app ficaram fora do vídeo** ("uma melhoria para fazer no aplicativo", "meio burro", "vou solicitar melhoria"). Destoam de quem recomenda o app e já estão na lista abaixo.

## Para o "Wine Study Lab system" (erros do app vistos neste episódio)

1. **[Alta]** #21: a nota ignora região, país, safra e teor que já estão na ficha. Por isso o placar diz "Regiões 1/2 · Países 1/2", quando deveria ser 2/3. No vídeo, a tela mostra só "67/100 · uvas 2 de 3".
2. **[Alta]** No quiz da Gamay, a **Suíça** aparece como distrator, mas é uma resposta certa.
3. **[Média]** Texto da Gamay com "século XV" e "1395" juntos. 1395 é século XIV.
4. **[Média]** #107: o cabeçalho diz "Borgonha" e o gabarito diz "Beaujolais". Falta definir uma hierarquia única.
5. **[Média]** Safra impossível sem alerta: Barolo 2024 aceito sem aviso de 38 meses.
6. **[UX]** Perguntas pelo número da garrafinha; ela pediu para não decorar números.
7. **[Feature]** Sugerir a ordem de prova (do mais leve ao mais tânico) depois do sorteio. É o pedido dela em 1748 s e a lição deste episódio.

## Pendências antes do render

- **`F_ep04.json` ainda não existe.** O lote de hesitações (`scratchpad/trans/run.sh`) está rodando o ep05 agora, depois faz o ep02 e então o ep04. Sem esse arquivo o `cleanfala` quebra. O plano só pode rodar quando o ep04 terminar.
- **Ouvir no editor**, porque a transcrição esticou palavras sobre um "ééé" ou um começo falso: "Eu dou preferência" (35–38 s), "um rubi, médio" (256–263 s, no turbo "é… uma… um rubi… é…"), "um carvalho" (485,95 s), "eu não vou colocar um Touriga" (703,95–708,7 s), "na parte sul da Borgonha" (b = 1918,98 s, colado no "Então"), "era um Gamay" (1845,88–1847,42 s).
- **Slides para a Natalie aprovar.** O deck no padrão do ep05 (`slides/bNNtK.html`) ainda precisa ser gerado a partir deste JSON. O `ferramentas/mock.py` importa `render`, `render_yt` e `pip`, que não estão em `ferramentas/`. Para as prévias de cada tela, o caminho é corrigir esses imports ou usar o `visual.py`.
