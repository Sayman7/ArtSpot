from celery.schedules import crontab



CHANNEL_LAYERS={
    'default':{
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_BEAT_SCHEDULE = {
    'delete_idle_lobbies': {
        'task': 'chat.tasks.delete_idle_lobbies',
        'schedule': crontab(minute=0, hour='*/1'),  # Runs every hour
    },
}
