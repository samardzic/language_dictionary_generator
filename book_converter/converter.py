#!/usr/bin/env python3
"""
PDF to TXT Converter

This module provides functionality to convert PDF files to plain text format.
Supports both single file conversion and batch processing of multiple PDFs.

Example:
    # Convert single file
    python converter.py input.pdf

    # Convert single file with output path
    python converter.py input.pdf output.txt

    # Convert all PDFs in a directory
    python converter.py --batch /path/to/pdfs

Dependencies:
    - PyPDF2 or pdfplumber (install via: pip install PyPDF2 pdfplumber)
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional, List

# Try to import PDF libraries (prefer pdfplumber for better text extraction)
try:
    import pdfplumber
    PDF_LIBRARY = 'pdfplumber'
except ImportError:
    try:
        from PyPDF2 import PdfReader
        PDF_LIBRARY = 'pypdf2'
    except ImportError:
        print("Error: No PDF library found. Please install one:")
        print("  pip install pdfplumber")
        print("  or")
        print("  pip install PyPDF2")
        sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PDFConverter:
    """Handle PDF to text conversion operations."""

    def __init__(self):
        """Initialize the PDF converter."""
        self.library = PDF_LIBRARY
        logger.info(f"Using {self.library} for PDF conversion")

    def convert_pdf_to_text(self, pdf_path: Path) -> str:
        """
        Extract text from a PDF file.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Extracted text content as string

        Raises:
            FileNotFoundError: If PDF file doesn't exist
            ValueError: If file is not a PDF
            Exception: If PDF extraction fails
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        if pdf_path.suffix.lower() != '.pdf':
            raise ValueError(f"File is not a PDF: {pdf_path}")

        logger.info(f"Converting: {pdf_path}")

        try:
            if self.library == 'pdfplumber':
                return self._convert_with_pdfplumber(pdf_path)
            else:
                return self._convert_with_pypdf2(pdf_path)
        except Exception as e:
            logger.error(f"Failed to convert {pdf_path}: {e}")
            raise

    def _convert_with_pdfplumber(self, pdf_path: Path) -> str:
        """
        Convert PDF using pdfplumber library.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text
        """
        text_content = []

        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            logger.info(f"Processing {total_pages} pages...")

            for page_num, page in enumerate(pdf.pages, 1):
                logger.debug(f"Processing page {page_num}/{total_pages}")
                text = page.extract_text()

                if text:
                    text_content.append(text)

        return '\n\n'.join(text_content)

    def _convert_with_pypdf2(self, pdf_path: Path) -> str:
        """
        Convert PDF using PyPDF2 library.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text
        """
        text_content = []

        reader = PdfReader(str(pdf_path))
        total_pages = len(reader.pages)
        logger.info(f"Processing {total_pages} pages...")

        for page_num, page in enumerate(reader.pages, 1):
            logger.debug(f"Processing page {page_num}/{total_pages}")
            text = page.extract_text()

            if text:
                text_content.append(text)

        return '\n\n'.join(text_content)

    def save_text(self, text: str, output_path: Path) -> None:
        """
        Save extracted text to a file.

        Args:
            text: Text content to save
            output_path: Path where to save the text file

        Raises:
            Exception: If file writing fails
        """
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(text, encoding='utf-8')
            logger.info(f"Saved to: {output_path}")
        except Exception as e:
            logger.error(f"Failed to save file {output_path}: {e}")
            raise

    def convert_file(self, pdf_path: Path, output_path: Optional[Path] = None) -> Path:
        """
        Convert a single PDF file to text.

        Args:
            pdf_path: Path to PDF file
            output_path: Optional output path (default: same name with .txt extension)

        Returns:
            Path to the created text file

        Raises:
            FileNotFoundError: If PDF doesn't exist
            Exception: If conversion fails
        """
        # Default output path
        if output_path is None:
            output_path = pdf_path.with_suffix('.txt')

        # Convert
        text = self.convert_pdf_to_text(pdf_path)

        # Save
        self.save_text(text, output_path)

        return output_path

    def convert_batch(self, directory: Path, output_dir: Optional[Path] = None) -> List[Path]:
        """
        Convert all PDF files in a directory.

        Args:
            directory: Directory containing PDF files
            output_dir: Optional output directory (default: same as input)

        Returns:
            List of paths to created text files

        Raises:
            FileNotFoundError: If directory doesn't exist
        """
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")

        if not directory.is_dir():
            raise ValueError(f"Path is not a directory: {directory}")

        # Find all PDF files
        pdf_files = list(directory.glob('*.pdf'))
        pdf_files.extend(list(directory.glob('*.PDF')))

        if not pdf_files:
            logger.warning(f"No PDF files found in {directory}")
            return []

        logger.info(f"Found {len(pdf_files)} PDF files")

        # Default output directory
        if output_dir is None:
            output_dir = directory
        else:
            output_dir.mkdir(parents=True, exist_ok=True)

        # Convert each file
        output_files = []
        success_count = 0
        fail_count = 0

        for pdf_file in pdf_files:
            try:
                output_path = output_dir / pdf_file.with_suffix('.txt').name
                self.convert_file(pdf_file, output_path)
                output_files.append(output_path)
                success_count += 1
            except Exception as e:
                logger.error(f"Failed to convert {pdf_file}: {e}")
                fail_count += 1

        logger.info(f"Conversion complete: {success_count} succeeded, {fail_count} failed")

        return output_files


def main():
    """Main entry point for the converter."""
    parser = argparse.ArgumentParser(
        description='Convert PDF files to plain text format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert single file (output: input.txt)
  python converter.py input.pdf

  # Convert with specific output path
  python converter.py input.pdf output.txt

  # Convert all PDFs in a directory
  python converter.py --batch /path/to/pdfs

  # Convert all PDFs with specific output directory
  python converter.py --batch /path/to/pdfs --output /path/to/output
        """
    )

    parser.add_argument(
        'input',
        type=str,
        help='Input PDF file or directory (with --batch)'
    )

    parser.add_argument(
        'output',
        type=str,
        nargs='?',
        help='Output text file or directory (optional)'
    )

    parser.add_argument(
        '--batch',
        action='store_true',
        help='Batch mode: convert all PDFs in directory'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Initialize converter
    converter = PDFConverter()

    try:
        if args.batch:
            # Batch conversion
            input_dir = Path(args.input)
            output_dir = Path(args.output) if args.output else None
            output_files = converter.convert_batch(input_dir, output_dir)

            print(f"\nConverted {len(output_files)} files successfully")
            if output_files:
                print("\nOutput files:")
                for file in output_files:
                    print(f"  - {file}")

        else:
            # Single file conversion
            input_file = Path(args.input)
            output_file = Path(args.output) if args.output else None
            result = converter.convert_file(input_file, output_file)

            print(f"\nConversion successful!")
            print(f"Output: {result}")

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        if args.verbose:
            raise
        sys.exit(1)


if __name__ == '__main__':
    main()