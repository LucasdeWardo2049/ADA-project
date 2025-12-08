import sys
import logging
from pathlib import Path
from typing import Dict, Any, Optional

from .cli.arguments import create_parser, validate_args
from .pdf.extractor import PDFExtractor
from .pdf.images import ImageExtractor
from .llm.summarize import Summarizer
from .utils.files import format_bytes


def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def print_analysis_results(analysis: Dict[str, Any]) -> None:
    print("\n" + "="*70)
    print("ANÁLISE DO PDF")
    print("="*70)
    print(f"\nArquivo: {analysis['file_name']}")
    print(f"Caminho: {analysis['file_path']}")
    print(f"\n📄 Número de páginas: {analysis['page_count']}")
    print(f"📦 Tamanho do arquivo: {format_bytes(analysis['file_size_bytes'])} ({analysis['file_size_bytes']:,} bytes)")
    print(f"📝 Total de palavras: {analysis['word_count']:,}")
    print(f"📚 Tamanho do vocabulário: {analysis['vocabulary_size']:,} palavras distintas")
    
    print(f"\n🔤 10 palavras mais comuns (sem stopwords):")
    for i, (word, count) in enumerate(analysis['most_common_words'], 1):
        print(f"   {i:2}. {word:<20} ({count:,} ocorrências)")
    
    print()


def print_image_results(image_paths: list, output_dir: str) -> None:
    print("="*70)
    print("EXTRAÇÃO DE IMAGENS")
    print("="*70)
    print(f"\n🖼️  Total de imagens extraídas: {len(image_paths)}")
    if image_paths:
        print(f"📁 Diretório de saída: {output_dir}")
        print(f"\nPrimeiras imagens:")
        for img_path in image_paths[:5]:
            print(f"   - {Path(img_path).name}")
        if len(image_paths) > 5:
            print(f"   ... e mais {len(image_paths) - 5} imagens")
    print()


def print_summary(summary: str) -> None:
    print("="*70)
    print("RESUMO DO DOCUMENTO (gerado por LLM)")
    print("="*70)
    print(f"\n{summary}\n")


def generate_markdown_report(
    analysis: Dict[str, Any],
    image_paths: list,
    summary: Optional[str],
    output_path: str
) -> None:
    logger = logging.getLogger(__name__)
    logger.info(f"Gerando relatório Markdown: {output_path}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Relatório de Análise de PDF\n\n")
        
        f.write("## 📄 Informações do Documento\n\n")
        f.write(f"- **Arquivo**: `{analysis['file_name']}`\n")
        f.write(f"- **Caminho**: `{analysis['file_path']}`\n")
        f.write(f"- **Número de páginas**: {analysis['page_count']}\n")
        f.write(f"- **Tamanho**: {format_bytes(analysis['file_size_bytes'])} ({analysis['file_size_bytes']:,} bytes)\n")
        f.write(f"- **Total de palavras**: {analysis['word_count']:,}\n")
        f.write(f"- **Vocabulário**: {analysis['vocabulary_size']:,} palavras distintas\n\n")
        
        f.write("## 🔤 Palavras Mais Comuns\n\n")
        f.write("| # | Palavra | Frequência |\n")
        f.write("|---|---------|------------|\n")
        for i, (word, count) in enumerate(analysis['most_common_words'], 1):
            f.write(f"| {i} | {word} | {count:,} |\n")
        f.write("\n")
        
        f.write("## 🖼️ Imagens Extraídas\n\n")
        f.write(f"**Total**: {len(image_paths)} imagens\n\n")
        if image_paths:
            f.write("### Lista de Imagens\n\n")
            for img_path in image_paths:
                f.write(f"- `{Path(img_path).name}`\n")
            f.write("\n")
        
        if summary:
            f.write("## 📝 Resumo do Documento\n\n")
            f.write(f"{summary}\n\n")
        
        f.write("---\n")
        f.write("*Relatório gerado pela ferramenta CLI de Análise de PDF*\n")
    
    logger.info(f"Relatório salvo em: {output_path}")


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
