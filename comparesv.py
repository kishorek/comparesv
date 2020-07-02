import os
from fuzzywuzzy import fuzz, process
from collections import OrderedDict
import time

ROW_THRESHOLD = 80
CELL_THRESHOLD = 80

__version__ = 0.01

def run(data1,
        headers1,
        data2,
        headers2,
        ignore_case=False,
        row_match='order',
        column_match='exact',
        string_match='exact',
        include_addnl_rows=False,
        include_addnl_columns=False,
        include_stats=True,
        save_output=True,
        ticker=None):
    headers1 = cleanup(headers1)
    headers2 = cleanup(headers2)
    matched_headers = prepare_headers(data1, headers1, headers2, column_match)
    comparison_output, added_rows, deleted_rows = compare_data(data1, data2, headers1, headers2, matched_headers, row_match=row_match, string_match=string_match, include_addnl_rows=include_addnl_rows,
                                                               include_addnl_columns=include_addnl_columns, ignore_case=ignore_case)

    rows_result_list, rows_values_list = populate_output(comparison_output)
    final_headers = headers1
    if include_addnl_columns:
        updated_headers = populate_headers(matched_headers, headers2)
        final_headers = final_headers + updated_headers

    final_result = {}
    final_result["results"] = rows_result_list
    final_result["values"] = rows_values_list
    final_result["added"] = added_rows
    final_result["deleted"] = deleted_rows
    final_result["headers"] = final_headers

    if include_stats:
        stats = populate_stats(final_headers, rows_result_list)
        final_result["stats"] = stats

    return final_result


def populate_stats(headers, results_list):
    stat = {}
    for index, header in enumerate(headers):
        header_data = [result[index] for result in results_list]
        total_records = len(header_data)
        matched_records = header_data.count(True)
        match_percentage = 100 * matched_records/total_records
        stat[header] = "{:.2f}".format(match_percentage)
    return stat


def populate_output(rows_match):
    rows_result_list = []
    rows_values_list = []
    for match in rows_match:
        row_result = []
        value_result = []
        for item in match:
            value_result.append(item[0])
            row_result.append(item[1])
        rows_result_list.append(row_result)
        rows_values_list.append(value_result)

    return rows_result_list, rows_values_list


def populate_headers(header_index, headers2):
    mapped_headers2 = [value['matched_header'] for item, value in header_index.items() if value['index'] > -1]
    addnl_headers2 = [header for header in headers2 if header not in mapped_headers2]
    return addnl_headers2


def compare_data(data1, data2, headers1, headers2, matched_headers, **kwargs):
    added_rows = []
    common_rows = []
    deleted_rows = []

    rows_output = []
    row_match = kwargs['row_match']
    data2_compared_indices = []

    # Comparing the data1 rows with available rows in data2
    for index, row1 in enumerate(data1):
        row2 = None
        data2_indices = list(range(len(data2)))
        data2_indices_left = [item for item in data2_indices if item not in data2_compared_indices]
        if row_match == 'order' and index < len(data2):
            row2 = data2[index]
            data2_compared_indices.append(index)
        elif row_match == 'fuzzy':
            row2, row2_index = fuzzy_row_find(row1, data2, headers1, matched_headers, data2_indices_left)
            data2_compared_indices.append(row2_index)
        elif row_match == 'deep':
            row2, row2_index = deep_row_find(row1, data2, headers1, headers2, matched_headers, data2_indices_left, kwargs)
            data2_compared_indices.append(row2_index)

        row_compare_result, mode = compare_rows(row1, row2, matched_headers, headers2, kwargs)
        if mode == 'added':
            added_rows.append(row2)
        elif mode == 'deleted':
            deleted_rows.append(row1)
        rows_output.append(row_compare_result)

    if kwargs.get('include_addnl_rows'):
        # Calculate and process the remaining records left in data2
        data2_indices = list(range(len(data2)))
        data2_indices_left = [item for item in data2_indices if item not in data2_compared_indices]
        for index in data2_indices_left:
            row1 = None
            row2 = data2[index]
            row_compare_result, mode = compare_rows(row1, row2, matched_headers, headers2, kwargs)
            added_rows.append(row2)
            rows_output.append(row_compare_result)
    return rows_output, added_rows, deleted_rows


def cleanup(headers):
    return [header.strip() for header in headers]


def exist_in_list(option, option_list):
    cleaned_list = [str(o).lower().strip() for o in option_list]
    exists = str(option).lower().strip() in cleaned_list
    index = -1
    if exists:
        index = cleaned_list.index(str(option).lower().strip())
    return exists, index


def prepare_headers(data1, headers1, headers2, column_match):
    mapped_headers_index = OrderedDict()
    mapped_indices2 = []
    for idx, header in enumerate(headers1):
        index = -1
        if column_match == 'exact':
            exists, index = exist_in_list(header, headers2)
        elif column_match == 'fuzzy':
            unmapped_header_indices = [x for x in range(len(headers2)) if x not in mapped_indices2]
            index = fuzzy_column_index(header, headers2, unmapped_header_indices)
            mapped_indices2.append(index)

        column_data = {}
        column_data['index'] = index
        if index != -1:
            column_data['matched_header'] = headers2[index]
            column_data['type'] = predict_column_type([val[idx] for val in data1])
        mapped_headers_index[header] = column_data

    return mapped_headers_index


def fuzzy_column_index(header, headers_list, unmapped_header_indices):
    unmapped_headers = [x for i,x in enumerate(headers_list) if i in unmapped_header_indices]

    exist, index = exist_in_list(header, unmapped_headers)
    if exist:
        original_index = unmapped_header_indices[index]
        return original_index

    highest = process.extractOne(header, unmapped_headers)
    if highest[1] < ROW_THRESHOLD:
        return -1
    unmapped_index = unmapped_headers.index(highest[0])
    original_index = unmapped_header_indices[unmapped_index]
    return original_index


def deep_row_find(row, data2, headers1, headers2, matched_headers, data2_indices_left, opts):
    """
    1. Take a row from data1
    2. Compare against all the rows in data2 by column wise data
    3. Get the best matched one
    """
    count = 0
    selected_index = -1
    selected_row = None
    for index in data2_indices_left:
        row2 = data2[index]
        row_comparison = compare_rows(row, row2, matched_headers, headers2, opts)
        results = [x[1] for x in row_comparison[0]]
        if results.count(True) > count:
            count = results.count(True)
            selected_index = index
            selected_row = row2
    
    return selected_row, selected_index

def fuzzy_row_find(row, data2, headers1, matched_headers, unmapped_indices2):
    row1 = ' '.join(str(x) for x in row)
    unmapped_data2 = [' '.join(str(x) for x in elem) for index, elem in enumerate(data2) if index in unmapped_indices2]
    highest = process.extractOne(row1, unmapped_data2)

    if highest[1] < ROW_THRESHOLD:
        return None, None

    index = unmapped_data2.index(highest[0])
    original_index = unmapped_indices2[index]
    return data2[original_index], original_index


def compare_rows(row1, row2, header_index, headers2, opts):
    mode = "existing"
    if not row1:
        mode = "added"
    if not row2:
        mode = "deleted"

    row_result = []
    for index, column in enumerate(header_index.keys()):
        result = None
        column_info = header_index[column]
        cell1 = row1[index] if row1 else ""
        cell2 = row2[column_info['index']] if row2 and column_info['index'] > -1 else ""

        result = compare_cells(cell1, cell2, fetch_compare_mode(column_info.get('type'), opts['string_match']), opts['ignore_case'])
        output = [f"[{cell1}]:[{cell2}]", result]
        row_result.append(output)

    if opts.get('include_addnl_columns'):
        mapped_headers2 = [value['matched_header'] for item, value in header_index.items() if value['index'] > -1]
        addnl_headers2_indices = [headers2.index(header) for header in headers2 if header not in mapped_headers2]
        for index in addnl_headers2_indices:
            cell1 = ""
            cell2 = row2[index]

            result = compare_cells(cell1, cell2, "str", opts['ignore_case'])
            output = [f"[{cell1}]:[{cell2}]", result]
            row_result.append(output)

    return row_result, mode


def fetch_compare_mode(data_type, string_match):
    if data_type == 'str' and string_match == 'fuzzy':
        return "fuzzy_string"
    else:
        return data_type


def compare_cells(cell1, cell2, comparison_type, ignore_case):
    if not cell1 and not cell2:
        return True
    elif not cell1 or not cell2:
        return False

    try:
        if comparison_type == 'fuzzy_string':
            if fuzz.token_set_ratio(cell1, cell2) > CELL_THRESHOLD:
                return True
        elif comparison_type == 'int':
            return int(cell1) == int(cell2)
        elif comparison_type == 'float':
            return float(cell1) == float(cell2)
        else:
            if ignore_case:
                cell1 = cell1.lower()
                cell2 = cell2.lower()

            return str(cell1).strip() == str(cell2).strip()
    except:
        if ignore_case:
            cell1 = cell1.lower()
            cell2 = cell2.lower()
        return str(cell1).strip() == str(cell2).strip()


def predict_column_type(data):
    """
    Predict the data type of the elements present in a list. It will be defaulted to string.

    Args:
        data : array

    Returns:
        type: Column data type
    """
    data_types = [type(item) for item in data]
    data_types = list(set(data_types))
    if len(data_types) == 1:
        return data_types[0].__name__
    elif str in data_types:
        return "str"
    elif float in data_types:
        return "float"
    elif int in data_types:
        return "int"
    else:
        return "str"