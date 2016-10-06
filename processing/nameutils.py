import re

# Tests
# Kevin J. Brown
# Ken Griffey Jr.
# Chien-Ming Wang
# Fautino De Los Santos

def normalize_first_and_last(name):
    name = name.strip()
    suffix = None
    suffix_pat = r'([J|S]r\.{0,1})$'
    m = re.search(suffix_pat, name)
    if m:
        suffix = m.group(1)
        # Remove suffix
        name = re.sub(suffix_pat, '', name)
        name = name.strip()

    #name_and_suffix_pat = r'^([\w\s\.]+)(,{0,1}\s*[J|S]r\.{0,1})*$'
    #m = re.search(name_and_suffix_pat, name)

    #if m:
    #    name = m.group(1).strip()
    #    suffix = m.group(2)
    #    if suffix:
    #        suffix = suffix.strip()

    last = name.split()[-1]
    first = name.split()[0]
    return normalized_name(first, last, suffix)

def normalize_last_and_first_initial(name):
    m = re.search(r'([\w\s]+)([J|S]r\.)*,\s+([\w\s]{1})', name)
    last = m.group(1)
    suffix = m.group(2)
    first = m.group(3)
    return normalized_name(first, last, suffix)

def normalized_name(first, last, suffix=None):
    norm_name = first[0].lower() + last.lower()
    if (suffix):
        norm_name = norm_name + suffix.lower()
    norm_name = norm_name.replace(' ', '')
    norm_name = norm_name.replace('.', '')
    return norm_name

name = 'Kevin J. Brown'
print(name)
norm_name = normalize_first_and_last(name)
print("Normalized: " + norm_name)
assert(norm_name == 'kbrown')

norm_name = normalize_first_and_last('Ken Griffey Jr.')
print("Normalized: " + norm_name)
assert(norm_name == 'kgriffeyjr')

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

name = "Young Jr., E"
norm_name = normalize_last_and_first_initial(name)
print("Normalized: " + norm_name)
assert(norm_name == 'eyoungjr')
