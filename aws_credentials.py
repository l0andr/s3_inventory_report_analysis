import os
from typing import Union

import boto3
from botocore.client import ClientError


class AwsCredentials:
    '''
        Object of this class can set, renew and store AWS credentials
        from parameters, from ENV. variables or from session
        store session object and return client object
        for specified service and region

        :type aws_key: string or None
        :param aws_key: AWS access key ID
        :type aws_secret: string or None
        :param aws_secret: AWS secret access key
        :type region: string or None
        :param region: AWS region
        :type use_env: bool
        :param use_env: If True try to use credentials from Env. Variable

    '''

    def __init__(self, aws_key: Union[str, None] = None, aws_secret: Union[str, None] = None,
                 region: Union[str, None] = None, use_env=True):
        self.__session = None
        self.__key = None
        self.__secret = None
        self.__credentials_source = None
        self.__region = region
        self.__use_env = use_env
        self.reset(aws_key, aws_secret, region)

    def reset(self, aws_key: Union[str, None] = None, aws_secret: Union[str, None] = None,
              region: Union[str, None] = None):
        if region:
            self.__region = region
        elif self.__use_env and 'AWS_DEFAULT_REGION' in os.environ:
            self.__region = os.environ['AWS_DEFAULT_REGION']

        if aws_key and aws_secret:
            self.__key = aws_key
            self.__secret = aws_secret
            self.__credentials_source = 'param'
        elif self.__use_env and 'AWS_ACCESS_KEY_ID' in os.environ and 'AWS_SECRET_ACCESS_KEY' in os.environ:
            self.__key = os.environ['AWS_ACCESS_KEY_ID']
            self.__secret = os.environ['AWS_SECRET_ACCESS_KEY']
            self.__credentials_source = 'env'
        self.__session = self.__create_session()
        sts_client = self.get_client('sts')
        try:
            sts_client.get_caller_identity()
            return True
        except ClientError:
            self.__session = None
            return False

    def __create_session(self):
        if not (self.__key and self.__secret):
            self.__credentials_source = 'session'
        return boto3.Session(aws_access_key_id=self.__key, aws_secret_access_key=self.__secret)

    def get_client(self, service: Union[str, None] = None, region: Union[str, None] = None):
        if not region and self.__region:
            region = self.__region
        return self.__session.client(service, region_name=region)

    @property
    def session(self):
        return self.__session

    def __str__(self):
        response = f'AwsCredentials. Credentials source:{self.__credentials_source}. ' \
                   f'Session created:{self.__session is not None} '
        return response
