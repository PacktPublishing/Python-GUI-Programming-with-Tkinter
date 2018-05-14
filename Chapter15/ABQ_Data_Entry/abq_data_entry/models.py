import csv
import os
import json
from .constants import FieldTypes as FT
import psycopg2 as pg
from psycopg2.extras import DictCursor


class SQLModel:

    fields = {
        "Date": {'req': True, 'type': FT.iso_date_string},
        "Time": {'req': True, 'type': FT.string_list,
                 'values': ['8:00', '12:00', '16:00', '20:00']},
        "Technician": {'req': True, 'type':  FT.string_list,
                       'values': []},
        "Lab": {'req': True, 'type': FT.string_list,
                'values': []},
        "Plot": {'req': True, 'type': FT.string_list,
                 'values': []},
        "Seed sample":  {'req': True, 'type': FT.string},
        "Humidity": {'req': True, 'type': FT.decimal,
                     'min': 0.5, 'max': 52.0, 'inc': .01},
        "Light": {'req': True, 'type': FT.decimal,
                  'min': 0, 'max': 100.0, 'inc': .01},
        "Temperature": {'req': True, 'type': FT.decimal,
                        'min': 4, 'max': 40, 'inc': .01},
        "Equipment Fault": {'req': False, 'type': FT.boolean},
        "Plants": {'req': True, 'type': FT.integer,
                   'min': 0, 'max': 20},
        "Blossoms": {'req': True, 'type': FT.integer,
                     'min': 0, 'max': 1000},
        "Fruit": {'req': True, 'type': FT.integer,
                  'min': 0, 'max': 1000},
        "Min Height": {'req': True, 'type': FT.decimal,
                       'min': 0, 'max': 1000, 'inc': .01},
        "Max Height": {'req': True, 'type': FT.decimal,
                       'min': 0, 'max': 1000, 'inc': .01},
        "Median Height": {'req': True, 'type': FT.decimal,
                          'min': 0, 'max': 1000, 'inc': .01},
        "Notes": {'req': False, 'type': FT.long_string}
    }
    lc_update_query = (
                'UPDATE lab_checks SET lab_tech_id = '
                '(SELECT id FROM lab_techs WHERE name = %(Technician)s) '
                'WHERE date=%(Date)s AND time=%(Time)s AND lab_id=%(Lab)s')

    lc_insert_query = (
        'INSERT INTO lab_checks VALUES (%(Date)s, %(Time)s, %(Lab)s, '
        '(SELECT id FROM lab_techs WHERE name LIKE %(Technician)s))')

    pc_update_query = (
        'UPDATE plot_checks SET seed_sample = %(Seed sample)s, '
        'humidity = %(Humidity)s, light = %(Light)s, '
        'temperature = %(Temperature)s, '
        'equipment_fault = %(Equipment Fault)s, '
        'blossoms = %(Blossoms)s, plants = %(Plants)s, '
        'fruit = %(Fruit)s, max_height = %(Max Height)s, '
        'min_height = %(Min Height)s, median_height = %(Median Height)s, '
        'notes = %(Notes)s WHERE date=%(Date)s AND time=%(Time)s '
        'AND lab_id=%(Lab)s AND plot=%(Plot)s')

    pc_insert_query = (
        'INSERT INTO plot_checks VALUES (%(Date)s, %(Time)s, %(Lab)s,'
        ' %(Plot)s, %(Seed sample)s, %(Humidity)s, %(Light)s,'
        ' %(Temperature)s, %(Equipment Fault)s, %(Blossoms)s, %(Plants)s,'
        ' %(Fruit)s, %(Max Height)s, %(Min Height)s,'
        ' %(Median Height)s, %(Notes)s)')

    def __init__(self, host, database, user, password):
        self.connection = pg.connect(host=host, database=database,
            user=user, password=password, cursor_factory=DictCursor)

        techs = self.query("SELECT * FROM lab_techs ORDER BY name")
        labs = self.query("SELECT id FROM labs ORDER BY id")
        plots = self.query("SELECT DISTINCT plot FROM plots ORDER BY plot")
        self.fields['Technician']['values'] = [x['name'] for x in techs]
        self.fields['Lab']['values'] = [x['id'] for x in labs]
        self.fields['Plot']['values'] = [str(x['plot']) for x in plots]


    def query(self, query, parameters=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, parameters)
        except (pg.Error) as e:
            self.connection.rollback()
            raise e
        else:
            self.connection.commit()
            # cursor.description is None when
            # no rows are returned
            if cursor.description is not None:
                return cursor.fetchall()

    def get_all_records(self, all_dates=False):
        """Return all records.

        By default, only return today's records, unless
        all_dates is True.
        """
        query = ('SELECT * FROM data_record_view '
            'WHERE NOT %(all_dates)s OR "Date" = CURRENT_DATE '
            'ORDER BY "Date", "Time", "Lab", "Plot"')
        return self.query(query, {'all_dates': all_dates})

    def get_record(self, date, time, lab, plot):
        """Return a single record

        requires all four key values
        """
        query = (
            'SELECT * FROM data_record_view '
            'WHERE "Date" = %(date)s AND "Time" = %(time)s '
            'AND "Lab" = %(lab)s AND "Plot" = %(plot)s')
        result = self.query(
            query, {"date": date, "time": time,
                    "lab": lab, "plot": plot})
        return result[0] if result else {}

    def save_record(self, record):

        date = record['Date']
        time = record['Time']
        lab = record['Lab']
        plot = record['Plot']

        if self.get_lab_check(date, time, lab):
            lc_query = self.lc_update_query
        else:
            lc_query = self.lc_insert_query
        if self.get_record(date, time, lab, plot):
            pc_query = self.pc_update_query
            self.last_write = 'update'
        else:
            pc_query = self.pc_insert_query
            self.last_write = 'insert'

        self.query(lc_query, record)
        self.query(pc_query, record)

    def get_lab_check(self, date, time, lab):
        query = ('SELECT date, time, lab_id, lab_tech_id, '
            'lt.name as lab_tech FROM lab_checks JOIN lab_techs lt '
            'ON lab_checks.lab_tech_id = lt.id WHERE '
            'lab_id = %(lab)s AND date = %(date)s AND time = %(time)s')
        results = self.query(
            query, {'date': date, 'time': time, 'lab': lab})
        return results[0] if results else {}

    def get_current_seed_sample(self, lab, plot):
        result = self.query('SELECT current_seed_sample FROM plots '
            'WHERE lab_id=%(lab)s AND plot=%(plot)s',
            {'lab': lab, 'plot': plot})
        return result[0]['current_seed_sample'] if result else ''

    def add_weather_data(self, data):
        query = (
            'INSERT INTO local_weather VALUES '
            '(%(observation_time_rfc822)s, %(temp_c)s, '
            '%(relative_humidity)s, %(pressure_mb)s, '
            '%(weather)s)'
        )
        try:
            self.query(query, data)
        except pg.IntegrityError:
            # already have weather for this datetime
            pass

    def get_growth_by_lab(self):
        query = (
            'SELECT date - (SELECT min(date) FROM plot_checks) AS day, '
            'lab_id, avg(median_height) AS avg_height FROM plot_checks '
            'GROUP BY date, lab_id ORDER BY day, lab_id;'
        )
        return self.query(query)

    def get_yield_by_plot(self):
        query = (
            'SELECT lab_id, plot, seed_sample, MAX(fruit) AS yield, '
            'AVG(humidity) AS avg_humidity, '
            'AVG(temperature) AS avg_temperature '
            'FROM plot_checks WHERE NOT equipment_fault '
            'GROUP BY lab_id, plot, seed_sample'
        )
        return self.query(query)


class CSVModel:
    """CSV file storage"""

    fields = {
        "Date": {'req': True, 'type': FT.iso_date_string},
        "Time": {'req': True, 'type': FT.string_list,
                 'values': ['8:00', '12:00', '16:00', '20:00']},
        "Technician": {'req': True, 'type':  FT.string},
        "Lab": {'req': True, 'type': FT.string_list,
                'values': ['A', 'B', 'C', 'D', 'E']},
        "Plot": {'req': True, 'type': FT.string_list,
                 'values': [str(x) for x in range(1, 21)]},
        "Seed sample":  {'req': True, 'type': FT.string},
        "Humidity": {'req': True, 'type': FT.decimal,
                     'min': 0.5, 'max': 52.0, 'inc': .01},
        "Light": {'req': True, 'type': FT.decimal,
                  'min': 0, 'max': 100.0, 'inc': .01},
        "Temperature": {'req': True, 'type': FT.decimal,
                        'min': 4, 'max': 40, 'inc': .01},
        "Equipment Fault": {'req': False, 'type': FT.boolean},
        "Plants": {'req': True, 'type': FT.integer,
                   'min': 0, 'max': 20},
        "Blossoms": {'req': True, 'type': FT.integer,
                     'min': 0, 'max': 1000},
        "Fruit": {'req': True, 'type': FT.integer,
                  'min': 0, 'max': 1000},
        "Min Height": {'req': True, 'type': FT.decimal,
                       'min': 0, 'max': 1000, 'inc': .01},
        "Max Height": {'req': True, 'type': FT.decimal,
                       'min': 0, 'max': 1000, 'inc': .01},
        "Median Height": {'req': True, 'type': FT.decimal,
                          'min': 0, 'max': 1000, 'inc': .01},
        "Notes": {'req': False, 'type': FT.long_string}
    }


    def __init__(self, filename, filepath=None):

        if filepath:
            if not os.path.exists(filepath):
                os.mkdir(filepath)
            self.filename = os.path.join(filepath, filename)
        else:
            self.filename = filename

    def get_all_records(self):
        """Read in all records from the CSV and return a list"""
        if not os.path.exists(self.filename):
            return []

        with open(self.filename, 'r', encoding='utf-8') as fh:
            # turning fh into a list is necessary for our unit tests
            csvreader = csv.DictReader(list(fh.readlines()))
            missing_fields = set(self.fields.keys()) - set(csvreader.fieldnames)
            if len(missing_fields) > 0:
                raise Exception(
                    "File is missing fields: {}"
                    .format(', '.join(missing_fields))
                )
            else:
                records = list(csvreader)

        # Correct issue with boolean fields
        trues = ('true', 'yes', '1')
        bool_fields = [
            key for key, meta
            in self.fields.items()
            if meta['type'] == FT.boolean
        ]
        for record in records:
            for key in bool_fields:
                record[key] = record[key].lower() in trues
        return records

    def get_record(self, rownum):
        """Get a single record by row number

        Callling code should catch IndexError
          in case of a bad rownum.
        """

        return self.get_all_records()[rownum]

    def save_record(self, data, rownum=None):
        """Save a dict of data to the CSV file"""

        if rownum is not None:
            # This is an update
            records = self.get_all_records()
            records[rownum] = data
            with open(self.filename, 'w', encoding='utf-8') as fh:
                csvwriter = csv.DictWriter(fh, fieldnames=self.fields.keys())
                csvwriter.writeheader()
                csvwriter.writerows(records)
        else:
            # This is a new record
            newfile = not os.path.exists(self.filename)

            with open(self.filename, 'a', encoding='utf-8') as fh:
                csvwriter = csv.DictWriter(fh, fieldnames=self.fields.keys())
                if newfile:
                    csvwriter.writeheader()
                csvwriter.writerow(data)


class SettingsModel:
    """A model for saving settings"""

    variables = {
        'autofill date': {'type': 'bool', 'value': True},
        'autofill sheet data': {'type': 'bool', 'value': True},
        'font size': {'type': 'int', 'value': 9},
        'theme': {'type': 'str', 'value': 'default'},
        'db_host': {'type': 'str', 'value': 'localhost'},
        'db_name': {'type': 'str', 'value': 'abq'},
        'weather_station': {'type': 'str', 'value': 'KBMG'},
        'abq_auth_url': {
            'type': 'str',
            'value': 'http://localhost:8000/auth'},
        'abq_upload_url': {
            'type': 'str',
            'value': 'http://localhost:8000/upload'},
        'abq_ftp_host': {'type': 'str', 'value': 'localhost'},
        'abq_ftp_port': {'type': 'int', 'value': 2100}
    }

    def __init__(self, filename='abq_settings.json', path='~'):
        # determine the file path
        self.filepath = os.path.join(os.path.expanduser(path), filename)

        # load in saved values
        self.load()

    def set(self, key, value):
        """Set a variable value"""
        if (
            key in self.variables and
            type(value).__name__ == self.variables[key]['type']
        ):
            self.variables[key]['value'] = value
        else:
            raise ValueError("Bad key or wrong variable type")

    def save(self, settings=None):
        """Save the current settings to the file"""
        json_string = json.dumps(self.variables)
        with open(self.filepath, 'w', encoding='utf-8') as fh:
            fh.write(json_string)

    def load(self):
        """Load the settings from the file"""

        # if the file doesn't exist, return
        if not os.path.exists(self.filepath):
            return

        # open the file and read in the raw values
        with open(self.filepath, 'r', encoding='utf-8') as fh:
            raw_values = json.loads(fh.read())

        # don't implicitly trust the raw values, but only get known keys
        for key in self.variables:
            if key in raw_values and 'value' in raw_values[key]:
                raw_value = raw_values[key]['value']
                self.variables[key]['value'] = raw_value
