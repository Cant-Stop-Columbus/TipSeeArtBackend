from api.models import PaymentProider
from api.database import get_db


async def seed_db():
    db = await get_db()
    print(type(db))


if __name__ == "__main__":
    seed_db()
