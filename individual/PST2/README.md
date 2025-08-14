Line 21-29: I added courses dictionary because I want to store course data by ID. next_course_id is also added for auto-increment of course IDs. I made this to enable proper course management system, in which both student and teacher can track their course ID.

Line 53-64: I added a add_student function which takes parameter of students name and enrolled course. Student ID will be assigned from app_data[next_student_id]. I create a new student dictionary, that stores students name, ID and enrolled course. When theres new students, the data will be added to the students list in app_data. Next student added will get a unique ID from app_data.

Line 59: I added .split() to separate the courses by adding comma in between. For example the courses would be ["Piano", "Guitar"]. This line is list comprehension. c.strip() is used to update the element to ensure that the new list wouldnt have spaces infront.

Line 66-81: I added add_course function to register a new course into my system with unique IDs. I can check whether the new course input is empty or just space from course_name.strip. Then I ensure that app_data dictionary contains courses dictionary and a next_course_id counter, it will automatically assign them if they dont exist. app_data['courses'][course_id] = course_name.strip() can add a new course to the system with a unique ID and a properly formatted name. The new course ID is returned for further use.

Line 95-98: I added a remove teacher function. First it will loop through app_data to find the teacher that we want to remove from a list of teacher dictionaries. This line creates a new list that only contain those teachers whose id is not equal to thhe teacher_id to be removed.

Line 100-107: I added update_student function. First it will loops through all students in app_data, iif there ius a matching id, the .update(fields) method will update the student dictionary with the new field provided.

Line 109-112: I added a remove student function which is similar to remove teacher function.

Line 121-148: I added something inside the check_in function. First, it will loops through all students Loops through all students in app_data['students']. It will find the student whose id matches student_id and stores the full student dictionary in the variable student. This allows me to get the student’s name later. Next, it will also look up course name using course ID. Under the check-in record I store both IDs and names for the student and course. Finally, the system adds the record to the app_data['attendance'] list.

Line 150-181: I added something extra to show the card content before saving into file. I created a string called card_content. The card is then saved to a text file. Finally I allow the system to print the card_content, and it will also be saved into file after user input their information for card printing.

Line 188-200: In the main application loop I added, add student, add teacher, update student info, remove teacher, view attendance record and add course.

Line 205-211: For check-in student, the system asks the user to enter ID and course for check in, after that check_in function will be called, the student attendance will be stored in app_data['attendance']. made_change flag will save the data immediately.

Line 213-255: For add student and add teacher, their function are similar. After inputting their information, the data will be stored in their respective function defined above.

Line 227-232: For print student card, system will prompts the user to enter their ID. function print_student_card(student_id) will be called to generate text file badge and display the student's card details.

Line 234-250: To update teacher info, user will be asked to enter ID, name and speciality. A dictionary fields is created to collect only the fields thatt the user want to update. Then update_teacher(teacher_id, **fields) function will be called to update the information. made_change is true to save data.

Line 252-268: Updating student info is similar to update teacher info. List comprehension is used to clean up course names here.

Line 271-282: To remove student and teacher, user will have to enter ID first, then the function used to remove them will be called. Their data will be removed from app_data as well.

Line 284-295: The system will look through data in app_data['attendance'], everything stored in their will be displayed, including time checked in, name and ID for student and the course. I use .get to safely fetch values, this can prevent errors if keys are missing. 

Line 297-301: If the school decided to add new course, they will have this option to add. They can enter course name to add. However, if the input is invalid it will returns None.

How to run:
1. Run the program
2. Choose 10 to add course. Confirmation will be printed.
3. Add a new student, choose 2. For example, Tam in Piano. Confirmation will be printed.
4. Add a new teacher, choose 3. For example, Lim in Piano. Confirmation will be printed.
5. Choose 1 to check in a student. For example, input student ID 1 and course ID 1. This record will appends to app_data['attendance'] and confirmation will be printed.
6. Choose 4 to print student card. After input student ID, for example student ID:1, the program creates 1_card.txt, and the file will be displayed to console, which is the student card.
7. Choose 5 to update teacher info. Input current ID, then input new name and speciality, program will update teacher dictionary and print confirmation.
8. Choose 6 to update student info. Input current ID, then input new name and courses, program will update student dictionary and print confirmation.
9. To remove student, choose 7, input student ID, then the student will be removed.
10. To remove teacher, choose 8, input teacher ID, then the teacher will be removed.
11. To view attendance records, choose 9, the program will print all the records from app_data['attendance'].
12. Choose q, the program will calls save_data() and writes all changes to msms.json. Finally, program exits cleanly.