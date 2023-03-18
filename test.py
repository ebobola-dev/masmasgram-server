import re

test_usernames = (
	'a',
	'_',
	'5',
	'5a',
	'a5',
	'_5a',
	'_a',
	'a5_',
    'aboba',
    '_aboba',
    'aboba54',
    'a_bob_a54_',
    '',
    ' ',
    ' aboba54',
    '_aboba54',
    '5abo ba54',
    '5aboba54_',
    '5aboba54_ ',
    '5ab:oba54_',
    '5a&b:oba54_',
    '5 a&b:oba54_',
    ' 5a&b:oba54_',
    '   5a&b:oba54_',
)

success = tuple(i for i in test_usernames if re.match(r'^\S+.+', i) is not None)
failed = tuple(i for i in test_usernames if re.match(r'^\S*.+', i) is None)
print(f"success: {success}")
print(f"failed: {failed}")
