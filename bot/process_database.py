import os
import ydb
import ydb.iam
import datetime
import string
import random

driver_config = ydb.DriverConfig(
    endpoint=os.getenv('YDB_ENDPOINT'), 
    database=os.getenv('YDB_DATABASE'),
    credentials=ydb.iam.MetadataUrlCredentials()
)

driver = ydb.Driver(driver_config)
# Wait for the driver to become active for requests.
driver.wait(fail_fast=True, timeout=5)
# Create the session pool instance to manage YDB sessions.
pool = ydb.SessionPool(driver)

def select_all(tablename):
    # create the transaction and execute query.
    text = f"SELECT * FROM `{tablename}`;"
    return pool.retry_operation_sync(lambda s: s.transaction().execute(
        text,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

def update_database(tablename, chat_id, field, value):
    text = f"UPDATE `{tablename}` SET {field}={value} WHERE chat_id={chat_id};"
    return pool.retry_operation_sync(lambda s: s.transaction().execute(
        text,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

def update_database_string(tablename, chat_id, field, value):
    text = f"UPDATE `{tablename}` SET {field}='{value}' WHERE chat_id={chat_id};"
    return pool.retry_operation_sync(lambda s: s.transaction().execute(
        text,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

def add_user_notifications(tablename, chat_id, is_notified=False, is_enabled=True, is_hourly=False):
    text = f"""INSERT INTO `{tablename}`
    SELECT
        {chat_id} as chat_id,
        {is_notified} as is_notified,
        {is_enabled} as is_enabled,
        {is_hourly} as is_hourly,
        '{str(datetime.datetime.utcnow())}' as datetime;"""
    return pool.retry_operation_sync(lambda s: s.transaction().execute(
        text,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

def select_user_status(tablename, chat_id):
    # create the transaction and execute query.
    text = f"SELECT * FROM `{tablename}` WHERE chat_id={chat_id};"
    return pool.retry_operation_sync(lambda s: s.transaction().execute(
        text,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))
