from typing import Dict, List, Any
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import PATCH_DB_HOST, PATCH_DB_PORT, PATCH_DB_NAME, PATCH_DB_USER, PATCH_DB_PASSWORD


def _conn():
    if not all([PATCH_DB_HOST, PATCH_DB_USER, PATCH_DB_PASSWORD]):
        raise RuntimeError("DB env vars missing. Set PATCH_DB_HOST/USER/PASSWORD or use --simulate.")
    return psycopg2.connect(
        host=PATCH_DB_HOST,
        port=PATCH_DB_PORT,
        dbname=PATCH_DB_NAME,
        user=PATCH_DB_USER,
        password=PATCH_DB_PASSWORD,
    )


def fetch_summary(table: str) -> Dict[str, Any]:
    # You can customize these columns to match your table design
    q = f"""
      SELECT
        count(*) as total,
        count(*) filter (where pre_reboot='success') as pre_reboot_ok,
        count(*) filter (where pre_reboot='failed')  as pre_reboot_fail,
        count(*) filter (where apply_patch='success') as apply_patch_ok,
        count(*) filter (where apply_patch='failed')  as apply_patch_fail,
        count(*) filter (where post_reboot='success') as post_reboot_ok,
        count(*) filter (where post_reboot='failed')  as post_reboot_fail,
        count(*) filter (where kernel_check='yes')    as kernel_ok,
        count(*) filter (where kernel_check='no')     as kernel_fail
      FROM {table};
    """

    with _conn() as c:
        with c.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(q)
            return dict(cur.fetchone() or {})


def fetch_failures(table: str, limit: int = 20) -> List[Dict[str, Any]]:
    q = f"""
      SELECT server,
             pre_reboot, pre_reboot_reason, pre_reboot_summary,
             apply_patch, apply_patch_reason, apply_patch_summary,
             post_reboot, post_reboot_reason, post_reboot_summary,
             kernel_check, kernel_check_reason, kernel_check_summary
      FROM {table}
      WHERE coalesce(pre_reboot,'')='failed'
         OR coalesce(apply_patch,'')='failed'
         OR coalesce(post_reboot,'')='failed'
         OR coalesce(kernel_check,'')='failed'
      ORDER BY server
      LIMIT %s;
    """
    with _conn() as c:
        with c.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(q, (limit,))
            return list(cur.fetchall() or [])
