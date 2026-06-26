# Comparação de Algoritmos de ML para Detecção de Malware Android

Apresentação do EP3 da disciplina **SIN5032 — Experimentação em ML Supervisionado (USP, 2026)**, com estudo empírico no dataset **TUANDROMD** para comparar classificadores em detecção de malware Android.

## Objetivo

Comparar os algoritmos **Random Forest (RF)**, **SVM**, **KNN** e **Árvore de Decisão (AD)**, avaliando:

- **F1-score**
- **AUC-ROC**
- **Significância estatística** das diferenças entre modelos (Wilcoxon pareado + Bonferroni)

## Base e protocolo experimental

- Dataset: **TUANDROMD**
- Tamanho: **4.464 instâncias**, **241 features binárias** (213 permissões + 28 APIs)
- Observações importantes:
  - **79,8%** das amostras são malware (desbalanceamento)
  - **3.802 duplicatas** no dataset
- Validação: **Stratified 10-fold CV** (`seed=42`)
- Pré-processamento: **MinMaxScaler** aplicado em SVM e KNN
- Teste estatístico: Wilcoxon pareado com correção de Bonferroni (**α = 0,0083**)

## Principais resultados

- **Random Forest** apresentou melhor desempenho:
  - **F1 = 0,9969**
  - **AUC = 0,9995**
- RF foi estatisticamente superior a SVM, KNN e AD (p ≤ 0,004).
- SVM, KNN e AD não apresentaram diferença estatística consistente entre si.

## Limitações

- Grande volume de duplicatas pode inflar métricas.
- Desbalanceamento de classes pode favorecer a classe majoritária.
- Avaliação em base única limita a generalização.
- Sem otimização extensa de hiperparâmetros (ex.: nested CV / busca ampla).

## Estrutura do repositório

- `index.html`: versão principal da apresentação
- `slides-print.html`: versão para impressão/exportação
- `apresentacaoEp3.pdf` e `ep03.pdf`: versão em PDF
- `assets/`: estilos, scripts e imagens dos slides

## Como visualizar

1. Abra o arquivo `index.html` no navegador.
2. Navegue pelos slides usando as setas na tela.

## Autor

**Fernando Pinéo de Abreu**  
Universidade de São Paulo — Nº USP: 17989742

