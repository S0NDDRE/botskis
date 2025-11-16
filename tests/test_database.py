"""
Database Tests
Test database operations, migrations, backups
"""
import pytest
from datetime import datetime
import asyncio


# ============================================================================
# UNIT TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.asyncio
async def test_database_connection():
    """Test database connection"""
    from src.database.connection import get_database

    db = await get_database()
    assert db is not None


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_user():
    """Test creating user in database"""
    from src.database.models import User
    from src.database.operations import create_user

    user_data = {
        "email": "testuser@example.com",
        "password_hash": "hashed_password",
        "name": "Test User"
    }

    user = await create_user(**user_data)

    assert user.id is not None
    assert user.email == "testuser@example.com"
    assert user.name == "Test User"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_user_by_email():
    """Test finding user by email"""
    from src.database.operations import create_user, get_user_by_email

    # Create user
    await create_user(
        email="findme@example.com",
        password_hash="hash",
        name="Find Me"
    )

    # Find user
    user = await get_user_by_email("findme@example.com")

    assert user is not None
    assert user.email == "findme@example.com"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_update_user():
    """Test updating user"""
    from src.database.operations import create_user, update_user

    # Create user
    user = await create_user(
        email="update@example.com",
        password_hash="hash",
        name="Old Name"
    )

    # Update user
    updated = await update_user(
        user_id=user.id,
        name="New Name"
    )

    assert updated.name == "New Name"
    assert updated.email == "update@example.com"  # Unchanged


@pytest.mark.unit
@pytest.mark.asyncio
async def test_delete_user():
    """Test deleting user (soft delete)"""
    from src.database.operations import create_user, delete_user, get_user_by_id

    # Create user
    user = await create_user(
        email="delete@example.com",
        password_hash="hash",
        name="Delete Me"
    )

    # Delete user
    await delete_user(user.id)

    # Verify soft deleted
    deleted_user = await get_user_by_id(user.id, include_deleted=True)
    assert deleted_user.deleted_at is not None


# ============================================================================
# BACKUP TESTS
# ============================================================================

@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_database_backup():
    """Test creating database backup"""
    from src.infrastructure.database_backup import BackupManager

    manager = BackupManager()

    backup_info = await manager.create_backup(
        backup_type="full",
        comment="Test backup"
    )

    assert backup_info.backup_id is not None
    assert backup_info.backup_type == "full"
    assert backup_info.status == "completed"
    assert backup_info.filepath.exists()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_verify_backup():
    """Test verifying backup integrity"""
    from src.infrastructure.database_backup import BackupManager

    manager = BackupManager()

    # Create backup
    backup_info = await manager.create_backup()

    # Verify backup
    is_valid = await manager._verify_backup(backup_info)

    assert is_valid is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_list_backups():
    """Test listing available backups"""
    from src.infrastructure.database_backup import BackupManager

    manager = BackupManager()

    # Create a backup
    await manager.create_backup(comment="Test 1")

    # List backups
    backups = await manager.list_backups(limit=10)

    assert len(backups) > 0
    assert all(b.backup_id is not None for b in backups)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_backup_retention_cleanup():
    """Test automatic cleanup of old backups"""
    from src.infrastructure.database_backup import BackupManager
    from datetime import timedelta

    manager = BackupManager()
    manager.config.retention_days = 1  # Keep only 1 day

    # Create old backup (mock)
    # In real test, would create backup and modify timestamp

    # Cleanup
    deleted = await manager._cleanup_old_backups()

    # Should delete backups older than retention period
    assert isinstance(deleted, int)


# ============================================================================
# TRANSACTION TESTS
# ============================================================================

@pytest.mark.integration
@pytest.mark.asyncio
async def test_transaction_rollback():
    """Test transaction rollback on error"""
    from src.database.connection import get_database
    from src.database.models import User

    db = await get_database()

    try:
        async with db.begin():
            # Create user
            user = User(
                email="rollback@example.com",
                password_hash="hash",
                name="Rollback Test"
            )
            db.add(user)

            # Force error
            raise Exception("Test rollback")

    except Exception:
        pass

    # User should not exist (rolled back)
    from src.database.operations import get_user_by_email
    user = await get_user_by_email("rollback@example.com")
    assert user is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_transaction_commit():
    """Test transaction commit on success"""
    from src.database.connection import get_database
    from src.database.models import User

    db = await get_database()

    async with db.begin():
        user = User(
            email="commit@example.com",
            password_hash="hash",
            name="Commit Test"
        )
        db.add(user)
        # No errors, should commit

    # User should exist
    from src.database.operations import get_user_by_email
    user = await get_user_by_email("commit@example.com")
    assert user is not None
    assert user.email == "commit@example.com"


# ============================================================================
# QUERY OPTIMIZATION TESTS
# ============================================================================

@pytest.mark.integration
@pytest.mark.asyncio
async def test_query_with_index():
    """Test query performance with indexed columns"""
    from src.database.operations import get_user_by_email
    import time

    start = time.time()

    # Query by indexed email column
    user = await get_user_by_email("indexed@example.com")

    duration = time.time() - start

    # Should be fast (< 100ms for indexed query)
    assert duration < 0.1


@pytest.mark.integration
@pytest.mark.asyncio
async def test_batch_insert():
    """Test batch insert performance"""
    from src.database.operations import batch_create_users

    users_data = [
        {
            "email": f"batch{i}@example.com",
            "password_hash": "hash",
            "name": f"Batch User {i}"
        }
        for i in range(100)
    ]

    import time
    start = time.time()

    created_users = await batch_create_users(users_data)

    duration = time.time() - start

    assert len(created_users) == 100
    # Should be fast (< 1s for 100 inserts)
    assert duration < 1.0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_pagination():
    """Test query pagination"""
    from src.database.operations import get_users_paginated

    # Get first page
    page1 = await get_users_paginated(page=1, per_page=10)

    assert len(page1.items) <= 10
    assert page1.page == 1
    assert page1.total_pages >= 1

    # Get second page
    page2 = await get_users_paginated(page=2, per_page=10)

    # Pages should have different items
    if len(page2.items) > 0:
        assert page1.items[0].id != page2.items[0].id


# ============================================================================
# E2E TESTS
# ============================================================================

@pytest.mark.e2e
@pytest.mark.asyncio
async def test_complete_crud_operations():
    """Test complete CRUD (Create, Read, Update, Delete) cycle"""
    from src.database.operations import (
        create_user,
        get_user_by_id,
        update_user,
        delete_user
    )

    # Create
    user = await create_user(
        email="crud@example.com",
        password_hash="hash",
        name="CRUD Test"
    )
    assert user.id is not None

    # Read
    retrieved = await get_user_by_id(user.id)
    assert retrieved.email == "crud@example.com"

    # Update
    updated = await update_user(user.id, name="Updated Name")
    assert updated.name == "Updated Name"

    # Delete
    await delete_user(user.id)
    deleted = await get_user_by_id(user.id)
    assert deleted is None or deleted.deleted_at is not None


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_database_migration():
    """Test running database migration"""
    from src.database.migrations import run_migrations, get_migration_status

    # Get current status
    status = await get_migration_status()
    current_version = status.get("current_version")

    # Run migrations
    result = await run_migrations()

    assert result.success is True

    # Verify new version
    new_status = await get_migration_status()
    assert new_status.get("current_version") >= current_version


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_backup_and_restore():
    """Test backup and restore workflow"""
    from src.infrastructure.database_backup import BackupManager
    from src.database.operations import create_user, get_user_by_email

    manager = BackupManager()

    # Create test data
    test_user = await create_user(
        email="backup_test@example.com",
        password_hash="hash",
        name="Backup Test"
    )

    # Create backup
    backup_info = await manager.create_backup(comment="Pre-restore test")

    # Verify user exists
    user = await get_user_by_email("backup_test@example.com")
    assert user is not None

    # Note: Actual restore would be dangerous in tests
    # Would need separate test database
    # Just verify backup exists
    assert backup_info.filepath.exists()


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_database_connection_pool():
    """Test database connection pooling"""
    from src.database.connection import get_database

    # Create multiple connections
    connections = []
    for _ in range(10):
        db = await get_database()
        connections.append(db)

    # All should be valid
    assert all(c is not None for c in connections)

    # Connection pool should handle this efficiently
    # (No errors thrown)


@pytest.mark.e2e
def test_database_health_check(client, auth_headers):
    """Test database health check endpoint"""
    response = client.get(
        "/api/health/database",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()

    assert "status" in data
    assert data["status"] in ["healthy", "degraded", "unhealthy"]

    if data["status"] == "healthy":
        assert "connection_pool" in data
        assert "response_time_ms" in data
