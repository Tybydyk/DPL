
from django.shortcuts import render, get_object_or_404

import logging

logger = logging.getLogger(__name__)


def index(request):
    logger.info('Index page accessed')
    return render(request, "index.html")


def contacts(request):
    logger.info("Contacts page accessed")
    return render(request, "contacts.html")
