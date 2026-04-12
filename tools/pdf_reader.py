#!/usr/bin/env python3
"""
PDF Reader Tool - Extract text from PDF files
Usage: python pdf_reader.py <pdf_file> [output_file]

Examples:
  python pdf_reader.py document.pdf
  python pdf_reader.py document.txt document.pdf
  python pdf_reader.py style_guide.pdf style_guide.txt

Features:
- Extracts all text from PDF
- Preserves paragraph structure
- Handles multi-column layouts
- Outputs to stdout or file
"""

import sys
import os

def extract_text_from_pdf(pdf_path, output_path=None):
    """Extract text from PDF and optionally save to file"""
    try:
        import PyPDF2
    except ImportError:
        print("Error: PyPDF2 not installed")
        print("Install with: pip install PyPDF2")
        sys.exit(1)

    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)

    print(f"Reading: {pdf_path}")
    print("-" * 60)

    extracted_text = []

    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            print(f"Total pages: {num_pages}")
            print("-" * 60)

            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text = page.extract_text()

                # Clean up the text
                text = text.strip()
                if text:
                    extracted_text.append(f"\n--- Page {page_num + 1} ---\n")
                    extracted_text.append(text)

        full_text = '\n'.join(extracted_text)

        # Output to file if specified
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_text)
            print(f"\n✓ Text saved to: {output_path}")
        else:
            print(full_text)

        print("-" * 60)
        print(f"✓ Extracted {len(full_text)} characters from {num_pages} pages")

        return full_text

    except Exception as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("PDF Reader Tool")
        print("\nUsage:")
        print("  python pdf_reader.py <pdf_file>")
        print("  python pdf_reader.py <output_file> <pdf_file>")
        print("\nExamples:")
        print("  python pdf_reader.py document.pdf")
        print("  python pdf_reader.py document.txt document.pdf")
        sys.exit(1)

    # Parse arguments
    if len(sys.argv) == 2:
        # Single argument: PDF file, output to stdout
        pdf_path = sys.argv[1]
        output_path = None
    else:
        # Two arguments: output file, PDF file
        output_path = sys.argv[1]
        pdf_path = sys.argv[2]

    extract_text_from_pdf(pdf_path, output_path)

if __name__ == "__main__":
    main()
