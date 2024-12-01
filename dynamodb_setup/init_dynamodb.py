import boto3

def create_tables():
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    
    # Example table for Users
    table = dynamodb.create_table(
        TableName='Users',
        KeySchema=[
            {'AttributeName': 'user_id', 'KeyType': 'HASH'},
        ],
        AttributeDefinitions=[
            {'AttributeName': 'user_id', 'AttributeType': 'S'},
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        },
    )
    print(f"Creating table {table.name}...")
    table.wait_until_exists()
    print(f"Table {table.name} created successfully!")

if __name__ == "__main__":
    create_tables()
