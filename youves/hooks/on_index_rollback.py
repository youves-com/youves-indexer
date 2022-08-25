from typing import Union

from dipdup.config import PostgresDatabaseConfig, SqliteDatabaseConfig
from dipdup.context import HookContext
from dipdup.enums import ReindexingReason
from dipdup.index import Index

import youves.backups as backups


async def on_index_rollback(
    ctx: HookContext,
    index: Index,
    from_level: int,
    to_level: int,
) -> None:
    # TODO(florin): Change the backup file from date to level, and use the most recent
    # level-6 back-up.

    """Hook to define what happens when the indexer rollback is happening."""
    await ctx.execute_sql("on_index_rollback")

    database_config: Union[
        SqliteDatabaseConfig, PostgresDatabaseConfig
    ] = ctx.config.database

    if database_config.kind != "postgres":
        await ctx.reindex(ReindexingReason.rollback)

    backup = backups.get_most_recent_backup()
    if not backup:
        await ctx.reindex(ReindexingReason.rollback)
    else:
        try:
            backups.restore(backup, database_config)
            await ctx.restart()
        except Exception:
            await ctx.reindex(ReindexingReason.rollback)
