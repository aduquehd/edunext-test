from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomerSetUp
from .serializer import CustomerSetUpSerializer
import json


class CustomerViewSet(APIView):
    authentication_classes = ([])
    permission_classes = ([])

    def get(self, request, pk):
        try:
            customer_setup_data = CustomerSetUp.objects.get(pk=pk, status=True)
            serializer = CustomerSetUpSerializer(customer_setup_data, many=False)
            return Response(serializer.data)
        except (CustomerSetUp.DoesNotExist, ValueError):
            return Response(data={'message': "Customer Doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'message': "Unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            customer_setup = CustomerSetUp.objects.filter(pk=pk)
            customer_setup_data = customer_setup.first().data
            post_data = request.data

            for key in request.data.keys():
                if key.isupper() and key in customer_setup_data:
                    customer_setup_data[key] = post_data[key]

            update_values = {'data': customer_setup_data}

            update_values = self.__update_customer_setup_status(update_values=update_values,
                                                                post_data=post_data)

            customer_setup.update(**update_values)

            data = {'data': post_data}
            return Response(data=data, status=status.HTTP_200_OK)

        except CustomerSetUp.DoesNotExist:
            return Response(data={'message': "User doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        except (KeyError, ValueError):
            response_data = {'message': "Customer Setup data has an incorrect json format"}
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(data={'message': "Unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def __update_customer_setup_status(update_values, post_data):
        try:
            if 'customer_setup_status' in post_data:
                update_values['status'] = json.loads(post_data['customer_setup_status'])
            return update_values
        except Exception or ValueError:
            raise


class CustomersViewSet(APIView):
    authentication_classes = ([])
    permission_classes = ([])

    def get(self, request):
        try:
            customer_setup_data = CustomerSetUp.objects.filter(status=True)
            serializer = CustomerSetUpSerializer(customer_setup_data, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(data={'message': "Unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            customer_data = json.loads(data.get('data'))
            customer_setup_data = CustomerSetUp.objects.create(name=data.get('name'), data=customer_data)
            customer_setup_data.save()
            response_data = {'message': "Customer Setup successfully created", 'id': customer_setup_data.pk}
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        except (KeyError, ValueError):
            response_data = {'message': "Customer Setup data has an incorrect json format"}
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(data={'message': "Unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
