from config import VECTOR_SERVICE_ENDPOINT


def build_vector_service_url(text: str):
    return VECTOR_SERVICE_ENDPOINT.replace("{{ text }}", text)

