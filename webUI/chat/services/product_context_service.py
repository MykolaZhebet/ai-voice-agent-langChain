import os
import logging
from pathlib import Path
class ProductContextLoaderService:
    @staticmethod
    def load_products():
        logger = logging.getLogger(__name__)
        context_dir = Path('chat/fixtures/product')
        
        all_content = ''
        context_loaded = 0
        
        for file_path in context_dir.glob("*"):
            if file_path.is_file():
                try:
                    content = file_path.read_text()
                    all_content += f"\n=== {file_path.name} ===\n{content}\n"
                    context_loaded += 1
                except Exception as e:
                    logger.error(f"Failed to load file context: {file_path.name}", exc_info=e)
                    # pass
        logger.info(f"Context loaded: {context_loaded}")
        return all_content.strip() or "No files found"