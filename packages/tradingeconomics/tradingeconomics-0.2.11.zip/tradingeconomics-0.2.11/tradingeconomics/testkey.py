def loginkey():
    global apikey
    apikey = raw_input('Enter APIkey: ')
    if apikey == '':
        apikey = 'guest:guest'
