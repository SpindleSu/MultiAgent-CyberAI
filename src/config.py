from __future__ import annotations

import os

from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:

    # =========================================================
    # MODELOS
    # =========================================================

    MODEL_NAME: str = os.getenv(
        "MODEL_NAME",
        "phi3:mini"
    )

    # =========================================================
    # LLM
    # =========================================================

    DEFAULT_TEMP: float = float(
        os.getenv("DEFAULT_TEMP", "0.3")
    )

    TOP_P: float = float(
        os.getenv("TOP_P", "0.9")
    )

    NUM_GPU: int = int(
        os.getenv("NUM_GPU", "0")
    )

    # =========================================================
    # PIPELINE
    # =========================================================

    MAX_RESPONSE_CHARS: int = int(
        os.getenv("MAX_RESPONSE_CHARS", "500")
    )


settings = Settings()