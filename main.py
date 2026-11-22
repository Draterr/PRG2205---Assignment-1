"""Course Prerequisite and CGPA Planner.

Given a course catalogue and student records, reports each student's CGPA and
honours classification, which courses they are eligible to take, and whether a
chosen set of courses fits their credit limit.

Group members and contributions:
    Yusup  (ID)  CGPA calculation and target checking.
                 Mechanisms: 2 function in a variable, 8 reducing,
                 10 list comprehensions.
    Jordan (ID)  Course eligibility rules.
                 Mechanisms: 3 list of functions, 4 passing functions as
                 arguments, 5 returning functions.
    Ben    (ID)  Student record handling and grade classification.
                 Mechanisms: 1 separating functions and data, 6 mapping.
    Daniel (ID)  Prerequisite resolution, credit limits, student queries.
                 Mechanisms: 7 filtering, 9 lambda expressions, 11 recursion.

Run:  python main.py
Dependencies: none, standard library only.
"""

# AI USE DECLARATION
# AI use: TODO Yes / No
# Tool(s): TODO
# Purpose and affected code: TODO name the functions
# Justification: TODO
# Verification: TODO what was tested, checked or changed

from functools import reduce
from typing import NamedTuple


# =============================================================================
# DATA                                                          OWNER: Ben
# =============================================================================
# MECHANISM 1: SEPARATING FUNCTIONS AND DATA
# Catalogue and students hold no behaviour. Every function below takes this
# data as a parameter and returns a new value instead of mutating it.
# TODO Ben: explain why this matters here.
#
# SHAPE NOT FINALISED. Three decisions the group still needs to make:
#   (a) subjects_taken must carry grades, not just course codes, or
#       calculate_cgpa has nothing to work with. Dict {code: grade} is
#       simplest; a list of (code, grade) tuples also works.
#   (b) current_credit_hours is derivable from subjects_taken plus the
#       catalogue. Storing it as well means two sources of truth that can
#       disagree. Recommend deriving it and dropping the field.
#   (c) min_cgpa per course is needed for the GPA eligibility rule
#       (function 4), so the catalogue entry needs that field.


class Student(NamedTuple):
    """Immutable student record. No methods: behaviour lives in functions."""

    student_id: str
    name: str
    subjects_taken: dict      # {course_code: grade}


CATALOGUE = {
    "PRG1101": {"name": "Programming Fundamentals", "credits": 4,
                "prereqs": [], "min_cgpa": 0.00},
    "MTH1114": {"name": "Computer Mathematics", "credits": 4,
                "prereqs": [], "min_cgpa": 0.00},
    "PRG2205": {"name": "Programming Languages", "credits": 4,
                "prereqs": ["PRG1101"], "min_cgpa": 0.00},
    "CSC2103": {"name": "Data Structures", "credits": 4,
                "prereqs": ["PRG1101", "MTH1114"], "min_cgpa": 2.00},
    "CSC3209": {"name": "Operating Systems", "credits": 4,
                "prereqs": ["CSC2103", "PRG2205"], "min_cgpa": 2.50},
    "CSC3024": {"name": "Distributed Systems", "credits": 4,
                "prereqs": ["CSC3209"], "min_cgpa": 2.50},
}

GRADE_POINTS = {"A": 4.00, "A-": 3.67, "B+": 3.33, "B": 3.00, "B-": 2.67,
                "C+": 2.33, "C": 2.00, "D": 1.00, "F": 0.00}

PASS_POINT = 2.00
CREDIT_LIMIT = 20

HONOURS_BANDS = [(3.70, "First Class"),
                 (3.00, "Second Class Upper"),
                 (2.50, "Second Class Lower"),
                 (2.00, "Third Class"),
                 (0.00, "Fail")]

STUDENTS = [
    Student("0001", "Demo A", {"PRG1101": "A", "MTH1114": "B+"}),
    Student("0002", "Demo B", {"PRG1101": "C", "MTH1114": "F"}),
    Student("0003", "Demo C", {}),
]


# =============================================================================
# 1. TARGET CHECK                                            OWNER: Yusup
# =============================================================================

# MECHANISM 2: ASSIGNING A FUNCTION TO A VARIABLE
# .get is bound rather than called inline, so an unrecognised grade returns a
# default instead of raising, and the lookup can be swapped in one place.
# TODO Yusup: explain how and why.
grade_to_point = GRADE_POINTS.get


def meets_target(student, target_cgpa, target_subjects):
    """Return True if the student reaches target_cgpa and has passed every
    course in target_subjects.

    MECHANISM 10: LIST COMPREHENSIONS
    The subject check is one comprehension inside all(), stating the condition
    for the whole set rather than accumulating a flag in a loop.
    TODO Yusup: explain how and why.
    """
    raise NotImplementedError


# =============================================================================
# 2. CGPA                                                    OWNER: Yusup
# =============================================================================

def calculate_cgpa(student):
    """Return the credit weighted CGPA, or 0.0 if nothing has been attempted.

    MECHANISM 8: REDUCING
    Folds the taken courses into a running (total_points, total_credits) pair
    and divides once at the end. Two accumulators advance together, which
    sum() cannot do.
    TODO Yusup: explain how and why, and note the empty-record edge case.
    """
    # reduce(step, student.subjects_taken.items(), (0.0, 0))
    raise NotImplementedError


# =============================================================================
# 3. ELIGIBILITY                                             OWNER: Jordan
# =============================================================================

def eligibility_rules(student):
    """Build the list of predicates a course must satisfy for this student.

    MECHANISM 3: CREATING AND USING A LIST OF FUNCTIONS
    The enrolment policy becomes a value the program holds, so adding a
    condition means appending one factory rather than editing a chain of ifs.
    TODO Jordan: explain how and why.

    Returns a list of functions, each (course_code) -> bool.
    """
    raise NotImplementedError


def is_eligible(course_code, rules):
    """Return True if the course satisfies every rule.

    MECHANISM 4: PASSING FUNCTIONS AS ARGUMENTS
    Contains no policy of its own, only knows how to apply predicates, so the
    ruleset can change without touching this function.
    TODO Jordan: explain how and why. Mention all() short circuiting.
    """
    raise NotImplementedError


# =============================================================================
# 4. RULE FACTORIES                                          OWNER: Jordan
# =============================================================================

def make_min_cgpa_rule(student):
    """Return a predicate: True when the student's CGPA meets the course
    minimum.

    MECHANISM 5: RETURNING FUNCTIONS
    The student's CGPA is captured in the closure, so the returned predicate
    takes only a course code. That uniform shape is what lets all the rules
    sit in one list.
    TODO Jordan: explain how and why a closure beats passing the student into
    every rule at every call site.
    """
    raise NotImplementedError


def make_prereq_rule(student):
    """Return a predicate: True when the course has no unmet prerequisites.

    MECHANISM 5 (second use). Calls unmet_prereqs from section 6.
    """
    raise NotImplementedError


def make_not_passed_rule(student):
    """Return a predicate: True when the student has not already passed the
    course. A failed course passes this rule, since a retake is allowed.

    MECHANISM 5 (third use).
    """
    raise NotImplementedError


# =============================================================================
# 5. GRADE AND HONOURS CLASSIFICATION                        OWNER: Ben
# =============================================================================

def classify(cgpa_value):
    """Return the honours classification for a CGPA using HONOURS_BANDS."""
    raise NotImplementedError


def classify_all(students):
    """Return (name, classification) for every student.

    MECHANISM 6: MAPPING
    A one to one transformation: each student produces exactly one result, so
    map expresses it directly. Keeping classify() as a separate single-student
    function means it is reusable anywhere one student needs classifying.
    TODO Ben: explain how and why, and contrast with filtering in section 10.
    """
    raise NotImplementedError


# =============================================================================
# 6. AVAILABLE COURSES                                       OWNER: Daniel
# =============================================================================

def unmet_prereqs(course_code, subjects_taken, seen=None):
    """Return every prerequisite not yet passed, direct and indirect.

    MECHANISM 11: RECURSION
    A course is blocked by its own missing prerequisites plus whatever blocks
    those. The definition is recursive and the chain has no fixed depth, so
    the function mirrors the rule directly instead of managing a stack by hand.
    TODO Daniel: explain how and why. Justify it as matching the shape of the
    data, not as being shorter.

    `seen` guards two real cases: a prerequisite reachable by more than one
    path, and a circular chain in the catalogue that would otherwise raise
    RecursionError. Start with `if seen is None: seen = set()` so the default
    is not a shared mutable.
    """
    raise NotImplementedError


def available_courses(student):
    """Return the courses the student can take now, closest to unlocked first.

    MECHANISM 9: LAMBDA EXPRESSIONS
    The sort key is inline because it is used once here and naming it would
    add an indirection for no gain.
    TODO Daniel: explain how and why.
    """
    # key=lambda c: (len(unmet_prereqs(c, student.subjects_taken)), c)
    raise NotImplementedError


# =============================================================================
# 7. STUDENT COURSE HANDLING                                 OWNER: Ben
# =============================================================================

def add_course(student, course_code, grade):
    """Return a NEW Student with the course recorded. The original is
    unchanged, which is what keeps the data passive (mechanism 1).

    TODO Ben: one line on why returning a copy beats mutating in place.
    """
    raise NotImplementedError


def credits_taken(student):
    """Return total credits for all attempted courses."""
    raise NotImplementedError


def credits_earned(student):
    """Return total credits for passed courses only."""
    raise NotImplementedError


# =============================================================================
# 8. OUTPUT                                                  OWNER: see note
# =============================================================================
# The group marked this as AI generated. Two consequences:
#   - it must be named in the AI declaration at the top, with what was
#     checked or changed;
#   - no assessed mechanism is placed here on purpose. These functions only
#     format strings that other sections produce, so nobody loses marks for a
#     mechanism they did not write.


def print_student_report(student):
    """Print CGPA, classification, credits and available courses."""
    raise NotImplementedError


def print_cohort_report(students):
    """Print the classification of every student."""
    raise NotImplementedError


# =============================================================================
# 9. CREDIT LIMIT                                            OWNER: Daniel
# =============================================================================

def within_credit_limit(student, chosen_courses):
    """Return True if the chosen courses fit under CREDIT_LIMIT."""
    raise NotImplementedError


def courses_within_limit(student, course_codes):
    """Return the courses that still fit under the remaining credit budget.

    MECHANISM 7: FILTERING
    A selection over existing records with no transformation, which is what
    filter expresses.
    TODO Daniel: explain how and why.
    """
    raise NotImplementedError


# =============================================================================
# 10. STUDENTS BY CLASSIFICATION                             OWNER: Daniel
# =============================================================================

def students_with_classification(students, classification):
    """Return the students in a given honours band.

    MECHANISM 7 (second use). Uses classify() from section 5, so the band
    boundaries stay defined in one place.
    """
    raise NotImplementedError


# =============================================================================
# 11. UPDATE STUDENT INFO                                    OWNER: Ben
# =============================================================================

def update_student(student, **changes):
    """Return a NEW Student with the given fields replaced.

    NamedTuple._replace does this without mutation, so no caller can be
    surprised by a record changing underneath it.
    """
    raise NotImplementedError


# =============================================================================

def main():
    """Demonstrate the program against the data at the top of this file."""
    # TODO group: per-student report, then the cohort report, then one
    # credit-limit example.
    raise NotImplementedError


if __name__ == "__main__":
    main()
