import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options


driver = full_table_data = None

def setup_module():
    global driver
    test_url = 'https://mystifying-beaver-ee03b5.netlify.app/'
    # options = Options()
    # options.add_argument('--headless')
    s=Service(ChromeDriverManager().install())
    # driver = webdriver.Chrome(service=s, options=options) # To run in headless mode
    driver = webdriver.Chrome(service=s)
    driver.get(test_url)
    driver.maximize_window()

def teardown_module():
    driver.quit()

def get_table_rows(filter_text, sort_field):
    """
        This method will fetch all the rows from the table and return them as a list of dictionaries.
        By doing this we will be able to access the column data using a the keys which are not impacted by any changes in the order/index of the columns.
    """
    filter = driver.find_element(By.ID, 'filter-input')
    filter.clear()
    filter.send_keys(filter_text)

    dropdown = Select(driver.find_element(By.ID, 'sort-select'))
    dropdown.select_by_value(sort_field)

    table_elements = driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div[2]').find_elements(By.CLASS_NAME,'table-row')

    table_data = []
    
    for table_row in table_elements:
        row = {}
        for col in table_row.find_elements(By.CLASS_NAME, 'table-data'):   
            col_name = col.get_attribute("class").split(' ')[1].split('-')[1]     
            row[col_name] = col.text.lower()
        table_data.append(row)

    return table_data

# Verify if the page loaded successfully
def test_01_check_page_load():
    h1 = driver.find_element(By.TAG_NAME, 'h1')
    assert h1.text == "Cyber attack completely fake statistics", "Page din't load successfully"

# Verify if table is present 
def test_02_check_table_presence():
    global full_table_data
    full_table_data = get_table_rows('', 'name') # This is the full table data. This will be used as reference for the validations done in all the succeeding tests.
    assert full_table_data is not None, "Table not present"

# Verifying that the data is sorted by NAME as expected
def test_03_filter_empty_sort_name():
    table = get_table_rows('', 'name')
    # Making sure that all the records in the full table are pulled in the above call since we are not filtering by anything
    assert len(table) == len(full_table_data), "Row count mismatch"

    table_names = [x['name'] for x in table]
    # Making sure that the names fetched are all in sorted order
    assert table_names == sorted(table_names), "Table not sorted accurately on NAME"

# Verifying that the data is sorted by NUMBER OF CASES as expected
def test_04_filter_empty_sort_cases():
    table = get_table_rows('', 'cases')
    table_cases = []
    for row in table:
        if 'k' in row['cases']:
            table_cases.append(float(row['cases'][:-1])*1000)
        elif 'm' in row['cases']:
            table_cases.append(float(row['cases'][:-1])*1000000)
        elif 'b' in row['cases']:
            table_cases.append(float(row['cases'][:-1])*1000000000)
        else:
            table_cases.append(float(row['cases']))

    assert table_cases == sorted(table_cases), "Table not sorted accurately on NUMBER OF CASES"

# Verifying that the data is sorted by AVERAGE IMPACT SCORE as expected
def test_05_filter_empty_sort_averageImpact():
    table = get_table_rows('', 'averageImpact')
    table_averageImpact = [float(x['averageImpact']) for x in table]
    assert table_averageImpact == sorted(table_averageImpact), "Table not sorted accurately on AVERAGE IMPACT SCORE"
    
# Verifying that the data is sorted by COMPLEXITY as expected
def test_06_filter_empty_sort_complexity():
    complexity_order = {'low': 1, 'medium': 2, 'high': 3}
    table = get_table_rows('', 'complexity')
    table_complexity = [x['complexity'] for x in table]
    # Sorting the complexity based on the custom sort order, i.e., low < medium < high and making sure its same as the order retrieved from the table
    assert table_complexity == sorted(table_complexity, key=lambda x:complexity_order[x]), "Table not sorted accurately on COMPLEXITY"

# Verifying that the filtered data is sorted by NAME as expected
# This test case can be written as 2 cases, i.e., 1 for full match filtering and another for partial match filtering if need be.
def test_07_filter_valid_text_sort_name():
    filter_txt = 'hi'
    table = get_table_rows(filter_txt, 'name')
    # Comparing the number of records returned by filtering in the UI to the number of records present in the refernce table having the filter text in the name or complexity
    assert len(table) == len([row for row in full_table_data if filter_txt in row['name'] or filter_txt in row['complexity']]), "Row count mismatch"

    table_names = [x['name'] for x in table]
    # Validating that the names are sorted as expected in the filtered records
    assert table_names == sorted(table_names), "Table not sorted accurately on NAME"

# Verifying that the filtering by numeric fields dont fetch any records
# Writing this test assuming this is a requirement, that the filters should work only on the text field.
# Another assumption here is that there are no numbers present in the text fields. This may not work as expected in such a scenario.
def test_08_filter_numbers_sort_name():
    filter_txt = '95'
    table = get_table_rows(filter_txt, 'name')
    assert len(table) == 0, "Filter not working as expected with number"

# Verifying that when we filter with a text that is not present in the table, then no records are returned.
def test_09_filter_invalid_text_sort_name():
    filter_txt = 'zzzzzzzzzzzzzzzzzzzzzzz'
    table = get_table_rows(filter_txt, 'name')
    assert len(table) == 0, "Filter not working as expected when using a text that is not present in the table"

# Verifying that the filter is case insensitive
def test_10_filter_case_insensitive_text_sort_averageImpact():
    table_upper = get_table_rows('m', 'name')
    table_lower = get_table_rows('M', 'name')
    assert table_lower == table_upper, "Filter doesn't seem to be case insensitive"