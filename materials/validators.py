import re


def validate_youtube_link(link):
    """Проверяет, является ли ссылка YouTube."""
    pattern = r'^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$'  # Регулярное выражение для ссылки YouTube
    if not re.match(pattern, link):
        raise ValueError("Ссылка должна быть на youtube.com")  # Генерируем исключение, если ссылка некорректна
