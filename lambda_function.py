import json

from crypto_info import CryptoInfo

def lambda_handler(event, context):

    symbol = None
    try:
        query_params = event.get('queryStringParameters', {})
        print(query_params)
        if query_params:
            symbol = query_params.get('symbol', 'default_value_if_missing')

        if symbol is None:
            return {
                    'statusCode': 404,
                    'headers': {
                        'Access-Control-Allow-Headers': '*',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },
                    'body': json.dumps("input variable is missing")
            }


        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(CryptoInfo().get_price(symbol))
        }

    except Exception as err:
        return {
            'statusCode': 404,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(f"Something is error while processing, {err}")
        }
    