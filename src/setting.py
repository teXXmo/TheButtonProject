import ujson
setting = {}

def set(par, val):
    global setting
    try:
        setting[par] = val
    except:
        print('ERROR in setting.set')

def get(par):
    global setting
    try:
        return setting[par]
    except:
        print('ERROR in setting.get')
        return ''

def load(file):
    global setting
    try:
        f = open(file)
        setting = ujson.loads(f.read())
        f.close()
    except:
        try:
            print('ERROR in setting.load Load Backup')
            f = open(file + '.bak')
            setting = ujson.loads(f.read())
            f.close()
        except:
            print('ERROR in setting.load Can not Load Backup')
            return
    f = open(file + '.bak', 'w')
    f.write(ujson.dumps(setting))
    f.close()
        
def save(file):
    global setting
    try:
        f = open(file, 'w')
        f.write(ujson.dumps(setting))
        f.close()
    except:
        print('ERROR in setting.save')

def post(json):
    global settings
    try:
        dict = ujson.loads(json)
        print(dict)
        setting.update(dict)
    except:
        print('ERROR in setting.post')