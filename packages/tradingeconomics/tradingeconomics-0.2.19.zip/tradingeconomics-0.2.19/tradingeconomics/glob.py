def login():
    global apikey
    apikey = raw_input('Enter APIkey: ')
    if apikey == None:
        apikey = 'guest:guest'
    return apikey
