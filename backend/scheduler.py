# scheduler

from apscheduler.schedulers.background import BackgroundScheduler

from services.game_service import GameService


def schedule_cleanups():
    scheduler = BackgroundScheduler()
    scheduler.add_job(GameService.cleanup_empty_games, 'interval', minutes=1)
    scheduler.add_job(GameService.cleanup_finished_games, 'interval', minutes=1)
    scheduler.start()


