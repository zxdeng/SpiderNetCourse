import re
import os
url = 'https://study.163.com/category/480000003121024#/?p='
print(re.compile(r'\d+').findall(url)[1])