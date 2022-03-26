"""Script for running templates and printing the output"""

import aiohttp
import asyncio
import os
import sys
import json

async def main():
    try:
        hass_url = os.getenv('HASS_URL')
        hass_api_key = os.getenv('HASS_API_KEY')
        template = get_template(sys.argv[1])
        result = await render_template(template, hass_url, hass_api_key)
        print(json.dumps({
            'items': [
                {'title': result}
            ]
        }))
    except:
        print_error()
        raise

def get_template(input: str):
    output = input.strip()
    if not output.startswith('{{'):
        output = '{{' + output
    if output.count('{{') > output.count('}}'):
        output = output + '}}'
    return output

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