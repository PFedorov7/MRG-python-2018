# -*- encoding: utf-8 -*-

def process(data, events, car):

    switched_cars = ''
    last_car_num = 0
    counter = 0
    
    for event in events:
        if(event['type'] == 'walk'):
            next_car = ''
            for train in data:
                for unit in train['cars']:
                    for figure in unit['people']:
                        if(figure == event['passenger'] ):
                            next_car = 'c' + str(int(unit['name'][1::]) + event['distance'])
                            for unit_check in train['cars']:
                                if (unit_check['name'] == next_car):
                                    counter = 1
                            if (counter == 0):
                                return -1 
                    if(counter):
                        unit['people'].remove(event['passenger'])
                        counter = 0
                for unit in train['cars']:
                    if(next_car == unit['name']):
                        unit['people'].append(event['passenger'])
                        
        if(event['type'] == 'switch'):    
            for train in data:
                if (train['name'] == event['train_from']):
                    if(event['cars'] > 0):
                        switched_cars = train['cars'][-event['cars']::]
                        train['cars'] = train['cars'][:- event['cars']:]
                    else:
                        switched_cars = train['cars'][:event['cars']:]
                        train['cars'] = train['cars'][event['cars']::]
            for train in data: 
                if (train['name'] == event['train_to']):
                    if (len(train['cars'])):
                        last_car_num = int(train['cars'][-1]['name'][1::])
                        for newlist in switched_cars:
                            counter += 1
                            newlist['name'] = 'c' + str(last_car_num + counter)
                    train['cars'].extend(switched_cars)
                    counter = 0
                    
    for train in data:
        for cars in train['cars']:
            if (cars['name'] == car):
                return (len(cars['people']))
                
