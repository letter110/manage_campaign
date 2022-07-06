import uvicorn
from model import *
import pymongo
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
import time


app = FastAPI()

logger = logging.getLogger('RotatingFileHandler')
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    './log/mylog.log', maxBytes=5000, backupCount=10)
formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


client = pymongo.MongoClient(
    "mongodb+srv://test:HHmm123456@cluster0.sheu0ff.mongodb.net/?retryWrites=true&w=majority")

db = client['mydb']
collection = db['campaigns']

# customer_data = [
#     Cutomer(name='duc', phone_number='012589', any='big brain'),
#     Cutomer(name='thu', phone_number='024587', any='big hand'),
#     Cutomer(name='lanh', phone_number='036549', any='so cool'),
#     Cutomer(name='quang', phone_number='042985', any='digital'),
#     Cutomer(name='le', phone_number='032569', any='trap girl')]

# schedule = Schedule(time=10, loop=True, isStarting=True)

# camp: Campaign = Campaign(
#     id=UUID('78007dc0-fc3e-11ec-aa2a-c0b88376b4ba'), name='go to school', cutomer_data=customer_data, schedule=schedule)


def checkExist(id: UUID):
    check = len(list((collection.find({'id': id})))) != 0
    return check


@app.post('/creating')
async def create(campaign: Campaign):
    id = str(campaign.id)
    if checkExist(str(campaign.id)):
        logger.warning(
            'this id: {} is exsit so can\'t creat new campaign'.format(id))
        return 'exist'
    else:
        collection.insert_one(jsonable_encoder(campaign))
        logger.info('this campaign with id: {} is created'.format(id))
        return jsonable_encoder(campaign)


@app.put('/updating')
async def update(id: UUID, campaign: Campaign):
    if checkExist(str(id)):
        collection.update_many(
            {'id': str(id)}, {'$set': jsonable_encoder(campaign)})
        logger.info('campaign with id: {} is updated'.format(str(id)))

        return jsonable_encoder(campaign)
    else:
        logger.warning(
            'this id: {} is not found so can\'t update this campaign'.format(str(id)))
        return 'not found'


@app.put('/starting')
async def start(id: UUID):
    if checkExist(str(id)):
        campaign = collection.find({'id': str(id)})[0]
        campaign.pop('_id')
        schedule = campaign['schedule']
        schedule = {**schedule, 'isStarting': True}
        campaign = {**campaign, 'schedule': schedule}

        collection.update_many(
            {'id': str(id)}, {'$set': (campaign)})
        logger.info('campaign is started')

        cutomer_data = campaign['cutomer_data']
        for customer in cutomer_data:
            phone_number = customer['phone_number']
            logger.info('calling to: '+phone_number +
                        ' for notify  about campaign start')
            time.sleep(3)
        return jsonable_encoder(campaign)
    else:
        logger.warning(
            'this id: {} is not found so can\'t start this campaign'.format(str(id)))
        return 'not found'


@app.put('/stoping')
async def start(id: UUID):
    if checkExist(str(id)):
        campaign = collection.find({'id': str(id)})[0]
        campaign.pop('_id')
        schedule = campaign['schedule']
        schedule = {**schedule, 'isStarting': False}
        campaign = {**campaign, 'schedule': schedule}

        collection.update_many(
            {'id': str(id)}, {'$set': (campaign)})
        logger.info('campaign is stoped')

        cutomer_data = campaign['cutomer_data']
        for customer in cutomer_data:
            phone_number = customer['phone_number']
            logger.info('calling to: '+phone_number +
                        ' for notify  about campaign stop')
            time.sleep(3)
        return jsonable_encoder(campaign)
    else:
        logger.warning(
            'this id: {} is not found so can\'t stop this campaign'.format(str(id)))
        return 'not found'


@app.put('/disabling')
async def start(id: UUID):
    if checkExist(str(id)):
        campaign = collection.find({'id': str(id)})[0]
        campaign.pop('_id')

        schedule = campaign['schedule']
        schedule = {**schedule, 'time': 0, 'runtime': 0}
        campaign = {**campaign, 'schedule': schedule}
        collection.update_many(
            {'id': str(id)}, {'$set': (campaign)})
        logger.info('campaign is stoped')

        cutomer_data = campaign['cutomer_data']
        for customer in cutomer_data:
            phone_number = customer['phone_number']
            logger.info('calling to: '+phone_number +
                        ' for notify  about campaign disable')
            time.sleep(3)
        return jsonable_encoder(campaign)
    else:
        logger.warning(
            'this id: {} is not found so can\'t disable this campaign'.format(str(id)))
        return 'not found'


@app.put('/duplicating')
async def duplicate(id: UUID):
    if checkExist(str(id)):
        campaign = collection.find({'id': str(id)})[0]
        campaign.pop('_id')

        schedule = campaign['schedule']
        schedule = {**schedule, 'loop': False}
        campaign = {**campaign, 'schedule': schedule}
        collection.update_many(
            {'id': str(id)}, {'$set': (campaign)})
        logger.info('campaign is duplicate')
        return jsonable_encoder(campaign)
    else:
        logger.warning(
            'this id: {} is not found so can\'t duplicate this campaign'.format(str(id)))
        return 'not found'

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)


# uvicorn main:app --reload --host 0.0.0.0 --port 8000
