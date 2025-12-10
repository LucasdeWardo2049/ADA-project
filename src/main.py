import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Dict, Any, Optional

from .cli.arguments import create_parser, validate_args
from .pdf.extractor import PDFExtractor
from .pdf.images import ImageExtractor
from .llm.summarize import Summarizer
from .utils.files import format_bytes, ensure_directory


def setup_logging(verbose: bool = False, quiet: bool = False, log_to_file: bool = True) -> None:
    """
    Configura o sistema de logging da aplicação com suporte a arquivo e console.
    
    Args:
        verbose: Se True, exibe logs DEBUG
        quiet: Se True, exibe apenas logs ERROR
        log_to_file: Se True, salva logs em arquivo com rotação
    """
    if quiet:
        log_level = logging.ERROR
    elif verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    handlers = []
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    handlers.append(console_handler)
    
    if log_to_file:
        try:
            log_dir = ensure_directory('logs')
            log_file = log_dir / 'pdf_analyzer.log'
            
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=5 * 1024 * 1024,
                backupCount=3,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter(log_format, date_format))
            handlers.append(file_handler)
        except Exception as error:
            print(f"Aviso: Não foi possível configurar log em arquivo: {error}")
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
        handlers=handlers
    )


def print_analysis_results(pdf_analysis: Dict[str, Any]) -> None:
    """
    Exibe os resultados da análise do PDF na saída padrão.
    
    Args:
        pdf_analysis: Dicionário contendo os resultados da análise
    """
    SEPARATOR = "=" * 70
    
    print(f"\n{SEPARATOR}")
    print("ANÁLISE DO PDF")
    print(SEPARATOR)
    print(f"\nArquivo: {pdf_analysis['file_name']}")
    print(f"Caminho: {pdf_analysis['file_path']}")
    print(f"\n📄 Número de páginas: {pdf_analysis['page_count']}")
    print(f"📦 Tamanho do arquivo: {format_bytes(pdf_analysis['file_size_bytes'])} ({pdf_analysis['file_size_bytes']:,} bytes)")
    print(f"📝 Total de palavras: {pdf_analysis['word_count']:,}")
    print(f"📚 Tamanho do vocabulário: {pdf_analysis['vocabulary_size']:,} palavras distintas")
    
    print(f"\n🔤 10 palavras mais comuns (sem stopwords):")
    for position, (word, frequency) in enumerate(pdf_analysis['most_common_words'], start=1):
        print(f"   {position:2}. {word:<20} ({frequency:,} ocorrências)")
    
    print()


def print_image_results(extracted_images: list, output_directory: str) -> None:
    """
    Exibe os resultados da extração de imagens.
    
    Args:
        extracted_images: Lista de caminhos das imagens extraídas
        output_directory: Diretório onde as imagens foram salvas
    """
    SEPARATOR = "=" * 70
    MAX_IMAGES_TO_SHOW = 5
    
    print(SEPARATOR)
    print("EXTRAÇÃO DE IMAGENS")
    print(SEPARATOR)
    print(f"\n🖼️  Total de imagens extraídas: {len(extracted_images)}")
    
    if extracted_images:
        print(f"📁 Diretório de saída: {output_directory}")
        print(f"\nPrimeiras imagens:")
        
        for image_path in extracted_images[:MAX_IMAGES_TO_SHOW]:
            print(f"   - {Path(image_path).name}")
        
        remaining_images = len(extracted_images) - MAX_IMAGES_TO_SHOW
        if remaining_images > 0:
            print(f"   ... e mais {remaining_images} imagens")
    
    print()


def print_summary(summary_text: str) -> None:
    """
    Exibe o resumo gerado pelo modelo LLM.
    
    Args:
        summary_text: Texto do resumo gerado
    """
    SEPARATOR = "=" * 70
    
    print(SEPARATOR)
    print("RESUMO DO DOCUMENTO (gerado por LLM)")
    print(SEPARATOR)
    print(f"\n{summary_text}\n")


def generate_markdown_report(
    pdf_analysis: Dict[str, Any],
    extracted_images: list,
    summary_text: Optional[str],
    report_output_path: str
) -> None:
    """
    Gera relatório completo em formato Markdown.
    
    Args:
        pdf_analysis: Resultados da análise do PDF
        extracted_images: Lista de imagens extraídas
        summary_text: Resumo gerado (ou None se desabilitado)
        report_output_path: Caminho onde salvar o relatório
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Gerando relatório Markdown: {report_output_path}")
    
    with open(report_output_path, 'w', encoding='utf-8') as report_file:
        report_file.write("# Relatório de Análise de PDF\n\n")
        
        report_file.write("## 📄 Informações do Documento\n\n")
        report_file.write(f"- **Arquivo**: `{pdf_analysis['file_name']}`\n")
        report_file.write(f"- **Caminho**: `{pdf_analysis['file_path']}`\n")
        report_file.write(f"- **Número de páginas**: {pdf_analysis['page_count']}\n")
        report_file.write(f"- **Tamanho**: {format_bytes(pdf_analysis['file_size_bytes'])} ({pdf_analysis['file_size_bytes']:,} bytes)\n")
        report_file.write(f"- **Total de palavras**: {pdf_analysis['word_count']:,}\n")
        report_file.write(f"- **Vocabulário**: {pdf_analysis['vocabulary_size']:,} palavras distintas\n\n")
        
        report_file.write("## 🔤 Palavras Mais Comuns\n\n")
        report_file.write("| # | Palavra | Frequência |\n")
        report_file.write("|---|---------|------------|\n")
        for position, (word, frequency) in enumerate(pdf_analysis['most_common_words'], start=1):
            report_file.write(f"| {position} | {word} | {frequency:,} |\n")
        report_file.write("\n")
        
        report_file.write("## 🖼️ Imagens Extraídas\n\n")
        report_file.write(f"**Total**: {len(extracted_images)} imagens\n\n")
        if extracted_images:
            report_file.write("### Lista de Imagens\n\n")
            for image_path in extracted_images:
                report_file.write(f"- `{Path(image_path).name}`\n")
            report_file.write("\n")
        
        if summary_text:
            report_file.write("## 📝 Resumo do Documento\n\n")
            report_file.write(f"{summary_text}\n\n")
        
        report_file.write("---\n")
        report_file.write("*Relatório gerado pela ferramenta CLI de Análise de PDF*\n")
    
    logger.info(f"Relatório salvo em: {report_output_path}")


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()
    
    if not validate_args(args):
        return 1
    
    setup_logging(verbose=args.verbose, quiet=args.quiet)
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Iniciando análise do PDF...")
        with PDFExtractor(args.pdf_file) as extractor:
            analysis = extractor.analyze()
        
        print_analysis_results(analysis)
        
        image_paths = []
        if not args.no_images:
            logger.info("Iniciando extração de imagens...")
            with ImageExtractor(args.pdf_file) as img_extractor:
                output_dir = args.output_dir or f"imagens/{Path(args.pdf_file).stem}"
                image_paths = img_extractor.extract_images(output_dir)
            
            print_image_results(image_paths, output_dir)
        
        summary = None
        if not args.no_summary:
            logger.info("Iniciando geração de resumo com LLM...")
            print("="*70)
            print("Gerando resumo com modelo de linguagem...")
            print("(Isso pode levar alguns minutos na primeira execução)")
            print("="*70 + "\n")
            
            summarizer = Summarizer(model_name=args.model)
            summary = summarizer.summarize(analysis['full_text'])
            summarizer.cleanup()
            
            print_summary(summary)
        
        if args.report:
            generate_markdown_report(analysis, image_paths, summary, args.report)
            print(f"📋 Relatório Markdown salvo em: {args.report}\n")
        
        print("="*70)
        print("✅ Processamento concluído com sucesso!")
        print("="*70 + "\n")
        
        return 0
    
    except FileNotFoundError as e:
        logger.error(f"Arquivo não encontrado: {e}")
        print(f"\n❌ Erro: {e}\n")
        return 1
    
    except Exception as e:
        logger.error(f"Erro durante o processamento: {e}", exc_info=True)
        print(f"\n❌ Erro: {e}\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())
