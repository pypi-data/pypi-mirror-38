
'''Okay, so this is the help docuement for this module
blah blah blah
etc etc etc'''


def calculate_at(dna):
    length = len(dna)
    a_count = dna.count('A')
    t_count = dna.count('T')
    at_content = (a_count + t_count) / length
    return at_content
