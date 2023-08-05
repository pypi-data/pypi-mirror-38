from base64 import b64decode
import boto3
import json
import os
from kms_client.logger import JsonLogger as log

logger = log(__file__)


class KMS_Client:
    def __init__(self, aws_profile="", aws_region=""):
        if not aws_profile and not aws_region:
            self.session = boto3.Session()
        else:
            self.session = boto3.Session(profile_name=aws_profile, region_name=aws_region)

    def get_client_credentials(self, bucket, s3_key_path, verify=True):
        """
        Args:
            bucket (str): S3 bucket name
            s3_key_path (str): S3 key path
        Returns:
            string tuple of client id and client secret
        """
        s3 = S3(self.session, verify=verify)
        encrypted_token = s3.get_encrypted_file_from_s3(bucket, s3_key_path)
        logger.log("S3 complete")

        kms = KMS(self.session, verify=verify)
        decrypted_token = kms.decrypt(encrypted_token)
        logger.log("Decrypat complete")
        decrypted_json = json.loads(decrypted_token)

        return decrypted_json


class S3:
    def __init__(self, session, verify=True):
        self.s3 = session.client("s3")

    def get_encrypted_file_from_s3(self, bucketName, key):
        """
        Gets the contnet of a S3 file
        Args:
            session (obj): Boto3 session object
            bucketName (str): S3 bucket name
            key (str): S3 key path
        Returns:
            S3 file content
        """
        obj = self.s3.get_object(Bucket=bucketName, Key=key)
        return obj["Body"].read().decode(("utf-8"))


class KMS:
    def __init__(self, session, verify=True):
        self.kms = session.client("kms")

    def decrypt(self, token):
        """
        Decrypts an encrypted token using AWS KMS
        Args:
            session (obj): Boto3 session object
            token (str): an encrypted token from KMS encryption
        Returns:
            a string which is the plaintext decrypted token
        """
        response = self.kms.decrypt(CiphertextBlob=b64decode(token))["Plaintext"]
        return response
