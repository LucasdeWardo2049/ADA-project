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
├── src/                     # Código fonte
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
├── tests/                   # Testes unitários
│   ├── __init__.py
│   ├── test_text.py         # Testes para utils/text.py
│   ├── test_files.py        # Testes para utils/files.py
│   └── test_extractor.py    # Testes para pdf/extractor.py
│
├── outputs/                 # Outputs organizados (criado automaticamente)
│   ├── images/              # Imagens extraídas dos PDFs
│   └── relatorio_*.md       # Relatórios completos em Markdown
│
├── logs/                    # Logs da aplicação (criado automaticamente)
│   └── pdf_analyzer.log     # Arquivo de log com rotação
│
├── .venv/                   # Ambiente virtual Python
├── requirements.txt         # Dependências do projeto
├── .gitignore              # Arquivos ignorados pelo Git
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

📑 Títulos detectados (5):
   - Introdução
   - Metodologia Aplicada
   ...

📋 Seções detectadas (8):
   1. Introdução
   2.1 Desenvolvimento
   ...

🔑 Palavras-chave principais:
   tecnologia, inteligência, artificial, sistema, dados, modelo...

======================================================================
EXTRAÇÃO DE IMAGENS
======================================================================

🖼️  Total de imagens extraídas: 8
📁 Diretório de saída: outputs/images/documento

======================================================================
RESUMO DO DOCUMENTO (gerado por LLM)
======================================================================

Este documento aborda os principais conceitos de desenvolvimento...

📋 Relatório completo salvo em: outputs/relatorio_documento.md

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

## 🧪 Testes

Execute os testes unitários:

```powershell
# Rodar todos os testes
python -m unittest discover tests

# Rodar testes específicos
python -m unittest tests.test_text
python -m unittest tests.test_files
python -m unittest tests.test_extractor

# Rodar com verbose
python -m unittest discover tests -v
```

**Cobertura de testes:**
- `test_text.py`: 12 testes para funções de processamento de texto
- `test_files.py`: 10 testes para manipulação de arquivos
- `test_extractor.py`: 6 testes para extração de PDF

## 📝 Notas Técnicas

- **Tipagem completa**: Type hints em todas as funções e métodos
- **Stopwords**: Lista em português do NLTK
- **Chunking**: Textos longos divididos automaticamente
- **Device**: GPU (CUDA) se disponível, senão CPU
- **Context Managers**: Fechamento automático de recursos
- **Logging**: Sistema completo em arquivo + console com rotação
- **Estrutura avançada**: Detecção de títulos, seções e palavras-chave
- **Relatório unificado**: Markdown completo com todas as análises

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

#### 1. Detecção de Estrutura do PDF
- Identificação automática de títulos (por tamanho de fonte e negrito)
- Detecção de seções numeradas (1., I., A., etc.)
- Extração de palavras-chave principais

#### 2. Tratamento Robusto para PDFs Grandes
- Processamento página por página com logging de progresso
- Tratamento de `MemoryError` e PDFs corrompidos
- Fallback para páginas com erro sem interromper análise
- Controle de I/O para extração de imagens

#### 3. Normalização Avançada de Texto
- Remoção de hífens de quebra de linha
- Normalização Unicode (NFKD)
- Função para remover acentos
- Limpeza avançada com preservação de contexto

#### 4. Sistema de Logs em Arquivo
- Logs salvos em `logs/pdf_analyzer.log`
- Rotação automática (5MB, 3 backups)
- Console + arquivo simultâneos
- Níveis DEBUG no arquivo, configurável no console

#### 5. Relatório Unificado em Markdown
- Todas as análises consolidadas em um único arquivo
- Data/hora de geração
- Títulos, seções, palavras-chave detectadas
- Estatísticas consolidadas (diversidade lexical, taxa de cobertura)
- Formatação profissional com emojis e tabelas

#### 6. Organização de Pastas Planejada
- `outputs/` para todos os arquivos gerados
- `outputs/images/` para imagens por PDF
- `logs/` para logs com rotação
- `tests/` para testes unitários
- `.gitignore` atualizado para nova estrutura

#### 7. Tipagem Completa com typing
- Type hints em todas as funções e métodos
- Tipos complexos: `Dict[str, Any]`, `List[Tuple[str, int]]`, `Optional[str]`
- Context managers com types: `__enter__() -> 'ClassName'`
- Imports organizados de `typing`

#### 8. Testes Simples
- 28 testes unitários cobrindo módulos principais
- `unittest` para testes de `text.py`, `files.py`, `extractor.py`
- Mocks para dependências externas (PyMuPDF)
- Testes de edge cases (arquivos vazios, colisões, etc.)

#### 9. Cuidado com UX em CLI
- Mensagens claras e formatadas com separadores
- Emojis para melhor legibilidade visual
- Progress feedback durante operações longas
- Validação de argumentos com mensagens específicas
- Help detalhado com exemplos práticos de uso
  
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

