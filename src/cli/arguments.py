import argparse
from pathlib import Path
from typing import Any


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ferramenta CLI para análise de PDFs e geração de resumos com LLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python -m src.main documento.pdf
  python -m src.main documento.pdf --output-dir ./minhas-imagens
  python -m src.main documento.pdf --no-summary --verbose
  python -m src.main documento.pdf --model google/flan-t5-small
        """
    )
    
    parser.add_argument(
        'pdf_file',
        type=str,
        help='Caminho para o arquivo PDF a ser analisado'
    )
    
    parser.add_argument(
        '-o', '--output-dir',
        type=str,
        default=None,
        help='Diretório para salvar as imagens extraídas (padrão: outputs/images/<nome-pdf>/)'
    )
    
    parser.add_argument(
        '-m', '--model',
        type=str,
        default='unicamp-dl/ptt5-base-portuguese-vocab',
        help='Nome do modelo LLM a usar (padrão: unicamp-dl/ptt5-base-portuguese-vocab)'
    )
    
    parser.add_argument(
        '--no-summary',
        action='store_true',
        help='Desabilita a geração de resumo (análise apenas)'
    )
    
    parser.add_argument(
        '--no-images',
        action='store_true',
        help='Desabilita a extração de imagens'
    )
    
    parser.add_argument(
        '-r', '--report',
        type=str,
        default=None,
        help='Gera relatório completo em Markdown (padrão: outputs/relatorio_<nome-pdf>.md se não especificado)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Exibe logs detalhados'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suprime logs (apenas erros)'
    )
    
    parser.add_argument(
        '--word-mode',
        type=str,
        choices=['text', 'pdf'],
        default='text',
        help='Modo de contagem de palavras: "text" (tokenização) ou "pdf" (estrutura do PDF)'
    )
    
    parser.add_argument(
        '--keep-numbers',
        action='store_true',
        help='Conta números como palavras (apenas no modo text)'
    )
    
    parser.add_argument(
        '--top-n-words',
        type=int,
        default=10,
        metavar='N',
        help='Número de palavras mais comuns a exibir (padrão: 10)'
    )
    
    parser.add_argument(
        '--no-structure',
        action='store_true',
        help='Pula detecção de títulos, seções e palavras-chave (mais rápido)'
    )
    
    parser.add_argument(
        '--max-pages',
        type=int,
        default=None,
        metavar='N',
        help='Limita análise aos primeiros N páginas do PDF'
    )
    
    parser.add_argument(
        '--min-image-size',
        type=int,
        default=100,
        metavar='PIXELS',
        help='Tamanho mínimo (largura ou altura) para extrair imagens (padrão: 100)'
    )
    
    parser.add_argument(
        '--deterministic',
        action='store_true',
        help='Gera resumos reproduzíveis (desabilita amostragem aleatória)'
    )
    
    # Configuração de logs
    parser.set_defaults(log=True)
    parser.add_argument(
        '--no-log-file',
        dest='log',
        action='store_false',
        help='Desabilita o registro de logs em arquivo (mantém apenas console)'
    )
    
    return parser


def validate_args(args: Any) -> bool:
    """Valida os argumentos da linha de comando.
    
    Args:
        args: Argumentos parseados do argparse
    
    Returns:
        True se argumentos são válidos, False caso contrário
    """
    pdf_path = Path(args.pdf_file)
    
    if not pdf_path.exists():
        print(f"[ERRO] Arquivo não encontrado: {args.pdf_file}")
        print(f"[INFO] Verifique o caminho e tente novamente")
        return False
    
    if not pdf_path.suffix.lower() == '.pdf':
        print(f"[ERRO] O arquivo deve ser um PDF: {args.pdf_file}")
        print(f"[INFO] Extensão detectada: {pdf_path.suffix}")
        return False
    
    if args.verbose and args.quiet:
        print("[ERRO] As opções --verbose e --quiet são mutuamente exclusivas")
        return False
    
    if args.top_n_words < 1:
        print(f"[ERRO] --top-n-words deve ser pelo menos 1, recebido: {args.top_n_words}")
        return False
    
    if args.max_pages is not None and args.max_pages < 1:
        print(f"[ERRO] --max-pages deve ser pelo menos 1, recebido: {args.max_pages}")
        return False
    
    if args.min_image_size < 0:
        print(f"[ERRO] --min-image-size não pode ser negativo, recebido: {args.min_image_size}")
        return False
    
    if args.report:
        report_dir = Path(args.report).parent
        if not report_dir.exists():
            try:
                report_dir.mkdir(parents=True, exist_ok=True)
                print(f"[INFO] Diretório criado para relatório: {report_dir}")
            except Exception as error:
                print(f"[ERRO] Não foi possível criar diretório para relatório: {error}")
                return False
    
    return True
