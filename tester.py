import getFromDB

def main():
    # print(getFromDB.getWeeks())
    week_tuples = [('2023 W40',), ('2023 W41',), ('2023 W43',), ('2023 W42',), ('2023 W39',)]
    
    #convert tuples to strings
    week_strings = [week_tuple[0] for week_tuple in week_tuples]
    data = []
    for week in week_strings:
        print(getFromDB.weekToDateRange(week))

        #get load miles for week
        miles = getFromDB.getMilesForWeek(week)

        #change week to date range
        start_date, end_date = getFromDB.weekToDateRange(week)
        miles['Week'] = f"{start_date} - {end_date}"

        data.append(miles)
        #print(miles)
        #print("\n")
        #print(data)
    
    monthStr = "2023 M10"

    destinationsData = getFromDB.getDestinationCountsFromUtahByMonth(monthStr)
    print(destinationsData)

    print(getFromDB.getMonthyRevenue(monthStr))
    print('\n')
    print(getFromDB.getWeeklyRevenue('2023 W40'))
            

if __name__ == "__main__":
    main()