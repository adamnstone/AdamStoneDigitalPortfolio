import matplotlib.pyplot as plt
from zoho_sheets_api import Zoho
import math

class Graphing:
    def __init__(self):
        self.c = -1

    def format_for_graphing(self, x_statistic, y_statistic, zoho):
        x_data = zoho.get_column_of_header(x_statistic)["range_details"][1:]
        y_data = zoho.get_column_of_header(y_statistic)["range_details"][1:]
        if int(x_data[0]["row_index"]) > int(y_data[0]["row_index"]):
            for i in range(len(y_data)):
                if y_data[i]["row_index"] == x_data[0]["row_index"]:
                    y_data = y_data[i:]
                    break
        else:
            for i in range(len(x_data)):
                if x_data[i]["row_index"] == y_data[0]["row_index"]:
                    x_data = x_data[i:]
                    break

        if len(x_data) > len(y_data):
            x_data = x_data[:len(y_data)]
        else:
            y_data = y_data[:len(x_data)]

        x_data = [x["row_details"][0]["content"] for x in x_data]
        y_data = [x["row_details"][0]["content"] for x in y_data]

        if not x_data[0].strip():
            x_data[0] = x_data[1]

        if not y_data[0].strip():
            y_data[0] = y_data[1]

        x_data = [(x[1:] if x[0] == "$" else (str(-int(x[2:]))) if x[1] == "$" else x) if x.strip() else x for x in x_data]
        y_data = [(x[1:] if x[0] == "$" else (str(-int(x[2:]))) if x[1] == "$" else x) if x.strip() else x for x in y_data]

        return x_data, y_data

    def next_counter(self):
        self.c += 1
        return self.c

    def reset_counter(self):
        self.c = -1

    def add_array(self, a):
        n = 0
        for i in a:
            n += i
        return n

    def sum_weeks(self, a):
        new_a = []
        for i in range(math.floor(len(a) / 7)):
            new_a.append(self.add_array(a[i * 7:i * 7 + 7]))
        return new_a

    def display_graphs(self, x_statistics, y_statistics, daily=True, weekly=True):
        zoho = Zoho()

        if len(x_statistics) != len(y_statistics):
            raise Exception(f"ERROR: X Statistics Length {len(x_statistics)} and Y Statistics Not The Same: {len(y_statistics)}")

        for d in range(2):
            fig, axs = plt.subplots(2, math.ceil(len(x_statistics) / 2))
            fig.suptitle(f"Laundromat Statistics {'Daily' if d == 0 else 'Weekly'}:")
            if ((not daily) and d == 0) or ((not weekly) and d == 1):
                continue
            for i in range(len(x_statistics)):
                xs, ys = self.format_for_graphing(x_statistics[i], y_statistics[i], zoho)

                try:
                    xs = [float(x.split()[0]) if x else 0 for x in xs]
                except Exception as e:
                    print(f"Error converting xs {xs[:3]}... to floats, skipping: {e}")
                try:
                    ys = [float(x.split()[0]) if x else 0 for x in ys]
                except Exception as e:
                    print(f"Error converting ys {ys[:3]}... to floats, skipping: {e}")

                starting_date_x = None
                starting_date_y = None

                if x_statistics[i].strip() == "Date":
                    starting_date_x = xs[0]
                    xs = range(len(ys))
                elif d == 1:
                    xs = self.sum_weeks(xs)
                if y_statistics[i].strip() == "Date":
                    starting_date_y = ys[0]
                    ys = range(len(xs))
                elif d == 1:
                    ys = self.sum_weeks(ys)

                if len(xs) > len(ys):
                    xs = xs[:len(ys)]
                else:
                    ys = ys[:len(xs)]

                print(f"XS: {xs}")
                print(f"YS: {ys}")

                axs_t = None

                try:
                    axs_t = axs[i % 2, int(i / 2)]
                except Exception as e:
                    print(f"Error with using [i] for axs so treating as non-list/tuple: {str(e)}")
                    axs_t = axs

                axs_t.plot(xs, ys)
                axs_t.set(xlabel=x_statistics[i] + " ($)" if x_statistics[i].strip() != "Date" else x_statistics[i] + f" {'weekly' if d == 1 else ''} starting from {starting_date_x}")
                axs_t.set(ylabel=y_statistics[i] + " ($)" if y_statistics[i].strip() != "Date" else y_statistics[i] + f" {'weekly' if d == 1 else ''} starting from {starting_date_y}")

            plt.show()

if __name__ == "__main__":
    graphing = Graphing()
    graphing.display_graphs(["Date" for x in range(5)], ["Washer", "Dryer", "Retail 5609", "Retail 3001", "Retail 5935"])
