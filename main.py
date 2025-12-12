# ==============================================================================
# VERSÃO CORRIGIDA E ROBUSTA (SEM IMPORTS)
# ==============================================================================

def ler_arquivo(nome_arquivo):
    dados_brutos = []
    try:
        with open(nome_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()
            
        # Remove linhas vazias se houver
        linhas = [l.strip() for l in linhas if l.strip()]

        if not linhas:
            print("ERRO: O arquivo está vazio!")
            return None, None

        cabecalho = linhas[0].split(',')
        config = {
            'n_proc': int(cabecalho[0]),
            'quantum': int(cabecalho[1]),
            't_troca': int(cabecalho[2])
        }

        for i in range(1, len(linhas)):
            partes = linhas[i].split(',')
            if len(partes) < 4: continue # Pula linhas incompletas
            p = {
                'id': int(partes[0]),
                'chegada': int(partes[1]),
                'prioridade': int(partes[2]),
                'tempo_total': int(partes[3])
            }
            dados_brutos.append(p)
            
        # Ordena por Chegada (e desempata por ID)
        dados_brutos.sort(key=lambda x: (x['chegada'], x['id']))
        return dados_brutos, config

    except FileNotFoundError:
        print("ERRO: Arquivo não encontrado.")
        return None, None
    except ValueError:
        print("ERRO: O arquivo contém letras onde deveria haver números.")
        return None, None

def criar_copia_limpa(lista_original):
    """Cria cópia segura para reiniciar a simulação"""
    nova = []
    for p in lista_original:
        nova.append({
            'id': p['id'],
            'chegada': p['chegada'],
            'prioridade': p['prioridade'],
            'tempo_total': p['tempo_total'],
            'tempo_restante': p['tempo_total'],
            'tempo_fim': 0
        })
    return nova

# ==============================================================================
# ALGORITMO ROUND ROBIN (Lógica de Ponteiro Segura)
# ==============================================================================
def round_robin(dados_originais, quantum, t_troca):
    processos = criar_copia_limpa(dados_originais)
    n_procs = len(processos)
    
    tempo = 0
    fila = []
    timeline = []
    concluidos = 0
    
    # Ponteiro para saber qual o próximo processo a entrar na fila
    idx_chegada = 0 
    
    proc_atual = None
    tempo_no_quantum = 0
    
    # Debug de segurança (para não travar o PC se algo der muito errado)
    while concluidos < n_procs and tempo < 10000: 
        
        # 1. Verifica quem chegou (até o tempo atual)
        while idx_chegada < n_procs and processos[idx_chegada]['chegada'] <= tempo:
            fila.append(processos[idx_chegada])
            idx_chegada += 1

        # 2. Se CPU vazia, tenta pegar processo
        if proc_atual is None:
            if len(fila) > 0:
                proc_atual = fila.pop(0)
                tempo_no_quantum = 0
            else:
                timeline.append("Ocioso")
                tempo += 1
                continue

        # 3. Executa
        proc_atual['tempo_restante'] -= 1
        tempo_no_quantum += 1
        timeline.append(f"P{proc_atual['id']}")
        tempo += 1

        # 4. Verifica se acabou o processo
        if proc_atual['tempo_restante'] == 0:
            proc_atual['tempo_fim'] = tempo
            concluidos += 1
            proc_atual = None
            
            # Troca de contexto (apenas se ainda faltam processos para terminar)
            if concluidos < n_procs:
                if t_troca > 0:
                    for _ in range(t_troca):
                        timeline.append("Escalonador")
                        tempo += 1
                        # Checa chegadas durante a troca
                        while idx_chegada < n_procs and processos[idx_chegada]['chegada'] <= tempo:
                            fila.append(processos[idx_chegada])
                            idx_chegada += 1
                            
        # 5. Verifica Quantum (Preempção)
        elif tempo_no_quantum == quantum:
            fila.append(proc_atual) # Volta pra fila
            proc_atual = None
            
            # Troca de contexto
            if t_troca > 0:
                for _ in range(t_troca):
                    timeline.append("Escalonador")
                    tempo += 1
                    # Checa chegadas durante a troca
                    while idx_chegada < n_procs and processos[idx_chegada]['chegada'] <= tempo:
                        fila.append(processos[idx_chegada])
                        idx_chegada += 1

    return timeline, processos, tempo

# ==============================================================================
# ALGORITMO PRIORIDADE (Lógica de Ponteiro Segura)
# ==============================================================================
def prioridade(dados_originais, t_troca):
    processos = criar_copia_limpa(dados_originais)
    n_procs = len(processos)
    
    tempo = 0
    fila = []
    timeline = []
    concluidos = 0
    idx_chegada = 0
    
    proc_atual = None
    
    while concluidos < n_procs and tempo < 10000:
        
        chegou_novo = False
        # 1. Checagem de Chegada
        while idx_chegada < n_procs and processos[idx_chegada]['chegada'] <= tempo:
            fila.append(processos[idx_chegada])
            idx_chegada += 1
            chegou_novo = True
            
        if chegou_novo:
            # Ordena: Menor Prioridade Numérica primeiro, depois Menor ID
            fila.sort(key=lambda p: (p['prioridade'], p['id']))

        # 2. Verifica Preempção (Se o da fila é mais importante que o atual)
        if proc_atual is not None and len(fila) > 0:
            if fila[0]['prioridade'] < proc_atual['prioridade']:
                fila.append(proc_atual) # Devolve atual
                proc_atual = None
                
                # Custo de troca
                if t_troca > 0:
                    for _ in range(t_troca):
                        timeline.append("Escalonador")
                        tempo += 1
                        # Checa chegadas durante a troca
                        while idx_chegada < n_procs and processos[idx_chegada]['chegada'] <= tempo:
                             fila.append(processos[idx_chegada])
                             idx_chegada += 1
                    
                fila.sort(key=lambda p: (p['prioridade'], p['id']))

        # 3. Seleção
        if proc_atual is None:
            if len(fila) > 0:
                proc_atual = fila.pop(0)
            else:
                timeline.append("Ocioso")
                tempo += 1
                continue

        # 4. Executa
        proc_atual['tempo_restante'] -= 1
        timeline.append(f"P{proc_atual['id']}")
        tempo += 1

        # 5. Verifica Fim
        if proc_atual['tempo_restante'] == 0:
            proc_atual['tempo_fim'] = tempo
            concluidos += 1
            proc_atual = None
            
            if concluidos < n_procs:
                if t_troca > 0:
                    for _ in range(t_troca):
                        timeline.append("Escalonador")
                        tempo += 1
                        # Checa chegadas
                        while idx_chegada < n_procs and processos[idx_chegada]['chegada'] <= tempo:
                             fila.append(processos[idx_chegada])
                             idx_chegada += 1

    return timeline, processos, tempo

# ==============================================================================
# GERAÇÃO DO ARQUIVO
# ==============================================================================
def formatar_saida(nome, timeline, processos, config, total_tempo):
    # Turnaround
    soma = sum([p['tempo_fim'] - p['chegada'] for p in processos])
    media = soma / len(processos)
    
    # Overhead
    trocas = timeline.count("Escalonador")
    overhead = (trocas * config['t_troca']) / total_tempo if total_tempo > 0 else 0
    
    # Linha do Tempo Visual
    visual = ""
    if timeline:
        atual = timeline[0]
        inicio = 0
        for i in range(1, len(timeline)):
            if timeline[i] != atual:
                visual += f"[{inicio}-{i}: {atual}] -> "
                atual = timeline[i]
                inicio = i
        visual += f"[{inicio}-{len(timeline)}: {atual}]"
    
    txt = f"--- {nome} ---\n"
    txt += f"Tempo médio de retorno: {media:.2f}\n"
    txt += f"Número de chaveamento de processos: {trocas}\n"
    txt += f"Overhead: {overhead:.4f} ({overhead*100:.2f}%)\n"
    txt += f"Tempo total para executar: {total_tempo}\n"
    txt += f"Linha do tempo:\n{visual}\n\n"
    return txt

def main():
    print("Iniciando simulador...")
    dados, config = ler_arquivo('EntradaProcessos.txt')
    
    if not dados:
        return # Para se deu erro na leitura

    print(f"Lido {len(dados)} processos. Rodando algoritmos...")

    # Round Robin
    tl_rr, procs_rr, tempo_rr = round_robin(dados, config['quantum'], config['t_troca'])
    out_rr = formatar_saida("Round Robin", tl_rr, procs_rr, config, tempo_rr)

    # Prioridade
    tl_prio, procs_prio, tempo_prio = prioridade(dados, config['t_troca'])
    out_prio = formatar_saida("Prioridade", tl_prio, procs_prio, config, tempo_prio)

    final = out_rr + ("="*50 + "\n\n") + out_prio
    
    with open('SaidaResultados.txt', 'w') as f:
        f.write(final)
        
    print("---------------------------------------------------")
    print("SUCESSO! Resultados salvos em 'SaidaResultados.txt'")
    print("---------------------------------------------------")
    # Mostra no terminal também
    print(final)

if __name__ == "__main__":
    main()