"""Text regions on a cropped card plus OCR. Part of PTCG Scanner."""

from .read_card import CardRead, Region, read_card, regions_from_obb

__all__ = ["CardRead", "Region", "read_card", "regions_from_obb"]
