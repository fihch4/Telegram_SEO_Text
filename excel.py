import pandas
import openpyxl


def write_keys_to_xlsx(list_keys):
    df = pandas.DataFrame({'Ключевые слова': list_keys
                       })
    df.to_excel('./teams.xlsx')




# write_keys_to_xlsx(['steklo', 'iphone', 'zakalennoe'])
# top_players = pd.read_excel('./teams.xlsx')
# top_players.head()
# print(top_players.head())
# excel_data_df = pandas.read_excel('records.xlsx', sheet_name='Employees')
# print(top_players['Ключевые слова'].tolist())
# df = pd.DataFrame({'Конкурент 1': ['1', '2', '3']
#                    })
# df.to_excel('./teams.xlsx')
# top_players = pd.read_excel('./teams.xlsx')
# top_players.head()
# print(top_players.head())




book = load_workbook('./teams.xlsx')
writer = pandas.ExcelWriter('./teams.xlsx', engine='openpyxl')
writer.book = book

## ExcelWriter for some reason uses writer.sheets to access the sheet.
## If you leave it empty it will not know that sheet Main is already there
## and will create a new sheet.

writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
df = pd.DataFrame({'Конкурент 1': ['1', '2', '3']
                   })
# df.to_excel(writer, "Main", cols=['Diff1', 'Diff2'])
df.to_excel(writer)

writer.save()

top_players = pd.read_excel('./teams.xlsx')
top_players.head()
print(top_players.head())