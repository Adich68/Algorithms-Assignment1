import sys

def read_input(file_path):
    try:
        with open(file_path, 'r') as f:
            input_text = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Input file '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)

    if not input_text:
        return 0, [], []

    data = input_text.split()
    iterator = iter(data)

    try:
        n = int(next(iterator))

        hospitals = []
        for _ in range(n):
            prefs = [int(next(iterator)) - 1 for _ in range(n)]
            hospitals.append(prefs)

        students = []
        for _ in range(n):
            prefs = [int(next(iterator)) - 1 for _ in range(n)]
            students.append(prefs)

        return n, hospitals, students
    except StopIteration:
        return 0, [], []


def read_matching(n):
    matching = {}
    matched_students = set()

    # Read lines from stdin (matcher.py)
    lines = sys.stdin.read().strip().split('\n')

    if not lines or (len(lines) == 1 and lines[0] == ''):
        if n == 0:
            return {}
        else:
            print("INVALID (Empty output from matcher)")
            sys.exit(0)

    for line in lines:
        try:
            parts = line.split()
            if len(parts) != 2:
                continue
            h, s = int(parts[0]) - 1, int(parts[1]) - 1

            if h in matching:
                print(f"INVALID (Hospital {h + 1} matched twice)")
                sys.exit(0)

            if s in matched_students:
                print(f"INVALID (Student {s + 1} matched twice)")
                sys.exit(0)

            matching[h] = s
            matched_students.add(s)

        except ValueError:
            continue

    return matching


def check_validity(n, matching):
    if len(matching) != n:
        print(f"INVALID (Size mismatch: expected {n} matches, got {len(matching)})")
        return False
    
    for h, s in matching.items():
        if not (0 <= h < n):
            print(f"INVALID (Hospital {h+1} out of range)")
            return False
        if not (0 <= s < n):
            print(f"INVALID (Student {s+1} out of range)")
            return False

    return True


def check_stability(n, hospitals, students, matching):
    student_match = {s: h for h, s in matching.items()}
    student_ranks = []
    for s_prefs in students:
        rank_map = {h: r for r, h in enumerate(s_prefs)}
        student_ranks.append(rank_map)

    for h in range(n):
        current_s = matching[h]
        h_prefs = hospitals[h]
        current_s_rank = h_prefs.index(current_s)

        for i in range(current_s_rank):
            better_s = h_prefs[i]
            h_prime = student_match[better_s]
            rank_h = student_ranks[better_s][h]
            rank_h_prime = student_ranks[better_s][h_prime]

            if rank_h < rank_h_prime:
                print(f"UNSTABLE (Blocking pair: Hospital {h + 1}, Student {better_s + 1})")
                return False

    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python verifier.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    n, hospitals, students = read_input(input_file)

    matching = read_matching(n)

    if not check_validity(n, matching):
        sys.exit(0)

    if check_stability(n, hospitals, students, matching):
        print("VALID STABLE")


if __name__ == "__main__":
    main()