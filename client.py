import requests


response = requests.post('http://127.0.0.1:5000/ads',
                         json={
                             'name': 'Test_name',
                             'description': 'Test_description',
                             'owner': 'Test_owner@gmail.com'}
                         )
print(response.status_code)
print(response.headers)
print(response.json())


response = requests.patch('http://127.0.0.1:5000/ads/1',
                          json={'name': 'Test_name_upd',
                                'description': 'Test_description_upd'
                                }
                          )

print(response.status_code)
print(response.headers)
print(response.json())


response = requests.get('http://127.0.0.1:5000/ads/1')
print(response.status_code)
print(response.json())


response = requests.delete('http://127.0.0.1:5000/ads/1')
print(response.status_code)
print(response.json())
