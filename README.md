# EclecticIQ-Assignment
Repo with the automation for the eclecticiq testing assignment

Install requirements using the below command <br />
```pip install -r requirements.txt```

The below test cases are cover:
1. Verify if the page loads successfully.
2. Verify the presence of the table with data.
3. Verify sorting by NAME without filtering any values.
4. Verify sorting by NUMBER OF CASES without filtering any values.
5. Verify sorting by AVERAGE IMPACT SCORE without filtering any values.
6. Verify sorting by COMPLEXITY without filtering any values.
7. Verify filtering using a text present in the table and sorting by NAME
8. Verify behaviour of filters when filtering with numbers
9. Verify filtering using a text that is not present in the table
10. Verify that the filter is not case sensitive

Tests can be run using the below command <br />
```py.test -s -v```
