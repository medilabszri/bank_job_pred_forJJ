from collections import defaultdict
import pandas
import datetime


def loop_generator(day1, diff, my_format):
    for i in range(31):
        x = day1 + datetime.timedelta(days=i)
        y = x - diff
        z = x + datetime.timedelta(days=-7)
        p = y + datetime.timedelta(days=-7)
        str_x = x.strftime(my_format).replace('/0', '/')
        str_y = y.strftime(my_format).replace('/0', '/')
        str_z = z.strftime(my_format).replace('/0', '/')
        str_p = p.strftime(my_format).replace('/0', '/')
        for ab in ['A', 'B']:
            yield str_x, str_y, str_z, str_p, ab


def result_day_generator(day1, diff, my_format, my_dict):
    for str_x, str_y, str_z, str_p, ab in loop_generator(day1, diff, my_format):
        v = 0
        try:
            v = int(my_dict[(str_y, ab)] * my_dict[(str_z, ab)] / my_dict[(str_p, ab)])
        except:
            pass
        my_dict[(str_x, ab)] = v
        yield '\n' + ','.join([str_x, ab, str(v)])


def period_day_generator(day1, diff, my_format, my_dict):
    for str_x, str_y, str_z, str_p, ab in loop_generator(day1, diff, my_format):
        for i in range(1, 49):
            v = 0
            try:
                v = int(my_dict[(str_y, ab, i)] * my_dict[(str_z, ab, i)] / my_dict[(str_p, ab, i)])
            except:
                pass
            my_dict[(str_x, ab, i)] = v
            yield '\n' + ','.join([str_x, ab, str(i), str(v)])


def work(train_set_path='train_v2.csv', start_date='2020/12/1', reference_date='2018/12/4',
         output_day='test_v2_day_filled.csv', output_period='test_v2_periods_filled.csv'):
    my_dict = defaultdict(int)
    my_format = "%Y/%m/%d"
    with open(train_set_path) as input_file:
        input_file.readline()
        for line in input_file.readlines():
            line = line.split(',')
            date = line[0]
            ab = line[1]
            amount = int(line[-1])
            period = int(line[-2])
            my_dict[(date, ab)] += amount
            my_dict[(date, ab, period)] += amount

    # day0 = pandas.to_datetime('2018/11/4', format=my_format)
    # day1 = pandas.to_datetime('2020/11/1', format=my_format)

    day0 = pandas.to_datetime(reference_date, format=my_format)
    day1 = pandas.to_datetime(start_date, format=my_format)
    diff = day1 - day0

    with open(output_day, 'w') as output_file:
        output_file.write('date,post_id,amount')
        output_file.writelines(result_day_generator(day1, diff, my_format, my_dict))

    with open(output_period, 'w') as output_file:
        output_file.write('date,post_id,periods,amount')
        output_file.writelines(period_day_generator(day1, diff, my_format, my_dict))


if __name__ == '__main__':
    # work('test_v1_day.csv', '2020/11/1', '2018/11/4', 'test_v1_day_filled.csv', 'test_v1_periods_filled.csv')
    work()
