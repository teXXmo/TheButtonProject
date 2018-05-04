def update():
    import ujson
    import setting
    import network
    try:
        FWnumber_me = setting.get('FWnumber')
        FWnumber_new = setting.get('FWnumberNew')
        print('FW me: ', FWnumber_me) 
        print('FW new: ', FWnumber_new)
        if FWnumber_me != FWnumber_new:
            import wget
            import wifi
            import os
            FWurl = setting.get('FWurl')
            print('Download new FW: ', FWurl)
            if wifi.wait_sta(15):
                print('Start Update: ', FWurl)
                encoded = wget.get(FWurl).decode()
                path_spl = FWurl.split('/')
                protokoll = path_spl.pop(0)
                path_spl.pop(0)
                server = path_spl.pop(0)
                file = path_spl.pop()
                path = '/'.join(path_spl)
                dict = ujson.loads(encoded)
                file_list = dict['INSTALL']
                for file in file_list:
                    print('Update File : ' + protokoll + '//' + server + '/' + path + '/' + file + ' >>> ' + file + '.tmp')
                    a = wget.get_file(protokoll + '//' + server + '/' + path + '/' + file, file + '.tmp')
                    fileSize = os.stat( file + '.tmp')
                    if fileSize[6] > 0:
                        os.rename(file + '.tmp', file)
                        print('Renamed file ' + file + '.tmp', file)
                    else:
                        print('Error updating file : ', file)
                        return
                setting.set('FWnumber', FWnumber_new)
                setting.set('FWversion', '{:04.2f}'.format(FWnumber_new/100))
    except:
        print('ERROR in RepUpdate.update')

def new(VBat):
    import setting
    import ubinascii
    import network
    try:
        keypresses = setting.get('keypresses') + 1        
        hwid = ubinascii.hexlify(network.WLAN().config('mac'),':').decode().upper()    
        setting.set('keypresses', keypresses)
        setting.set('hwid', hwid) 
        setting.set('VBat', VBat)
        setting.set('RSSI', network.WLAN().status('rssi'))
    except:
        print('ERROR in RepUpdate.new')
