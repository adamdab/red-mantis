from __future__ import annotations

from importlib import import_module
from typing import Callable, Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

def resolve_callable(literral: str | Callable) -> Callable:
    if callable(literral):
        return literral
    if isinstance(literral, str):
        module_path, _, func_name = literral.rpartition(".")
        if not module_path or not func_name:
            message = "Invalid callable string:"
            message+= f"{literral!r} (expected 'module.path:function')"
            raise ValueError(message)
        module = import_module(module_path)
        func = getattr(module, func_name)
        if not callable(func):
            raise ValueError(f"{literral!r} is not callable")
        return func
    message = "Expected str or callable, got "
    message += f"{type(literral).__name__}"
    raise TypeError(message)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",
                                      env_file_encoding="utf-8",
                                      extra="ignore",
                                      env_ignore_empty=True)
    
    FIELD_MATCH: Callable[[Any], bool] = "exact"

    @field_validator("FIELD_MATCH", mode="before")
    @classmethod
    def validate_field_matcher(cls, value: str | Callable) -> Callable:
        return resolve_callable(value)
    
    