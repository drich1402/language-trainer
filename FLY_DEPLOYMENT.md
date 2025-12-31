# Fly.io Deployment Guide (SQLite Version - Free!)

## Prerequisites

1. Install the Fly CLI: https://fly.io/docs/hands-on/install-flyctl/
2. Sign up for a Fly.io account: `flyctl auth signup` or login: `flyctl auth login`

## Deployment Steps

### 1. Initialize Fly App (First Time Only)

```bash
flyctl launch
```

This will:

- Detect your Dockerfile
- Use the existing `fly.toml` configuration file
- Ask you to choose an app name and region
- Say "yes" when asked to create a volume for persistent storage

### 2. Create Persistent Volume for SQLite Database

If not created during launch, create it manually:

```bash
flyctl volumes create vocab_data --size 1 --region iad
```

### 3. Set Environment Variables

```bash
flyctl secrets set SECRET_KEY="your-super-secret-key-here"
flyctl secrets set CORS_ORIGINS="https://your-app-name.fly.dev"
```

To generate a secure SECRET_KEY:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. Deploy

```bash
flyctl deploy
```

### 5. Run Database Migrations

After first deployment, SSH in and run migrations:

```bash
flyctl ssh console --app your-app-name
cd /app
alembic upgrade head
exit
```

Or add a release command to fly.toml:

```toml
[deploy]
  release_command = "alembic upgrade head"
```

### 6. Open Your App

```bash
flyctl open
```

## Cost Breakdown (100% FREE for small apps!)

✅ **SQLite on Persistent Volume**: FREE (3GB included in free tier)
✅ **1 VM with 512MB RAM**: FREE (included in free tier)
✅ **160GB data transfer**: FREE (included in free tier)

No PostgreSQL charges! Your entire app runs for **$0/month** on the free tier.

## Useful Commands

### View Logs

```bash
flyctl logs
```

### SSH into Container

```bash
flyctl ssh console
```

### Check Volume Status

```bash
flyctl volumes list
```

### Backup SQLite Database

```bash
flyctl ssh console --app your-app-name -C "cat /data/vocab_trainer.db" > backup.db
```

### Restore SQLite Database

```bash
flyctl ssh console --app your-app-name
cat > /data/vocab_trainer.db
# Paste your backup and press Ctrl+D
```

### Check App Status

```bash
flyctl status
```

## Migrating to PostgreSQL Later (Optional)

If your app grows and you need PostgreSQL:

1. Create a Postgres database:

```bash
flyctl postgres create --name your-app-db
flyctl postgres attach your-app-db
```

2. The DATABASE_URL secret will be automatically set
3. Redeploy: `flyctl deploy`
4. Run migrations: `flyctl ssh console -C "alembic upgrade head"`

## Troubleshooting

### Check Build Logs

```bash
flyctl logs --app your-app-name
```

### If Database Won't Initialize

1. SSH in: `flyctl ssh console`
2. Check volume is mounted: `ls -la /data`
3. Check permissions: `chmod 777 /data`
4. Manually run migrations: `cd /app && alembic upgrade head`

### If Frontend Doesn't Load

1. Verify static files were built: `flyctl ssh console` then `ls /app/static`
2. Check CORS settings in environment variables

## Production Considerations

1. **Database Backups**: Create a cron job or GitHub Action to regularly backup your SQLite database
2. **Volume Snapshots**: Consider periodic volume snapshots via Fly.io
3. **Health Checks**: Already configured in fly.toml using `/api/health`
4. **HTTPS**: Automatically handled by Fly.io
5. **Monitor**: Use `flyctl dashboard` or visit dashboard.fly.io

## Notes

- SQLite is perfect for apps with <100k records and moderate traffic
- The database file persists in the `/data` volume across deploys
- For high-concurrency needs, consider upgrading to PostgreSQL
- Automatic backups are YOUR responsibility with SQLite
