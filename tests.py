import comparesv


def test_basic():
	h1 = ["id", "age"]
	h2 = ["id", "age"]
	d1 = [["A1", 23], ["A2", 24], ["A3", 34]]
	d2 = [["A1", 23], ["A2", 24], ["A3", 34]]

	result = [[True, True], [True, True], [True, True]]
	values = [['[A1]:[A1]', '[23]:[23]'], ['[A2]:[A2]', '[24]:[24]'], ['[A3]:[A3]', '[34]:[34]']]
	output = comparesv.run(d1, h1, d2, h2)
	assert result == output['results']
	assert values == output['values']


def test_column_order():
	h1 = ["id", "age"]
	h2 = ["age", "id"]
	d1 = [["A1", 23], ["A2", 24], ["A3", 34]]
	d2 = [[23, "A1"], [24, "A2"], [34, "A3"]]

	result = [[True, True], [True, True], [True, True]]
	values = [['[A1]:[A1]', '[23]:[23]'], ['[A2]:[A2]', '[24]:[24]'], ['[A3]:[A3]', '[34]:[34]']]
	output = comparesv.run(d1, h1, d2, h2)
	assert result == output['results']
	assert values == output['values']


def test_fuzzy_column_order():
	h1 = ["id", "age", "building age"]
	h2 = ["age of student", "identity", "building age"]
	d1 = [["A1", 23, 100], ["A2", 24, 100], ["A3", 34, 100]]
	d2 = [[23, "A1", 100], [24, "A2", 100], [34, "A3", 100]]

	result = [[True, True, True], [True, True, True], [True, True, True]]
	values = [['[A1]:[A1]', '[23]:[23]','[100]:[100]'], ['[A2]:[A2]', '[24]:[24]','[100]:[100]'], ['[A3]:[A3]', '[34]:[34]','[100]:[100]']]
	output = comparesv.run(d1, h1, d2, h2, column_match='fuzzy')
	assert result == output['results']
	assert values == output['values']


def test_row_order_fuzzy():
	h1 = ["id", "age"]
	h2 = ["id", "age"]
	d1 = [["A1", 23], ["A2", 24], ["A3", 34]]
	d2 = [["A2", 24], ["A1", 23], ["A3", 34]]

	result = [[True, True], [True, True], [True, True]]
	values = [['[A1]:[A1]', '[23]:[23]'], ['[A2]:[A2]', '[24]:[24]'], ['[A3]:[A3]', '[34]:[34]']]
	output = comparesv.run(d1, h1, d2, h2, row_match='fuzzy')
	assert result == output['results']
	assert values == output['values']


def test_extra_column():
	h1 = ["id", "age", "name"]
	h2 = ["id", "age"]
	d1 = [["A1", 23, "Alpha"], ["A2", 24, "Beta"], ["A3", 34, "Gamma"]]
	d2 = [["A2", 24], ["A1", 23], ["A3", 34]]

	result = [[True, True, False], [True, True, False], [True, True, False]]
	values = [['[A1]:[A1]', '[23]:[23]', '[Alpha]:[]'], ['[A2]:[A2]', '[24]:[24]', '[Beta]:[]'], ['[A3]:[A3]', '[34]:[34]', '[Gamma]:[]']]
	output = comparesv.run(d1, h1, d2, h2, row_match='fuzzy')
	assert result == output['results']
	assert values == output['values']


def test_include_extra_rows():
	h1 = ["id", "age"]
	h2 = ["id", "age"]
	d1 = [["A1", 23], ["A2", 24], ["A3", 34]]
	d2 = [["A1", 23], ["A2", 24], ["A3", 34], ["A4", 34]]

	result = [[True, True], [True, True], [True, True], [False, False]]
	values = [['[A1]:[A1]', '[23]:[23]'], ['[A2]:[A2]', '[24]:[24]'], ['[A3]:[A3]', '[34]:[34]'], ['[]:[A4]', '[]:[34]']]
	output = comparesv.run(d1, h1, d2, h2, include_addnl_rows=True)
	assert result == output['results']
	assert values == output['values']


def test_include_extra_column():
	h1 = ["id", "age"]
	h2 = ["id", "age", "name"]
	d1 = [["A2", 24], ["A1", 23], ["A3", 34]]
	d2 = [["A1", 23, "Alpha"], ["A2", 24, "Beta"], ["A3", 34, "Gamma"]]

	output = comparesv.run(d1, h1, d2, h2, include_addnl_columns=True)
	result = [[False, False, False], [False, False, False], [True, True, False]]
	values = [['[A2]:[A1]', '[24]:[23]', '[]:[Alpha]'],
			  ['[A1]:[A2]', '[23]:[24]', '[]:[Beta]'],
			  ['[A3]:[A3]', '[34]:[34]', '[]:[Gamma]']]

	assert result == output['results']
	assert values == output['values']


def test_basic_case():
	h1 = ["id", "age"]
	h2 = ["id", "age"]
	d1 = [["A1", 23], ["A2", 24], ["A3", 34]]
	d2 = [["a1", 23], ["a2", 24], ["a3", 34]]

	result = [[True, True], [True, True], [True, True]]
	values = [['[A1]:[a1]', '[23]:[23]'], ['[A2]:[a2]', '[24]:[24]'], ['[A3]:[a3]', '[34]:[34]']]
	output = comparesv.run(d1, h1, d2, h2, ignore_case=True)
	assert result == output['results']
	assert values == output['values']

def test_include_rows():
	h1 = ["id", "age"]
	h2 = ["id", "age"]
	d1 = [["A1", 23], ["A2", 24], ["A3", 34]]
	d2 = [["A1", 23], ["A2", 24], ["A3", 34],["A4", 34]]

	result = [[True, True], [True, True], [True, True], [False, False]]
	values = [['[A1]:[A1]', '[23]:[23]'], ['[A2]:[A2]', '[24]:[24]'], ['[A3]:[A3]', '[34]:[34]'], ['[]:[A4]', '[]:[34]']]
	output = comparesv.run(d1, h1, d2, h2, include_addnl_rows=True)
	assert result == output['results']
	assert values == output['values']

def test_include_columns():
	h1 = ["id", "age"]
	h2 = ["id", "age","gender"]
	d1 = [["A1", 23], ["A2", 24], ["A3", 34]]
	d2 = [["A1", 23,"M"], ["A2", 24,"F"], ["A3", 34,"O"]]

	result = [[True, True, False], [True, True, False], [True, True, False]]
	values = [['[A1]:[A1]', '[23]:[23]', '[]:[M]'],
			['[A2]:[A2]', '[24]:[24]', '[]:[F]'],
			['[A3]:[A3]', '[34]:[34]', '[]:[O]']]
	headers = ['id', 'age', 'gender']
	output = comparesv.run(d1, h1, d2, h2, include_addnl_columns=True)
	assert result == output['results']
	assert values == output['values']
	assert headers == output['headers']