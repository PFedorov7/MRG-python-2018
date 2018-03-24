# -*- encoding: utf-8 -*-

def process(data, events, car):

    for train in data:
        print(train['name'])
        for carm in train['cars']:
            print('\t{}'.format(carm['name']))
            for man in carm['people']:
                print('\t\t{}'.format(man))
                
    for event in events:
        if(event['type'] == 'walk'):
            passenger = event['passenger']
            distance = event['distance']
            for train in data:
                counter = 0
                unitz = ''
                for unit in train['cars']:
                    for figure in unit['people']:
                        if(figure == passenger):
                            num = int(unit['name'][1::]) + distance
                            unitz = 'c' + str(num)
                            for unit1 in train['cars']:
                                if (unit1['name'] == unitz):
                                    counter = 1
                            if (counter == 0):
                                return -1 
                    if(counter):
                        unit['people'].remove(passenger)
                        counter = 0
                for unit in train['cars']:
                    if(unitz == unit['name']):
                        unit['people'].append(passenger)
                        
        if(event['type'] == 'switch'):
            newcars = ''
            names = 0
            i = 0
            for train in data:
                if (train['name'] == event['train_from']):
                    if(event['cars'] > 0):
                        position = - event['cars']
                        newcars = train['cars'][position::]
                        train['cars'] = train['cars'][:position:]
                    else:
                        position = event['cars']
                        newcars = train['cars'][:position:]
                        train['cars'] = train['cars'][position::]
            for train in data: 
                if (train['name'] == event['train_to']):
                    if (len(train['cars'])):
                        for carss in train['cars']:
                            if(carss):
                                names = int(carss['name'][1::])
                        for newlist in newcars:
                            i = i + 1
                            newlist['name'] = 'c' + str(names + i)
                        train['cars'].extend(newcars)
                    else:
                        train['cars'].extend(newcars)
                    
    for train in data:
        print(train['name'])
        for carz in train['cars']:
            print('\t{}'.format(carz['name']))
            for man in carz['people']:
                print('\t\t{}'.format(man))
    
    
    for train in data:
        for cars in train['cars']:
            if (cars['name'] == car):
                return (len(cars['people']))
                
