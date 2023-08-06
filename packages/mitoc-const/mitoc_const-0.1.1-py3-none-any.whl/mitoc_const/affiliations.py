"""
Affiliations are used across 4 different projects!
They're kept here as constants to ensure translation is properly done

Codes are used in:
- MITOC Trips (`ws_participant.affiliation`)
- MITOC Gear (`people_memberships.membership_type`)

String values are used in:
- MITOC Gear (`people.affiliation`)
- DocuSign (Affiliation radio buttions). Referenced in:
    - `mitoc-waiver`: JSON template
    - `mitoc-member`: Processing submitted forms
"""
from collections import namedtuple

__all__ = [
    'MIT_UNDERGRAD',
    'MIT_GRAD_STUDENT',
    'NON_MIT_UNDERGRAD',
    'NON_MIT_GRAD_STUDENT',
    'MIT_ALUM',
    'MIT_AFFILIATE',
    'NON_AFFILIATE',
    'DEPRECATED_STUDENT',
]

Affiliation = namedtuple('Affiliation', ['CODE', 'VALUE'])

MIT_UNDERGRAD = Affiliation('MU', 'MIT undergrad')
MIT_GRAD_STUDENT = Affiliation('MG', 'MIT grad student')
NON_MIT_UNDERGRAD = Affiliation('MU', 'Non-MIT undergrad')
NON_MIT_GRAD_STUDENT = Affiliation('MG', 'Non-MIT grad student')
MIT_ALUM = Affiliation('ML', 'MIT alum')
MIT_AFFILIATE = Affiliation('MA', 'MIT affiliate')
NON_AFFILIATE = Affiliation('NA', 'Non-affiliate')

# This status reflects a student where we don't know their affiliation!
DEPRECATED_STUDENT = Affiliation('S', 'Student')
