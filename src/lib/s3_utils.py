import boto3
import logging
from botocore.exceptions import ClientError


class BucketClient:
    def __init__(self):
        # create bucket connection
        self.s3 = boto3.resource('s3')

    def list_objects(self, bucket_name):
        """
        list bucket objects
        """
        bucket = self.s3.Bucket(bucket_name)
        file_names = [data.key for data in bucket.objects.all()]
        return file_names

    def create_presigned_url(self, bucket_name, object_name, expiration=3600):
        """Generate a presigned URL to share an S3 object

        :param bucket_name: string
        :param object_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """

        # Generate a presigned URL for the S3 object
        try:
            response = self.s3.meta.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': object_name},
                ExpiresIn=expiration,
            )
        except ClientError as err:
            logging.error(err)
            return None

        # The response contains the presigned URL
        return response

    def get_object_as_string(self, bucket_name, object_key):
        """Fetching and converting S3 object file content into string format
        :param bucket_name: string
        :param object_key: string
        :return: string out of object file content
        """
        try:
            return (
                self.s3.Object(bucket_name, object_key)
                .get()['Body']
                .read()
                .decode('utf-8')
            )
        # pylint: disable-next=bare-except
        except:
            return None
