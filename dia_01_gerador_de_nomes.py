# Missão 1: Gerador de nomes de recursos para AWS

# 1. Usando print() para dar boas vindas
  print(" -- Gerador de nomes de recursos da AWS -- )

# 2. Usando input() para pedir informações e variáveis para armazená-las
# A resposta do input() é sempre texto (string)
    nome_do_projeto = input("Digite um nome pro projeto: ")
    ambiente = input("Digite o ambiente (ex. 'dev', 'prod', 'staging': ")
    numero_curso = input("Digite o número do recurso: ")

# 3. Usando f-string() para combinaras variáveis e criar nomes padronizados
# f-string() é a forma mais fácil de misturar texto e variável
    nome_bucket_s3 = f"{nome_do_projeto}-bucket-{ambiente}-{nume_recurso}"
    nome_instancia_ec2 = f"{nome_do_projeto}-ec2-{ambiente}-{nume_recurso}"
    nome_banco_de_dados = f"{nome_do_projeto}-db-{ambiente}-{nume_recurso}"

# 4. Exibindo resultado para usuário
    print("\n--- Nomes gerados ---")
    print(f"Nome do Bucket S3: {nome_bucket_s3}")
    print(f"Nome da Instância EC2: {nome_instancia_ec2}")
    print(f"Nome do Banco de Dados {nome_banco_de_dados}")

