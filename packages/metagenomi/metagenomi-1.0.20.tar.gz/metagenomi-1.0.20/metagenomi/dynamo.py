'''
import pandas as pd
import boto3
import json
import shlex
import subprocess
import time
import datetime
import doctest
import os
import stat

class MgObj:

    Class all three object types will inherit from.

    Functions:

    write to dynamo
    get mg-identifier
    delete from dynamo
    rename

    ATTS:
    associated
    project
    date added
    s3 path



    def __init__():
        pass

class MgAssembly:
    pass

class MgRead:
    pass

class MgSample:
    pass


def get_mg_id(sra, dbname='mg-project-metadata',
                   region='us-west-2',
                   index='sra-id-index'):


    Given an SRA id, return mg-identifer


    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(dbname)

    response = table.query(
                        IndexName=index,
                        KeyConditionExpression=Key('sra-id').eq(sra)
                        )

    if len(response['Items']) <1:
        return('NA')
    else:
        if len(response['Items']) > 1:
            raise ValueError(f'Multiple entries for {value} exist in {dbname} \
                            (index = {index})')
        else:
            return(response['Items'][0]['mg-identifier'])


def get_metadata(mg_id, dbname='mg-project-metadata',
                        region='us-west-2',
                        index='sra-id-index'):

    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(dbname)

    response = table.get_item(
        Key={
            'mg-identifier': mg_id,
            }
        )

    if 'Item' in response:
        # Figure out what the item is and
        return

    return True


'''
