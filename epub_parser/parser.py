import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def extract_chapters(epub_path):
    """
    Extracts chapter titles and text from an EPUB file.
    
    :param epub_path: Path to the EPUB file
    :return: A dictionary {chapter_title: chapter_text}
    """
    book = epub.read_epub(epub_path)
    chapters = {}

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.content, "html.parser")

            # Extract chapter title (h1, h2, etc.)
            title_tag = soup.find(["h1", "h2", "h3"])  # Adjust as needed
            chapter_title = title_tag.get_text(strip=True) if title_tag else f"Chapter {len(chapters) + 1}"

            # Extract chapter text
            chapter_text = soup.get_text(separator=" ", strip=True)

            chapters[chapter_title] = chapter_text

    return chapters
