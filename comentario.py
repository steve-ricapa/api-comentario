import boto3
import json
import uuid
import os

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    body = event['body']
    if isinstance(body, str):
        body = json.loads(body)

    tenant_id = body['tenant_id']
    texto = body['texto']
    nombre_tabla = os.environ["TABLE_NAME"]
    nombre_bucket = os.environ["INGESTA_BUCKET"]
    # Proceso
    uuidv1 = str(uuid.uuid1())
    comentario = {
        'tenant_id': tenant_id,
        'uuid': uuidv1,
        'detalle': {
          'texto': texto
        }
    }
    dynamodb = boto3.resource('dynamodb')
    s3 = boto3.client('s3')
    table = dynamodb.Table(nombre_tabla)
    response = table.put_item(Item=comentario)
    s3.put_object(
        Bucket=nombre_bucket,
        Key=f'comentarios/{tenant_id}/{uuidv1}.json',
        Body=json.dumps(comentario),
        ContentType='application/json'
    )
    # Salida (json)
    print(comentario)
    return {
        'statusCode': 200,
        'comentario': comentario,
        'response': response
    }
