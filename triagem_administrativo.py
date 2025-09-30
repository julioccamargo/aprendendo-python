# --- 1. Importações ---
import fitz
import docx
import ezodf
import pandas as pd
import re
from pathlib import Path
from datetime import date
import spacy
import hashlib

# --- 2. Definições, Critérios e Modelos ---
print("Carregando modelo de NLP (spaCy)... Isso pode levar um momento.")
nlp = spacy.load("pt_core_news_lg")
print("Modelo carregado.")

CRITERIOS = {
    'obrigatorios': {
        ' rotinas administrativas': 15, ' faturamento': 10, ' nota fiscal': 10,
        ' planilhas': 8, ' atendimento': 8, ' boleto': 5,
    },
    'desejaveis': {
        ' pós-vendas': 5, ' sefaz': 4, ' compra de materiais': 3, ' correspondências': 3,
    }
}

PALAVRAS_CHAVE_SUPERIOR = [
    'graduação', 'graduado', 'graduada', 'bacharel', 'bacharelado', 'licenciatura',
    'tecnólogo', 'superior completo', 'ensino superior', 'universidade', 'faculdade',
    'ciências contábeis', 'administração'
]

# --- 3. Configuração de Caminhos ---
DIRETORIO_ATUAL = Path(__file__).parent
PASTA_CURRICULOS = DIRETORIO_ATUAL / "curriculos_administrativo"
ARQUIVO_SAIDA_EXCEL = DIRETORIO_ATUAL / "Resultado_Triagem_ADMINISTRATIVO.xlsx"
ARQUIVO_HASHES = DIRETORIO_ATUAL / "hashes_processados.txt"

# --- 4. Funções Auxiliares ---
def calcular_hash_arquivo(caminho_arquivo):
    sha256 = hashlib.sha256()
    try:
        with open(caminho_arquivo, 'rb') as f:
            while bloco := f.read(8192):
                sha256.update(bloco)
        return sha256.hexdigest()
    except IOError:
        return None

def carregar_hashes_processados(caminho_arquivo_hashes):
    if not caminho_arquivo_hashes.exists():
        return set()
    with open(caminho_arquivo_hashes, 'r') as f:
        return set(line.strip() for line in f)

def salvar_hash_processado(caminho_arquivo_hashes, hash_valor):
    with open(caminho_arquivo_hashes, 'a') as f:
        f.write(hash_valor + '\n')

def extrair_texto_pdf(caminho_arquivo):
    try:
        with fitz.open(caminho_arquivo) as doc: return "".join(p.get_text() for p in doc)
    except Exception: return ""

def extrair_texto_docx(caminho_arquivo):
    try:
        doc = docx.Document(caminho_arquivo)
        return "\n".join(p.text for p in doc.paragraphs)
    except Exception: return ""

def extrair_texto_odt(caminho_arquivo):
    try:
        doc = ezodf.opendoc(str(caminho_arquivo))
        return "\n".join(str(p) for p in doc.body.getElementsByType(ezodf.text.P))
    except Exception: return ""

def extrair_nome_candidato(texto, nome_arquivo, nlp_model):
    doc = nlp_model(texto[:1000])
    for ent in doc.ents:
        if ent.label_ == 'PER': return ent.text.strip().title()
    
    nome_limpo = Path(nome_arquivo).stem.lower().replace('curriculo', '').replace('cv', '').strip()
    return re.sub(r'[\d_-]', ' ', nome_limpo).strip().title() or "Nome não encontrado"

def verificar_curso_superior(texto_lower, palavras_chave):
    return "Sim" if any(p in texto_lower for p in palavras_chave) else "Não"

def calcular_experiencia_total(texto):
    padrao = re.compile(r'\((\d{1,2})\s?[/.-]\s?(\d{4})\s*-\s*(\d{1,2})\s?[/.-]\s?(\d{4})\)|'
                        r'\((\d{1,2})\s?[/.-]\s?(\d{4})\s*-\s*(o momento|atual|presente)\)', re.IGNORECASE)
    matches, total_meses, data_atual = padrao.findall(texto), 0, date.today()
    for match in matches:
        try:
            if match[5]:
                mes_inicio, ano_inicio, data_fim = int(match[4]), int(match[5]), data_atual
            else:
                mes_inicio, ano_inicio, mes_fim, ano_fim = map(int, match[:4])
                data_fim = date(ano_fim, mes_fim, 1)
            data_inicio = date(ano_inicio, mes_inicio, 1)
            total_meses += (data_fim.year - data_inicio.year) * 12 + (data_fim.month - data_inicio.month) + 1
        except (ValueError, IndexError): continue
    if total_meses == 0: return "Não especificado", 0
    anos, meses = divmod(total_meses, 12)
    texto_exp = []
    if anos > 0: texto_exp.append(f"{anos} ano{'s' if anos > 1 else ''}")
    if meses > 0: texto_exp.append(f"{meses} mês{'meses' if meses > 1 else ''}")
    return " e ".join(texto_exp), total_meses

# --- 5. Lógica Principal de Processamento ---
hashes_processados = carregar_hashes_processados(ARQUIVO_HASHES)
resultados_finais = []

if not PASTA_CURRICULOS.exists():
    print(f"[ERRO] A pasta de currículos '{PASTA_CURRICULOS}' não foi encontrada.")
    exit()

for arquivo_cv in PASTA_CURRICULOS.iterdir():
    if not arquivo_cv.is_file(): continue

    hash_atual = calcular_hash_arquivo(arquivo_cv)
    if not hash_atual or hash_atual in hashes_processados:
        if hash_atual: print(f"Arquivo duplicado, ignorando: {arquivo_cv.name}")
        continue
    
    texto_cv = ""
    if arquivo_cv.suffix == '.pdf': texto_cv = extrair_texto_pdf(arquivo_cv)
    elif arquivo_cv.suffix == '.docx': texto_cv = extrair_texto_docx(arquivo_cv)
    elif arquivo_cv.suffix == '.odt': texto_cv = extrair_texto_odt(arquivo_cv)
    else: continue

    if not texto_cv: continue

    nome_candidato = extrair_nome_candidato(texto_cv, arquivo_cv.name, nlp)
    texto_cv_lower, pontuacao, habilidades_encontradas = texto_cv.lower(), 0, []

    todos_criterios = {**CRITERIOS['obrigatorios'], **CRITERIOS['desejaveis']}
    for habilidade, pontos in todos_criterios.items():
        if habilidade.lower() in texto_cv_lower:
            pontuacao += pontos
            habilidades_encontradas.append(habilidade.strip())

    tempo_experiencia_texto, total_meses_exp = calcular_experiencia_total(texto_cv)
    if total_meses_exp >= 12: pontuacao += 5
    if total_meses_exp >= 36: pontuacao += 10

    tem_superior = verificar_curso_superior(texto_cv_lower, PALAVRAS_CHAVE_SUPERIOR)
    padrao_emprego_atual = r'-\s*(o momento|atual|presente|hoje)\b'
    empregado_atualmente = "Sim" if re.search(padrao_emprego_atual, texto_cv_lower, re.IGNORECASE) else "Não"
    email = re.search(r'[\w\.-]+@[\w\.-]+', texto_cv)
    telefone = re.search(r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}', texto_cv)

    resultados_finais.append({
        'Arquivo': arquivo_cv.name, 'Nome do Candidato': nome_candidato, 'Pontuação': pontuacao,
        'Empregado Atualmente': empregado_atualmente, 'Curso Superior': tem_superior,
        'Tempo de Experiência': tempo_experiencia_texto, 'Habilidades': ", ".join(habilidades_encontradas),
        'Email': email.group(0) if email else "Não encontrado",
        'Telefone': telefone.group(0) if telefone else "Não encontrado",
    })
    
    salvar_hash_processado(ARQUIVO_HASHES, hash_atual)
    hashes_processados.add(hash_atual)
    print(f"Processado: {arquivo_cv.name} | Candidato: {nome_candidato}")

# --- 6. Geração do Relatório em Excel ---
if resultados_finais:
    df_resultados = pd.DataFrame(resultados_finais)
    colunas_ordenadas = ['Arquivo', 'Nome do Candidato', 'Pontuação', 'Empregado Atualmente', 'Curso Superior',
                         'Tempo de Experiência', 'Habilidades', 'Email', 'Telefone']
    df_resultados = df_resultados[colunas_ordenadas]
    df_resultados = df_resultados.sort_values(by='Pontuação', ascending=False)
    
    try:
        df_resultados.to_excel(ARQUIVO_SAIDA_EXCEL, index=False)
        print(f"\n[SUCESSO] Triagem finalizada. {len(resultados_finais)} novos currículos processados.")
    except Exception as e:
        print(f"\n[ERRO] Não foi possível salvar o arquivo Excel. Erro: {e}")
else:
    print("\n[AVISO] Nenhum currículo novo foi encontrado para processar.")
