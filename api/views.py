from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def getdata(request):
    person = {'name':'eshaan', 'age':18}
    return Response(person)