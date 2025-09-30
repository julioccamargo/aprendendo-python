# Aqui você encontra meus exercícios do aprendizado de Python focado em Cloud Computing

## Separei em 3 dias para dar os primeiros passos:

* [Dia 1](https://github.com/julioccamargo/aprendendo-python/blob/main/dia_01_gerador_de_nomes.py)
* [Dia 2](https://github.com/julioccamargo/aprendendo-python/blob/main/dia_02_analisador_de_recursos.py)
* [Dia 3](https://github.com/julioccamargo/aprendendo-python/blob/main/dia_03_inventario_aws.py)


## Projeto real aplicado no trabalho
### Enquanto trabalhava no Grupo COMAK foram abertas vagas e o RH recebeu muitos candidatos, para melhorar a triagem criamos um filtro (parecido com ATS) para rankear os proponentes. Segue abaixo os códigos que geravam planilhas de acordo com os itens que o RH sugeriu para pontuar um candidato:

#### Exemplo: Vaga Vendedor de E-Commerce onde os critérios foram selecionados conforme o código abaixo escrito em Python3:

``` CRITERIOS = {
    'obrigatorios': {
        ' peças agrícolas': 15, ' vendas': 10, ' e-commerce': 10,
        ' ecommerce': 10, ' cotação': 8, ' orçamento': 8, ' atendimento online': 5,
    },
    'desejaveis': {
        ' magento': 15, ' pós-vendas': 5, ' pós vendas': 5, ' whatsapp': 3, ' chat': 3,
    }
}
```

#### Com isso geramos scripts para cada vaga, com características diferentes e identificação de palavras chave. Foram geradas colunas comuns entre todos: Nome do arquivo enviado, Nome, Telefone e E-mail

```resultados_finais.append({
        'Arquivo': arquivo_cv.name, 'Nome do Candidato': nome_candidato, 'Pontuação': pontuacao,
        'Empregado Atualmente': empregado_atualmente, 'Curso Superior': tem_superior,
        'Tempo de Experiência': tempo_experiencia_texto, 'Habilidades': ", ".join(habilidades_encontradas),
        'Email': email.group(0) if email else "Não encontrado",
        'Telefone': telefone.group(0) if telefone else "Não encontrado",
    })
```

    
#### Também foram levadas em consideração possíveis duplicações, lemos arquivos nos principais formatos: .doc, .docx, .pdf, .odt
