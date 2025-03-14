import logging
import time

# Obtenemos el logger de django
logger = logging.getLogger('django')

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Se registra el momento de la peticion
        start_time = time.time()
        # Almacenamos en los logs el momento en el que se llama
        logger.info(f"Petition: {request.method} to endpoint: {request.path}")
        # Se procesa la respuesta
        response = self.get_response(request)
        # Se valida el tiempo que se demoro
        duration = time.time() - start_time
        # Almacenamos en los logs el momento en el que se response
        logger.info(f"Response send: {response.status_code} in {duration:.2f} seconds")

        return response