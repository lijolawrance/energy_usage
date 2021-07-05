used the package datautil and calendar

More changes that can be done based on time

1. Two type of solution has been implemented one using the dict method with multiple classes and another with pandas framework. 
   Pandas code has been commented in the bill_member.py.This method I believe will be faster(yet to be tested). Unit testing is also not implemented 
   for the pandas coding given the time limit.
2. User defined exception to be introduced. Exception handling to be made better   
3. Currently, PyUnit framework is used for testing; we can plan to use PyTest framework for more extensive testing
4. Introducing database is another option

Overall Review Comments
1. The candidate provided a solid set of automated tests, covering a lot of cases and using mocked data.
2. The application solves the problem correctly (however knowledge about linear usage of energy was not taken into account). The candidate      added also an alternative solution, using pandas library, but it requires some refactoring and bugfixing to work as expected.
3. The solution is properly designed and well modularized. The implementation follows object-oriented programming principles, the code is    clean and readable.
4. Overall Rating: 4.25

Code Review Comments
1. accounts.py
   Line no 40: It’s better to use more specific exceptions (like except InvalidBillMemberException:)
2. bill_member.py
   Line no 40: I appreciate that you attached pandas based solution, but unfortunately, the quality leaves a little to be desired:
   you use a lot of non-descriptive variable names, like i,df2,df3`
   logic of the pandas solution is not correct (and it’s different from the first solution) because of line 77. which expect that the reading date is the same as the bill date (and calling e.g. with --bill_date 2018-02-28 does not give the expected result).
3. member.py
   Line no 9: It can be changed to something like f"Member ID {self.member_id} not available in bill readings"
   Line no 23: The KeyError exception is raised when the provided account id is not present in the readings file. It would be better to handle that case and for example, show some useful message for the user.
4. test_bill_member.py
   Line no 11: as context part is not necessary here because it’s unused.
   
'''''''''''''''''''''''''''''''''''''''''''''''''''''Challenge details''''''''''''''''''''''''''''''''''''''''''''''''''
For this challenge you CANNOT edit the following files which are provided to you.

readings.json You can add files to your submission, but if you edit any of the provided files, other than those
specified, your changes will be IGNORED.

Please read these instructions carefully before starting to code:
When you assemble your code challenge solution for submission please create it as a ZIP file. Please do NOT include
generated files in your submitted solution. Your ZIP upload will be cleaned to remove ignored (e.g. generated) files.
Files will be removed and ignored based on standard gitignore files as specified in this GitHub project:
github/gitignore. When you upload your code, you will be shown which files are accepted for code review and which will
be ignored. The ignored files will NOT be provided to the reviewer. Create your solution WITHIN the structure of the
starting ZIP file that you have downloaded. When you are ready to upload your code, you can re-ZIP from the starting
top-level directory and upload the entire ZIP by clicking the UPLOAD SOLUTION button below.

Overview Thank you for interviewing at Bulb and taking the time to complete this coding exercise.

We expect the challenge to take around 3-4 hours, however feel free to take as long as you need. If you run out of time,
that’s fine, just send us a README with the details of what you planned to include in your implementation.

Please approach this as you would a production problem with respect to quality and consider that we will ask you to
extend your work in a pairing exercise as part of the technical interview.

The instructions are duplicated in the README.md file in the starting code ZIP file that should download.

In this challenge, we’d like you to write a small program which, given a set of meter readings, computes a member’s
monthly energy bill. To do this, we have stubbed out the following files for you:

bill_member.py, which contains functions to compute the customer bill and print it to screen. You should implement
calculate_bill. This is the entry point to your solution. calculate_bill is currently hardcoded to give the correct
answer for August 2017. There’s no need to change calculate_and_print_bill. test_bill_member.py, a test module for
bill_member. main.py, the entry point for the program, there’s no need to make changes to this module. tariff.py, prices
by kWh for all energy load_readings.py, provides a function for loading the readings from the given json. readings.json,
contains a set of monthly meter readings for a given year, member and fuel We’d like you to:

Implement the calculate_bill function, so that given a member_id, optional account argument and billing date, we can
compute the bill for the customer. We do not want you to spend time on:

Making this backwards compatible with python <= 3. You can assume:

All times are UTC. We’re only dealing with £ denominated billing. You only need to handle electricity and gas billing.
Energy is consumed linearly. The billing date is the last day of the month. Readings are always taken at midnight. There
is only one meter reading per billing period. The JSON file structure will remain the same in any follow on exercise.