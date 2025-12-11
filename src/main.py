import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Dict, Any, Optional, List

from .cli.arguments import create_parser, validate_args
from .pdf.extractor import PDFExtractor
from .pdf.images import ImageExtractor
from .llm.summarize import Summarizer
from .utils.files import format_bytes, ensure_directory


def setup_logging(verbose: bool = False, quiet: bool = False, log_to_file: bool = True, run_id: Optional[str] = None) -> None:
    """Configura o sistema de logging da aplicação com suporte a arquivo e console.
    
    Args:
        verbose: Se True, exibe logs DEBUG
        quiet: Se True, exibe apenas logs ERROR
        log_to_file: Se True, salva logs em arquivo com rotação
        run_id: Identificador único da execução para agrupar logs
    """
    if quiet:
        log_level = logging.ERROR
    elif verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    
    if run_id:
        log_format = f'%(asctime)s - [{run_id}] - %(name)s - %(levelname)s - %(message)s'
    else:
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
            print(f"[AVISO] Não foi possível configurar log em arquivo: {error}")
    
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
    
    if 'avg_words_per_page' in pdf_analysis:
        print(f"📊 Média de palavras por página: {pdf_analysis['avg_words_per_page']:.2f}")
    if 'lexical_diversity' in pdf_analysis:
        print(f"📈 Diversidade lexical: {pdf_analysis['lexical_diversity']:.2f}%")
    
    print(f"\n🔤 10 palavras mais comuns (sem stopwords):")
    for position, (word, frequency) in enumerate(pdf_analysis['most_common_words'], start=1):
        print(f"   {position:2}. {word:<20} ({frequency:,} ocorrências)")
    
    if 'titles' in pdf_analysis and pdf_analysis['titles']:
        print(f"\n📑 Títulos detectados ({len(pdf_analysis['titles'])}):")
        for title in pdf_analysis['titles'][:5]:
            print(f"   - {title}")
    
    if 'sections' in pdf_analysis and pdf_analysis['sections']:
        print(f"\n📋 Seções detectadas ({len(pdf_analysis['sections'])}):")
        for section in pdf_analysis['sections'][:5]:
            print(f"   {section['number']} {section['title']}")
    
    if 'keywords' in pdf_analysis and pdf_analysis['keywords']:
        print(f"\n🔑 Palavras-chave principais:")
        keywords_list = [word for word, _ in pdf_analysis['keywords'][:10]]
        print(f"   {', '.join(keywords_list)}")
    
    print()


def print_image_results(extracted_images: List[str], output_directory: str) -> None:
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
    extracted_images: List[str],
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
    
    from datetime import datetime
    
    with open(report_output_path, 'w', encoding='utf-8') as report_file:
        report_file.write("# 📊 Relatório Completo de Análise de PDF\n\n")
        report_file.write(f"**Gerado em**: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}\n\n")
        report_file.write("---\n\n")
        
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
        
        if 'titles' in pdf_analysis and pdf_analysis['titles']:
            report_file.write("## 📑 Títulos Detectados\n\n")
            for title in pdf_analysis['titles']:
                report_file.write(f"- {title}\n")
            report_file.write("\n")
        
        if 'sections' in pdf_analysis and pdf_analysis['sections']:
            report_file.write("## 📋 Seções Identificadas\n\n")
            for section in pdf_analysis['sections']:
                report_file.write(f"- **{section['number']}** {section['title']}\n")
            report_file.write("\n")
        
        if 'keywords' in pdf_analysis and pdf_analysis['keywords']:
            report_file.write("## 🔑 Palavras-Chave Principais\n\n")
            keywords_text = ', '.join([word for word, _ in pdf_analysis['keywords']])
            report_file.write(f"{keywords_text}\n\n")
        
        report_file.write("## 🖼️ Imagens Extraídas\n\n")
        report_file.write(f"**Total**: {len(extracted_images)} imagens\n\n")
        if extracted_images:
            report_file.write("### Lista de Imagens\n\n")
            for image_path in extracted_images:
                report_file.write(f"- `{Path(image_path).name}`\n")
            report_file.write("\n")
        
        if summary_text:
            report_file.write("## 📝 Resumo Gerado por LLM\n\n")
            report_file.write(f"> {summary_text}\n\n")
        else:
            report_file.write("## 📝 Resumo Gerado por LLM\n\n")
            report_file.write("*Resumo não gerado (use --summarize para ativar)*\n\n")
        
        report_file.write("---\n\n")
        report_file.write("## 📈 Estatísticas Consolidadas\n\n")
        report_file.write(f"- Total de páginas analisadas: **{pdf_analysis['page_count']}**\n")
        report_file.write(f"- Palavras únicas no vocabulário: **{pdf_analysis['vocabulary_size']:,}**\n")
        report_file.write(f"- Taxa de diversidade lexical: **{(pdf_analysis['vocabulary_size'] / max(pdf_analysis['word_count'], 1) * 100):.2f}%**\n")
        
        if 'titles' in pdf_analysis:
            report_file.write(f"- Títulos identificados: **{len(pdf_analysis['titles'])}**\n")
        if 'sections' in pdf_analysis:
            report_file.write(f"- Seções estruturadas: **{len(pdf_analysis['sections'])}**\n")
        
        report_file.write(f"- Imagens extraídas: **{len(extracted_images)}**\n")
        report_file.write(f"- Resumo LLM: **{'✓ Gerado' if summary_text else '✗ Não gerado'}**\n\n")
        
        report_file.write("---\n\n")
        report_file.write("*Relatório gerado automaticamente pela ferramenta CLI de Análise de PDF com Sumarização por LLM*\n")
    
    logger.info(f"Relatório salvo em: {report_output_path}")


def _run_pdf_analysis(args: Any, logger: logging.Logger) -> Dict[str, Any]:
    """Executa análise do PDF com parâmetros configuráveis.
    
    Args:
        args: Argumentos parseados da linha de comando
        logger: Logger configurado
    
    Returns:
        Dicionário com resultados da análise
    """
    logger.info("Iniciando análise do PDF...")
    
    with PDFExtractor(args.pdf_file) as extractor:
        if extractor.get_page_count() == 0:
            raise ValueError("[ERRO] PDF está vazio (0 páginas)")
        
        max_pages = args.max_pages if args.max_pages else None
        if max_pages and extractor.get_page_count() > max_pages:
            logger.info(f"Limitando análise aos primeiros {max_pages} páginas")
        
        analysis = extractor.analyze(
            word_mode=args.word_mode,
            keep_numbers=args.keep_numbers,
            top_n_words=args.top_n_words,
            analyze_structure=not args.no_structure
        )
    
    return analysis


def _run_image_extraction(args: Any, logger: logging.Logger) -> List[str]:
    """Executa extração de imagens do PDF.
    
    Args:
        args: Argumentos parseados da linha de comando
        logger: Logger configurado
    
    Returns:
        Lista de caminhos das imagens extraídas
    """
    logger.info("Iniciando extração de imagens...")
    
    with ImageExtractor(args.pdf_file) as img_extractor:
        pdf_name = Path(args.pdf_file).stem
        output_dir = args.output_dir or f"outputs/images/{pdf_name}"
        image_paths = img_extractor.extract_images(
            output_dir,
            min_size=args.min_image_size
        )
    
    return image_paths


def _run_summarization(args: Any, analysis: Dict[str, Any], logger: logging.Logger) -> Optional[str]:
    """Executa geração de resumo com LLM.
    
    Args:
        args: Argumentos parseados da linha de comando
        analysis: Resultados da análise do PDF
        logger: Logger configurado
    
    Returns:
        Texto do resumo ou None
    """
    logger.info("Iniciando geração de resumo com LLM...")
    print("="*70)
    print("Gerando resumo com modelo de linguagem...")
    print("(Isso pode levar alguns minutos na primeira execução)")
    print("="*70 + "\n")
    
    summarizer = Summarizer(model_name=args.model)
    summary = summarizer.summarize(
        analysis['full_text'],
        deterministic=args.deterministic
    )
    summarizer.cleanup()
    
    return summary


def _generate_report_with_metadata(
    args: Any,
    analysis: Dict[str, Any],
    image_paths: List[str],
    summary: Optional[str],
    run_id: str,
    duration: float
) -> str:
    """Gera relatório com metadados de execução.
    
    Args:
        args: Argumentos da linha de comando
        analysis: Resultados da análise
        image_paths: Imagens extraídas
        summary: Resumo gerado
        run_id: ID da execução
        duration: Duração total em segundos
    
    Returns:
        Caminho do relatório gerado
    """
    from datetime import datetime
    import sys
    
    pdf_name = Path(args.pdf_file).stem
    report_path = args.report or f"outputs/relatorio_{pdf_name}.md"
    
    logger = logging.getLogger(__name__)
    logger.info(f"Gerando relatório: {report_path}")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 📊 Relatório Completo de Análise de PDF\n\n")
        f.write(f"**Gerado em**: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}\n")
        f.write(f"**Run ID**: `{run_id}`\n")
        f.write(f"**Duração**: {duration:.2f}s\n\n")
        f.write("## 🔧 Configuração da Execução\n\n")
        f.write(f"**Comando**: `{' '.join(sys.argv)}`\n\n")
        f.write(f"- Modo de contagem: `{args.word_mode}`\n")
        f.write(f"- Números contados: `{'Sim' if args.keep_numbers else 'Não'}`\n")
        f.write(f"- Top N palavras: `{args.top_n_words}`\n")
        f.write(f"- Análise de estrutura: `{'Não' if args.no_structure else 'Sim'}`\n")
        if not args.no_summary:
            f.write(f"- Modelo LLM: `{args.model}`\n")
            f.write(f"- Modo determinístico: `{'Sim' if args.deterministic else 'Não'}`\n")
        f.write("\n---\n\n")
        
        f.write("## 📄 Informações do Documento\n\n")
        f.write(f"- **Arquivo**: `{analysis['file_name']}`\n")
        f.write(f"- **Caminho**: `{analysis['file_path']}`\n")
        f.write(f"- **Número de páginas**: {analysis['page_count']}\n")
        f.write(f"- **Tamanho**: {format_bytes(analysis['file_size_bytes'])} ({analysis['file_size_bytes']:,} bytes)\n")
        f.write(f"- **Total de palavras**: {analysis['word_count']:,}\n")
        f.write(f"- **Vocabulário**: {analysis['vocabulary_size']:,} palavras distintas\n")
        
        if 'avg_words_per_page' in analysis:
            f.write(f"- **Média palavras/página**: {analysis['avg_words_per_page']:.2f}\n")
        if 'lexical_diversity' in analysis:
            f.write(f"- **Diversidade lexical**: {analysis['lexical_diversity']:.2f}%\n")
        f.write("\n")
        
        f.write("## 🔤 Palavras Mais Comuns\n\n")
        f.write("| # | Palavra | Frequência |\n")
        f.write("|---|---------|------------|\n")
        for i, (word, freq) in enumerate(analysis['most_common_words'], 1):
            f.write(f"| {i} | {word} | {freq:,} |\n")
        f.write("\n")
        
        if analysis.get('titles'):
            f.write("## 📑 Títulos Detectados\n\n")
            for title in analysis['titles']:
                f.write(f"- {title}\n")
            f.write("\n")
        
        if analysis.get('sections'):
            f.write("## 📋 Seções Identificadas\n\n")
            for section in analysis['sections']:
                f.write(f"- **{section['number']}** {section['title']}\n")
            f.write("\n")
        
        if analysis.get('keywords'):
            f.write("## 🔑 Palavras-Chave Principais\n\n")
            keywords_text = ', '.join([word for word, _ in analysis['keywords']])
            f.write(f"{keywords_text}\n\n")
        
        f.write("## 🖼️ Imagens Extraídas\n\n")
        f.write(f"**Total**: {len(image_paths)} imagens\n\n")
        if image_paths:
            f.write("### Lista de Imagens\n\n")
            for img_path in image_paths:
                f.write(f"- `{Path(img_path).name}`\n")
            f.write("\n")
        
        if summary:
            f.write("## 📝 Resumo Gerado por LLM\n\n")
            f.write(f"> {summary}\n\n")
        
        f.write("---\n\n")
        f.write("*Relatório gerado automaticamente pela ferramenta CLI de Análise de PDF*\n")
    
    return report_path


def main() -> int:
    """Função principal do programa."""
    import time
    from datetime import datetime
    
    parser = create_parser()
    args = parser.parse_args()
    
    if not validate_args(args):
        return 1
    
    # Gera ID único para esta execução
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    start_time = time.time()
    
    setup_logging(verbose=args.verbose, quiet=args.quiet, log_to_file=args.log, run_id=run_id)
    logger = logging.getLogger(__name__)
    
    logger.info(f"[Run ID: {run_id}] Iniciando processamento do PDF")
    
    try:
        # 1. Análise do PDF
        analysis = _run_pdf_analysis(args, logger)
        print_analysis_results(analysis)
        
        # 2. Extração de imagens
        image_paths = []
        if not args.no_images:
            image_paths = _run_image_extraction(args, logger)
            output_dir = args.output_dir or f"outputs/images/{Path(args.pdf_file).stem}"
            print_image_results(image_paths, output_dir)
        
        # 3. Geração de resumo com LLM
        summary = None
        if not args.no_summary:
            summary = _run_summarization(args, analysis, logger)
            if summary:
                print_summary(summary)
        
        # 4. Geração de relatório final
        duration = time.time() - start_time
        report_path = args.report
        if not report_path:
            pdf_name = Path(args.pdf_file).stem
            report_path = f"outputs/relatorio_{pdf_name}.md"
        
        _generate_report_with_metadata(args, analysis, image_paths, summary, run_id, duration)
        print(f"📋 Relatório completo salvo em: {report_path}\n")
        
        print("="*70)
        print(f"✅ Processamento concluído em {duration:.2f}s!")
        print("="*70 + "\n")
        
        logger.info(f"[Run ID: {run_id}] Processamento concluído com sucesso em {duration:.2f}s")
        return 0
    
    except FileNotFoundError as e:
        logger.error(f"[ERRO] Arquivo não encontrado: {e}")
        print(f"\n❌ [ERRO] Arquivo não encontrado: {e}\n")
        return 1
    
    except ValueError as e:
        logger.error(f"[ERRO] Validação: {e}")
        print(f"\n❌ {e}\n")
        return 1
    
    except Exception as e:
        logger.error(f"[ERRO] Erro durante o processamento: {e}", exc_info=True)
        print(f"\n❌ [ERRO] Erro inesperado: {e}\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())
