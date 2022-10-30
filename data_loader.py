def load_data(type, params):
    if type == 'csv':
        return load_from_csv(params)
    elif type == 'api':
        return load_from_api(params)
    elif type == 'mongo':
        return load_from_mongo(params)


def load_from_csv(params):
    pass

def load_from_api(params):
    pass

def load_from_mongo(params):
    pass

def verify_params(params, validation, messages):
    pass