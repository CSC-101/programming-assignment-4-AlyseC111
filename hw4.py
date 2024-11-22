import sys
import build_data


#Helper function that intakes the field from the line, and returns a list with the key and attribute
def field_split(field):
    if isinstance(field, str):
        split = field.split(".")
        return split
    else:
        return field


#Prints the county information for each county in 'data' into the terminal in a user-friendly format
def display(data):
    for i in data:
        print(i.county, ", " + i.state, "\n", "\t", "Population: ",  i.population['2014 Population'])
        print("\t Age: \n \t\t < 5: ", i.age['Percent Under 5 Years'], "\n \t\t < 18: ", i.age['Percent Under 18 Years'], "\n \t\t > 65: ", i.age['Percent 65 and Older'],)
        print("\t Education: \n \t\t >= High School: ", i.education['High School or Higher'], "\n \t\t >= Bachelor's: ", i.education["Bachelor's Degree or Higher"])
        print("\t Ethnicity Percentages: \n \t\t American Indian and Alaska Native: ", i.ethnicities['American Indian and Alaska Native Alone'], "\n \t\t Asian Alone: ", i.ethnicities['Asian Alone'], "\n \t\t Black Alone: ", i.ethnicities['Black Alone'], "\n \t\t Hispanic or Latino: ", i.ethnicities['Hispanic or Latino'], "\n \t\t Native Hawaiian and Other Pacific Islander Alone: ", i.ethnicities['Native Hawaiian and Other Pacific Islander Alone'], "\n \t\t Two or More Races: ", i.ethnicities['Two or More Races'], "\n \t\t White Alone: ", i.ethnicities['White Alone'], "\n \t\t White Alone, not Hispanic or Latino: ", i.ethnicities['White Alone, not Hispanic or Latino'])
        print("\t Age: \n \t\t Median Household: ", i.income['Median Houseold Income'], "\n \t\t Per Capita: ", i.income['Per Capita Income'], "\n \t\t Below Poverty Level: ", i.income['Persons Below Poverty Level'],)

#Filters through 'data' and returns a list of all the counties whose state matches the input state.
def filter_state(data, state):
    filtered = []
    for i in data:
        if i.state == state:
            filtered.append(i)
    return filtered

#Returns a list of all the counties where the population of the specified field is greater than the input number
def filter_gt(data, field, number):
    field = field_split(field)
    filtered = []
    if field[0] == 'Education':
        for i in data:
            if i.education[field[1]] > number:
                filtered.append(i)
    elif field[0] == 'Ethnicities':
        for i in data:
            if i.ethnicities[field[1]] > number:
                filtered.append(i)
    elif field[0] == 'Income':
        for i in data:
            if i.income[field[1]] > number:
                filtered.append(i)
    return filtered

#Returns a list of all the counties where the population of the specified field is less than the input number
def filter_lt(data, field, number):
    field = field_split(field)
    filtered = []
    if field[0] == 'Education':
        for i in data:
            if i.education[field[1]] < number:
                filtered.append(i)
    elif field[0] == 'Ethnicities':
        for i in data:
            if i.ethnicities[field[1]] < number:
                filtered.append(i)
    elif field[0] == 'Income':
        for i in data:
            if i.income[field[1]] < number:
                filtered.append(i)
    return filtered
#Prints to the terminal the total 2014 population across all current counties in 'data'
def population_total(data):
    total = 0
    for i in data:
        total += i.population['2014 Population']
    return total

#Returns the total population of the specified field for all the counties in 'data'
def population(data, field):
    field = field_split(field)
    att = field[0]
    sub_pop = 0
    for i in data:
        if att == 'Education':
            sub_pop += (i.education[field[1]] / 100) * i.population["2014 Population"]
        elif att == 'Ethnicities':
            sub_pop += (i.ethnicities[field[1]] / 100) * i.population["2014 Population"]
        elif att == 'Income':
            sub_pop += (i.income[field[1]] / 100) * i.population["2014 Population"]
    return round(sub_pop, 2)

#Prints the percentage of the total population within the sub-population specified by 'field' for the counties in 'data'
def percent(data, field):
    field = field_split(field)
    perc = round(population(data, field) / population_total(data) * 100, 2)
    return perc

#Executes the correct function based on the input line, with the dataset specified by the input 'data'
def operations(line, data):
    line = line.rstrip("\n")
    x = line.split(":")
    if x[0] == "display":
        display(data)
    elif x[0] == "filter-state":
        data = filter_state(data, x[1])
        print("Filter: state = ", x[1],"(", len(filter_state(data, x[1])), "entries )")
    elif x[0] == "filter-gt":
        data = filter_gt(data, x[1], int(x[2]))
        print("Filter:", x[1], "gt", x[2], "(", len(filter_gt(data, x[1], int(x[2]))), "entries )")
    elif x[0] == "filter-lt":
        data = filter_lt(data, x[1], int(x[2]))
        print("Filter:", x[1], "lt", x[2], "(", len(filter_lt(data, x[1], int(x[2]))), "entries )")
    elif x[0] == "population-total":
        population_total(data)
        print("2014 population:", population_total(data))
    elif x[0] == "population":
        population(data, x[1])
        print("2014", x[1], "population:", population(data, x[1]))
    elif x[0] == "percent":
        percent(data, x[1])
        print("2014", x[1], "percentage: %", percent(data, x[1]))
    return data

def main():
    try:
        data = build_data.get_data()
        print(len(data), "records loaded")
        with open(sys.argv[1], 'r') as operation:
            contents = operation.readlines()
            for line in contents:
                data = operations(line, data)
    except IOError as e:
        print("Error - ", e)
if __name__ == '__main__':
    main()