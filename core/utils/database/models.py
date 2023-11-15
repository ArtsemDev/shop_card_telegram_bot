from sqlalchemy import Column, BIGINT, VARCHAR, SMALLINT, ForeignKey, INT, BOOLEAN

from .base import Base


__all__ = [
    "Shop",
    "User",
    "UserCard",
    "BarcodeType"
]


class BarcodeType(Base):
    __tablename__ = "barcode_types"

    name = Column(VARCHAR(12), primary_key=True)


class Shop(Base):
    __tablename__ = "shops"

    name = Column(VARCHAR(128), primary_key=True)
    barcode_type = Column(
        VARCHAR(12),
        ForeignKey(column="barcode_types.name", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        server_default="Code128"
    )

    def __str__(self) -> str:
        return self.name


class User(Base):
    __tablename__ = "users"

    id = Column(BIGINT, primary_key=True)
    is_admin = Column(BOOLEAN, default=False, nullable=False)


class UserCard(Base):
    __tablename__ = "user_cards"

    id = Column(INT, primary_key=True)
    user_id = Column(
        BIGINT,
        ForeignKey(column="users.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False
    )
    shop = Column(
        VARCHAR(128),
        ForeignKey(column="shops.name", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )
    barcode = Column(VARCHAR(32), nullable=False)
