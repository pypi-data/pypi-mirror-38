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

from boto3.dynamodb.conditions import Key, Attr

from metagenomi.helpers import is_unique_mgid
from metagenomi.helpers import get_country_codes
from metagenomi.helpers import basename


def get_efetch_cmd(wd, dry_run = False):
    '''
    Generates efetch command in a file places in wd
    :param wd: working directory
    :return: local file containing efetch command
    '''
    print(f'WD AT THIS POINT: {wd}')

    local_out = f'{wd}/efetch.sh'
    with open(local_out, 'w') as f:
        cmd = '#!/bin/bash\nBIOSAMPLE=$1\nOUTFILE=$2\n'
        cmd += 'esearch -db biosample -query $BIOSAMPLE | '
        cmd += 'efetch -format summary > $OUTFILE\n'
        f.write(cmd)

    os.chmod(local_out, stat.S_IXOTH | stat.S_IXUSR)

    # catmd = f'echo "{cmd}"'
    #
    # local_out = f'{wd}/efetch.sh'

    # if dry_run:
    #         print(f'{catmd} > {local_out}')

    # else:
    # with open(local_out, 'w') as f:
    #     subprocess.check_call(shlex.split(catmd), stdout=f)
    # subprocess.check_call(shlex.split(f'chmod 740 {local_out}'))
    #
    return local_out


def RepresentsInt(s):
    '''
    :return: True if string is also an int, False if not
    '''
    try:
        int(s)
        return True
    except ValueError:
        return False


def fill_required(sdict, req_atts):
    '''
    Fills in required attributes to a dictionary
    :param sdict: dictionary that may or may not contain req attributes
    :req_atts: Required attributes
    :return: Updated dictionary with required attributes
    '''
    # -values = S/W
    # +values = N/E
    # Lat = N/S
    # Lon = E/W

    if 'latitude and longitude' not in sdict:
        if 'latitude' in sdict and 'longitude' in sdict:
            latitude = sdict['latitude']
            longitude = sdict['longitude']
            lat = 'N'
            lon = 'E'
            if float(sdict['latitude']) <0:
                latitude = latitude[1:]
                lat = 'S'
            if float(sdict['longitude'])<0:
                longitude = longitude[1:]
                lon = 'W'

            latlon = f'{latitude} {lat} {longitude} {lon}'
            sdict['latitude and longitude'] = latlon
        else:
            sdict['latitude and longitude'] = 'NA'

    if 'collection date' not in sdict:
        print(f'Collection date not included: {sdict}')
        sdict['collection date']='NA'

    if 'geographic location' not in sdict:
        print(f'Geographic location not included: {sdict}')
        sdict['geographic location']='NA'

    if 'isolation source' not in sdict:
        #print(f'isolation source not included: {sdict}')
        if 'environment biome' in sdict:
            iso = sdict['environment biome']
            if 'environment feature' in sdict:
                i = sdict['environment feature']
                iso += f' / {i}'

            sdict['isolation source'] = iso
        else:
            sdict['isolation source'] = 'NA'

    for a in req_atts:
        if a not in sdict:
            sdict[a]='NA'
    return sdict


def parse_biosample(bsfile):
    '''
    Parses biosample file into dictionary of attributes
    :param bsfile: biosample file in 'summary' format
    :return: Dictionary in form: {BIOSAMPLE: {att1:X, att2:Y}}
    '''
    print('Biosample file = ', bsfile)
    bs_dict = {}
    required_atts = ['collection date', 'geographic location',
                    'latitude and longitude', 'isolation source']

    with open(bsfile) as bs:
        lines = bs.readlines()
        i = 0
        for i in range(len(lines)):
            l = lines[i]
            if 'Identifiers:' in l:
                single_sample_dict = {}
                biosample = l.split(';')[0].split(' ')[-1]
                sra = l.split('SRA: ')[-1].split(';')[0].rstrip()
                single_sample_dict['sra'] = sra

                j = i+3
                att = []
                while 'Accession' not in lines[j]:
                    att.append(lines[j].rstrip())
                    j+=1

                for a in att:
                    if '=' in a:
                        key = a.split('=')[0].split('/')[-1]
                        value = a.split('=')[-1].replace('"', '')
                        single_sample_dict[key] = value

                single_sample_dict_complete = fill_required(single_sample_dict,
                                                            required_atts)
                bs_dict[biosample] = single_sample_dict_complete

    print(bs_dict)
    return(bs_dict)


def fetch_BioSampleInfo(biosample, wd, dry_run=False):
    esearchcmd = f'esearch -db biosample -query {biosample}'
    efetchcmd = f'efetch -format summary'


    local_out = f'{wd}/biosample.txt'

    with open(f'{local_out}', 'w') as f:
        process_esearch = subprocess.Popen(shlex.split(esearchcmd),
                                        stdout=subprocess.PIPE,
                                        shell=False)

        process_efetch = subprocess.Popen(shlex.split(efetchcmd),
                                        stdin=process_esearch.stdout,
                                        stdout=f)

        process_esearch.stdout.close()
        process_esearch.wait()
        process_efetch.wait()
        if process_esearch.returncode != 0:
            raise RuntimeError('Exited "process_esearch" command in error')

    return parse_biosample(local_out)




def fetch_BioSampleInfoDEPRECATED(biosample, wd, dry_run=False):
    '''
    :param biosample: str format biosample accession number
    :param wd: str format working directory. No trailing '/'
    :return: dictionary of biosample attributes
    '''


    efetchcmd = get_efetch_cmd(wd)
    print(f'efetch command = {efetchcmd}')

    local_out = f'{wd}/biosample.txt'
    cmd = f'{efetchcmd} {biosample} {local_out}'

    if dry_run:
            print(f'{cmd}')

    else:
        subprocess.check_call(shlex.split(cmd))

        return parse_biosample(local_out)
    return(f'ERROR, unable to find biosample {biosample}')


def fetch_SraRunInfo(sra, wd, dry_run = False):
    '''
    :param sra: Sra accession id
    :param wd: str format working directory. No trailing '/'
    :return: pandas dataframe of RunInfo for given accession
    '''
    if 'RR' not in sra:
        print('NOOOOO ', sra)

    url = 'http://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?save=efetch&db=sra&rettype=runinfo&term='
    url+= sra
    local_out = f'{wd}/sra.info'
    cmd = f'wget -q -O {local_out} '
    cmd+= f'"{url}"'

    if dry_run:
        print('--- dry run ---')
        print(cmd)

    else:
        subprocess.check_call(shlex.split(cmd))
        df = pd.read_csv(local_out)
        return(df)

    return('dry run')


def generate_sra_sample_json(sra, wd, dry_run=False):
    '''
    :param sra: Sra accession id
    :param wd: str format working directory. No trailing '/'
    :return: dictionary of SRA metadata
    '''

    sradf = fetch_SraRunInfo(sra, wd, dry_run)

    sradf = sradf.dropna(axis='columns')
    sradf = sradf.drop(columns=['download_path', 'RunHash', 'ReadHash'],
                       errors = 'ignore')

    sradict = sradf.to_dict('records')[0]

    return(sradict)


def add_to_archive(mg_id, key, value, writenew=True, **dbargs):
    dbname = dbargs['dbname']
    region = dbargs['region']

    if 'dry_run' in dbargs and dbargs['dry_run']==True:
        print('----dry_run----')
        print(f'Would add {key}:{value} to the database {dbname}')

    else:
        if is_unique_mgid(mg_id, dbname) and not writenew:
            raise ValueError(f'ERROR: {mg_id} not yet in the database. ')
            # ADD IT IN????
        else:
            db = boto3.resource('dynamodb', region_name=region)
            table = db.Table(dbname)
            response = table.update_item(
                Key={
                    'mg-identifier': mg_id
                },
                UpdateExpression=f"set {key} = :r",
                ExpressionAttributeValues={
                    ':r': value,
                },
                ReturnValues="UPDATED_NEW"
            )


def change_s3_path(mg_id, newpath, **dbargs):
    s3_path = 's3-path'
    dbname = dbargs['dbname']
    region = dbargs['region']

    db = boto3.resource('dynamodb', region_name=region)
    table = db.Table(dbname)
    response = table.update_item(
        Key={
            'mg-identifier': mg_id
        },
        UpdateExpression=f"set #fn = :r",
        ExpressionAttributeNames={
            '#fn':s3_path
        },
        ExpressionAttributeValues={
            ':r': newpath
        },
        ReturnValues="UPDATED_NEW"
    )



def archive_data(mg_id, mg_type, key, value, proj, date_added,
                associations,
                s3path,
                sra_id,
                overwrite = False,
                **kwargs):
    '''
    Archives data using batch writer
    '''

    dbname = kwargs['dbname']
    region = kwargs['region']

    if 'dry_run' in kwargs and kwargs['dry_run'] == True:
        print("------DRY RUN-----")
        print(f'Would write to database {dbname}')
        test = {
                 'mg-identifier':mg_id,
                 'mg-object':mg_type,
                 's3-path':s3path,
                 'sra-id':sra_id,
                 'mg-project':proj,
                 'date_added':date_added,
                 'associated':associations,
                 key:value
                 }
        print(test)
        return()


    else:
        if overwrite == False:
            if not is_unique_mgid(mg_id, dbname):
                raise ValueError(f'Not authorized to overwrite and mg-id \
                                {mg_id} already exists')


        if mg_type not in ['read', 'sample', 'assembly']:
            raise ValueError(f'Invalid data type "{mg_type}"')

        db = boto3.resource('dynamodb', region_name=region)
        tbl = db.Table(dbname)

        print(f'FROM METADATA: IMPORTING {mg_id} right now')
        with tbl.batch_writer() as batch:
            batch.put_item(
                Item={
                     'mg-identifier':mg_id,
                     'mg-object':mg_type,
                     's3-path':s3path,
                     'sra-id':sra_id,
                     'mg-project':proj,
                     'date_added':date_added,
                     'associated':associations,
                     key:value
                }
            )
        return()


def generate_BioSample_id(read_id, biosample):
    '''
    Generates BioSample id based on input mg-identifier for a read
    '''
    bs_id = '_'.join(read_id.split('_')[:-1])
    bs_id = bs_id+'_SRA-samp'

    if is_unique_mgid(bs_id):
        return bs_id
    else:
        raise ValueError(f'Could not create unique biosample ID from {read_id}')


def get_htime():
    '''
    Returns current timestamp in human readable format
    '''
    t = time.time()
    return(datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S'))


def exists_in_db(key, value, **dbargs):
    '''
    write
    '''

    dynamodb = boto3.resource('dynamodb', region_name=dbargs['region'])
    table = dynamodb.Table(dbargs['dbname'])

    response = table.query(
                        IndexName=dbargs['index'],
                        KeyConditionExpression=Key(key).eq(value)
                        )

    if len(response['Items']) <1:
        return('NA')
    else:
        if len(response['Items']) > 1:
            raise ValueError(f'Multiple entries for {value} exist in {dbname} \
                            (index = {index})')
        else:
            return(response['Items'][0]['mg-identifier'])


def import_object_sra(sra, mg_id, s3path, wd, **kwargs):
    '''
    Imports a 'read' object from the SRA. If BioSample does not exist,
    imports that too.
    :return: nothing
    '''

    proj_code = mg_id[:4]
    print(proj_code)

    # STEP 1: Check if mg-id exists in the database
    if 'NA' in exists_in_db('sra-id', sra, **kwargs):
        print(f'working on: {sra}')
        # If it does not yet, generate timestamp, sra metadata, biosample,
        # biosample metadata
        ts = get_htime()
        sraMD = generate_sra_sample_json(sra, wd)
        biosample = sraMD['BioSample']
        # print(get_efetch_cmd(wd))
        bsMD = fetch_BioSampleInfo(biosample, wd)
        print('bsMD = ', bsMD)

        if len(bsMD) > 1:
            print('OH NO!! Multiple biosamples retrieved')


        # STEP 2: Check if biosample exists in the database
        if 'NA' in exists_in_db('sra-id', biosample, **kwargs):
            print(f'Associated biosample {biosample} not \
                represented in the DB')

            # If not, generate associations, mg-id for the biosample,
            assoc = {'read':[mg_id]}
            bs_id = generate_BioSample_id(mg_id, biosample)

            # Archive it
            archive_data(bs_id,'sample', 'metadata', bsMD[biosample],
                    proj_code, ts, assoc, s3path, sra_id=biosample, **kwargs)

        # If biosample does exist, fetch its mg-id
        else:
            bs_id = exists_in_db('sra-id', biosample, **kwargs)

        # STEP 3: Archive sra read object
        print(f'Archiving {mg_id}...')
        assoc = {'sample':[bs_id]}
        archive_data(mg_id, 'read', 'metadata', sraMD, proj_code, ts,
                        assoc, s3path, sra_id=sra, **kwargs)

    else:
        print(f'{sra} already in database. Skipping.')



def import_object(type, mg_id, s3path, wd, sra=True, **kwargs):
    '''
    Wrapper script to import various types of objects into the metadata DB
    :param type: one of 'read' 'sample' 'assembly'
    :param mg_id: properly formatted mg-identifier
    :param wd: working directory
    :param sra: Boolean: does data have an sra accn?
    :return: nothing
    '''

    if not properly_formatted_mgid(mg_id, False):
        raise ValueError(f'Improperly formated mg-identifier "{mg_id}"')

    if type not in ['read', 'assembly', 'sample']:
        raise ValueError(f'Invalid data type "{type}"')

    if sra:
        import_object_sra(kwargs['accn'], mg_id, s3path, wd, **kwargs)

    if type == 'assembly':
        ts = get_htime()
        key = kwargs['key']
        value = kwargs['value']
        associations = kwargs['assoc']
        project = mg_id[:4]

        proj = # GET PROJECT from mg_id
        archive_data(mg_id, type, key, value, project, ts,
                        associations,
                        s3path,
                        'NA',
                        overwrite = False,
                        **kwargs)


def get_mg_id(filename, filetype='read', **dbargs):
    if filetype not in ['read']:
        raise ValueError(f'cannot find mg-identifier in {filename}')

    if 'read' in filetype:
        mgid = basename(filename)
        print(f'Basename = {mgid}')
        if properly_formatted_mgid(mgid):
            return(mgid)
        if properly_formatted_mgid(mgid[:22]):
            return(mgid[:22])
        # Check if named with SRA id
        else:
            sraid = mgid.split('.')[0].split('_')[0]
            if 'RR' in sraid:
                if 'NA' in exists_in_db('sra-id', sraid, **dbargs):
                    raise ValueError(f'cannot find mg-identifier in {filename}')
                else:
                    return exists_in_db('sra-id', sraid, **dbargs)
            else:
                raise ValueError(f'cannot find mg-identifier in {filename}')


def properly_formatted_mgid(mgid, verbose=False):
    '''
    Check if mg-identifier is properly formatted
    :mgid: string
    :return: True or False

    :::TEST SUITE:::
    >>> print(properly_formatted_mgid('HYDR_0001_USA_SRA-read'))
    True
    >>> print(properly_formatted_mgid('HYDR_0000_USA_SRA-read'))
    True
    >>> print(properly_formatted_mgid('HYDR_9999_USA_SRA-assm'))
    True

    >>> print(properly_formatted_mgid('HYDR_000A_USA_SRA-read'))
    False
    >>> print(properly_formatted_mgid('HYDR_00011_USA_SRA-read'))
    False
    >>> print(properly_formatted_mgid('HYDR_0001_USA_SRA-reads'))
    False
    >>> print(properly_formatted_mgid('HYDR_0001_XSA_SRA-read'))
    False
    >>> print(properly_formatted_mgid('hydr_0001_USA_SRA-read'))
    False
    >>> print(properly_formatted_mgid('HYD_0001_USA_SRA-read'))
    False
    >>> print(properly_formatted_mgid('HYD0001_USA_SRA-read'))
    False
    >>> print(properly_formatted_mgid('HYDR_0001_USA_SRA_read'))
    False
    >>> print(properly_formatted_mgid('HYDA0001_USA_SRA_read'))
    False
    '''

    if verbose: print(f'Examining {mgid}')
    if len(mgid) == 22:
        if len(mgid.split('_')) == 4:
            p = mgid[:4]
            n = mgid.split('_')[1]
            c = mgid.split('_')[2]
            t = mgid.split('-')[-1]
            country_codes = get_country_codes()

            if p.isalpha() and p.isupper():
                if len(n) == 4:
                    if c.isalpha() and c in country_codes.values():
                        if t in ['read', 'samp', 'assm', 'tran']:
                            return True
                        elif verbose:
                            print(f'ending ({t}) is not "read", "samp", "assm", or "tran"')
                    elif verbose:
                        print(f'Country ({c}) is not capital or a valid code')
                elif verbose:
                    print(f'Num ({n}) is not an int, or is not 4 characters long')
            elif verbose:
                print(f'Project code ({p}) is not uppercase or alpha-characters')
        elif verbose:
            print(f'There are not 4 "_" in {mgid}')
    elif verbose:
        print(f'Length of ({mgid}) is not 22')

    return False


# def run_tests():
    # wd = '/Users/audra/work/mginfra/mg-data-fetcher'
    # d = {'contaminant_removal': {'contaminants': '30',
    #     'total_removed': '30'}, 'adapter_removal': {'total_reads': '4600284',
    #         'total_bases': '496830672', 'FTrimmed': '4600284', 'KTrimmed': '7462',
    #          'trimmed_by_overlap': '2812', 'total_removed': '40'},
    #          'quality_trimming': {'total_removed': '0', 'done': True}}
    #
    # add_to_archive('HTSP_1111_ISL_SRA-read', 'bbmap_metadata', d,
    #     dbname='mg-project-metadata', region='us-west-2')

    # change_s3_path('HTSP_0004_ISL_SRA-read', 's3://metagenomi/projects/hot-springs/reads/qc/ERR2529108/ERR2529108',
                # dbname='mg-project-metadata', region='us-west-2')
    # print(get_mg_id('/Users/audra/work/mginfra/mg-bbmap/HTSP_0004_ISL_SRA-read.fastq.gz', 'read'))
    # Exists in DB tests
    # print(exists_in_db('sra-id', 'SRR1747023', index='sra-id-index', dbname='mg-project-metadata', region='us-west-2'))

    # s3path = 'TEST_PATH'
    # import_object("read", 'BOON_0001_KEN_SRA-read', 'TEST PATH', wd, accn='SRR1747023', sra=True, index='sra-id-index', dbname='mg-project-metadata', region='us-west-2', dry_run = True)
    # import_object_sra('SRR1747023', 'BOON_0001_KEN_SRA-read', 'BOON', wd)

    # f = 's3://metagenomi/projects/test/ERR1662530/ERR1662530.gz'
    # d = get_mg_id(f, filetype='read', dbname = 'mg-project-metadata', region='us-west-2', index='sra-id-index')

#     wd = '/Users/audra/work/mginfra/metagenomi/metagenomi'
#     fetch_BioSampleInfo('SAMEA2341965', wd)
#     # print(d)
#
#
# if __name__ == '__main__':
#     # doctest.testmod()
#     run_tests()
#     pass
