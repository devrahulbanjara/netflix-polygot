from fastapi import APIRouter, HTTPException, Depends
import asyncpg
from app.database import get_pg_pool
from app.models.user import UserCreate, UserResponse, SubscriptionCreate
from uuid import UUID

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(payload: UserCreate, pool: asyncpg.Pool = Depends(get_pg_pool)):
    try:
        row = await pool.fetchrow(
            """
            INSERT INTO users (email, full_name)
            VALUES ($1, $2)
            RETURNING user_id, email, full_name, created_at, is_active
            """,
            payload.email, payload.full_name
        )
        return dict(row)
    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=409, detail="Email already registered")

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, pool: asyncpg.Pool = Depends(get_pg_pool)):
    row = await pool.fetchrow(
        "SELECT user_id, email, full_name, created_at, is_active FROM users WHERE user_id = $1",
        user_id
    )
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(row)

@router.post("/{user_id}/subscribe", status_code=201)
async def subscribe(
    user_id: UUID,
    payload: SubscriptionCreate,
    pool: asyncpg.Pool = Depends(get_pg_pool)
):
    # ── This is a TRANSACTION: charge + subscription must both succeed ──
    # This is the core argument for PostgreSQL. If the billing insert fails,
    # the subscription insert is rolled back automatically.
    async with pool.acquire() as conn:
        async with conn.transaction():
            plan = await conn.fetchrow(
                "SELECT plan_id, price_usd FROM subscription_plans WHERE name = $1",
                payload.plan_name
            )
            if not plan:
                raise HTTPException(status_code=404, detail="Plan not found")

            sub = await conn.fetchrow(
                """
                INSERT INTO subscriptions (user_id, plan_id, expires_at)
                VALUES ($1, $2, NOW() + INTERVAL '30 days')
                RETURNING subscription_id, started_at, expires_at
                """,
                user_id, plan["plan_id"]
            )

            await conn.execute(
                """
                INSERT INTO billing_events (user_id, amount_usd, event_type)
                VALUES ($1, $2, 'charge')
                """,
                user_id, plan["price_usd"]
            )

    return {
        "subscription_id": str(sub["subscription_id"]),
        "plan": payload.plan_name,
        "expires_at": sub["expires_at"],
        "charged_usd": float(plan["price_usd"])
    }