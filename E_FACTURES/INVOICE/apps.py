# invoice/apps.py
from django.apps import AppConfig
import logging
from functools import partial
from ollama import chat

logger = logging.getLogger('invoice')

class InvoiceAppConfig(AppConfig):
    name = 'invoice'
    ollama_model = None  # Class-level attribute for the callable

    def ready(self):
        try:
            # Create a callable that always uses the 'mistral' model
            InvoiceAppConfig.ollama_model = partial(chat, model='mistral')
            logger.info("Ollama model preloaded successfully.")
        except Exception as e:
            logger.error(f"Error pre-loading Ollama model: {str(e)}")
