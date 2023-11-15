from io import BytesIO

from barcode import __BARCODE_MAP
from barcode.writer import ImageWriter

from core.utils.database import Shop, session


def create_barcode(barcode: str, shop: str):
    with session() as s:
        shop_object = s.get(Shop, shop)
        if shop_object is not None:
            protocol = __BARCODE_MAP.get(shop_object.barcode_type)
            if protocol is not None:
                img = BytesIO()
                protocol(barcode, writer=ImageWriter()).write(fp=img)
                img.seek(0)
                return img
