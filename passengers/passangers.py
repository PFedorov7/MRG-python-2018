# -*- encoding: utf-8 -*-

def process(data, events, car):

    new_index = 0
    for event in events:
        if(event['type'] == 'walk'):
            for train in data:
                for index, unit in enumerate(train['cars']):
                    if(unit['people'].count(event['passenger']) != 0):
                        new_index = index + event['distance']
                        if(new_index >= 0 and new_index <= len(train['cars'])):
                            unit['people'].remove(event['passenger'])
                            train['cars'][new_index]['people'].append(event['passenger'])
                            break
                        else:
                            return -1
                        
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
                    train['cars'].extend(switched_cars)
                    
    for train in data:
        for cars in train['cars']:
            if (cars['name'] == car):
                return (len(cars['people']))
                
