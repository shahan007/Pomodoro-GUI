import requests as req
header = {
    'Accept': 'application/json',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
counter = 0
def get_quote_categories():
    url = 'https://quotes.rest/qod/categories'
    res = req.get(url,headers=header)
    if res.ok:
        cat = res.json()
        return list(cat['contents']['categories'].keys())
    return f'Error!: {res.status_code}'

quote_categories = get_quote_categories()
def get_quote(type=quote_categories[-1]):
    url = 'https://quotes.rest/qod'
    res = req.get(url, headers=header, params={'category':type})
    if res.ok:
        quote = res.json()
        return quote
    return f'Error!: {res.status_code}'
print(get_quote())
    
