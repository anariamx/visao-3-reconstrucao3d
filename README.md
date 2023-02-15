# visao-3-reconstrucao3d
Reconstrução da posição 3D durante o movimento de um robô móvel

# Dúvidas
- Como usar a distorção radial, que é uma das saídas de 'parametros.py'?

## Estrutura:
- assets: Arquivos grande demais para o Github. Necessários ao programa.
	- Vídeos das 4 câmeras
- calibrate: Dados de calibração das 4 câmeras e rotina de leitura
- aruco: Rotinas auxiliares para detecção de ArUco
## Instruções de Instalação (Linux)
```
sudo apt install virtualenv
virtualenv vision-2
source vision-2/bin/activate
pip3 install -r requirements.txt 
```
## ATENÇÃO - MUITO IMPORTANTE
Nos arquivos .json que contém os dados de calibração das câmeras do espaço inteligente, a matriz de rotação e translação que representam os parâmetros extrínsecos representam a transformação [R,T] que converte do referencial da câmera para o mundo.
Para resolver o trabalho, de acordo com o modelo de projeção pinhole, vocês precisam da transformação que converte do mundo para a câmera, ou seja, do inverso da matriz fornecida. Então..... ATENÇÃO!!!!!

Vocês devem extrair os dados de R e T, montar a matriz de transformação geométrica e invertê-la antes de usar.
Depois de inverter, a matrix representa a transformação que converte do mundo para a câmera, ou seja, o R e T que vocês precisam. 

Outro detalhe importante, filtrem as detecções de ArUco para o ID = 0 (zero), pois às vezes ocorre a detecção de outros IDs e isso pode causar problemas para vocês.

## Proposta do trabalho
> Neste trabalho vocês deverão detectar o robô nos vídeos das 4 câmeras do espaço inteligente e obter a reconstrução da sua posição 3D no mundo. Feito isso, vocês deverão gerar um gráfico da posição do robô, mostrando a trajetória que ele realizou.

Para detectar o robô será usado um marcador ARUCO acoplado a sua plataforma. Rotinas de detecção desse tipo de marcador poderão ser usadas para obter sua posição central, assim como as suas quinas nas imagens. Essas informações, juntamente com os dados de calibração das câmeras, poderão ser usadas para localização 3D do robô.

Informações a serem consideradas:

- Só é necessário a reconstrução do ponto central do robô (ou suas quinas, se vocês acharem melhor). Para isso, vocês podem usar o método explicado no artigo fornecido como material adicional ou nos slides que discutimos em sala de aula.

- O robô está identificado por um marcador do tipo ARUCO - Código ID 0 (zero) - Tamanho 30 x 30 cm

- Os vídeos estão sincronizados para garantir que a cada quadro vocês estarão processando imagens do robô capturadas no mesmo instante.

- A calibração das câmeras é fornecida em 4 arquivos no formato JSON (Para saber como ler os dados, basta procurar no Google).

- Rotinas de detecção dos marcadores Aruco em imagens e vídeo são fornecidas logo abaixo.

ATENÇÃO: Existem rotinas de detecção de ARUCO que já fornecem sua localização e orientação 3D, se a calibração da câmera e o tamanho do padrão forem fornecidas. Essas rotinas poderão ser usadas para fazer comparações com a reconstrução 3D fornecida pelo trabalho de vocês, mas não serão aceitas como o trabalho a ser feito. Portanto, lembrem-se que vocês deverão desenvolver a rotina de reconstrução, a partir da detecção do ARUCO acoplado ao robô nas imagens 2D capturadas nos vídeos.
