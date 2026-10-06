"""Text regions on a cropped card plus OCR. Part of PTCG Scanner."""

from .read_card import (
    CardRead,
    Region,
    catalog_language_codes,
    create_reader,
    fold_text,
    read_card,
    regions_from_obb,
    script_family,
)

__all__ = [
    "CardRead",
    "Region",
    "catalog_language_codes",
    "create_reader",
    "fold_text",
    "read_card",
    "regions_from_obb",
    "script_family",
]
