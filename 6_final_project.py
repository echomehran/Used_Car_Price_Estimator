from itertools import count
from typing import Any, Dict, Optional, Iterable, Tuple

import math

from requests import Session


BASE_PARAMS = {
    'city': 'denver',
    'collapse': 'true',
    'fallback': 'true',
    'include_incentives': 'true',
    'include_targeted_incentives': 'true',
    'new_or_used': 'u',
    'per_page': 30,
    'postal_code': '80210',
    'search_event': 'true',
    'sort[]': 'best_match',
    'sponsored': 'true',
    'state': 'ny',
}


def get_truecar(session: Session, make_name: str, page: int) -> Dict[str, Any]:
    with session.get(
        'https://www.truecar.com/abp/api/vehicles/used/listings',
        params={
            **BASE_PARAMS,
            'make_slug': make_name.lower(),
            'page': page,
        },
    ) as response:
        response.raise_for_status()
        return response.json()


def depaginate_truecar(
    session: Session, make_name: str, max_pages: Optional[int],
) -> Iterable[Tuple[Dict[str, Any], int, int]]:
    if max_pages is None:
        pages = count(1)
    else:
        pages = range(1, max_pages + 1)

    for page in pages:
        doc = get_truecar(session, make_name, page=page)
        total = doc.get('total')
        per_page = int(doc['per_page'])

        if total is None:
            n_pages = 1
        else:
            n_pages = math.ceil(total / per_page)
            if max_pages is not None:
                n_pages = min(max_pages, n_pages)

        yield doc, page, n_pages

        if total is None or page >= n_pages:
            break


def reshape(doc: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    for listing in doc['listings']:
        vehicle = listing['vehicle']

        yield {
            'ex_color': vehicle['exterior_color'],
            'in_color': vehicle['interior_color'],
            'location': vehicle['location'],
            'price': vehicle['list_price'],
            'make': vehicle['make'],
            'model': vehicle['model'],
            'mileage': vehicle['mileage'],
            'style': vehicle['style'],
            'year': vehicle['year'],
            'engine': vehicle['engine'],
            'accidentCount': vehicle['condition_history']['accidentCount'],
            'ownerCount': vehicle['condition_history']['ownerCount'],
            'isCleanTitle': vehicle['condition_history']['titleInfo']['isCleanTitle'],
            'isFrameDamaged': vehicle['condition_history']['titleInfo']['isFrameDamaged'],
            'isLemon': vehicle['condition_history']['titleInfo']['isLemon'],
            'isSalvage': vehicle['condition_history']['titleInfo']['isSalvage'],
            'isTheftRecovered': vehicle['condition_history']['titleInfo']['isTheftRecovered'],
        }


def main():
    car_name = input('Enter car name: ')
    max_pages = input('Enter page limit, or press enter for none: ')
    if max_pages == '':
        max_pages = None
    else:
        max_pages = int(max_pages)

    cars = []

    with Session() as session:
        session.headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json',
            'Referer': 'https://www.truecar.com/shop/used/?filterType=brand',
        }

        for doc, page, n_pages in depaginate_truecar(session, car_name, max_pages):
            print(f'{page}/{n_pages}')
            cars.extend(reshape(doc))


if __name__ == '__main__':
    main()

# ! adding the database is up to you and it's sth like this

# first of all we need to import mysql.connector

# then ...

# checks the connection
# print('CONNECTING ...')

# mydb = mysql.connector.connect(
#     host="x",
#     user="x",
#     password="x",
#     port='x',
#     database='x'
# )

# print('CONNECTED')

# # checking the connection is done

# my_cursor = mydb.cursor(buffered=True)
# # create_command = ''' create table car_information (exterior_color varchar(255), interior_color varchar(255),location varchar(255),price varchar(255),make varchar(255),model varchar(255),mileage varchar(255),
# #         style varchar(255),year varchar(255),engine varchar(255),accidentCount varchar(255),ownerCount varchar(255),isCleanTitle varchar(255),isFrameDamaged varchar(255),
# #         isLemon varchar(255), isSalvage varchar(255),isTheftRecovered varchar(255))'''

# # my_cursor.execute(create_command)
# # print('created')
# insert_command = '''INSERT INTO car_information (exterior_color, interior_color,location,price,make,model,mileage,
#         style,year,engine,accidentCount,ownerCount,isCleanTitle,isFrameDamaged,
#         isLemon, isSalvage,isTheftRecovered) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
# my_cursor.executemany(insert_command, values)
# mydb.commit()

# print(my_cursor.rowcount, "Record Inserted")

# mydb.close()
