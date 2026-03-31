"""
Адаптеры интерфейсов - слой контроллеров и схем.
Содержит REST API контроллеры и Pydantic схемы для валидации.
"""

from adapters import controllers
from adapters import schemas

__all__ = ['controllers', 'schemas']