import mysql.connector
import numpy as np
import datetime
from scipy.optimize import curve_fit


def polynom(x, a, b, c, d, e, f):
    return a * x + b * x ** 2 + c * x ** 3 + d * x ** 4 + e * x ** 5 + f


class RegressionDatabase:

    def __init__(self):

        self.table ={'temperature': [],
                     'humidity': [],
                     'pressure': [],
                     'illuminance': [],
                     'date': []}

        self.records = {'days': [],
                         'nights': []
        }

        self.divided = {'date': [[None] for i in range(0, 21)],
                        'temperature': [[None] for i in range(0, 21)],
                        'humidity': [[None] for i in range(0, 21)],
                        'pressure': [[None] for i in range(0, 21)],
                        'illuminance': [[None] for i in range(0, 21)]}

        self.mean_values_20_days = {'date': [],
                                       'temperature': [],
                                       'humidity': [],
                                       'pressure': [],
                                       'illuminance': []
        }

        self.mean_values_20_nights = {'date': [],
                                       'temperature': [],
                                       'humidity': [],
                                       'pressure': [],
                                       'illuminance': []
        }

        self.predictions_day = {'temperature': 0,
                           'humidity': 0,
                           'pressure': 0,
                           'illuminance': 0}

        self.predictions_night = {'temperature': 0,
                             'humidity': 0,
                             'pressure': 0,
                             'illuminance': 0}

    def get_data_from_database(self):
        mydb = mysql.connector.connect(
            host="23.102.182.59",
            user="swawproject",
            password="swawProject1324",
            database="SWaWProject"
        )

        sql_select_query = "select * from SWaWProject"
        cursor = mydb.cursor()
        cursor.execute(sql_select_query)
        records = cursor.fetchall()


        for row in records:
            self.table['temperature'].append(row[2])
            self.table['humidity'].append(row[3])
            self.table['pressure'].append(row[4])
            self.table['illuminance'].append(row[5])
            self.table['date'].append(row[1])

    def get_single_day(self):

        j = 0

        for index, row in enumerate(self.table['date']):
            if index != 0:
                if row.day == self.table['date'][index - 1].day:
                    for key, value in self.divided.items():
                        if key == "date":
                            self.divided[key][j].append(row)
                        else:
                            self.divided[key][j].append(self.table[key][index])
                else:
                    j += 1
                    for key, value in self.divided.items():
                        if key == "date":
                            self.divided[key][j][0] = row
                        else:
                            self.divided[key][j][0] = self.table[key][index]

            else:
                for key, value in self.divided.items():
                    if key == "date":
                        self.divided[key][0][0] = row
                    else:
                        self.divided[key][0][0] = self.table[key][index]

        if len(self.divided['date']) != 20:
            self.divided['date'].pop()

    def divide_day_night_hours(self, day_data, day_temperature, day_humidity, day_pressure, day_illuminance):

            day_info_dict = {'data': day_data,
                             'temperature': day_temperature,
                             'humidity': day_humidity,
                             'pressure': day_pressure,
                             'illuminance': day_illuminance}

            day_hours_info ={'data': [],
                        'temperature': [],
                        'humidity': [],
                        'pressure': [],
                        'illuminance': []}

            night_hours_info ={'data': [],
                        'temperature': [],
                        'humidity': [],
                        'pressure': [],
                        'illuminance': []}

            day_hours = [i for i in range(9, 21)]
            night_hours = [i for i in range(21, 24)] + [i for i in range(0, 9)]

            for index, row in enumerate(day_info_dict['data']):
                if row.hour in day_hours:
                    for key, value in day_hours_info.items():
                        day_hours_info[key].append(day_info_dict[key][index])
                elif row.hour in night_hours:
                    for key, value in night_hours_info.items():
                        night_hours_info[key].append(day_info_dict[key][index])

            return day_hours_info, night_hours_info

    def get_mean_temperature_day_night(self):

        mean_values_night_hours = []
        mean_values_day_hours = []

        for index, row in enumerate(self.divided['date']):
            day_hours_info, night_hours_info = self.divide_day_night_hours(row,
                                                              self.divided['temperature'][index],
                                                              self.divided['humidity'][index],
                                                              self.divided['pressure'][index],
                                                              self.divided['illuminance'][index])

            mean_values_day_hours.append({'mean_date': day_hours_info['data'][-1],
                                 'mean_temperature': int(np.mean(day_hours_info['temperature'])),
                                 'mean_humidity': int(np.mean(day_hours_info['humidity'])),
                                 'mean_pressure': int(np.mean(day_hours_info['pressure'])),
                                 'mean_illuminance': int(np.mean(day_hours_info['illuminance']))})

            mean_values_night_hours.append({'mean_date': night_hours_info['data'][-1],
                                 'mean_temperature': int(np.mean(night_hours_info['temperature'])),
                                 'mean_humidity': int(np.mean(night_hours_info['humidity'])),
                                 'mean_pressure': int(np.mean(night_hours_info['pressure'])),
                                 'mean_illuminance': int(np.mean(night_hours_info['illuminance']))})

        return mean_values_day_hours, mean_values_night_hours

    def append_to_overall_table(self):

        mean_values_day_hours, mean_values_night_hours = self.get_mean_temperature_day_night()

        for row in mean_values_night_hours:
            for key, value in self.mean_values_20_nights.items():
                self.mean_values_20_nights[key].append(row['mean_' + key])

        for row in mean_values_day_hours:
            for key, value in self.mean_values_20_days.items():
                self.mean_values_20_days[key].append(row['mean_' + key])

    def cacl_predicted_data(self):

        self.get_single_day()
        self.append_to_overall_table()

        x_days = np.linspace(0, 19, 20)

        fit_day ={'temperature': None,
              'humidity': None,
              'pressure': None,
              'illuminance': None,
              }

        fit_night = {'temperature': None,
              'humidity': None,
              'pressure': None,
              'illuminance': None,
              }
        for key, values in fit_day.items():
            fit_day[key], _ = curve_fit(polynom, x_days, self.mean_values_20_days[key])

        for key, values in fit_day.items():
            fit_night[key], _ = curve_fit(polynom, x_days, self.mean_values_20_nights[key])

        x_days_tomorrow = np.append(x_days, 20)

        for key, value in fit_day.items():
            a, b, c, d, e, f = fit_day[key]
            self.predictions_day[key] = int(polynom(x_days_tomorrow, a, b, c, d, e, f)[-1])

        for key, value in fit_night.items():
            a, b, c, d, e, f = fit_night[key]
            self.predictions_night[key] = int(polynom(x_days_tomorrow, a, b, c, d, e, f)[-1])

    def class_precipitation(self):

        following_day = self.mean_values_20_days['date'][-1] + datetime.timedelta(days=1)

        humidity_lvl_day = {1: 80,
                       2: 77,
                       3: 70,
                       4: 63,
                       5: 59,
                       6: 61,
                       7: 62,
                       8: 64,
                       9: 73,
                       10: 76,
                       11: 80,
                       12: 82}
        humidity_lvl_night = {1: 85,
                        2: 82,
                        3: 75,
                        4: 68,
                        5: 64,
                        6: 66,
                        7: 67,
                        8: 69,
                        9: 78,
                        10: 81,
                        11: 85,
                        12: 87}

        if self.predictions_day['pressure'] >= 1000:
            if self.predictions_day['humidity'] > humidity_lvl_day[following_day.month]:
                precipitation_day = 1
            else:
                precipitation_day = 0
        else:
            precipitation_day = 1

        if self.predictions_night['pressure'] >= 1000:
            if self.predictions_night['humidity'] > humidity_lvl_night[following_day.month]:
                precipitation_night = 1
            else:
                precipitation_night = 0
        else:
            precipitation_night = 1

        return precipitation_day, precipitation_night

    def predicted_values_to_html(self):

        precipitation_day, precipitation_night = self.class_precipitation()

        with open('/var/www/html/index2.html', 'w') as file:
            file.write('<div id="TemperatureDay">' + str(self.predictions_day['temperature']) + '</div>\n')
            file.write('<div id="TemperatureNight">' + str(self.predictions_night['temperature']) + '</div>\n')
            file.write('<div id="HumidityDay">' + str(self.predictions_day['humidity']) + '</div>\n')
            file.write('<div id="HumidityNight">' + str(self.predictions_night['humidity']) + '</div>\n')
            file.write('<div id="PressureDay">' + str(self.predictions_day['pressure']) + '</div>\n')
            file.write('<div id="PressureNight">' + str(self.predictions_night['pressure']) + '</div>\n')
            file.write('<div id="IlluminanceDay">' + str(self.predictions_day['illuminance']) + '</div>\n')
            file.write('<div id="IlluminanceNight">' + str(self.predictions_night['illuminance']) + '</div>\n')
            file.write('<div id="PrecipitationDay">' + str(precipitation_day) + '</div>\n')
            file.write('<div id="PrecipitationNight">' + str(precipitation_night) + '</div>')

    def run_prediction_and_update(self):

        self.get_data_from_database()
        self.calc_predicted_data()
        self.predicted_values_to_html()


if __name__ == '__main__':

    weather_station = RegressionDatabase()
    weather_station.get_data_from_database()

    weather_station.cacl_predicted_data()

    print("temp", weather_station.mean_values_20_days['temperature'])
    print("huminidty", weather_station.mean_values_20_days['humidity'])
    print("pressure", weather_station.mean_values_20_days['pressure'])
    print("illuminance", weather_station.mean_values_20_days['illuminance'])

    print("temp n", weather_station.mean_values_20_nights['temperature'])
    print("huminidty n", weather_station.mean_values_20_nights['humidity'])
    print("pressure n", weather_station.mean_values_20_nights['pressure'])
    print("illuminance n", weather_station.mean_values_20_nights['illuminance'])

    weather_station.predicted_values_to_html()
