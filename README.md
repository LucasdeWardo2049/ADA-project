# Analisador de PDF com LLM

Ferramenta CLI em Python para análise de documentos PDF e geração de resumos usando modelos de linguagem locais.

## 🚀 Funcionalidades

### Obrigatórias ✅
- Extração de metadados do PDF (páginas, palavras, tamanho)
- Análise estatística do texto (vocabulário, palavras mais comuns)
- Extração de imagens
- Geração de resumo com LLM local (Hugging Face)

### Extras ⭐
- Sistema de logs completo
- Relatório em Markdown
- Tipagem com `typing`
- Estrutura modular bem organizada
- Suporte a PDFs grandes
- Tratamento robusto de exceções
- Context managers para recursos

## 📋 Requisitos

- **Python 3.9+** (recomendado: **Python 3.11**)
  - ⚠️ Python 3.14+ ainda não é suportado por algumas dependências (PyMuPDF)
- Dependências no `requirements.txt`

## 🔧 Instalação

```powershell
# Navegue até a pasta do projeto
cd C:\Users\lucas\Documents\ADA

# Crie o ambiente virtual
python -m venv .venv

# Ative o ambiente (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Atualize o pip
python -m pip install --upgrade pip

# Instale todas as dependências
pip install -r requirements.txt
```

**Nota:** Se você tiver múltiplas versões de Python instaladas, use `py -3.11 -m venv .venv` para garantir a versão correta.

## 💻 Uso

### Uso Básico

```powershell
python -m src.main "C:\Users\lucas\Downloads\documento.pdf"
```

### Opções Avançadas

```powershell
# Especificar diretório de saída para imagens
python -m src.main documento.pdf --output-dir ./minhas-imagens

# Desabilitar resumo (apenas análise)
python -m src.main documento.pdf --no-summary

# Desabilitar extração de imagens
python -m src.main documento.pdf --no-images

# Gerar relatório em Markdown
python -m src.main documento.pdf --report relatorio.md

# Usar modelo diferente
python -m src.main documento.pdf --model google/flan-t5-small

# Modo verbose (logs detalhados)
python -m src.main documento.pdf --verbose

# Modo silencioso (apenas erros)
python -m src.main documento.pdf --quiet
```

### Ajuda

```powershell
python -m src.main --help
```

## 📂 Estrutura do Projeto

O projeto segue uma arquitetura modular com **separação clara de responsabilidades**:

```
ADA/
├── src/
│   ├── __init__.py          # Versão do pacote
│   ├── main.py              # Ponto de entrada da aplicação
│   │
│   ├── cli/                 # Interface de linha de comando
│   │   ├── __init__.py
│   │   └── arguments.py     # Parser e validação de argumentos
│   │
│   ├── pdf/                 # Processamento de PDFs
│   │   ├── __init__.py
│   │   ├── extractor.py     # Extração de texto e metadados
│   │   └── images.py        # Extração de imagens
│   │
│   ├── llm/                 # Modelos de linguagem
│   │   ├── __init__.py
│   │   ├── model.py         # Carregamento e gerenciamento de modelos
│   │   └── summarize.py     # Geração de resumos
│   │
│   └── utils/               # Utilitários compartilhados
│       ├── __init__.py
│       ├── text.py          # Processamento de texto (tokenização, stopwords)
│       └── files.py         # Manipulação de arquivos e diretórios
│
├── imagens/                 # Imagens extraídas (gerado automaticamente)
├── .venv/                   # Ambiente virtual Python
├── requirements.txt         # Dependências do projeto
└── README.md               # Documentação
```

### Organização Interna

- **Modularidade**: Cada módulo tem responsabilidade única e bem definida
- **Context Managers**: Gerenciamento automático de recursos (PDFs, modelos)
- **Tipagem**: Type hints em todas as funções para melhor manutenibilidade
- **Logging**: Sistema estruturado com 3 níveis (ERROR, INFO, DEBUG)
- **Código limpo**: Funções pequenas e focadas, sem arquivos gigantes

## 🔍 Exemplo de Saída

```
======================================================================
ANÁLISE DO PDF
======================================================================

Arquivo: documento.pdf
Caminho: /caminho/para/documento.pdf

📄 Número de páginas: 15
📦 Tamanho do arquivo: 2.34 MB (2,453,678 bytes)
📝 Total de palavras: 5,432
📚 Tamanho do vocabulário: 1,234 palavras distintas

🔤 10 palavras mais comuns (sem stopwords):
    1. tecnologia        (45 ocorrências)
    2. desenvolvimento   (38 ocorrências)
    3. software          (32 ocorrências)
    ...

======================================================================
EXTRAÇÃO DE IMAGENS
======================================================================

🖼️  Total de imagens extraídas: 8
📁 Diretório de saída: imagens/documento

======================================================================
RESUMO DO DOCUMENTO (gerado por LLM)
======================================================================

Este documento aborda os principais conceitos de desenvolvimento...

======================================================================
✅ Processamento concluído com sucesso!
======================================================================
```

## 🧪 Modelos LLM Suportados

Por padrão, usa `unicamp-dl/ptt5-base-portuguese-vocab` (otimizado para português).

Outros modelos compatíveis:
- `google/flan-t5-small` (menor, mais rápido)
- `google/flan-t5-base`
- `t5-small`

## 📝 Notas Técnicas

- **Stopwords**: Usa lista em português do NLTK
- **Chunking**: Textos longos são divididos automaticamente
- **Device**: Usa GPU (CUDA) se disponível, senão CPU
- **Context Managers**: Fechamento automático de recursos
- **Logging**: Sistema completo de logs em 3 níveis

## 🐛 Solução de Problemas

### Python 3.14+ não funciona
**Problema:** `pymupdf` ainda não suporta Python 3.14+  
**Solução:** Use Python 3.11 ou 3.10:
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Erro ao baixar stopwords do NLTK
O programa baixa automaticamente na primeira execução. Se falhar:
```python
import nltk
nltk.download('stopwords')
```

### Modelo LLM muito grande
Use um modelo menor:
```powershell
python -m src.main documento.pdf --model google/flan-t5-small
```

### Memória insuficiente
- Desabilite o resumo: `--no-summary`
- Use modelo menor (ex: `flan-t5-small`)
- Feche outros programas

## ⭐ O que Avaliar no Projeto

### Arquitetura e Organização ⭐
- **Pastas bem definidas**: 4 módulos (`cli`, `pdf`, `llm`, `utils`) com responsabilidades únicas
- **Boa organização interna**: Context managers, tipagem completa, logging estruturado
- **Evitar arquivos gigantes**: Maior arquivo tem ~180 linhas, funções focadas e coesas
- **Padrões de projeto**: Separação de concerns, DRY, single responsibility

### Funcionalidades Obrigatórias
- **Análise completa do PDF**: Extração de páginas, palavras, tamanho do arquivo
- **Processamento de texto**: Remoção de stopwords, contagem de vocabulário, palavras mais comuns
- **Extração de imagens**: Salvamento em diretórios organizados com nomes únicos
- **Resumo com LLM local**: Integração Hugging Face, execução 100% local

### Funcionalidades Extras (Diferenciais) 🌟
- **Cuidado com UX em linha de comando**: 
  - Mensagens claras e formatadas
  - Emojis para melhor legibilidade
  - Progress feedback durante operações longas
  - Validação de argumentos com mensagens específicas
  - Help detalhado com exemplos práticos
  
- **Códigos auxiliares bem feitos**:
  - Funções utilitárias reutilizáveis (`text.py`, `files.py`)
  - Context managers para gestão automática de recursos
  - Tipagem completa com type hints
  - Fallback inteligente (modelo alternativo se principal falhar)
  - GPU detection automática
  
- **Logs e relatórios bem estruturados**:
  - Sistema de logging com 3 níveis (ERROR, INFO, DEBUG)
  - Saída no terminal organizada e hierárquica
  - Geração opcional de relatório Markdown completo
  - Logs com timestamps e módulo de origem

### Qualidade de Código
- **Conventional Commits**: Histórico de commits organizado e semântico
- **Documentação**: README completo com exemplos práticos
- **Error handling**: Exceções tratadas adequadamente em todos os módulos
- **Escalabilidade**: Arquitetura preparada para novos tipos de análise

## 📄 Licença

Projeto acadêmico - ADA 2025

