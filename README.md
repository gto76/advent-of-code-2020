# Advent of Code 2020

<p class="banner"><sup><a href="https://adventofcode.com/2020">Go to the site</a>, <a href="https://raw.githubusercontent.com/gto76/advent-of-code-2020/master/advent_2020.py">Download Python script</a> or <a href="https://github.com/gto76/advent-of-code-2020">Fork me on GitHub</a>.</sup></p>

<p class="banner"><img src="web/image_888.png" alt="Advent of Code"></p>

## Day 1: Entries

```text
1721
979
366
299
675
1456
```

### Find the two entries that sum to 2020; what do you get if you multiply them together?

```python
def problem_1_a(lines):
    '''514579'''
    import itertools
    numbers = [int(line) for line in lines]
    for l, r in itertools.combinations(numbers, 2):
        if l + r == 2020:
            return l * r
```

### In your expense report, what is the product of the three entries that sum to 2020?

```python
def problem_1_b(lines):
    '''241861950'''
    import itertools
    numbers = [int(line) for line in lines]
    for a, b, c in itertools.combinations(numbers, 3):
        if a + b + c == 2020:
            return a * b * c
```

## Day 2: Passwords

```text
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
```

### How many passwords are valid according to their policies?

```python
def problem_2_a(lines):
    '''2'''
    import re
    def is_valid(line):
        min_, max_, letter, password = re.match('^(\d+)-(\d+) (\w): (\w+)$', line).groups()
        return int(min_) <= password.count(letter) <= int(max_)
    return sum(is_valid(line) for line in lines)
```

### How many passwords are valid according to the new interpretation of the policies?

```python
def problem_2_b(lines):
    '''1'''
    import re
    def is_valid(line):
        i_1, i_2, letter, password = re.match('^(\d+)-(\d+) (\w): (\w+)$', line).groups()
        return (password[int(i_1)-1] == letter) + (password[int(i_2)-1] == letter) == 1
    return sum(is_valid(line) for line in lines)
```

## Day 3: Trees

```text
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
```

### Starting at the top-left corner of your map and following a slope of right 3 and down 1, how many trees would you encounter?

```python
def problem_3_a(lines):
    '''7'''
    import collections
    P = collections.namedtuple('P', 'x y')
    positions = (P(x=y*3, y=y) for y in range(len(lines)))
    is_tree = lambda p: lines[p.y][p.x % len(lines[0])] == '#'
    return sum(is_tree(p) for p in positions)
```

### What do you get if you multiply together the number of trees encountered on each of the listed slopes?

```python
def problem_3_b(lines):
    '''336'''
    import collections, functools, itertools, operator
    P = collections.namedtuple('P', 'x y')
    def get_positions(slope):
        x_generator = itertools.count(start=0, step=slope.x)
        return (P(next(x_generator), y) for y in range(0, len(lines), slope.y))
    is_tree = lambda p: lines[p.y][p.x % len(lines[0])] == '#'
    count_trees = lambda slope: sum(is_tree(p) for p in get_positions(slope))
    slopes = [P(x=1, y=1), P(x=3, y=1), P(x=5, y=1), P(x=7, y=1), P(x=1, y=2)]
    return functools.reduce(operator.mul, (count_trees(slope) for slope in slopes))
```

## Day 4: Passports

```text
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
```

### In your batch file, how many passports are valid?

```python
def problem_4_a(lines):
    '''2'''
    passports = ' '.join(lines).split('  ')
    get_keys = lambda passport: {item.split(':')[0] for item in passport.split()}
    is_valid = lambda passport: len(get_keys(passport) - {'cid'}) == 7
    return sum(is_valid(p) for p in passports)
```

### In your batch file, how many passports are valid?

```python
def problem_4_b(lines):
    '''2'''
    import re
    RULES = dict(
        byr=lambda v: 1920 <= int(v) <= 2002,
        iyr=lambda v: 2010 <= int(v) <=  2020,
        eyr=lambda v: 2020 <= int(v) <=  2030,
        hgt=lambda v: 150 <= int(v[:-2]) <= 193 if 'cm' in v else 59 <= int(v[:-2]) <= 76,
        hcl=lambda v: re.match('#[0-9a-f]{6}$', v) != None,
        ecl=lambda v: v in 'amb blu brn gry grn hzl oth'.split(),
        pid=lambda v: re.match('\d{9}$', v) != None
    )
    def is_field_valid(key, value):
        try:
            return RULES[key](value)
        except Exception:
            return False
    def is_passport_valid(passport):
        return sum(is_field_valid(*item.split(':')) for item in passport.split()) == 7
    passports = ' '.join(lines).split('  ')
    return sum(is_passport_valid(p) for p in passports)
```

## Day 5: Seat IDs

```text
BBFFBBFLLR
BBFFBBFLRL
BBFFBBFRLL
```

### What is the highest seat ID on a boarding pass?

```python
def problem_5_a(lines):
    '''820'''
    get_bin = lambda code: ''.join('0' if ch in 'FL' else '1' for ch in code)
    get_id  = lambda code: int(get_bin(code), 2)
    return max(get_id(code) for code in lines)
```

### What is the ID of your seat?

```python
def problem_5_b(lines):
    '''819'''
    get_bin   = lambda code: ''.join('0' if ch in 'FL' else '1' for ch in code)
    get_id    = lambda code: int(get_bin(code), 2)
    taken_ids = {get_id(code) for code in lines}
    all_ids   = range(min(taken_ids), max(taken_ids)+1)
    return (set(all_ids) - taken_ids).pop()
```

## Day 6: Answers

```text
abc

a
b
c

ab
ac

a
a
a
a

b
```

### For each group, count the number of questions to which anyone answered "yes". What is the sum of those counts?

```python
def problem_6_a(lines):
    '''11'''
    groups = (set(group) - {' '} for group in ' '.join(lines).split('  '))
    return sum(len(group) for group in groups)
```

### For each group, count the number of questions to which everyone answered "yes". What is the sum of those counts?

```python
def problem_6_b(lines):
    '''6'''
    import functools, operator
    groups             = ' '.join(lines).split('  ')
    split_group        = lambda group: (set(a) for a in group.split(' '))
    get_common_answers = lambda group: functools.reduce(operator.and_, split_group(group))
    return sum(len(get_common_answers(group)) for group in groups)
```

## Day 7: Bags

```text
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
```

### How many bag colors can eventually contain at least one shiny gold bag?

```python
def problem_7_a(lines):
    '''4'''
    import re
    def parse_line(line):
        container, contents = line.split(' bags contain ')
        if contents == 'no other bags.':
            return container, set()
        get_color = lambda token: re.search('\d+ (.*) .*$', token).group(1) 
        return container, {get_color(a) for a in contents.split(',')}
    bags = dict(parse_line(line) for line in lines)
    out = {k for k, v in bags.items() if 'shiny gold' in v}
    while True:
        new_colors = {k for k, v in bags.items() if out & v}
        if new_colors <= out:
            return len(out)
        out |= new_colors
```

### How many individual bags are required inside your single shiny gold bag?

```python
def problem_7_b(lines):
    '''32'''
    import re
    def parse_line(line):
        container, contents = line.split(' bags contain ')
        if contents == 'no other bags.':
            return container, set()
        get_number_and_color = lambda token: re.search('(\d+) (.*) .*$', token).groups()
        return container, {get_number_and_color(a) for a in contents.split(',')}
    def get_n_bags(color):
        contents = bags[color]
        if not contents:
            return 1
        return 1 + sum(int(n) * get_n_bags(color) for n, color in contents)
    bags = dict(parse_line(line) for line in lines)
    return get_n_bags('shiny gold') - 1
```

## Day 8: Program

```text
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
```

### Run your copy of the boot code. Immediately before any instruction is executed a second time, what value is in the accumulator?

```python
def problem_8_a(lines):
    '''5'''
    OPERATIONS = dict(
        acc=lambda pc, accumulator, argument: (pc+1, accumulator+int(argument)),
        jmp=lambda pc, accumulator, argument: (pc+int(argument), accumulator),
        nop=lambda pc, accumulator, argument: (pc+1, accumulator)
    )
    pc = 0
    accumulator = 0
    executed = set()
    while pc not in executed:
        executed.add(pc)
        operation, argument = lines[pc].split()
        pc, accumulator = OPERATIONS[operation](pc, accumulator, argument)
    return accumulator
```

### Fix the program so that it terminates normally by changing exactly one jmp (to nop) or nop (to jmp). What is the value of the accumulator after the program terminates?

```python
def problem_8_b(lines):
    '''8'''
    def main():
        for program in program_generator():
            result = run(program)
            if result is not None:
                return result

    def program_generator():
        for i, line in enumerate(lines):
            if line.startswith('acc'):
                continue
            line = line.replace('jmp', 'nop') if 'jmp' in line else line.replace('nop', 'jmp')
            yield lines[:i] + [line] + lines[i+1:]

    def run(program):
        OPERATIONS = dict(
            acc=lambda pc, accumulator, argument: (pc+1, accumulator+int(argument)),
            jmp=lambda pc, accumulator, argument: (pc+int(argument), accumulator),
            nop=lambda pc, accumulator, argument: (pc+1, accumulator)
        )
        pc = 0
        accumulator = 0
        executed = set()
        while pc not in executed:
            executed.add(pc)
            operation, argument = program[pc].split()
            pc, accumulator = OPERATIONS[operation](pc, accumulator, argument)
            if pc == len(program):
                return accumulator
        return None

    return main()
```

## Day 9: Encryption

```text
20
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
21
22
23
24
25
45
65
```

### The first step of attacking the weakness in the XMAS data is to find the first number in the list (after the preamble) which is not the sum of two of the 25 numbers before it. What is the first number that does not have this property?

```python
def problem_9_a(lines):
    '''65'''
    import itertools
    def is_sum(candidate, numbers):
        for pair in itertools.combinations(numbers, 2):
            if sum(pair) == candidate:
                return True
    numbers = [int(line) for line in lines]
    for i in range(25, len(numbers)):
        if not is_sum(numbers[i], numbers[i-25:i]):
            return numbers[i]
```

### What is the encryption weakness in your XMAS-encrypted list of numbers?

```python
def problem_9_b(lines):
    '''21'''
    invalid_number = problem_9_a(lines)
    numbers = [int(line) for line in lines]
    for i in range(len(numbers)):
        for j in range(i+2, len(numbers)):
            sum_ = sum(numbers[i:j])
            if sum_ == invalid_number:
                return min(numbers[i:j]) + max(numbers[i:j])
            elif sum_ > invalid_number:
                break
```

## Day 10: Adapters

```text
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
```

### What is the number of 1-jolt differences multiplied by the number of 3-jolt differences?

```python
def problem_10_a(lines):
    '''220'''
    numbers = [0] + sorted(int(a) for a in lines)
    deltas = [b-a for a, b in zip(numbers, numbers[1:])]
    return deltas.count(1) * (deltas.count(3)+1)
```

### What is the total number of distinct ways you can arrange the adapters to connect the charging outlet to your device?

```python
def problem_10_b(lines):
    '''19208'''
    import functools, operator as op
    numbers = sorted(int(a) for a in lines)
    numbers = [0] + numbers + [numbers[-1]+3]
    deltas = [b-a for a, b in zip(numbers, numbers[1:])]
    d = ''.join(str(a) for a in deltas)
    dd = [[1, 2, 4, 7, 13, 23][len(a)-1] for a in d.split('3') if a]
    return functools.reduce(op.mul, dd)
```

## Day 11: Seats

```text
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
```

### Simulate your seating area by applying the seating rules repeatedly until no seats change state. How many seats end up occupied?

```python
def problem_11_a(lines):
    '''37'''
    import collections
    P = collections.namedtuple('P', 'x y')

    def main():
        layout = {P(x, y): ch for y, line in enumerate(lines) for x, ch in enumerate(line)}
        while True:
            new_layout = step(layout)
            if new_layout == layout:
                return list(layout.values()).count('#')
            layout = new_layout

    def step(layout):
        out = dict(layout)
        for p, ch in layout.items():
            adjecent_chars = [layout.get(a) for a in get_adjecent_positions(p)]
            if ch == 'L' and '#' not in adjecent_chars:
                out[p] = '#'
            elif ch == '#' and adjecent_chars.count('#') >= 4:
                out[p] = 'L'
        return out

    def get_adjecent_positions(p):
        deltas = [P(-1, -1), P(0, -1), P(1, -1), P(-1, 0), P(1, 0), P(-1, 1), P(0, 1), P(1, 1)]
        return (P(p.x + delta.x, p.y + delta.y) for delta in deltas)

    return main()
```

### Given the new visibility method and the rule change for occupied seats becoming empty, once equilibrium is reached, how many seats end up occupied?

```python
def problem_11_b(lines):
    '''26'''
    import collections
    P = collections.namedtuple('P', 'x y')

    layout = {P(x, y): ch for y, line in enumerate(lines) for x, ch in enumerate(line)}

    def main():
        nonlocal layout
        while True:
            new_layout = {p: get_new_ch(p, ch) for p, ch in layout.items()}
            if new_layout == layout:
                return list(layout.values()).count('#')
            layout = new_layout

    def get_new_ch(p, ch):
        directions = [P(-1, -1), P(0, -1), P(1, -1), P(-1, 0), P(1, 0), P(-1, 1), P(0, 1), 
                      P(1, 1)]
        visible_chairs = [get_visible_chair(p, direction) for direction in directions]
        if ch == 'L' and '#' not in visible_chairs:
            return '#'
        elif ch == '#' and visible_chairs.count('#') >= 5:
            return 'L'
        return ch

    def get_visible_chair(p, direction):
        while p in layout:
            p = P(p.x + direction.x, p.y + direction.y)
            if p in layout and layout[p] in 'L#':
                return layout[p]

    return main()
```

## Day 12: Navigation

```text
F10
N3
F7
R90
F11
```

### Figure out where the navigation instructions lead. What is the Manhattan distance between that location and the ship's starting position?

```python
def problem_12_a(lines):
    '''25'''
    import collections, enum

    P = collections.namedtuple('P', 'x y')
    D = enum.Enum('D', 'n e s w')

    def main():
        p, d = P(0, 0), D.e
        for line in lines:
            p, d = step(p, d, line)
        return abs(p.x) + abs(p.y)

    def step(p, d, line):
        DELTAS = {D.n: P(0, 1), D.e: P(1, 0), D.s: P(0, -1), D.w: P(-1, 0)}
        ACTIONS = dict(
            N=lambda p, d, arg: (P(p.x, p.y+arg), d),
            S=lambda p, d, arg: (P(p.x, p.y-arg), d),
            E=lambda p, d, arg: (P(p.x+arg, p.y), d),
            W=lambda p, d, arg: (P(p.x-arg, p.y), d),
            L=lambda p, d, arg: (p, turn(d, -arg)),
            R=lambda p, d, arg: (p, turn(d, arg)),
            F=lambda p, d, arg: (P(p.x + DELTAS[d].x*arg, p.y + DELTAS[d].y*arg), d)
        )
        action_id, arg = line[0], int(line[1:])
        return ACTIONS[action_id](p, d, arg)

    def turn(d, degrees):
        directions = list(D)
        index = (directions.index(d) + degrees//90) % len(directions)
        return directions[index]

    return main()
```

### Figure out where the navigation instructions actually lead. What is the Manhattan distance between that location and the ship's starting position?

```python
def problem_12_b(lines):
    '''286'''
    import collections
    P = collections.namedtuple('P', 'x y')

    def main():
        p, waypoint = P(0, 0), P(10, 1)
        for line in lines:
            p, waypoint = step(p, waypoint, line)
        return abs(p.x) + abs(p.y)

    def step(p, waypoint, line):
        ACTIONS = dict(
            N=lambda p, waypoint, arg: (p, P(waypoint.x, waypoint.y+arg)),
            S=lambda p, waypoint, arg: (p, P(waypoint.x, waypoint.y-arg)),
            E=lambda p, waypoint, arg: (p, P(waypoint.x+arg, waypoint.y)),
            W=lambda p, waypoint, arg: (p, P(waypoint.x-arg, waypoint.y)),
            L=lambda p, waypoint, arg: (p, turn(waypoint, -arg)),
            R=lambda p, waypoint, arg: (p, turn(waypoint, arg)),
            F=lambda p, waypoint, arg: (P(p.x + waypoint.x*arg, p.y + waypoint.y*arg), 
                                        waypoint)
        )
        action_id, arg = line[0], int(line[1:])
        return ACTIONS[action_id](p, waypoint, arg)

    def turn(waypoint, degrees):
        degrees += 360 if degrees < 0 else 0
        TURN = {90:  P(x=waypoint.y,  y=-waypoint.x),
                180: P(x=-waypoint.x, y=-waypoint.y), 
                270: P(x=-waypoint.y, y=waypoint.x)}
        return TURN[degrees]

    return main()
```

## Day 13: Buses

```text
939
7,13,x,x,59,x,31,19
```

### What is the ID of the earliest bus you can take to the airport multiplied by the number of minutes you'll need to wait for that bus?

```python
def problem_13_a(lines):
    '''295'''
    import itertools
    stamp = int(lines[0])
    ids = [int(a) for a in lines[1].split(',') if a != 'x']
    get_departures = lambda stamp, id_: range(0, stamp+id_, id_)
    timetable = [get_departures(stamp, id_) for id_ in ids]
    departure = min(a for a in itertools.chain.from_iterable(timetable) if a >= stamp)
    id_ = [a for a in ids if departure % a == 0][0]
    return id_ * (departure - stamp)
```

### What is the earliest timestamp such that all of the listed bus IDs depart at offsets matching their positions in the list?

```python
def problem_13_b(lines):
    '''1068781'''
    buses = [(offset, int(id_)) for offset, id_ in enumerate(lines[1].split(','))
                if id_ != 'x']
    timestamp = 0
    least_common_multiple = 1
    for offset, id_ in buses:
        while (timestamp + offset) % id_ != 0:
            timestamp += least_common_multiple
        least_common_multiple *= id_
    return timestamp
```

## Day 14: Bitmasks

```text
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
```

### Execute the initialization program. What is the sum of all values left in memory after it completes?

```python
def problem_14_a(lines):
    '''51'''
    import re
    def get_word(val, mask):
        bin_val = bin(int(val))[2:]
        bin_val_padded = '0' * (len(mask)-len(bin_val)) + bin_val
        return ''.join(a if m == 'X' else m for a, m in zip(bin_val_padded, mask))
    mem = {}
    for line in lines:
        if line.startswith('mask'):
            _, mask = line.split(' = ')
            continue
        addr, val = re.search('\[(\d+)\] = (\d+)', line).groups()
        mem[addr] = get_word(val, mask)
    return sum(int(a, 2) for a in mem.values())
```

### Execute the initialization program using an emulator for a version 2 decoder chip. What is the sum of all values left in memory after it completes?

```python
def problem_14_b(lines):
    '''208'''
    import itertools, re
    def get_addresses(addr, mask):
        bin_addr = bin(int(addr))[2:]
        bin_addr_padded = '0' * (len(mask)-len(bin_addr)) + bin_addr
        addr_template = ''.join(a if m == '0' else m for a, m in zip(bin_addr_padded, mask))
        out = []
        for floating_bits in itertools.product('01', repeat=addr_template.count('X')):
            floating_bits = iter(floating_bits)
            out.append(''.join(a if a != 'X' else next(floating_bits) for a in addr_template))
        return out
    mem = {}
    for line in lines:
        if line.startswith('mask'):
            _, mask = line.split(' = ')
            continue
        addr, val = re.search('\[(\d+)\] = (\d+)', line).groups()
        for address in get_addresses(addr, mask):
            mem[address] = val
    return sum(int(a) for a in mem.values())
```