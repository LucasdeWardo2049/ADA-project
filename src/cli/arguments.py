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
        help='Diretório para salvar as imagens extraídas (padrão: imagens/<nome-pdf>/)'
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
        help='Gera relatório em Markdown no caminho especificado'
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
    
    return parser


def validate_args(args: Any) -> bool:
    pdf_path = Path(args.pdf_file)
    
    if not pdf_path.exists():
        print(f"Erro: Arquivo não encontrado: {args.pdf_file}")
        return False
    
    if not pdf_path.suffix.lower() == '.pdf':
        print(f"Erro: O arquivo deve ser um PDF: {args.pdf_file}")
        return False
    
    if args.verbose and args.quiet:
        print("Erro: As opções --verbose e --quiet são mutuamente exclusivas")
        return False
    
    return True
