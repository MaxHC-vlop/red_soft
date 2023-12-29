from typing import List

from .database import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]

    virtual_machine: Mapped[List["VirtualMachine"]] = relationship(
        back_populates="user", cascade="all, delete-orphan",
    )

    def __str__(self):
        return f"Пользователь:{self.id} {self.email}"


class VirtualMachine(Base):
    __tablename__ = "virtual_machine"

    id: Mapped[int] = mapped_column(primary_key=True)
    ram: Mapped[int]
    cpu: Mapped[int]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_account.id"),
    )

    user: Mapped["User"] = relationship(
        back_populates="virtual_machine",
    )

    hard_disk: Mapped[List["HardDisk"]] = relationship(
        back_populates="virtual_machine", cascade="all, delete-orphan",
    )

    def __str__(self):
        return f"Машина:{self.id} RAM:{self.ram} CPU:{self.cpu}"


class HardDisk(Base):
    __tablename__ = "hard_disk"

    id: Mapped[int] = mapped_column(primary_key=True)
    memory: Mapped[int]
    virtual_machine_id: Mapped[int] = mapped_column(
        ForeignKey("virtual_machine.id"),
    )

    virtual_machine: Mapped["VirtualMachine"] = relationship(
        back_populates="hard_disk",
    )

    def __str__(self):
        return f"HD:{self.id} Memory:{self.memory}"
