# Visão Computacional – Reconstrução 3D do Movimento de um Robô  
📍 *Terceiro trabalho da disciplina de Visão Computacional*  
👤 **Autores:** Breno Ferreira e Mariana Godoy
---

## 📌 Objetivo

Este projeto realiza a **reconstrução tridimensional da trajetória de um robô móvel** utilizando visão computacional multiview.  
A localização do robô é calculada usando **triangulação 3D a partir de 4 câmeras**, com rastreamento via marcador **ArUco**.

---

## 📂 Estrutura do Repositório

| Arquivo/Pasta | Descrição |
|---|---|
| `main.py` | Script principal — detecta o ArUco, triangula e plota resultados |
| `0.json, 1.json, 2.json, 3.json` | Parâmetros de calibração das câmeras |
| `aruco-examples/` | Testes e exemplos de detecção ArUco |
| `calibration-examples/` | Scripts auxiliares de calibração |
| `path-append.py / path-loop.py` | Testes de trajetória e variação do pipeline |
| `requirements.txt` | Lista de dependências para instalação |

---

## ⚙️ Funcionamento do Sistema

1. Carrega a calibração de cada câmera (intrínseca + extrínseca)
2. Lê os vídeos sincronizados (`camera-00.mp4` a `camera-03.mp4`)
3. Detecta o marcador ArUco em cada frame
4. Se ≥ 2 câmeras encontrarem o marcador → triangulação via **SVD**
5. Pontos reconstruídos são armazenados no vetor `path`
6. Gráficos são plotados ao final (3D e projeções 2D)

---

## 🛠️ Requisitos e Instalação

### Instalação (Linux)

```bash
sudo apt install virtualenv
virtualenv vision-2
source vision-2/bin/activate
pip3 install -r requirements.txt
```

🔔 **IMPORTANTE:** há um bug conhecido no OpenCV que pode exigir o uso do pacote correto indicado em `requirements.txt`.  
Recomenda-se instalar exatamente as versões fornecidas.


## ▶️ Execução

Certifique-se de que os vídeos das câmeras estão na mesma pasta do projeto.
```bash
python main.py
```

Para habilitar debug:
```bash
debug = 1
```

## 🧩 Principais Funções no Código

| Função                              | Descrição                                  |
| ----------------------------------- | ------------------------------------------ |
| `camera_parameters(file)`           | Lê calibração: matriz K + R + t            |
| `read_frame(img, ID)`               | Detecta marcador ArUco e retorna vértices  |
| `assemble_matrix(P, points, found)` | Monta matriz para triangulação             |
| `np.linalg.svd`                     | Cálculo do ponto 3D a partir das projeções |

## 📊 Resultados

O sistema produz:

- Trajetória 3D real do robô -> Gerada a partir de triangulação multi-camera

- Projeção 2D por câmera -> Valida a detecção e consistência espacial do alvo
