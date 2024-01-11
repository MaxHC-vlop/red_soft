from sqlalchemy.orm import Session
from orm.database import engine
from orm.models import User, VirtualMachine, HardDisk


with Session(engine) as session:
    user1 = User(
        email="test1@test.com",
        hashed_password="$2b$12$RVz5IfJVOGEuU9lZI1sTBu9gTYDue0bmDCop3.2EtI5w.3IqmGYni",
        virtual_machine=[
           VirtualMachine(
               ram=111,
               cpu=111,
               hard_disk=[
                   HardDisk(
                       memory=1000,
                   ),
                    HardDisk(
                       memory=1000,
                   ),
               ]
           ),
            VirtualMachine(
               ram=222,
               cpu=222,
               hard_disk=[
                   HardDisk(
                       memory=1000,
                   ),
                    HardDisk(
                       memory=1000,
                   ),
               ]
           ),
        ]
    )
    user2 = User(
        email="test2@test.com",
        hashed_password="$2b$12$7VRX3kDTTD6pA.v96AgNDuTOjYRGMJiJaa6U7N9Hv0rZX30qaYrtC",
        virtual_machine=[
           VirtualMachine(
               ram=333,
               cpu=333,
               hard_disk=[
                   HardDisk(
                       memory=1000,
                   ),
                    HardDisk(
                       memory=1000,
                   ),
               ]
           ),
            VirtualMachine(
               ram=444,
               cpu=444,
               hard_disk=[
                   HardDisk(
                       memory=1000,
                   ),
                    HardDisk(
                       memory=1000,
                   ),
               ]
           ),
        ]
    )

    session.add_all([user1, user2])

    session.commit()
