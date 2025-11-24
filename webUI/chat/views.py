from django.shortcuts import render
from django.http import HttpResponse
# from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)
# Create your views here.
def home_page(request):
    cerebras_key = os.getenv('CEREBRAS_API_KEY')
    cartesia_key = os.getenv('CARTESIA_API_KEY')
    logger.info(f"cerebras_key: {cerebras_key}; cartesia_key: {cartesia_key}")
    return HttpResponse('Chat Home page')