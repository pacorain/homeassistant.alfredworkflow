"""Script for getting the state of entities"""

import aiohttp
import asyncio
import os
import sys
import json

async def main():
    try:
        hass_url = os.getenv('HASS_URL')
        hass_api_key = os.getenv('HASS_API_KEY')
        query = sys.argv[1] if len(sys.argv) > 1 else None
        result = await process_query(query, hass_url, hass_api_key)
        print(json.dumps(result))
        
    except:
        print_error()
        raise

async def process_query(query, hass_url, hass_api_key):
    states = await fetch_states(hass_url, hass_api_key)
    query_args = query.split()
    if len(query_args) < 1 or query_args[0] == '':
        return {
            'items': [
                {
                    'title': entity.get('entity_id'),
                    'subtitle': entity.get('state'),
                    'uid': entity.get('entity_id'),
                    'autocomplete': entity.get('entity_id'),
                    'text': entity.get('state'),
                    'arg': entity.get('entity_id')
                } for entity in states
            ]
        }
    states_filtered = []
    for state in states:
        if state['entity_id'] == query_args[0]:
            states_filtered = [state]
            break
        elif query_args[0] in state['entity_id']:
            states_filtered.append(state)
    if len(states_filtered) > 1:
        return {
            'items': [
                {
                    'title': entity.get('entity_id'),
                    'subtitle': entity.get('state'),
                    'uid': entity.get('entity_id'),
                    'autocomplete': entity.get('entity_id'),
                    'text': entity.get('state'),
                    'arg': entity.get('entity_id')
                } for entity in states_filtered
            ],
            'rerun': 1
        }
    elif len(states_filtered) == 0:
        return {
            'items': [
                {
                    'title': 'No entities found',
                    'subtitle': 'Try a different query.',
                    'valid': False
                }
            ]
        }
    found_entity = states_filtered[0]
    items = []
    if len(query_args) < 2 or query_args[1] == '':
        items.append({
            'title': found_entity.get('entity_id') + ' state',
            'subtitle': found_entity.get('state'),
            'text': found_entity.get('state'),
            'arg': found_entity.get('entity_id')
        },)
    if len(found_entity['attributes']) == 0:
        items.append({
            'title': 'No attributes',
            'subtitle': "This entity doesn't have any attributes to search.",
            'valid': False
        })
        return {'items': items, 'rerun': 1}
    for key, val in found_entity['attributes'].items():
        if len(query_args) < 2 or query_args[1] in key:
            items.append(
                {
                    'title': 'Attribute ' + key,
                    'subtitle': val,
                    'text': val,
                    'arg': found_entity.get('entity_id'),
                    'uid': found_entity.get('entity_id') + '.' + key
                }
            )
    return {'items': items, 'rerun': 1}

async def fetch_states(hass_url, hass_api_key) -> dict:
    async with aiohttp.ClientSession(headers={'Authorization': 'Bearer ' + hass_api_key}) as session:
        async with session.get(hass_url + '/api/states') as response:
            if response.status >= 400:
                error_message = await response.text()
                raise ValueError(error_message)
            return await response.json()

async def render_template(template, hass_url, hass_api_key) -> str:
    template_url = f'{hass_url}/api/template'
    
    async with aiohttp.ClientSession(headers={'Authorization': 'Bearer ' + hass_api_key}) as session:
        async with session.post(template_url, json={'template': template}) as response:
            text = await response.text()
            if response.status >= 400:
                raise ValueError(text)
            return text

def print_error():
    print(json.dumps({
        'items': [
            {
                'title': 'Something went wrong',
                'subtitle': 'Please debug in Alfred',
                'valid': False
            }
        ]
    }))

if __name__ == '__main__':
    asyncio.run(main())