import sys
from build_data import *

#Helper function
def field_split(field: str):
    split = field.split(".")
    label = split[1]
    return label

def display(data):
    for i in data:
        print("County: " + i.county('County'), "State: " + i.county("State"))

def filter_state(data, state: str):
    filtered = []
    for i in data:
        if i.county("State") == state:
            filtered.append(i)
    print("Filter: state == <state abbreviation>" + str(len(filtered)) + "entries)")
    return filtered

def filter_gt(data, field: str, number: int):
    field = field_split(field)
    filtered = []
    for i in data:
        if i.field > number:
            filtered.append(i)
    print("Filter:", field, "gt", number, str(len(filtered)))
    return filtered

def filter_lt(data, field: str, number: int):
    field = field_split(field)
    filtered = []
    for i in data:
        if i.field < number:
            filtered.append(i)
    print("Filter:", field, "lt", number, str(len(filtered)))
    return filtered

def population_total(data):
    total = 0
    for i in data:
        total += i.population["2014 population"]
    print("2014 population:", total)
    return total

def population(data, field: str):
    field = field_split(field)
    sub_pop = 0
    for i in data:
        sub_pop += (i.field() * 100) * i.population["2014 population"]
    pop = sub_pop
    print("2014", field, "population:", pop)
    return pop

def percent(data, field: str):
    field = field_split(field)
    perc = population(data, field) / population_total(data)
    print("2014", field, "percentage:", perc)
    return perc


def operations(line):
    data = get_data()
    line = line.rstrip("\n")
    x = line.split(":")
    if x[0] == "display":
        display(data)
    elif x[0] == "filter-state":
        data = filter_state(data, x[1])
    elif x[0] == "filter-gt":
        data = filter_gt(data, x[1], int(x[2]))
    elif x[0] == "filter-lt":
        data = filter_lt(data, x[1], int(x[2]))
    elif x[0] == "population-total":
        population_total(data)
    elif x[0] == "population":
        population(data, x[1])
    elif x[0] == "percent":
        percent(data, x[1])
    return data
def main():
    if len(sys.argv) != 2:
        print("No operations file detected")
        sys.exit(1)
    with open(sys.argv[1], 'r') as operation:
        contents = operation.readlines()
        for line in contents:
            data = operations(line)
if __name__ == '__main__':
    main()
















    
