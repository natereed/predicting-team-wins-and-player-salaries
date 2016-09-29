import re

# Tests
# Kevin J. Brown
# Ken Griffey Jr.
# Chien-Ming Wang
# Fautino De Los Santos

def normalize_first_and_last(name):
    name = name.strip()
    name_and_suffix_pat = r'(.*),*\s+([J|S]r\.)$'
    m = re.search(name_and_suffix_pat, name)

    if m:
        name = m.group(1).strip()

    last = name.split()[-1]
    first = name.split()[0]
    return normalized_name(first, last)

def normalize_last_and_first_initial(name):
    m = re.search(r'([\w\s]+),\s+([\w\s]{1})', name)
    last = m.group(1)
    first = m.group(2)
    return normalized_name(first, last)

def normalized_name(first, last):
    norm_name = first[0].lower() + last.lower()
    norm_name = norm_name.replace(' ', '')
    return norm_name

name = 'Kevin J. Brown'
norm_name = normalize_first_and_last(name)
print("Normalized: " + norm_name)
assert(norm_name == 'kbrown')

norm_name = normalize_first_and_last('Ken Griffey Jr.')
print("Normalized: " + norm_name)
assert(norm_name == 'kgriffey')

norm_name = normalize_first_and_last('Chien-Ming Wang')
print("Normalized: " + norm_name)
assert(norm_name == 'cwang')

norm_name = normalize_first_and_last('Fautino De Los Santos')
print("Normalized: " + norm_name)
assert(norm_name == 'fsantos')

# Test the last name, first initial names
name = 'Whitaker, L'
norm_name = normalize_last_and_first_initial(name)
print("Normalized: " + norm_name)
assert(norm_name == 'lwhitaker')

