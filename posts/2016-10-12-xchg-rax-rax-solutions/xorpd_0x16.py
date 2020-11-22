from __future__ import print_function
import itertools

# The function implemented by snippet 0x16
def fn_0x16(a, b, c, bits):
	mask = (1 << bits) - 1
	rhs = (a^b) + (c^b)
	if rhs > mask:
		rhs &= mask
		lhs = 0
	else:
		lhs = a^c
	return lhs == rhs

def get_bin(x, bits):
	return ('0' * bits + bin(x)[2:])[-bits:]

def popcount(x):
    n = 0
    while x:
        n += 1
        x &= (x - 1)	# Clear the bottom-most set bit - c.f. snippet 0x2f
    return n

def num_solutions(a, c, bits):
	mask = (1 << bits) - 1
	# There are 2^popcount(a ^ c) normal solutions
	solns = 1 << popcount(a ^ c)
	# bottom bits need to match, top bits need to differ, at least one bit needs to match
	x = -(a ^ c) & mask
	if x != 1 and (x & (x - 1)) == 0:
		solns += 1 << popcount(a ^ c)
	return solns

# Total solutions for n bits:
# No-Overflow solutions:
#  For each of $2^n$ choices of a there are $C(n, r)$ choices of c such that c differs in exactly r bits
#  and each such combination gives rise to $2^r$ values for b. Hence the total No-Overflow solutions are:
#  $$2^n \sum_{r=0}^n C(n, r) 2^r = 2^n (1 + 2)^n = 6^n$$
#  Using the binomial expansion theorem.
# Overflow solutions:
#  For each of $2^n$ choices of a there is exactly one choice of c that is different to a on all r top bits and
#  the same as a on the remaining bottom bits, however r has to be less than n as a and c need to match on at least
#  one bit. There are 2^r choices for b given this (a, c) pair. Hence we have:
#  $$2^n\sum_{r=0}^{n-1} 2^r = 2^n(2^n - 1) = 4^n - 2^n$$
# And the total is: $6^n + 4^n - 2^n$
def num_total_solutions(bits):
	return pow(6, bits) + pow(4, bits) - pow(2, bits)

def count_solutions(a, c, bits):
	n = 0
	for b in xrange(1 << bits):
		if fn_0x16(a, b, c, bits):
			n += 1
	return n

def brute_solutions(a, c, bits):
	for b in xrange(1 << bits):
		if fn_0x16(a, b, c, bits):
			yield b

# Generate all bit combinations for given mask
def generate_bits(mask, overlay = 0):
	# locate set bits
	bits = []
	for i in xrange(mask.bit_length()):
		if mask & (1 << i):
			bits.append(i)
	for m in xrange(1 << len(bits)):
		k = 0
		for i, s in enumerate(bits):
			k |= (m & (1 << i)) << s - i
		yield k | overlay

# Generate all combinations of bits selected from a and c
def generate_selected(a, c):
	for R in generate_bits(a ^ c):
		yield (a & R) | (c & ~R)

def generate_solutions(a, c, bits):
	mask = (1 << bits) - 1
	gb = lambda x: get_bin(x, bits)
	solns = generate_selected(a, c)
	# Check if overlow solutions are possible
	x = a ^ c
	z = -x & mask
	if z != 1 and (z & (z - 1)) == 0:
		bit_k = z >> 1
		# Handle the case where a == c
		if bit_k == 0:
			bit_k = 1 << (bits - 1)
		overlay = (c & (((z - 1) & mask) >> 1)) | (bit_k ^ (c & bit_k))
#		print(list(map(gb, [ a, c, overlay ])))
		solns = itertools.chain(solns, generate_bits(x, overlay))
	return solns

def check_solution_counts(bits):
	for a, c in itertools.product(range(1 << bits), repeat=2):
		ns = num_solutions(a, c, bits)
		cs = count_solutions(a, c, bits)
		# assert count_solutions(a, c, bits) == num_solutions(a, c, bits)
		if ns != cs:
			print('Miscounted for (%02x, %02x): %u was actually %u' % (a, c, ns, cs))

def verify_solutions(bits):
	gb = lambda x: get_bin(x, bits)
	total = 0
	for a, c in itertools.product(range(1 << bits), repeat=2):
		# problem is symmetric in a, c
		if a < c:
			continue
		sols = set(brute_solutions(a, c, bits))
		if sols != set(generate_solutions(a, c, bits)):
			print('Failed to generate correct solutions for (%02x, %02x)' % (a, c))
			print(list(map(gb, brute_solutions(a, c, bits))))
			print(list(map(gb, generate_solutions(a, c, bits))))
			break
		if a == c:
			total += len(sols)
		else:
			total += 2 * len(sols)
	assert total == num_total_solutions(bits)


def show_solutions(bits):
	mask = (1 << bits) - 1
	for a, c, b in itertools.product(xrange(1 << bits), repeat=3):
		if a > c:
			continue
		if not fn_0x16(a, b, c, bits):
			continue
#		if (a^b) + (b^c) > mask:
		print('  '.join(map(lambda x: get_bin(x, bits), [ a, c, b ])), (a^b) + (b^c) > mask)


if __name__ == '__main__':
	check_solution_counts(4)
	verify_solutions(4)
	bits = 3
	print('All solutions for word size of 3 bits (format is a, c, b, overflow)')
	show_solutions(bits)
	print('%d total solutions' % num_total_solutions(bits))

