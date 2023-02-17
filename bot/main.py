from bot.handlers.start import router as start
from bot.app import bot, dp

dp.include_router(start)
dp.run_polling(bot, allowed_updates=dp.resolve_used_update_types())
