import os
import xlrd

def tolist(filename):
    result = []
    if os.path.exists(filename):
        wb = xlrd.open_workbook(filename)
        sheet = wb.sheet_by_index(0)
        row_num, clo_num = sheet.nrows, sheet.ncols
        field = sheet.row_values(0)
        for row in range(1, row_num):
            obj = {}
            data = sheet.row_values(row)
            for i in range(clo_num):
                obj[field[i]] = data[i]
            result.append(obj)
    return result



def read_field(filename):
    if os.path.exists(filename):
        wb = xlrd.open_workbook(filename)
        sheet = wb.sheet_by_index(0)
        field = sheet.row_values(0)
        return field


def read_line(filename, func):
    if os.path.exists(filename):
        wb = xlrd.open_workbook(filename)
        sheet = wb.sheet_by_index(0)
        row_num, clo_num = sheet.nrows, sheet.ncols
        field = sheet.row_values(0)
        for row in range(1, row_num):
            obj = {}
            data = sheet.row_values(row)
            for i in range(clo_num):
                obj[field[i]] = data[i]
                func(data)