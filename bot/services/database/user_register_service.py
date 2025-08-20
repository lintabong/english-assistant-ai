

from sqlalchemy.future import select
from bot.services.database import AsyncSessionLocal
from bot.services.database.models.users import User
from bot.services.database.models.package import Package
from bot.services.database.models.user_package import UserPackage
from bot.services.database.models.cashflow import Cashflow
from sqlalchemy.exc import IntegrityError


class UserAlreadyExistsError(Exception):
    pass


async def register_free_user(telegram_id: str, username: str):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # 1. Cek apakah user sudah ada dengan is_active=False
            result = await session.execute(
                select(User).where(
                    User.telegram_id == telegram_id,
                    User.is_active == False
                )
            )
            existing_user = result.scalar_one_or_none()
            if existing_user:
                raise UserAlreadyExistsError(
                    f"User dengan telegram_id {telegram_id} sudah ada dan is_active=False"
                )

            # 2. Ambil paket free (id=1)
            result = await session.execute(
                select(Package).where(Package.id == 1)
            )
            free_package = result.scalar_one_or_none()
            if not free_package:
                raise ValueError("Paket free (id=1) tidak ditemukan.")

            # 3. Insert ke tabel users
            new_user = User(
                telegram_id=telegram_id,
                username=username,
                is_active=True
            )
            session.add(new_user)
            await session.flush()  # supaya new_user.id terisi

            # 4. Insert ke tabel user_packages
            user_package = UserPackage(
                user_id=new_user.id,
                package_id=free_package.id,
                quota_prompt=free_package.quota_prompt
            )
            session.add(user_package)

            # 5. Insert ke tabel cashflows
            cashflow = Cashflow(
                user_id=new_user.id,
                name="Personal"
            )
            session.add(cashflow)

            # 6. Commit dilakukan otomatis saat keluar dari session.begin()
            return new_user
