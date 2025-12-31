# Quick Deployment Guide - SQLite Version (FREE)

This guide uses SQLite instead of PostgreSQL - perfect for testing and small apps!
**Total Cost: $0/month** 🎉

## Quick Start

```bash
# 1. Login to Fly.io
flyctl auth login

# 2. Launch (follow prompts, say YES to creating a volume)
flyctl launch --copy-config

# 3. Set secrets
flyctl secrets set SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
flyctl secrets set CORS_ORIGINS="https://your-app-name.fly.dev"

# 4. Deploy
flyctl deploy

# 5. Run migrations
flyctl ssh console -C "cd /app && alembic upgrade head"

# 6. Open your app!
flyctl open
```

## What Changed from PostgreSQL?

✅ **No $38/month PostgreSQL charge**
✅ Uses SQLite with persistent volume (free 3GB included)
✅ Reduced memory to 512MB (still plenty, stays in free tier)
✅ Database file stored in `/data/vocab_trainer.db`

## Backup Your Data

```bash
# Download database
flyctl ssh console -C "cat /data/vocab_trainer.db" > backup_$(date +%Y%m%d).db

# Restore database
cat backup_20250101.db | flyctl ssh console --stdin -C "cat > /data/vocab_trainer.db"
```

## When to Upgrade to PostgreSQL?

SQLite works great for:

- Testing and development
- Small apps (<100k records)
- Low to moderate traffic
- Single instance deployments

Consider PostgreSQL when:

- You need multiple instances/regions
- You have high concurrent writes
- You need advanced database features
- Your data grows beyond 1GB

See [FLY_DEPLOYMENT.md](FLY_DEPLOYMENT.md) for full details.
