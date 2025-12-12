# Simulação de Escalonador de Processos (APS 05)
**Disciplina:** Arquitetura de Computadores e Sistemas Operacionais (CIn - UFPE)  
**Algoritmos:** Round Robin & Prioridade (Preemptivo)
---
**Alunos:**
Maria Eduarda, Maria Luísa, Willian Rupert


## 📂 Estrutura dos Arquivos

O que cada arquivo faz:

* **`main.py`**: O código fonte do simulador (Python).
* **`EntradaProcessos.txt`**: ⚠️ **Arquivo de Entrada Principal**. O programa LÊ este arquivo. Para mudar o teste, devemos colar os dados aqui dentro.
* **`SaidaResultados.txt`**: O arquivo gerado automaticamente após a execução, contendo as métricas e a linha do tempo.

### Arquivos de Teste (Para validação manual)
* **`Entrada_Teste1.txt`**: Dados do exemplo oficial do PDF (Quantum 20). Exemplo de Andson
* **`Entrada_Teste2.txt`**: Dados do caso de borda (Quantum curto e empates). Nosso exemplo
* **`TesteX_Saida_Manual.txt`**: Nossas análises manuais explicando o que acontece em cada teste.

---

## 🚀 Como Rodar

1. **Prepare o Teste:**
   Abra o arquivo `Entrada_Teste1.txt` (ou Teste2), copie o conteúdo (numérico apenas) e cole dentro do **`EntradaProcessos.txt`**. Salve o arquivo.

2. **Abra o Terminal:**
   Certifique-se de estar na pasta do projeto.

3. **Execute o Comando:**
   ```bash
   python main.py

4. **Confira o Resultado:**
5. O programa irá gerar/atualizar o arquivo SaidaResultados.txt. Abra-o para ver a linha do tempo e o cálculo do overhead.
