import json

class Chart:
    def __init__(self, type, title, data):
        self.type=type
        self.data = data
        self.data_points = []
        self.title = title
        self.chart_data = None

    def parse_data(self):
        response_string = f"{{\ntitle: {{\ntext : '{self.title}'\n}},\ndata: [\n{{\n"
        response_string +=f"type: '{self.type}',\ndataPoints: "
        dps = []
        for d in self.data:
            dps.append(f"{{label: '{str(d.date)}'\n,y: {d.reading}}},\n")
        last_value = dps[-1]
        last_value = last_value[0:-2]
        dps[-1]=last_value
        concat = "".join(dps)
        response_string+=f'\n[\n{concat}]\n}}]\n}}'
        print(response_string)
        self.chart_data = response_string

    def update_page(self, path, target):
        self.parse_data()
        chart_file_data = []
        with open(path, "r+") as f:
            line_entry = f.readlines()
            for line in line_entry:
                if 'replace' in line:
                    #converted_dictionary = json.dumps(self.chart_data, indent=4)
                    line = self.chart_data
                chart_file_data.append(line)

        with open(target, "w") as f:
            f.truncate(0)
            f.write("".join(chart_file_data))


