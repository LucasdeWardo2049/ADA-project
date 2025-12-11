# Analisador de PDF com LLM

> **Desafio de Processo Seletivo - ADA Tech**  
> Ferramenta CLI em Python para análise completa de documentos PDF e geração de resumos usando modelos de linguagem locais (Hugging Face).

**Desenvolvido por:** Lucas de Wardo  
**Repositório:** [github.com/LucasdeWardo2049/ADA-project](https://github.com/LucasdeWardo2049/ADA-project)

##  Funcionalidades

### Obrigatórias 
- Extração de metadados do PDF (páginas, palavras, tamanho)
- Análise estatística do texto (vocabulário, palavras mais comuns)
- Extração de imagens
- Geração de resumo com LLM local (Hugging Face)

### Extras 
- Sistema de logs completo
- Relatório em Markdown
- Tipagem com `typing`
- Estrutura modular bem organizada
- Suporte a PDFs grandes
- Tratamento robusto de exceções
- Context managers para recursos

## Requisitos

- **Python 3.9+** (recomendado: **Python 3.11**)
  - ⚠️ Python 3.14+ ainda não é suportado por algumas dependências (PyMuPDF)
- Dependências no `requirements.txt`

## 🔧 Instalação

```powershell
# Navegue até a pasta do projeto
cd C:\Users\....\ADA

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

## Uso

### Uso Básico

```powershell
python -m src.main "C:\.......\documento.pdf"
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

##  Exemplo de Saída

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

##  Modelos LLM Suportados

Por padrão, usa `unicamp-dl/ptt5-base-portuguese-vocab` (otimizado para português).

Outros modelos compatíveis:
- `google/flan-t5-small` (menor, mais rápido)
- `google/flan-t5-base`
- `t5-small`

##  Testes

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

##  Notas Técnicas

- **Tipagem completa**: Type hints em todas as funções e métodos
- **Stopwords**: Lista em português do NLTK
- **Chunking**: Textos longos divididos automaticamente
- **Device**: GPU (CUDA) se disponível, senão CPU
- **Context Managers**: Fechamento automático de recursos
- **Logging**: Sistema completo em arquivo + console com rotação
- **Estrutura avançada**: Detecção de títulos, seções e palavras-chave
- **Relatório unificado**: Markdown completo com todas as análises

##  Solução de Problemas

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

---

## Como Rodar o Projeto

### Pré-requisitos
- **Python 3.11** (recomendado) ou Python 3.9+
- Git instalado
- Conexão com internet (primeira execução para baixar modelo LLM)

### Passo a Passo

#### 1. Clone o Repositório
```powershell
git clone https://github.com/LucasdeWardo2049/ADA-project.git
cd ADA-project
```

#### 2. Configure o Ambiente Virtual
```powershell
# Crie o ambiente virtual
python -m venv .venv

# Ative o ambiente (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Ou no Linux/Mac
source .venv/bin/activate
```

#### 3. Instale as Dependências
```powershell
# Atualize o pip
python -m pip install --upgrade pip

# Instale todas as dependências
pip install -r requirements.txt
```

#### 4. Execute o Programa
```powershell
# Análise completa (extração + imagens + resumo LLM + relatório)
python -m src.main "caminho/para/seu/arquivo.pdf"

# Exemplos práticos:
python -m src.main documento.pdf                           # Análise completa
python -m src.main documento.pdf --no-summary              # Sem resumo LLM
python -m src.main documento.pdf --verbose                 # Com logs detalhados
python -m src.main documento.pdf --output-dir ./imagens    # Diretório customizado
```

#### 5. Execute os Testes (Opcional)
```powershell
# Rodar todos os testes
python -m unittest discover tests -v

# Rodar testes específicos
python -m unittest tests.test_text
python -m unittest tests.test_files
```

### Estrutura de Saída

Após a execução, o programa cria automaticamente:
- **`outputs/relatorio_<nome>.md`** - Relatório completo em Markdown
- **`outputs/images/<nome>/`** - Imagens extraídas do PDF
- **`logs/pdf_analyzer.log`** - Arquivo de log com histórico

---

##  Funcionalidades Implementadas

### ✅ Funcionalidades Obrigatórias

#### 1. Análise Completa do PDF
- ✅ Extração de metadados: número de páginas, tamanho do arquivo
- ✅ Contagem total de palavras
- ✅ Análise de vocabulário (palavras únicas)
- ✅ Processamento com remoção de stopwords em português (NLTK)
- ✅ Identificação das 10 palavras mais comuns

#### 2. Extração de Imagens
- ✅ Extração automática de todas as imagens do PDF
- ✅ Salvamento organizado em diretórios separados por PDF
- ✅ Nomenclatura única evitando colisões (page1_img1, page1_img2...)
- ✅ Suporte a múltiplos formatos (PNG, JPEG, etc.)

#### 3. Resumo com LLM Local
- ✅ Integração com Hugging Face Transformers
- ✅ Modelo em português: `unicamp-dl/ptt5-base-portuguese-vocab`
- ✅ Execução 100% local (sem enviar dados para APIs externas)
- ✅ Chunking automático para textos longos
- ✅ Fallback para modelo alternativo em caso de erro
- ✅ Detecção automática de GPU (CUDA) ou CPU

#### 4. Interface CLI
- ✅ Argumentos de linha de comando com `argparse`
- ✅ Validação de entrada (arquivo existe, é PDF, etc.)
- ✅ Mensagens de erro claras e específicas
- ✅ Help completo com exemplos de uso


### Funcionalidades Extras (Diferenciais) 

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

#### 9. Experiência do Usuário (UX)
- Mensagens claras e formatadas com separadores visuais
- Emojis para melhor legibilidade (📄, 🖼️, 📝, ✅)
- Progress feedback durante operações longas
- Validação de argumentos com mensagens específicas
- Help detalhado com exemplos práticos de uso
- Geração automática de relatório mesmo sem flag `--report`

---

##  O que eu gostaria que fosse avaliado:

### 1. Arquitetura e Organização do Código 

#### Estrutura Modular
- **4 módulos principais** com responsabilidades únicas:
  - `cli/` - Interface de linha de comando
  - `pdf/` - Processamento de PDFs (extração e imagens)
  - `llm/` - Modelos de linguagem e sumarização
  - `utils/` - Utilitários reutilizáveis (texto e arquivos)

#### Boas Práticas
- **Separação de responsabilidades**: Cada arquivo tem propósito claro
- **DRY (Don't Repeat Yourself)**: Funções utilitárias compartilhadas
- **Single Responsibility Principle**: Funções pequenas e focadas
- **Context Managers**: Gerenciamento automático de recursos (PDFs, modelos)
- **Arquivos enxutos**: Maior arquivo tem ~200 linhas, funções coesas

#### Organização de Outputs
- Estrutura planejada: `outputs/`, `outputs/images/`, `logs/`
- `.gitignore` atualizado para nova estrutura
- Geração automática de diretórios quando necessário

### 2. Qualidade e Manutenibilidade do Código 

#### Tipagem Completa
- **Type hints em 100% das funções e métodos**
- Tipos complexos: `Dict[str, Any]`, `List[Tuple[str, int]]`, `Optional[str]`
- Context managers tipados: `__enter__() -> 'ClassName'`
- Imports organizados de `typing`

#### Documentação
- **Docstrings** em todas as funções públicas
- Parâmetros e retornos documentados
- README completo com exemplos práticos
- Comentários onde a lógica não é óbvia

#### Testes
- **28 testes unitários** cobrindo módulos principais
- Framework `unittest` padrão do Python
- Mocks para dependências externas (PyMuPDF)
- Cobertura de edge cases (arquivos vazios, colisões, erros)

#### Tratamento de Erros
- Try-catch específicos em todos os módulos
- Mensagens de erro claras e acionáveis
- Fallback inteligente (modelo alternativo se principal falhar)
- Graceful degradation (continua análise mesmo com erro em página)

### 3. Funcionalidades Avançadas e Diferenciais 

#### Detecção de Estrutura do PDF
- Identificação automática de títulos (tamanho de fonte + negrito)
- Detecção de seções numeradas com regex (1., I., A.)
- Extração de palavras-chave mais relevantes
- **Valor**: Análise semântica além de simples contagem

#### Suporte a PDFs Grandes
- Processamento página por página
- Logging de progresso a cada 20-50 páginas
- Tratamento de `MemoryError`
- Controle de exceções em nível de página e imagem
- **Valor**: Robustez para documentos corporativos reais

#### Normalização Avançada de Texto
- Remoção de hífens de quebra de linha (`desenvolvi-\nmento`)
- Normalização Unicode (NFKD)
- Função para remover acentos
- Limpeza preservando contexto
- **Valor**: Qualidade superior na análise de texto

#### Sistema de Logs Profissional
- Logs em arquivo + console simultâneos
- Rotação automática (5MB, 3 backups)
- 3 níveis configuráveis (ERROR, INFO, DEBUG)
- Timestamps e módulo de origem
- **Valor**: Debugging e auditoria em produção

#### Relatório Consolidado
- Markdown profissional com todas as análises
- Data/hora de geração automática
- Estatísticas consolidadas (diversidade lexical)
- Formatação com emojis e tabelas
- **Valor**: Documento único pronto para compartilhar

### 4. Experiência do Desenvolvedor (DX) 

- **Instalação simples**: `pip install -r requirements.txt`
- **Uso intuitivo**: Comandos claros e help detalhado
- **Feedback constante**: Logs informativos sem poluir
- **Validação proativa**: Erros detectados cedo com mensagens claras
- **Extensibilidade**: Fácil adicionar novos analisadores ou modelos

### 5. Critérios Específicos do Desafio ADA 

| Critério | Implementação | Destaque |
|----------|---------------|----------|
| **Pastas bem definidas** | ✅ 4 módulos + tests + outputs | Separação clara de concerns |
| **Boa organização interna** | ✅ Context managers, tipagem, logs | Context managers em todas as classes |
| **Evitar arquivos gigantes** | ✅ Máximo ~200 linhas | Funções pequenas e coesas |
| **Códigos auxiliares** | ✅ utils/text.py, utils/files.py | 15+ funções utilitárias |
| **Nomes claros** | ✅ Variáveis descritivas | `pdf_analysis` vs `analysis` |
| **Logs/relatórios** | ✅ Sistema completo | Arquivo + console + Markdown |

---

##  Diferenciais Técnicos

1. **Codigo intuitivo** - Código autoexplicativo 
2. **Commits organizados** - Seguindo Conventional Commits
3. **GPU Detection** - Usa CUDA se disponível, CPU caso contrário
4. **Chunking inteligente** - Textos longos divididos automaticamente
5. **Relatório sempre gerado** - Mesmo sem flag `--report`

---

##  Tecnologias Utilizadas

- **Python 3.11** - Linguagem principal
- **PyMuPDF (fitz)** - Extração de PDF
- **Hugging Face Transformers** - Modelos LLM
- **PyTorch** - Backend para modelos
- **NLTK** - Processamento de linguagem natural
- **unittest** - Framework de testes

##  Autor

**Lucas de Wardo**
- GitHub: [@LucasdeWardo2049](https://github.com/LucasdeWardo2049)
- LinkedIn: [linkedin.com/in/lucasdewardo](https://linkedin.com/in/lucasdewardo)

---

##  Sobre o Desafio

Este projeto foi desenvolvido como resposta ao desafio técnico do processo seletivo da **ADA Tech**, que solicitava:

1. ✅ Uma ferramenta CLI em Python
2. ✅ Análise de arquivos PDF
3. ✅ Extração de metadados e imagens
4. ✅ Geração de resumo com LLM local
5. ✅ Código bem organizado e documentado

**Diferenciais implementados além do solicitado:**
- Detecção automática de estrutura (títulos, seções)
- Sistema profissional de logs com rotação
- Tratamento robusto para PDFs grandes
- Relatório consolidado em Markdown
- 28 testes unitários
- Tipagem completa com type hints
- Normalização avançada de texto

---

**⭐ Se este projeto atendeu suas expectativas, considere dar uma estrela no repositório!**


