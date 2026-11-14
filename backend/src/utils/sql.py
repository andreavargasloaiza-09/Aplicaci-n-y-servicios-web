"""Utilidades para construir restricciones SQL."""


def lista_sql(valores) -> str:
    """('a', 'b') -> "'a', 'b'" para usar dentro de un CHECK ... IN (...)."""
    return ", ".join(f"'{v}'" for v in valores)
