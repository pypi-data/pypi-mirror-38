import functions as fn

def login():
    global apikey
    apikey = raw_input('Enter APIkey: ')
    if apikey == '':
        apikey = 'guest:guest'
    if apikey != 'guest:guest':
        fn.credCheck(apikey)
    return apikey
