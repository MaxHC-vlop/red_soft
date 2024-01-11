from orm.models import User

from sqlalchemy import select, delete, update


def test_added_user(mocked_session):
    user = User(email='johndoe@example.com', hashed_password='password123')

    mocked_session.add(user)
    mocked_session.commit()

    assert mocked_session.query(User).filter_by(email='johndoe@example.com') is not None


def test_delete_user(mocked_session):
    stmt = delete(User).where(User.id == 1)
    mocked_session.execute(stmt)
    mocked_session.commit()

    stmt = select(User).where(
            User.id == 1,
        )

    result = mocked_session.scalars(stmt).one_or_none()

    assert result is None


def test_update_user(mocked_session):
    stmt = (
        update(User).
        where(User.id == 1).
        values(
            email='email',
            hashed_password='qwe',
        )
    )
    mocked_session.execute(stmt)
    mocked_session.commit()

    stmt = select(User).where(
        User.id == 1,
    )

    result = mocked_session.scalars(stmt).one_or_none()

    assert result.email == 'email'
