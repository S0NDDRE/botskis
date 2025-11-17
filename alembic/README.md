# Database Migrations with Alembic

This directory contains database migrations for the Mindframe platform.

## Quick Start

### Initialize Database (First Time)

```bash
# Apply all migrations
alembic upgrade head
```

### Create New Migration

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Manually create migration
alembic revision -m "Description of changes"
```

### Apply Migrations

```bash
# Upgrade to latest
alembic upgrade head

# Upgrade one version
alembic upgrade +1

# Upgrade to specific revision
alembic upgrade <revision_id>
```

### Rollback Migrations

```bash
# Downgrade one version
alembic downgrade -1

# Downgrade to specific revision
alembic downgrade <revision_id>

# Downgrade all (WARNING: destroys all data)
alembic downgrade base
```

### View Migration History

```bash
# Show current revision
alembic current

# Show migration history
alembic history

# Show detailed history
alembic history --verbose
```

## Production Deployment

### Step 1: Backup Database

```bash
# PostgreSQL backup
pg_dump -h localhost -U mindframe_user mindframe > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Step 2: Apply Migrations

```bash
# Set production database URL
export DATABASE_URL="postgresql://user:pass@host:5432/mindframe"

# Apply migrations
alembic upgrade head
```

### Step 3: Verify

```bash
# Check current revision
alembic current

# Test database connection
psql $DATABASE_URL -c "SELECT COUNT(*) FROM users;"
```

## Migration Files

### 001_initial_schema.py

Initial database schema with all core tables:

- **users**: User accounts with authentication
- **agents**: AI agent instances
- **agent_templates**: Marketplace agent templates
- **onboarding_sessions**: User onboarding wizard data
- **agent_runs**: Agent execution history
- **subscriptions**: Stripe subscription data
- **health_checks**: System health monitoring

## Troubleshooting

### "Can't locate revision identified by 'head'"

Database is not initialized. Run:

```bash
alembic upgrade head
```

### "Target database is not up to date"

Your database is behind. Apply pending migrations:

```bash
alembic upgrade head
```

### "Downgrade from 'head' to '<revision>' failed"

Check the downgrade() function in the migration file. You may need to manually fix data before downgrading.

### Database Connection Error

Check your DATABASE_URL in .env:

```bash
# .env
DATABASE_URL="postgresql://user:password@localhost:5432/mindframe"
```

## Best Practices

1. **Always backup before migrations** in production
2. **Test migrations** in staging environment first
3. **Review auto-generated migrations** before applying
4. **Never edit applied migrations** - create new ones instead
5. **Use transactions** for data migrations
6. **Document complex migrations** with comments

## Environment-Specific Migrations

### Development

```bash
# Auto-generate from model changes
alembic revision --autogenerate -m "Add new column"
```

### Staging

```bash
# Test migration before production
DATABASE_URL=$STAGING_DB_URL alembic upgrade head
```

### Production

```bash
# Backup first!
pg_dump $PROD_DB > backup.sql

# Apply with caution
DATABASE_URL=$PROD_DB_URL alembic upgrade head
```

## Common Migration Patterns

### Adding a Column

```python
def upgrade():
    op.add_column('users', sa.Column('phone', sa.String(), nullable=True))

def downgrade():
    op.drop_column('users', 'phone')
```

### Adding an Index

```python
def upgrade():
    op.create_index('ix_users_email', 'users', ['email'])

def downgrade():
    op.drop_index('ix_users_email')
```

### Data Migration

```python
from sqlalchemy import table, column

def upgrade():
    # Update existing data
    users_table = table('users', column('is_active', sa.Boolean))
    op.execute(
        users_table.update().values(is_active=True)
    )

def downgrade():
    pass
```

## Configuration

All migration configuration is in `alembic.ini` and `env.py`.

Database URL is automatically loaded from `config/settings.py`.

## Support

For migration issues, check:

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- Mindframe deployment guide
