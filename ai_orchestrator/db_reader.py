import os
import psycopg2
from psycopg2.extras import RealDictCursor

def env(name: str, default=None):
    v = os.environ.get(name, default)
    if v is None:
        raise RuntimeError(f"Missing env var: {name}")
    return v

def conn():
    return psycopg2.connect(
        host=env("PATCH_DB_HOST"),
        port=int(env("PATCH_DB_PORT","5432")),
        dbname=env("PATCH_DB_NAME"),
        user=env("PATCH_DB_USER"),
        password=env("PATCH_DB_PASSWORD"),
    )

def fetch_summary(table: str):
    q = f"""
    SELECT
      count(*) AS total,
      count(*) FILTER (WHERE pre_reboot='success') AS pre_ok,
      count(*) FILTER (WHERE pre_reboot='failed')  AS pre_fail,
      count(*) FILTER (WHERE apply_patch='success') AS patch_ok,
      count(*) FILTER (WHERE apply_patch='failed')  AS patch_fail,
      count(*) FILTER (WHERE post_reboot='success') AS reboot_ok,
      count(*) FILTER (WHERE post_reboot='failed')  AS reboot_fail,
      count(*) FILTER (WHERE post_check='success') AS post_ok,
      count(*) FILTER (WHERE post_check='failed')  AS post_fail,
      count(*) FILTER (WHERE kernel_check='success') AS kernel_ok,
      count(*) FILTER (WHERE kernel_check='failed')  AS kernel_fail
    FROM {table};
    """
    with conn() as c, c.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(q)
        return cur.fetchone()

def fetch_failures(table: str, limit: int = 20):
    q = f"""
    SELECT server,
           pre_reboot, pre_reboot_reason, pre_reboot_summary,
           apply_patch, apply_patch_reason, apply_patch_summary,
           post_reboot, post_reboot_reason, post_reboot_summary,
           post_check, post_check_reason, post_check_summary,
           kernel_check, kernel_check_reason, kernel_check_summary
    FROM {table}
    WHERE pre_reboot='failed'
       OR apply_patch='failed'
       OR post_reboot='failed'
       OR post_check='failed'
       OR kernel_check='failed'
    ORDER BY server
    LIMIT %s;
    """
    with conn() as c, c.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(q, (limit,))
        return cur.fetchall()
