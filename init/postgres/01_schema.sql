-- users
CREATE TABLE users (
    user_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       VARCHAR(255) UNIQUE NOT NULL,
    full_name   VARCHAR(255) NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    is_active   BOOLEAN NOT NULL DEFAULT TRUE
);

-- subscription plans
CREATE TABLE subscription_plans (
    plan_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR(50) NOT NULL,   -- 'basic', 'standard', 'premium'
    price_usd   NUMERIC(10,2) NOT NULL,
    max_streams INT NOT NULL
);

INSERT INTO subscription_plans (name, price_usd, max_streams) VALUES
    ('basic',    8.99,  1),
    ('standard', 15.49, 2),
    ('premium',  22.99, 4);

-- subscriptions
CREATE TABLE subscriptions (
    subscription_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    plan_id         UUID NOT NULL REFERENCES subscription_plans(plan_id),
    started_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at      TIMESTAMPTZ NOT NULL,
    status          VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'cancelled', 'expired'))
);

-- billing events
CREATE TABLE billing_events (
    event_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(user_id),
    amount_usd      NUMERIC(10,2) NOT NULL,
    event_type      VARCHAR(30) NOT NULL,  -- 'charge', 'refund', 'chargeback'
    occurred_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata        JSONB                  -- flexible extra data
);

-- indices
CREATE INDEX idx_subscriptions_user   ON subscriptions(user_id);
CREATE INDEX idx_billing_user_time    ON billing_events(user_id, occurred_at DESC);