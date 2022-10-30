class DataTransformer:
    @staticmethod
    def format_dates(line):
        delimit = line.split(',')
        date_range = f'?period_from={delimit[0]}T00:00Z&period_to={delimit[1]}T00:00Z'
        return date_range