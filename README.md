# CorridaRealidadeAumentada

Projeto de TCC que envolve um jogo de corrida que utiliza imagens de pistas desenhadas em um quadro branco e um projetor para projetar o carro do player e um oponente npc em cima dos desenhos feitos na vida real.

+ Atualizações no github serão esparsas visto que é um projeto de apenas 1 integrante e quase todo o desenvolvimento já foi feito no período de férias. Alguns pequenos ajustes e melhorias de qualidade são esperados para o futuro.

+ As Mecânicas relacionadas a movimentação dos carros, assets e outros elementos de jogo foram utilizadas (com diversas modificações e adaptações) do projeto [Pygame-Car-Racer](https://github.com/techwithtim/Pygame-Car-Racer) feito por [Tim Ruscica](https://github.com/techwithtim).

+ Há algumas imagens e scripts de versões anteriores do projeto que já não tem mais relevância atualmente. A exclusão e potencialmente a renomeação dos arquivos **será** feita futuramente.

Breve descrição do funcionamento do jogo :


1. É capturada uma imagem de uma pista desenhada em um quadro branco ( melhor exemplo é este [arquivo](pictures/IMG_20240419_134307~2.jpg) ).
2. A imagem é redimensionada para a resolução HD (1280 x 720 px)
3. Um filtro gaussiano é aplicado (redução de ruído) e, em seguida, é aplicado um filtro de sobel para detecção das bordas da pista que será salva em um arquivo
4. A região interna da pista é preenchida, dilatada e esqueletonizada para a obtenção do caminho central que será percorrido pelo oponente npc (também será salvo em um arquivo).
5. A posição da linha de chegada é definida pelo clique do mouse em cima da imagem da borda da pista gerada.
6. Usando o passo anterior e os arquivos gerados, o jogo é iniciado.

+ É importante ressaltar que o jogo é iniciado em tela cheia e o monitor deve ser espelhado com o projetor. A correspondência com a projeção da pista com o desenho da mesma deve ser feita de forma manual (ao afastar ou aproximar o projetor, mudando suas configurações, etc).