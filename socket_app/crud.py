import json

from orm.database import session_maker
from orm.models import User, VirtualMachine, HardDisk

from utils import get_password_hash
from sqlalchemy import select, delete, func, update


def get_user(mail: str) -> User | None:
    with session_maker() as session:
        stmt = select(User).where(
            User.email == mail,
        )

        result = session.scalars(stmt).one_or_none()

    return result


def create_virtual_machine(user: User, *args: tuple) -> None:
    with session_maker() as session:
        session.add(user)
        ram, cpu = args
        new_vm = VirtualMachine(
            ram=ram,
            cpu=cpu,
            user_id=user.id,
        )
        user.virtual_machine.append(new_vm)
        session.add(new_vm)

        session.commit()


def get_all_virtual_machines(user: User, *args: tuple) -> bytes:
    result = {}
    with session_maker() as session:
        stmt = select(VirtualMachine)

        query = session.scalars(stmt).all()
        for machine in query:
            result[machine.id] = str(machine)

    return json.dumps(result).encode()


def update_client(user: User, *args: tuple) -> None:
    with session_maker() as session:
        email, hashed_password = args
        stmt = (
            update(User).
            where(User.id == user.id).
            values(
                email=email,
                hashed_password=get_password_hash(hashed_password),
            )
        )
        session.execute(stmt)
        session.commit()


def get_all_hard_disks(user: User) -> bytes:
    result = {}
    with session_maker() as session:
        stmt = select(HardDisk)

        query = session.scalars(stmt).all()
        for disk in query:
            result[disk.id] = disk.memory

    return json.dumps(result).encode()


def delete_virtual_machine(user: User, *args: tuple):
    with session_maker() as session:
        machine_id = args[0]
        stmt = delete(VirtualMachine).where(VirtualMachine.id == machine_id)
        session.execute(stmt)
        session.commit()


def get_statistic(user: User) -> bytes:
    with session_maker() as session:
        total_machines = session.query(func.count(VirtualMachine.id)).scalar()
        total_ram_cpu = session.query(func.sum(VirtualMachine.cpu)).scalar()
        total_ram_ram = session.query(func.sum(VirtualMachine.ram)).scalar()
        result = {
            "Общее количество машин:": total_machines,
            "Общий объем RAM:": total_ram_ram,
            "Общий объем CPU:": total_ram_cpu,
        }

    return json.dumps(result).encode()


db_methods = {
    '1': create_virtual_machine,
    '2': get_all_virtual_machines,
    '3': update_client,
    '4': get_all_hard_disks,
    '5': delete_virtual_machine,
    '6': get_statistic,
}
