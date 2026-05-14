from __future__ import annotations

import logging


def setup_logging() -> None:
    """
    Configuración centralizada del sistema de logs.
    """

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        ),
    )