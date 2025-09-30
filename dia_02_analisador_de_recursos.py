# Missão Dia 2: Analisador de Servidores EC2

print("--- Analisador de Servidores EC2 ---")

## 1. Simulando dados da AWS> Uma lista de dicionários
### Cada dicionário representa um servidor (uma instância EC2)

servidores = [
    {'id': 'i-12345', 'estado': 'rodando', 'tipo': 't2.micro'},
    {'id': 'i-67890', 'estado': 'parado', 'tipo': 't3.large'},
    {'id': 'i-abcde', 'estado': 'rodando', 'tipo': 't2.micro'},
    {'id': 'i-fghij', 'estado': 'terminado', 'tipo': 'm5.xlarge'},
    {'id': 'i-klmno', 'estado': 'rodando', 'tipo': 't3.large'}
]
  

### 2. Usando um 'for loop' para passar por cada servidor na lista

for servidor in servidores:
  print(f"\nAnalisando servidor ID: {servidor['id']}") 

### 3. Usando if/else/elif para tomar decisões baseadas no estado do servidor identificado

if servidor ['estado'] == 'rodando': 
  print(f" - AVISO: O servidor do tipo {servidor['tipo']} está LIGADO.")
elif servidor ['estado' == 'parado':
  print(f" - INFO: O servidor está DESLIGADO. Nenhuma ação é necessária.")
else:
  print(f" - CRÍTICO: O servidor está no estado '{servidor['estado']}. Requer atenção!")

