import pickle
from celery_config import celery  # This imports the Celery instance configured above

@celery.task
def process_paladin(paladin_data):
    # Deserialize the Paladin object
    paladin = pickle.loads(paladin_data)
    # Processing code here
    return paladin