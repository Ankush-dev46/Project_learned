import requests, os
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

RAIN_URL = 'https://data.gov.in/sites/default/files/sub-divisional-monthly-rainfall-1901-2017.csv'
CROP_URL = 'https://data.gov.in/sites/default/files/district_wise-season-wise-crop-production-statistics-1997.csv'

targets = [
    (RAIN_URL, os.path.join(DATA_DIR, 'rainfall.csv')),
    (CROP_URL, os.path.join(DATA_DIR, 'crops.csv')),
]

for url, path in targets:
    print('Downloading', url)
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r.iter_content(1024*8):
                f.write(chunk)
        print('Saved:', path)
    else:
        print('Failed:', url)
