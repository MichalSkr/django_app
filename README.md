# Setting up
## 
In terminal go to postgres: psql postgres
```
GRANT ALL PRIVILEGES ON DATABASE test TO django_user;
ALTER USER django_user CREATEDB;
```

## Docker
In main folder
```
docker-compose up -d
```
To run docker in a background
## Staring app manually
```
python manage.py runserver
```

#Available views
In order to execute below methods one should call specified url: 
```
http://127.0.0.1:8000/main_app/{specified_methid_name}
```

## get_average
Get method returns json with average age for example
```
{
  "average_age": 32
}
```
##count_average
Method that calculates average age for selected dataset values.
##filter_birthday
Post method, filters records for and returns those with selected age ranges, example usage
```
{
"filter_by":
       {
        "date_from": "1901-01-01",
	"date_to": "2001-01-10"
	}
}
```
Example result
```
{
  "data": [
    {
      "first_name": "FIRST NAME",
      "last_name": "LAST NAME",
      "email": "test@email.com",
      "birthday": "1995-01-10"
    },
    {
      "first_name": "FIRST NAME",
      "last_name": "LAST NAME",
      "email": "test@123",
      "birthday": "1991-01-21"
    },
    {
      "first_name": "FIRST NAME",
      "last_name": "LAST NAME",
      "email": "t@123",
      "birthday": "2000-05-20"
    },
    {
      "first_name": "FIRST NAME",
      "last_name": "LAST NAME",
      "email": "tja@1234",
      "birthday": "1963-01-01"
    }
  ]
}
```
##data_post
Post method that allows post a single record in a postgresql databse
example usage:
```
{
	"first_name": "Michal",
	"last_name": "Sklyar",
	"email": "test@email.com",
	"birthday": "10.01.1995"
}
```
Returns HttpResponse
##upload_data_file
Post method, allows to upload csv file into database. In order to use it
one has to post a whole csv file. Returns HttpResponse.
##Important to notice
Only records with email that is not in a database will be saved there 
because email has to have unique value there.
##Running tests
In order to run tests go to catalogue main_app and execute
```
python ../manage.py test
```