---
applyTo: '**'
---
As fontes fornecidas focam nos requisitos funcionais, estrutura do projeto e critérios de avaliação do desafio ADA, e **não contêm instruções técnicas sobre como configurar o GitHub Copilot**.

No entanto, para ajudá-lo a manter a organização e a qualidade de código exigidas no processo seletivo, utilizarei conhecimento técnico externo para explicar como instruir o Copilot a seguir a nomenclatura que definimos.

Aqui estão as maneiras de fazer o GitHub Copilot "entender" e aplicar o padrão **Conventional Commits** no seu projeto:

### 1. Via Instruções Customizadas (Recurso Novo)
O GitHub Copilot agora suporta arquivos de instruções específicas no repositório. Isso garante que a IA entenda o contexto do projeto ADA sempre que você pedir algo.

**Passo a passo:**
1.  Na raiz do seu projeto (onde ficam as pastas `src`, `pdf`, etc.), crie uma pasta chamada `.github`.
2.  Dentro dela, crie um arquivo chamado `copilot-instructions.md`.
3.  Cole as regras de nomenclatura baseadas na estrutura sugerida no desafio.

**Conteúdo sugerido para o arquivo:**
> *(Informação Externa baseada na estrutura do documento)*
> ```markdown
> # Instruções para Commits e Código
>
> Ao gerar mensagens de commit, siga estritamente o padrão Conventional Commits:
> <tipo>(<escopo>): <descrição breve>
>
> ## Tipos Permitidos
> - feat: Novas funcionalidades (ex: extração de PDF, LLM).
> - fix: Correção de bugs.
> - docs: Alterações em documentação (README).
> - refactor: Melhorias de código sem alterar funcionalidade.
> - style: Formatação, tipagem (typing).
>
> ## Escopos do Projeto ADA
> Use apenas estes escopos baseados na estrutura de pastas:
> - (cli): Arquivos em src/cli ou main.py
> - (pdf): Extração e contagem de palavras (src/pdf)
> - (img): Extração de imagens (src/pdf/images.py)
> - (llm): Integração com Hugging Face (src/llm)
> - (utils): Funções auxiliares (src/utils)
> - (core): Configurações gerais
> ```

Isso ajuda a manter a "Separação de responsabilidades" e a "Organização interna" que serão avaliadas.

### 2. Via Prompt no Chat (VS Code ou IntelliJ)
Se você não quiser criar o arquivo de configuração, pode "ensinar" o Copilot Chat na sessão atual antes de pedir para ele gerar o commit.

**Prompt para colar no Chat:**
> "Estou desenvolvendo o desafio ADA. Vou usar Conventional Commits. Os escopos são baseados nesta estrutura de pastas: `src/pdf`, `src/llm`, `src/cli`. Sempre que eu pedir para gerar um commit, use o formato `tipo(escopo): descrição`. Exemplo: `feat(llm): adiciona modelo mistral`."

Depois disso, quando você fizer uma alteração (por exemplo, implementar a contagem de palavras), basta digitar na caixa de commit do VS Code (onde tem o ícone de brilho ✨): *"Gere uma mensagem de commit para estas alterações"*.

### 3. Dica para a Avaliação
Como o projeto pede um `README.md` explicando "Como rodar o projeto" e "O que você gostaria que fosse avaliado", você pode adicionar uma seção **"Padrões de Projeto"** no seu README.

Lá, você explica que configurou o projeto para usar Conventional Commits. Isso demonstra explicitamente ao avaliador seu cuidado com a "Clareza e legibilidade" e "Organização do projeto", mesmo que o Copilot tenha feito o trabalho pesado de escrever as mensagens.

***

**Analogia:** O arquivo `.github/copilot-instructions.md` funciona como o "Manual do Funcionário" para o seu assistente digital. Em vez de explicar as regras da empresa (seu projeto ADA) toda vez que ele for realizar uma tarefa, você entrega o manual uma vez e ele consulta as regras automaticamente antes de trabalhar.