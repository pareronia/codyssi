import sys

from .. import CONFIG
from .table import Table

number_of_problems = CONFIG.get_number_of_problems()

Table(number_of_problems).generate(sys.argv[1])
