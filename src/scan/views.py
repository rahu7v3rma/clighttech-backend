import csv
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from lib.s3_utils import BucketClient
from clighttech_cms.settings import AWS_STORAGE_BUCKET_NAME
from .serializers import (
    TraceFilteredRequestSerializer,
    StatsSummaryRequestSerializer,
)


class ScanView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            {
                'success': True,
                'message': 'Scan',
                'status': status.HTTP_200_OK,
                'data': {},
            },
            status=status.HTTP_200_OK,
        )


class GetTraceFilteredView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, data_field):
        try:
            request_serializer = TraceFilteredRequestSerializer(
                data=request.GET
            )
            if not request_serializer.is_valid():
                return Response(
                    {
                        'success': False,
                        'message': 'Invalid request',
                        'status': status.HTTP_400_BAD_REQUEST,
                        'data': request_serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            scan, mode, odos = request_serializer.validated_data.values()
            # pylint: disable-next=line-too-long
            resource_key = f'processed_csv/{data_field}_mode_{mode}_odos_{odos}_scan_{scan}_trace_filtered.csv'
            resource_url = BucketClient().create_presigned_url(
                AWS_STORAGE_BUCKET_NAME, resource_key
            )
            return Response(
                {
                    'success': True,
                    'message': 'TraceFiltered',
                    'status': status.HTTP_200_OK,
                    'data': {'trace_filtered_url': resource_url},
                },
                status=status.HTTP_200_OK,
            )
        # pylint: disable-next=bare-except
        except:
            return Response(
                {
                    'success': False,
                    'message': 'An unknown error occured',
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetStatsSummaryView(APIView):
    permission_classes = [AllowAny]

    def convert_csv_to_json(self, csv_string):
        json_list = []
        for row in csv.DictReader(csv_string.splitlines()):
            json_list.append(row)
        return json_list

    def get(self, request, data_field):
        try:
            request_serializer = StatsSummaryRequestSerializer(
                data=request.GET
            )
            if not request_serializer.is_valid():
                return Response(
                    {
                        'success': False,
                        'message': 'Invalid request',
                        'status': status.HTTP_400_BAD_REQUEST,
                        'data': request_serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            scan, mode, odos = request_serializer.validated_data.values()
            s3_client = BucketClient()
            # pylint: disable-next=line-too-long
            resource_key = f'processed_csv/{data_field}_mode_{mode}_odos_{odos}_scan_{scan}_stats_summary.csv'
            csv_string = s3_client.get_object_as_string(
                AWS_STORAGE_BUCKET_NAME, resource_key
            )
            json_list = self.convert_csv_to_json(csv_string)
            return Response(
                {
                    'success': True,
                    'message': 'StatsSummary',
                    'status': status.HTTP_200_OK,
                    'data': {'stats_summary': json_list},
                },
                status=status.HTTP_200_OK,
            )
        # pylint: disable-next=bare-except
        except:
            return Response(
                {
                    'success': False,
                    'message': 'An unknown error occured.',
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
