# This program implements the hospital-proposing Gale–Shapley algorithm
# for the one-to-one stable matching problem.
import sys

def read_input(): 
    """
    Reads input from standard input.

    Expected format:
    n
    n lines of hospital preference lists
    n lines of student preference lists

    Returns:
        n (int): number of hospitals/students
        hospitals (list of lists): hospital preferences (0-indexed)
        students (list of lists): student preferences (0-indexed)
    """
    # Read all input tokens
    input_text = sys.stdin.read().strip()
    if not input_text:
        # Empty input file
        return 0, [], []

    # Split into list of strings
    data = input_text.split()
    
    index = 0
    n = int(data[index])
    index += 1

    hospitals = []
    for _ in range(n):
        # Take next n tokens, convert to integers, convert to 0-indexed
        prefs = []
        for j in range(n):
            prefs.append(int(data[index]) - 1)
            index += 1
        hospitals.append(prefs)

    students = []
    for _ in range(n):
        prefs = []
        for j in range(n):
            prefs.append(int(data[index]) - 1)
            index += 1
        students.append(prefs)   
    return n, hospitals, students

def validate_input(n, hospital_prefs, student_prefs):
    """
    Validates the input to ensure: 
    - correct number of prefernce lists
    - Each preference list is a permutation of 0..n-1
    """

    if len(hospital_prefs) != n or len(student_prefs) != n: 
        return False
    
    valid_set = set(range(n))

    # Check each hospital preference list
    for prefs in hospital_prefs:
        if set(prefs) != valid_set:
            return False
        
    # Check each student preference list
    for prefs in student_prefs:
        if set(prefs) != valid_set:
            return False
        
    return True

def gale_shapley(n, hospital_prefs, student_prefs):
    """
    Implements the hospital-proposing Gale–Shapley algorithm.

    Returns: 
        hospital_match (list): hospital_match[h] = student matched to hospital h
        proposals (int): number of proposals made (optional statistic)
    """

    if n == 0: 
        return [], 0
    
    # Precompute student rankings (list of dicts)
    student_rank = []
    for s in range(n):
        ranks = {}
        for rank_index in range(n):
            h = student_prefs[s][rank_index]
            ranks[h] = rank_index
        student_rank.append(ranks)
    
    # Initialize all hospitals and students as unmatched
    hospital_match = [-1] * n
    student_match =  [-1] * n

    # Tracks the next student each hospital will propose to
    next_proposal = [0] * n

    # List of currently free hospitals
    free_hospitals = []
    for h in range(n):
        free_hospitals.append(h)

    proposals = 0

    # If there is a free hospital then continue

    while len(free_hospitals) > 0:
        h = free_hospitals.pop(0) 

        # Skip if hospital already proposed to all students
        if next_proposal[h] >= n:
            continue
    
        # Hospital proposes to the next student on its list
        s = hospital_prefs[h][next_proposal[h]]
        next_proposal[h] += 1
        proposals += 1

        # if student is free, accept the proposal
        if student_match[s] == -1:
            student_match[s] = h
            hospital_match[h] = s
        else:
            # Student compares current match with new proposal
            current = student_match[s]

            if student_rank[s][h] < student_rank[s][current]:
                # Student prefers new hospital
                student_match[s] = h
                hospital_match[h] = s
                hospital_match[current] = -1
                free_hospitals.append(current)
            else:
                # Student rejects the proposal
                free_hospitals.append(h)

    return hospital_match, proposals

def main():
    """
    Main driver function:
    - Reads input
    - Validates input
    - Runs Gale–Shapley
    - Prints the final matching
    """

    n, hospital_prefs, student_prefs = read_input()

    if not validate_input(n, hospital_prefs, student_prefs):
        print("INVALID INPUT", file=sys.stderr)
        sys.exit(1)

    matching, _ = gale_shapley(n, hospital_prefs, student_prefs)

    for h in range(n):
        print(str(h + 1) + " " + str(matching[h] + 1))



if __name__ == "__main__":
    main()
    