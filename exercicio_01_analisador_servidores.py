# Semana 1 - Missão Prática: Analisador de Servidores

# 1. OS DADOS: Nossa lista de servidores, simulando a nuvem.
inventario_servidores = [
    {'nome': 'srv-prod-db-01', 'status': 'ativo', 'ambiente': 'producao'},
    {'nome': 'srv-dev-web-01', 'status': 'ativo', 'ambiente': 'desenvolvimento'},
    {'nome': 'srv-prod-api-01', 'status': 'inativo', 'ambiente': 'producao'},
    {'nome': 'srv-staging-app-01', 'status': 'ativo', 'ambiente': 'staging'},
    {'nome': 'srv-prod-web-02', 'status': 'ativo', 'ambiente': 'producao'},
    {'nome': 'srv-dev-db-01', 'status': 'inativo', 'ambiente': 'desenvolvimento'},
]

# 2. A FERRAMENTA: Uma função para guardar e reutilizar lógica de filtro.
def encontrar_servidores_criticos(inventario):
    """
    Recebe uma lista de servidores (dicionários) e retorna uma nova lista
    apenas com os nomes dos servidores que são de 'producao' e estão 'ativos'.
    """
    servidores_criticos_encontrados = [] # Lista vazia para guardar os resultados.

    # 3. A LÓGICA: Um 'for loop' para checar cada item e um 'if' para decidir.
    for servidor in inventario:
        # A condição do if é o nosso filtro.
        if servidor['ambiente'] == 'producao' and servidor['status'] == 'ativo':
            # Se um servidor passa no filtro, adicionamos seu nome à lista de resultados.
            servidores_criticos_encontrados.append(servidor['nome'])

    return servidores_criticos_encontrados


# --- EXECUÇÃO DO SCRIPT ---

# 4. A AÇÃO: Usamos a ferramenta, passando os dados para ela.
servidores_para_monitorar = encontrar_servidores_criticos(inventario_servidores)

# 5. O RESULTADO: Exibe de forma clara.
print("--- Relatório de Monitoramento ---")
print("Servidores de produção atualmente ativos:")
print(servidores_para_monitorar)
