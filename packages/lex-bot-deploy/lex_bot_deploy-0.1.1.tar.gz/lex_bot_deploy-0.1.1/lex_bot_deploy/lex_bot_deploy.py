###################################################################################################
#### Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
####
#### Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file
#### except in compliance with the License. A copy of the License is located at
####
####     http://aws.amazon.com/apache2.0/
####
#### or in the "license" file accompanying this file. This file is distributed on an "AS IS"
#### BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#### License for the specific language governing permissions and limitations under the License.
###################################################################################################

import json
import boto3
import logging
import zipfile
import ntpath
import io
import botocore
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

DEFAULT_REGION = 'us-east-1'

logger = logging.getLogger(__name__)

LATEST_ALIAS = '$LATEST'


@retry(stop=stop_after_attempt(10), wait=wait_exponential(multiplier=1.5),
       retry=retry_if_exception_type(boto3.client('lex-models').exceptions.ConflictException))
def retry_function(f, **kwargs):
    """
    retries the function passed in
    :param f: function name
    :param kwargs: parameters for the function
    :return: function result
    """
    if retry_function.retry.statistics['attempt_number'] > 1:
        logger.warning("Got ConflictException. More than 1 attempt for: {}, {}, {}".format(f, retry_function.retry.statistics, kwargs))
    return f(**kwargs)


@retry(stop=stop_after_attempt(30), wait=wait_exponential(multiplier=1), retry=retry_if_exception_type(ValueError))
def wait_async(f, status_name, status_values, failed_statuses=None, **kwargs):
    """
    wait till function is not in status_values any more
    you can change the params like this: wait_async.retry_with(stop=stop_after_attempt(4))()
    :param f: function to call to receive status
    :param status_name: attribute in response to check
    :param status_values: will wait as long as status is in status_values
    :param failed_statuses: raises Exception when status is in failed_statuses
    :param kwargs: any function parameter
    :return: response or Exception in case of error or status in failed_statuses
    """
    if failed_statuses is None:
        failed_statuses = []
    wait_response = f(**kwargs)
    if wait_response[status_name] in status_values:
        logger.info("Waiting. status_name: '{}' still in '{}', waiting to exit status '{}'."
                    .format(status_name, wait_response[status_name], status_values))
        raise ValueError("Waiting. status_name: '{}' still in '{}', waiting to exit status '{}'."
                         .format(status_name, wait_response[status_name], status_values))

    if wait_response[status_name] in failed_statuses:
        logger.error("failed, no need to wait longer. response: {}\n".format(wait_response))
        raise Exception("wait_response[status_name]: {} in failed_statuses: {}"
                        .format(wait_response[status_name], failed_statuses))

    return wait_response


def lex_deploy(lex_schema_file, lex_alias=LATEST_ALIAS, lambda_endpoint=None, region=None, log_level='INFO'):
    """deploys Amazon Lex schema file to either the $LATEST or a specific alias.
        The temp_folder is important for storing the zip file for deployment
        """
    logger.setLevel(log_level)

    try:
        lex_client = boto3.client('lex-models') \
            if not region \
            else boto3.client('lex-models', region_name=region)
    except botocore.exceptions.NoRegionError:
        logger.warning("no region defined or configured, going to default to: {}".format(DEFAULT_REGION))
        lex_client = boto3.client('lex-models', region_name=DEFAULT_REGION)

    if region:
        lex_client = boto3.client('lex-models', region_name=region)

    with open(lex_schema_file) as lex_schema_file_input:
        full_schema = json.load(lex_schema_file_input)

        if lambda_endpoint:
            for intent in full_schema['resource']['intents']:
                if 'fulfillmentActivity' in intent and 'codeHook' in intent['fulfillmentActivity']:
                    logger.info(
                        "changing {} to {}".format(intent['fulfillmentActivity']['codeHook']['uri'], lambda_endpoint))
                    intent['fulfillmentActivity']['codeHook']['uri'] = lambda_endpoint
                if 'dialogCodeHook' in intent:
                    logger.info("changing {} to {}".format(intent['dialogCodeHook']['uri'], lambda_endpoint))
                    intent['dialogCodeHook']['uri'] = lambda_endpoint

        buff = io.BytesIO()

        zipfile_ob = zipfile.ZipFile(buff, mode='w')
        zipfile_ob.writestr(ntpath.basename(lex_schema_file), json.dumps(full_schema))

        buff.seek(0)

        start_import_response = lex_client.start_import(
            payload=buff.read(),
            resourceType='BOT',
            mergeStrategy='OVERWRITE_LATEST'
        )

        logger.debug("start_import_response: {}".format(start_import_response))

        import_id = start_import_response['importId']
        wait_async(lex_client.get_import, 'importStatus', ["IN_PROGRESS"], ["FAILED"], importId=import_id)

        schema_resource = full_schema['resource']
        voice_id = schema_resource['voiceId']
        bot_name = schema_resource['name']
        logger.debug("voice_id: {}".format(voice_id))

        for slot_type in schema_resource['slotTypes']:
            slot_type_name = slot_type['name']
            get_slot_type_response = lex_client.get_slot_type(
                name=slot_type_name,
                version=LATEST_ALIAS
            )
            logger.debug("{}, {}".format(slot_type_name, get_slot_type_response['checksum']))

            create_slot_type_version_response = retry_function(lex_client.create_slot_type_version,
                                                               name=slot_type_name,
                                                               checksum=get_slot_type_response['checksum'])
            logger.debug(create_slot_type_version_response)

        bot_intents = []
        for intent in schema_resource['intents']:
            intent_name = intent['name']
            get_intent_response = lex_client.get_intent(
                name=intent_name,
                version=LATEST_ALIAS
            )
            logger.debug("{}, {}".format(intent_name, get_intent_response['checksum']))

            create_intent_version_response = retry_function(lex_client.create_intent_version, name=intent_name,
                                                            checksum=get_intent_response['checksum'])
            bot_intents.append({
                'intentName': intent_name,
                'intentVersion': create_intent_version_response['version']
            })

            logger.debug(create_intent_version_response)

        logger.info("deployed all intents")

        get_bot_response = lex_client.get_bot(
            name=bot_name,
            versionOrAlias=LATEST_ALIAS
        )
        logger.debug("STATUS: {}".format(get_bot_response['status']))

        wait_async(lex_client.get_bot, 'status', ['BUILDING'], ["FAILED"], name=bot_name, versionOrAlias=LATEST_ALIAS)

        logger.debug("checksum get_bot_response: {}".format(get_bot_response['checksum']))

        put_bot_response = retry_function(lex_client.put_bot,
                                          name=bot_name,
                                          checksum=get_bot_response['checksum'],
                                          childDirected=False,
                                          locale=schema_resource['locale'],
                                          abortStatement=schema_resource['abortStatement'],
                                          clarificationPrompt=schema_resource['clarificationPrompt'],
                                          intents=bot_intents,
                                          processBehavior='BUILD',
                                          voiceId=voice_id
                                          )
        logger.debug("put_bot_response: %s", put_bot_response)

        response = wait_async(lex_client.get_bot, 'status', ['BUILDING', 'NOT_BUILT', 'READY_BASIC_TESTING'],
                              ["FAILED"], name=bot_name, versionOrAlias=LATEST_ALIAS)

        create_bot_version_response = retry_function(lex_client.create_bot_version,
                                                     name=bot_name,
                                                     checksum=response['checksum']
                                                     )

        new_version = create_bot_version_response['version']

        logger.debug("create_bot_version_response: {}".format(create_bot_version_response))

        if lex_alias == LATEST_ALIAS:
            logger.debug("deployed to alias: %s, no specific alias given", lex_alias)
            wait_response = wait_async(lex_client.get_bot, 'status', ['BUILDING', 'NOT_BUILT', 'READY_BASIC_TESTING'],
                                       ["FAILED"], name=bot_name, versionOrAlias=LATEST_ALIAS)

            logger.info("success. bot_status: {} for alias: {}".format(wait_response['status'], LATEST_ALIAS))

        else:
            logger.debug("deploying to alias: %s with version: %s.", lex_alias, new_version)
            try:
                # check if alias exists, need the checksum if updating
                bot_alias = lex_client.get_bot_alias(
                    name=lex_alias,
                    botName=bot_name
                )
                checksum = bot_alias['checksum']
                old_version = bot_alias['botVersion']

                if new_version != old_version:
                    logger.debug("new version: {} for existing alias: {} and version: '{}'"
                                 .format(new_version, lex_alias, old_version))
                    put_bot_alias_response = retry_function(lex_client.put_bot_alias,
                                                            name=lex_alias,
                                                            description='latest test',
                                                            botVersion=new_version,
                                                            botName=bot_name,
                                                            checksum=checksum
                                                            )
                    logger.debug("put_bot_alias_response : {}".format(put_bot_alias_response))

                    # wait for new version
                    wait_async(lex_client.get_bot, 'version', [old_version],
                               name=bot_name, versionOrAlias=lex_alias)
                    wait_response = wait_async(lex_client.get_bot, 'status',
                                               ['BUILDING', 'NOT_BUILT', 'READY_BASIC_TESTING'],
                                               ["FAILED"], name=bot_name, versionOrAlias=lex_alias)
                    logger.info("success. bot_status: {} for alias: {}".format(wait_response['status'], lex_alias))
                else:
                    logger.info('No change for bot. old version == new version ({} == {})'
                                .format(old_version, new_version))

            except lex_client.exceptions.NotFoundException:
                # alias not found, create new alias
                logger.debug("create new alias: '{}'.".format(lex_alias))
                put_bot_alias_response = retry_function(lex_client.put_bot_alias,
                                                        name=lex_alias,
                                                        description='latest test',
                                                        botVersion=new_version,
                                                        botName=bot_name
                                                        )

                logger.debug("put_bot_alias_response : {}".format(put_bot_alias_response))
