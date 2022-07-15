import uvicorn
from model import *
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from db import campaigns, running_campaigns
from tasks import call
import logging

app = FastAPI()


logging.basicConfig(filename='./log/mylog.log',
                    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def checkExist(id: UUID):
    check = len(list((campaigns.find({'id': str(id)})))) != 0
    return check


def checkRunning(id: UUID):
    check = len(list((running_campaigns.find({'id': str(id)})))) != 0
    return check


@app.post('/creating')
async def create(campaign: Campaign):
    id = str(campaign.id)
    if checkExist(str(campaign.id)):

        return {'status': 'exist'}
    else:
        campaigns.insert_one(jsonable_encoder(campaign))
        return jsonable_encoder(campaign)


@app.put('/updating')
async def update(id: UUID, campaign: Campaign):
    if checkExist(id):
        campaign.id = id
        campaigns.update_many(
            {'id': str(id)}, {'$set': jsonable_encoder(campaign)})
        return campaigns.find({'id': str(id)})
    else:
        return {'status': 'error'}


@app.post('/starting')
async def start(id: UUID):
    if checkExist(id) and not checkRunning(id):
        campaign = campaigns.find({'id': str(id)})[0]
        running_campaigns.insert_one(campaign)
        campaign.pop('_id')
        customer_data = campaign['customer_data']
        for customer in customer_data:
            phone_number = customer['phone_number']
            call.delay(phone_number, campaign['name'])
        return jsonable_encoder(campaign)
    else:
        return {'status': 'error'}


@app.delete('/stoping')
async def stop(id: UUID):
    if checkExist(id) and checkRunning(id):
        campaign = campaigns.find({'id': str(id)})[0]
        running_campaigns.delete_one({'id': str(id)})
        campaign.pop('_id')
        customer_data = campaign['customer_data']
        for customer in customer_data:
            phone_number = customer['phone_number']
            call.delay(phone_number, campaign['name'], isStart=False)
        return jsonable_encoder(campaign)
    else:
        return {'status': 'error'}


@app.delete('/disabling')
async def start(id: UUID):
    if checkRunning(id):
        running_campaigns.delete_one({'id': str(id)})
    if checkExist(id):
        campaigns.delete_one({'id': str(id)})
        return str(id)
    else:
        return {'status': 'error'}


@app.post('/duplicating')
async def duplicate(id: UUID):
    if checkExist(id):
        campaign = campaigns.find({'id': str(id)})[0]
        campaign.pop('_id')
        id = str(uuid4())
        campaign = {**campaign, 'id': id}
        campaigns.insert_one(campaign)
        return str(id)
    return {'status': 'error'}

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)


# uvicorn main:app --reload --host 0.0.0.0 --port 8000
