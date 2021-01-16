from typing import List

from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from data import load_users, load_parties, load_coalitions, \
    load_topics_distributions
from models import *
from response import TopicDistribution

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"])

users = load_users()
parties = load_parties()
coalitions = load_coalitions()

topics_dist = load_topics_distributions()


@app.get("/user")
async def get_all_users() -> List[User]:
    return users


@app.get("/user/{username}")
async def get_user(username: str) -> User:
    user = next((user for user in users if user.username == username), None)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found')
    else:
        return user


@app.get("/user/{username}/topic", response_model=List[TopicDistribution])
async def get_topics_by_username(username: str):
    topics_per_user = topics_dist['per_user']

    if username not in topics_per_user.keys():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found')
    else:
        return topics_per_user[username]


@app.get("/party")
async def get_all_parties() -> List[Party]:
    return parties


@app.get("/party/{party_id}")
async def get_party(party_id: int) -> Party:
    party = next((party for party in parties if party.party_id == party_id),
                 None)

    if party is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Party not found')
    else:
        return party


@app.get("/party/{party_id}/topic", response_model=List[TopicDistribution])
async def get_topics_by_party(party_id: int):
    topics_per_party = topics_dist['per_party']

    party = next((party for party in parties if party.party_id == party_id),
                 None)

    if party is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Party not found')
    else:
        return topics_per_party[party.name]


@app.get("/coalition")
async def get_all_coalitions() -> List[Coalition]:
    return coalitions


@app.get("/coalition/{coalition_id}")
async def get_coalition(coalition_id: int) -> Coalition:
    coalition = next((coalition for coalition in coalitions if
                      coalition.coalition_id == coalition_id), None)

    if coalition is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Coalition not found')
    else:
        return coalition


@app.get("/coalition/{coalition_id}/topic",
         response_model=List[TopicDistribution])
async def get_topics_by_coalition(coalition_id: int):
    topics_per_coalition = topics_dist['per_coalition']

    coalition = next((coalition for coalition in coalitions if
                      coalition.coalition_id == coalition_id), None)

    if coalition is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Party not found')
    else:
        return topics_per_coalition[coalition.name]
