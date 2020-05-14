import pandas as pd 
import pygal

def chart_data(start_date, end_date):

    #read files
    exchange_rates = pd.read_excel('data/FX_EUR_GBP.xlsx', names = ['Name', 'GBP', 'EUR'])
    time_series_data = pd.read_excel('data/TimeSeriesData_Apr15-Apr20.xlsx') #Name is Date
    static_data_20_04_2020 = pd.read_excel('data/StaticData_Apr20.xlsx')

    #data
    data = pd.merge(time_series_data, exchange_rates, on= 'Name')
    companies = static_data_20_04_2020['NAME'].tolist()
    currency_code_list = dict(zip(companies, static_data_20_04_2020['CURRENCY CODE'].tolist()))
    number_of_dates = len(time_series_data["Name"])
    dates = range(0, number_of_dates)

    #Divisor
    total_market_cap = 0
    for company in companies: 
        total_market_cap += data[company][0] * data[f"{company} - NUMBER OF SHARES"][0]
    D = total_market_cap / 100

    #daily index values
    index_values = []
    for date in dates:
        total_market_cap = 0
        for company in companies: 
            total_market_cap += data[company][date] * data[f"{company} - NUMBER OF SHARES"][date]
        M = 0
        for company in companies:
            price = data[company][date]
            shares_outstanding = data[f"{company} - NUMBER OF SHARES"][date]
            free_float = data[f"{company} - FREE FLOAT NOSH"][date]
            company_cap = data[company][date] * data[f"{company} - NUMBER OF SHARES"][date]
            weighted_cap = company_cap / total_market_cap
            exchange_rate = 1
            if currency_code_list[company] == 'GBP':
                exchange_rate = data['GBP'][date]
            elif currency_code_list[company] == 'EUR':
                exchange_rate = data['EUR'][date]
            M += (price * shares_outstanding * free_float * weighted_cap * exchange_rate)
        daily_index = M / D
        index_values.append(daily_index)

    df = pd.DataFrame(data={"date": data["Name"], "daily_index_values": index_values})
    data_in_dates = df.where(df["date"] >= start_date).where(df["date"] <= end_date).dropna()
    return data_in_dates

def create_chart(data):
    line_chart = pygal.Line(height=500, width=1300, explicit_size=True, x_label_rotation=20, x_title = "Date", y_title="Index Points")
    line_chart.title = 'Daily Index Values'
    x_axis = []
    for date in data['date']:
        str_date = str(date).split(" ")[0]
        x_axis.append(str_date)
    if len(x_axis) > 30 and len(x_axis) <= 252:
        for index, val in enumerate(x_axis):
            if index == 0 or index == len(x_axis) - 1:
                x_axis[index] = val
            elif val.split('-')[2] == '01':
                x_axis[index] = val
            elif val.split('-')[2] == '02' and x_axis[index - 1] == '':
                x_axis[index] = val
            elif val.split('-')[2] == '03' and x_axis[index - 1] == '' and x_axis[index - 2] == '':
                x_axis[index] = val
            else:
                x_axis[index] = ''
    elif len(x_axis) > 252:
        for index, val in enumerate(x_axis):
            if index == 0 or index == len(x_axis) - 1:
                x_axis[index] = val
            elif val.split('-', 1)[1] == '01-01':
                x_axis[index] = val
            elif val.split('-', 1)[1] == '01-02' and x_axis[index - 1] == '':
                x_axis[index] = val
            elif val.split('-', 1)[1] == '01-03' and x_axis[index - 1] == '' and x_axis[index - 2] == '':
                x_axis[index] = val
            else:
                x_axis[index] = '' 
    line_chart.x_labels = x_axis
    line_chart.add(None,data['daily_index_values'].tolist())
    return line_chart