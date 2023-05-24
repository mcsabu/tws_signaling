
import pandas

sickle_wick_data = []
sickle_wick_frame = pandas.DataFrame(sickle_wick_data, columns=['reqID', 'Symbol'])
sickle_wick_frame.to_csv(f'C:\\Users\\user\\PycharmProjects\\pythonProject\\'
                         f'sickle_wick_list.csv', index=False)
