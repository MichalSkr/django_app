from django.http import HttpResponse, Http404
from django.http import JsonResponse
from main_app.models import DataSet
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json
import csv

data_query = None


def get_average(request):
    """
    Get function returns average age of people in database in years.

    :param request:
    :return:
    """
    if request.method == 'GET':
        data_query = DataSet.objects.all()
        total_age = count_average(data_query.values('birthday'))
        args = {'average_age': total_age}
        return JsonResponse(args)


def count_average(dataset):
    """
    Counts average age for selected dataset values.

    :param dataset: Dataset with birth dates.
    :return: returns integer with average years calculated for dataset.
    """
    date_today = datetime.now().date()
    total_age = 0
    for record in dataset:
        total_age += (date_today - record['birthday']).days
    total_age = int((total_age / len(dataset)) / 365)
    return total_age


@csrf_exempt
def filter_birthday(request):
    """
    Post method, that returns filtered json data.

    :param request: json data
    :return: Json
    """
    global data_query
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            filter_by = json_data.get('filter_by', "")
            filters = {}
            for key in filter_by.keys():
                val = filter_by[key]
                if val:
                    if key == 'date_from':
                        key = 'birthday__gte'
                    if key == 'date_to':
                        key = 'birthday__lte'
                    filters[key] = val
            data_query = DataSet.objects.filter(**filters)

        except DataSet.DoesNotExist:
            raise Http404("Poll does not exist")
        args = {'data': list(data_query.values())}

        return JsonResponse(args)


@csrf_exempt
def data_post(request):
    """
    Method to post one record to a postgres database.

    :param request: json data
    :return: HttpResponse
    """
    if request.method == 'POST':
        json_data = json.loads(request.body)
        if not all(json_data.get(name) for name in ('first_name', 'last_name', 'email', 'birthday')):
            return HttpResponse("At least one of the parameters missing")
        try:
            same_email = DataSet.objects.filter(email=json_data['email'])
            if same_email:
                return HttpResponse("Specified email already exists in a database")
        except DataSet.DoesNotExist:
            return HttpResponse("Dataset does not exists")
        try:
            birth_date = datetime.strptime(json_data['birthday'], '%d.%m.%Y').date()
            d = DataSet(first_name=json_data['first_name'],
                        last_name=json_data['last_name'],
                        email=json_data['email'],
                        birthday=birth_date)
            d.save()
        except ValueError:
            return HttpResponse("Date argument was not in a correct format."
                                "Should be like dd.mm.yyyy")
        return HttpResponse("Got json data")


@csrf_exempt
def upload_data_file(request):
    """
    Method to upload full csv into database.

    :param request: json data
    :return: HttpResponse
    """
    if request.method == 'POST':

        csv_reader = csv.reader(request.body.decode('utf-8').splitlines())
        line_count = 0
        col_names = list()
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                col_names = row
                line_count += 1
            else:
                dict_values = {}
                index_email = col_names.index('email')
                if row:
                    try:
                        same_email = DataSet.objects.filter(email=row[index_email])
                        if same_email:
                            # If we encounter same email address that is primary key
                            #  and should be unique we skip the record.
                            continue
                        for i in range(len(row)):

                            if col_names[i] == 'birthday':
                                row_data = datetime.strptime(row[i], '%d.%m.%Y').date()
                            else:
                                row_data = row[i]

                            dict_values[col_names[i]] = row_data
                        d = DataSet(**dict_values)
                        d.save()
                    except ValueError:
                        return HttpResponse("At least one of date arguments was not in a correct format."
                                            "Should be like dd.mm.yyyy")

    return HttpResponse("Updated data")
