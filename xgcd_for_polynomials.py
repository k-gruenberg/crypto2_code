from typing import List

class Table:
	def __init__(self, surroundingText: str, headerRow: List[str],\
				 columns: List[List[str]], file_name: str = "???"):
		"""
		Initalize a new Table that has already been parsed.

		If the `columns` haven't been parsed for a `headerRow` yet,
		set headerRow=[] and
		call the parse_header_row() method after construction!

		`headerRow` may be `[]` but never `None`!
		"""

		self.surroundingText = surroundingText  # (1) Using Textual Surroundings
		self.headerRow = headerRow  # (2) Using Attribute Names
		self.columns = columns  # (3) Using Attribute Extensions
		self.file_name = file_name

	def __eq__(self, other):
		if isinstance(other, Table):
			# Equality check should only matter when having parsed a file with
			#   existing annotations (--annotations-file parameter).
			# In that case, the tables should be exactly equal, so we can be
			#   this strict:
			return self.surroundingText == other.surroundingText\
				and self.headerRow == other.headerRow\
				and self.columns == other.columns
				#and self.file_name == other.file_name
				#(This is too strict when importing using a renamed corpus!)
		return False

	def width(self) -> int:
		"""
		Returns the width of this Table, i.e. the number of columns.
		"""
		return len(self.columns)  # width == # of columns

	def min_height(self, includingHeaderRow=True) -> int:
		"""
		Returns the height of this Table, i.e. the number of rows.
		Including the header row by default (if this Table has one, that is).
		Set includingHeaderRow=False to exclude a possible header row.

		The value returned is different to that of max_height() only if
		the columns don't all have the same height, which they should have.
		"""
		return min(len(col) for col in self.columns) +\
			(1 if includingHeaderRow and self.headerRow != [] else 0)

	def max_height(self, includingHeaderRow=True) -> int:
		"""
		Returns the height of this Table, i.e. the number of rows.
		Including the header row by default (if this Table has one, that is).
		Set includingHeaderRow=False to exclude a possible header row.

		The value returned is different to that of min_height() only if
		the columns don't all have the same height, which they should have.
		"""
		return max(len(col) for col in self.columns) +\
			(1 if includingHeaderRow and self.headerRow != [] else 0)

	def min_dimension(self, includingHeaderRow=True) -> int:
		"""
		Example: when this is a 4x10 table, returns 4.
		"""
		return min(self.width(),\
			self.min_height(includingHeaderRow=includingHeaderRow))

	def pretty_print(self, maxNumberOfTuples=6, maxColWidth=25,\
		maxTotalWidth=180) -> str:
		"""
		A pretty printable version of this Table, e.g.:

		Restaurant Name       | Rating | Price | Reviews
		------------------------------------------------
		Aquarius              |        | $$    | 0
		BIG & little's        |        | $     | 0
		Brown Bag Seafood Co. |        | $$    | 0
		...                   | ...    | ...   | ...

		(in this example, maxNumberOfTuples=3)
		"""

        # The width (number of characters) of each column, only regarding
        #   the first `maxNumberOfTuples` rows each:
		columnWidths: List[int] = list(map(\
			lambda column: max(map(\
				lambda cell: len(cell),\
				column[0:maxNumberOfTuples]\
			)),\
			self.columns\
			))
		# If a header name is longer than corresponding column width, it
		#   has to be increased further:
		if self.headerRow != []:
			columnWidths = list(\
				map(\
					lambda tuple: max(tuple[0], tuple[1]),\
					zip(columnWidths, map(lambda header: len(header),\
						self.headerRow))\
					)\
				)
		# Every column shall have a width of at least 3:
		columnWidths = [max(3, cw) for cw in columnWidths]
		# Every column shall have a width of at most `maxColWidth`:
		columnWidths = [min(maxColWidth, cw) for cw in columnWidths]

		def print_row(cells: List[str], widths: List[int]) -> str:
			res: str = ""
			for i in range(0, len(cells)):
				width = widths[i]
				res += cells[i][:width] + " " * (width-len(cells[i]))
				if i != len(cells)-1: res += " | "
			res += "\n"
			return res

		result: str = ""

		if self.headerRow != []:
			result += print_row(self.headerRow, columnWidths)
		else:  # no header row to print => print empty header row:
			result += print_row([""] * len(columnWidths), columnWidths)

		totalWidth = sum(columnWidths) + 3*(len(columnWidths)-1)
		result += "-" * totalWidth + "\n" # "-----------------------------"

		for y in range(0, min(maxNumberOfTuples, len(self.columns[0]))):
			result += print_row(\
				[self.columns[x][y] for x in range(0, len(self.columns))],\
				 columnWidths)

		if maxNumberOfTuples < len(self.columns[0]):  # print "... | ..." row:
			result += print_row(["..."] * len(columnWidths), columnWidths)

		if maxTotalWidth > 0:
			result = "\n".join(map(lambda line: line\
				if len(line) <= maxTotalWidth\
				else line[:maxTotalWidth-4] + " ...", result.splitlines()))

		# Replace Zero Width No-Break Spaces (\ufeff) with Spaces
		#   to avoid misalignment of columns:
		result = result.replace("\ufeff", " ")

		return result










"""
# Example:

load("/Users/kendrick/Documents/Github_k-gruenberg/crypto2_code/xgcd_for_polynomials.py")

S.<t> = PolynomialRing(GF(2),'t')
 
xgcd(t**2 + 1, t**8 + t**4 + t**3 + t + 1)
	Bézout coefficients: (t^6 + t^4 + t, 1)
	greatest common divisor: 1

# Check:
 
F256(t**2 + 1)**254
	tbar^6 + tbar^4 + tbar

# Another one:

xgcd(t**3 + t + 1, t**8 + t**4 + t**3 + t + 1)
	Bézout coefficients: (t^7 + t^6, t^2 + t + 1)
	greatest common divisor: 1

F256(t**3 + t + 1)**254
	tbar^7 + tbar^6

# But also simply:

xgcd(99, 78)
	Bézout coefficients: (-11, 14)
	greatest common divisor: 3
"""

"""
Can be used to invert an element of Rihndael's finite field.
When you specify said element as the first argument and the Rijndael polynomial
    t**8 + t**4 + t**3 + t + 1
as the second argument, the inverse of the first argument in Rihndael's finite field
will be the left Bézout coefficient.
"""
def xgcd(poly1, poly2):
	print("")

	# adapted pseudo-code from https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
	(old_r, r) = (poly1, poly2)
	(old_s, s) = (1, 0)
	(old_t, t) = (0, 1)

	prints = []
	while (r != 0):
		quotient = old_r // r
		prints.append([f"[{old_r}] = [{quotient}] * [{r}] + [{old_r - quotient * r}]", f"[{old_r - quotient * r}] = [{old_r}] - [{quotient}] * [{r}]", f"= [{old_s - quotient * s}] * [{poly1}] + [{old_t - quotient * t}] * [{poly2}]"])
		(old_r, r) = (r, old_r - quotient * r)
		(old_s, s) = (s, old_s - quotient * s)
		(old_t, t) = (t, old_t - quotient * t)
	print(Table("", [], [[prints[i][j] for i in range(len(prints))] for j in range(3)]).pretty_print(\
		maxNumberOfTuples=100000, maxColWidth=100000, maxTotalWidth=100000))

	print("")
	print(f"Bézout coefficients: {(old_s, old_t)}")
	print(f"greatest common divisor: {old_r}")
	print("")
