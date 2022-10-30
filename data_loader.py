def load_data(type, params):
    if type == 'csv':
        return load_from_csv(params)
    elif type == 'api':
        return load_from_api(params)
    elif type == 'mongo':
        return load_from_mongo(params)


def load_from_csv(params):
    if verify_params(params, ['database','collection','filename'], {'passed':'load from csv params good','failed':'load from csv parameter error, expect database, collection, filename'}):
        #run load from file logic
        return True
    else:
        return False

def load_from_api(params):
    if verify_params(params, ['source'],{'passed':'load from api params good','failed':'load from api parameter error, expect source | optional dates'}):
        #run load from api logic
        return True
    else:
        return False

def load_from_mongo(params):
    if verify_params(params, ['collection'],{'passed':'load from mongo params good','failed':'load from mongo parameter error, expect collection | optional dates'}):
        #run load from mongo logic
        return True
    else:
        return False


def verify_params(params, validation, messages):
    if all (item in validation for item in params):
        print(messages['passed'])
        return True
    else:
        print(messages['failed'])
        return False
