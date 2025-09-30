# Missão Dia 3: Módulo de Inventário AWS

# 1. Importando uma biblioteca. Conceito de 'import'

import datetime

# 2. Criando uma função reutilizável.

def analisar_servidores_aws(lista_de_servidores):
    """
    Esta função analisa uma lista de servidores e retorna um relatório.
    """
    print("- Iniciando Análise de Servidores -")
    servidores_ligados = 0
    
    for servidor in lista_de_servidores:
        if servidor['estado'] == 'rodando':
            print(f"  - AVISO: Servidor {servidor['id']} está LIGADO.")
            servidores_ligados = servidores_ligados + 1
    
    # 3. A função 'retorna' um resultado.
    return servidores_ligados


# --- Início do Script ---

# Dados que poderiam vir de uma chamada real à AWS.
meu_inventario_ec2 = [
    {'id': 'i-12345', 'estado': 'rodando', 'tipo': 't2.micro'},
    {'id': 'i-67890', 'estado': 'parado', 'tipo': 't3.large'},
    {'id': 'i-abcde', 'estado': 'rodando', 'tipo': 't2.micro'}
]

# Chamando nossa função e passando os dados para ela.
total_ligados = analisar_servidores_aws(meu_inventario_ec2)

# Usando o resultado
print("\n--- Relatório Final ---")
print(f"Data da análise: {datetime.date.today()}")
print(f"Total de servidores ligados: {total_ligados}")
