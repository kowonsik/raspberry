
def secret(plug_id):
	plug_secret = (plug_id * 2654435761) % 8192
	return plug_secret


print map(secret, [100101, 100103, 100104])
print map(secret, [100201, 100203, 100204])
print map(secret, [100301, 100303, 100304])
print map(secret, [100401, 100403, 100404])
print map(secret, [100501, 100503, 100504])

print map(secret, [100601, 100603, 100604])
print map(secret, [100701, 100703, 100704])
print map(secret, [100801, 100803, 100804])
print map(secret, [100901, 100903, 100904])
print map(secret, [101001, 101003, 101004])


