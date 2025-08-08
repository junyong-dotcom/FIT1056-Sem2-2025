
https://github.com/junno-dotcom/FIT1056-Sem2-2025

 8ccb219 (Update README.md)
PST 1
Line 42: I added 'if' conditional statement which is similar to the 'list_students' above. This can ensure that when users input 
non-existence name, the program will returns a sentence to the user.

Line 51 & 68: I added 'results' which is a variable . [] is an empty list that will store all the data of all the students and 
teachers that match the search.

Line 52 & 69: I added 'term_lower = term.lower()'. 'term_lower' is a variable. 'term.lower()' is a function that will converts a 
string to lowercase, this can ensure user input to search for students or teacher is case-insensitive

Line 53 & 70: I added 'for student in student_db' and 'for teacher in teacher_db". These are for loops that will repeats code 
for each student or teacher which is being stored in student_db and teacher_db respectively.

Line 54: I added 'if (term_lower in student.name.lower())' which is an if conditional statement. The code 'in' is used to check
if one string is part of the student list. .lower() makes the student's name lowercase to ensure the search is case-insensitive.

Line 55 & 72: I added 'results.append()' for both teacher and student. This is a function that adds the matching student to the 
results list added before.

Line 57-61 & 74-78: I added if conditional statement. Thus, when the results list does not have a match for the input in search, 
a message "No Match Found" will returns to user. 'else' will be run when the results list is not empty, which means there is a 
match for the input in search. 'for __ in __' means if the input match results list, program will print the information of the
person.

Line 71: ' if (term_lower in teacher.name.lower()) or (term_lower in teacher.speciality.lower())' is similar to line 54, for
both teacher's name and speciality will be case-insensitive.

To run the code, I type 'dotnet.run' on the console.

To test it,
1. Register a student 
- Choose 1
- Input Name: Tam, Instrument: Piano
- The output would be:
  Front Desk: Enrolled student 1 in 'Piano'.
  Front Desk: Successfully registered 'Tam' and enrolled them in 'Piano'.

2. Enrol an existing student
- Choose 2
- Input Student ID: 1 
- Input instrument to enrol in: Guitar
- The output would be:
   Front Desk: Enrolled student 1 in 'Guitar'.

3. Look up  Student or Teacher
- Choose 3
- Input Tam or Elyon
- As Tam is in the results list, the output would be: 
  --- Student List ---
  ID: 1, Name: Tam, Enrolled in: ['Piano', 'Guitar']
- Elyon is not in the results list, the output would be:
  --- Performing lookup for 'Elyon' ---

  --- Finding Students matching 'Elyon' ---
  No Match Found.

  --- Finding Teachers matching 'Elyon' ---
  No Match Found.
- Same goes to teacher, only (Dr. Keys, "Piano") and ("Ms. Fret", "Guitar") is in the list.

4. List Students / Teachers
- Choose 4 or 5
- They will print all current records.
<<<<<<< HEAD

=======
>>>>>>> 8ccb219 (Update README.md)
