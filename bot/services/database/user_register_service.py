from bson import ObjectId
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from bot.services.database import AsyncSessionLocal
from bot.services.database.models.user import User
from bot.services.database.models.package import Package
from bot.services.database.models.user_package import UserPackage
from bot.services.database.models.conversation_set import ConversationSet
from bot.services.database.models.user_conversation_log import UserConversationLog
from bot.services.database.models.conversation_item import ConversationItem


class UserAlreadyExistsError(Exception):
    """Exception jika user sudah ada di database"""
    pass


async def register_free_user(telegram_id: int, username: str):
    """
    Registrasi user baru dengan paket free (id=1).
    - Cek apakah user sudah ada.
    - Ambil paket free.
    - Simpan ke tabel users + user_package.
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # 1. Cek apakah user sudah ada
            result = await session.execute(
                select(User).where(
                    User.telegram_id == telegram_id,
                    User.is_active == True
                )
            )
            existing_user = result.scalar_one_or_none()
            if existing_user:
                raise UserAlreadyExistsError(
                    f"User dengan telegram_id {telegram_id} sudah terdaftar."
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
                id=str(ObjectId()),
                telegram_id=telegram_id,
                username=username,
                is_active=True,
                conversation_set_id=1,  # default
                score=0
            )
            session.add(new_user)
            await session.flush()  # supaya new_user.id bisa dipakai

            # 4. Insert ke tabel user_package
            user_package = UserPackage(
                user_id=new_user.id,
                package_id=free_package.id,
                quota_prompt=free_package.quota_prompt,
                quota_input=free_package.quota_input,
                quota_output=free_package.quota_output
            )
            session.add(user_package)

            # 5. Commit otomatis dengan session.begin()
            return new_user
