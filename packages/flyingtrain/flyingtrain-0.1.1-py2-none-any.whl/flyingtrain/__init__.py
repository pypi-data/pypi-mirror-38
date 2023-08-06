# -*- coding: utf-8 -*-
import ijson

name = "flyingtrain"


def extract_data(test_file):
    model = None
    model_flag = 0  # 1: car, 2: train, 3: planes

    car_capacity = 0
    car = {"passenger-capacity": 0}

    train_capacity = 0
    train = {"number-wagons": 0, "w-passenger-capacity": 0}

    plane_capacity = 0
    plane = {"b-passenger-capacity": 0, "e-passenger-capacity": 0}

    distinct_cars = set()
    distinct_trains = set()
    distinct_planes = set()

    for prefix, event, value in ijson.parse(open(test_file)):
        if prefix.endswith('.model'):
            model = value

        elif prefix.endswith('.manufacturer'):
            model_flag = 1
        elif prefix.endswith('.passenger-capacity'):
            model_flag = 1
            car["passenger-capacity"] = value

        elif prefix.endswith('.number-wagons'):
            model_flag = 2
            train["number-wagons"] = value
        elif prefix.endswith('.w-passenger-capacity'):
            model_flag = 2
            train["w-passenger-capacity"] = value

        elif prefix.endswith('.b-passenger-capacity'):
            model_flag = 3
            plane["b-passenger-capacity"] = value
        elif prefix.endswith('.e-passenger-capacity'):
            model_flag = 3
            plane["e-passenger-capacity"] = value

        elif prefix.endswith('.item') and event == 'end_map':
            if model_flag == 1:
                car_capacity += car["passenger-capacity"]
                distinct_cars.add(model)
            if model_flag == 2:
                train_capacity += (train["number-wagons"] * train["w-passenger-capacity"])
                distinct_trains.add(model)
            if model_flag == 3:
                plane_capacity += (plane["b-passenger-capacity"] + plane["e-passenger-capacity"])
                distinct_planes.add(model)

    print '"planes":', plane_capacity
    print '"trains":', train_capacity
    print '"cars":', car_capacity
    print '\n'
    print '"distinct-cars":', len(distinct_cars)
    print '"distinct-planes":', len(distinct_planes)
    print '"distinct-trains":', len(distinct_trains)
