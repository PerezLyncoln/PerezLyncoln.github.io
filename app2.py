from flask import Flask, render_template, request

app = Flask(__name__)

PRELIM_PERCENT = 0.2
MIDTERM_PERCENT = 0.3
FINAL_PERCENT = 0.5
PASSING_GRADE =  75
DEAN_LISTER = 90

@app.route('/', methods=['GET', 'POST'])
#Input 
def index():
    result = None
    if request.method == 'POST':
        try:
                #Retrieves input values from the form
            prelim_grade = request.form.get('prelim_grade')
            midterm_grade = request.form.get('midterm_grade')
            final_grade = request.form.get('final_grade')

                #If there was no inputs submitted
            if not prelim_grade and not midterm_grade and not final_grade:
                return render_template('index.html', error="Please input grades")
            
            prelim_grade = float(prelim_grade) if prelim_grade else None
            midterm_grade = float(midterm_grade) if midterm_grade else None
            final_grade = float(final_grade) if final_grade else None
            
                #Checking whether inputted grades are in between 0 - 100
            if (prelim_grade is not None and (prelim_grade < 0 or prelim_grade > 100)) or \
               (midterm_grade is not None and (midterm_grade < 0 or midterm_grade > 100)) or \
               (final_grade is not None and (final_grade < 0 or final_grade > 100)):
                return render_template('index.html', error="Please enter valid grades between 0 and 100.")
            
            #Checks if input value is not numerical
        except ValueError:
            return render_template('index.html', error="Please input a numerical value")
        
        result = calculating(prelim_grade, midterm_grade, final_grade)
    
    return render_template('index.html', result=result)

def calculating(prelim_grade=None, midterm_grade=None, final_grade=None):
    
#Formula used (Prelim Grade * Prelim%(20%)) + (Midterm Grade * Midterm(30%)) + (Final Grade * Final(50%)) = Passing Grade(75)
    #If only one single grade was given
    if prelim_grade is not None and midterm_grade is None and final_grade is None:
        required_grade = (PASSING_GRADE - (prelim_grade * PRELIM_PERCENT)) / (MIDTERM_PERCENT + FINAL_PERCENT)
        dean_grade = (DEAN_LISTER - (prelim_grade * PRELIM_PERCENT)) / (MIDTERM_PERCENT + FINAL_PERCENT)
        total_grade = (prelim_grade * PRELIM_PERCENT) + (required_grade * MIDTERM_PERCENT) + (required_grade * FINAL_PERCENT)
        if required_grade < 80:
            result = f"In order to reach a total grade of {total_grade: .2f}, you will need to have a grade of {required_grade:.2f} in Midterms and Finals to pass, or {dean_grade: .2f} to become a dean's lister."
        elif required_grade >= 80 and dean_grade <= 100:
            result = f"In order to reach a total grade of {total_grade: .2f}, you will need to study hard to have a grade of {required_grade:.2f} in Midterms and Finals to pass ,or {dean_grade: .2f} to become a dean's lister."
        elif required_grade >= 80 and dean_grade > 100:
            result = f"In order to reach a total grade of {total_grade: .2f}, you will need to study hard to have a grade of {required_grade:.2f} in Midterms and Finals to pass. It is not possible to become a dean's lister with a required grade of {dean_grade: .2f}"

    elif prelim_grade is None and midterm_grade is not None and final_grade is None:
        required_grade = (PASSING_GRADE - (midterm_grade * MIDTERM_PERCENT)) / (PRELIM_PERCENT + FINAL_PERCENT)
        dean_grade = (DEAN_LISTER - (midterm_grade * MIDTERM_PERCENT)) / (PRELIM_PERCENT + FINAL_PERCENT)
        total_grade = (required_grade * PRELIM_PERCENT) + (midterm_grade * MIDTERM_PERCENT) + (required_grade * FINAL_PERCENT)
        if required_grade < 78:
            result = f"In order to reach a total grade of {total_grade: .2f}, you will need to have a grade of {required_grade:.2f} in Prelims and Finals to pass, or {dean_grade: .2f} to become a dean's lister."
        elif required_grade >= 78 and dean_grade <= 100:
            result = f"In order to reach a total grade of {total_grade: .2f}, you will need to study hard to have a grade of {required_grade:.2f} in Prelims and Finals to pass ,or {dean_grade: .2f} to become a dean's lister."
        elif required_grade >= 78 and dean_grade > 100:
            result = f"In order to reach a total grade of {total_grade: .2f}, you will need to study hard to have a grade of {required_grade:.2f} in Prelims and Finals to pass. It is not possible to become a dean's lister with a required grade of {dean_grade: .2f}"

    elif prelim_grade is None and midterm_grade is None and final_grade is not None:
        required_grade = (PASSING_GRADE - (final_grade * FINAL_PERCENT)) / (PRELIM_PERCENT + MIDTERM_PERCENT)
        dean_grade = (DEAN_LISTER - (final_grade * FINAL_PERCENT)) / (PRELIM_PERCENT + MIDTERM_PERCENT)
        total_grade = (required_grade * PRELIM_PERCENT) + (required_grade * MIDTERM_PERCENT) + (final_grade * FINAL_PERCENT)
        if required_grade < 70:
            result = f"In order to reach a total grade of {total_grade: .2f}, you will need to have a grade of {required_grade:.2f} in Prelims and Midterms to pass, or {dean_grade: .2f} to become a dean's lister."
        elif required_grade >= 70 and dean_grade <= 100:
            result = f"In order to reach a total grade of {total_grade: .2f}, you will need to study hard to have a grade of {required_grade:.2f} in Prelims and Midterms to pass ,or {dean_grade: .2f} to become a dean's lister."
        elif required_grade >= 70 and dean_grade > 100:
            result = f"In order to reach a total grade of {total_grade: .2f}, you will need to study hard to have a grade of {required_grade:.2f} in Prelims and Midterms to pass. It is not possible to become a dean's lister with a required grade of {dean_grade: .2f}"

    #All three grades were given
    elif prelim_grade is not None and midterm_grade is not None and final_grade is not None:
        total_grade = (prelim_grade * PRELIM_PERCENT) + (midterm_grade * MIDTERM_PERCENT) + (final_grade * FINAL_PERCENT)
        if total_grade >= 90:
            result = f"You are suitable for running deans lister with a total grade of {total_grade:.2f}."
        elif total_grade >= 75:
            result = f"You have passed with an overall grade of {total_grade:.2f} but not suitable for dean's lister"
        elif total_grade < 75:
            result = f"You are not able to reach the passing grade 75 with a total grade of {total_grade:.2f}."

    #If two grades were given
    #Prelims
    elif prelim_grade is not None and midterm_grade is not None and final_grade is None:
        required_grade = (PASSING_GRADE - ((prelim_grade * PRELIM_PERCENT) + (midterm_grade * MIDTERM_PERCENT))) / FINAL_PERCENT
        dean_grade = (DEAN_LISTER - ((prelim_grade * PRELIM_PERCENT) + (midterm_grade * MIDTERM_PERCENT))) / FINAL_PERCENT
        total_grade = (prelim_grade * PRELIM_PERCENT) + (midterm_grade * MIDTERM_PERCENT) + (required_grade * FINAL_PERCENT)
        if required_grade < 70:
            result = f"In order to reach the passing grade {total_grade: .2f}, you need to have {required_grade: .2f} in Finals, or {dean_grade: .2f} to become a dean's lister."
        elif required_grade >= 100 and dean_grade > 100:
            result = f"It is not possible to pass and become a dean's lister with a required grade of {required_grade: .2f} in Finals and {dean_grade: .2f} for dean's lister"
        elif required_grade >= 70 and dean_grade <= 100:
            result = f"In order to reach the passing grade {total_grade: .2f}, you will need to study hard to achieve a grade of {required_grade: .2f} in Finals, or {dean_grade: .2f} to become a dean's lister."
        elif required_grade >= 70 and dean_grade > 100:
            result = f"You will need to study hard to achieve a grade of {required_grade: .2f} in Finals to reach the passing grade 75. It is not possible to become dean's lister as you need a required grade of {dean_grade: .2f}."
            

    #Midterms
    elif prelim_grade is not None and midterm_grade is None and final_grade is not None:
        required_grade = (PASSING_GRADE - ((prelim_grade * PRELIM_PERCENT) + (final_grade * FINAL_PERCENT))) / MIDTERM_PERCENT
        dean_grade = (DEAN_LISTER - ((prelim_grade * PRELIM_PERCENT) + (final_grade * FINAL_PERCENT))) / MIDTERM_PERCENT
        total_grade = (prelim_grade * PRELIM_PERCENT) + (required_grade * MIDTERM_PERCENT) + (final_grade * FINAL_PERCENT)
        #Verify if Pass or Fail
        if required_grade < 70 and dean_grade <= 100:
            result = f"In order to reach the passing grade {total_grade: .2f}, you need to have {required_grade: .2f} in Midterms, or {dean_grade: .2f} to become a dean's lister."
        elif required_grade >= 100 and dean_grade > 100:
            result = f"It is not possible to pass and become a dean's lister with a required grade of {required_grade: .2f} in Midterms and {dean_grade: .2f} for dean's lister"
        #Pass but not a dean's lister
        elif required_grade < 70 and dean_grade > 100:
            result = f"In order to reach the passing grade {total_grade: .2f}, you need to have {required_grade: .2f} in Midterms, but it is not possible to become a dean lister with a required grade of {dean_grade: .2f}"
        #Study hard to pass and to become or not become a dean's lister
        elif required_grade >= 70 and dean_grade <= 100:
            result = f"In order to reach the passing grade {total_grade: .2f}, you will need to study hard to achieve a grade of {required_grade: .2f} in Midterms, or {dean_grade: .2f} to become a dean's lister."
        elif required_grade >= 70 and dean_grade > 100:
            result = f"You will need to study hard to achieve a grade of {required_grade: .2f} in Midterms to reach the passing grade 75. It is not possible to become dean's lister as you need a required grade of {dean_grade: .2f}."

    #Finals
    elif prelim_grade is None and midterm_grade is not None and final_grade is not None:
        required_grade = (PASSING_GRADE - ((midterm_grade * MIDTERM_PERCENT) + (final_grade * FINAL_PERCENT))) / PRELIM_PERCENT
        dean_grade = (DEAN_LISTER - ((midterm_grade * MIDTERM_PERCENT) + (final_grade * FINAL_PERCENT))) / PRELIM_PERCENT
        total_grade = (required_grade * PRELIM_PERCENT) + (midterm_grade * MIDTERM_PERCENT) + (final_grade * FINAL_PERCENT)
        #Verify if Pass or Fail
        if required_grade < 70 and dean_grade <= 100:
            result = f"In order to reach the passing grade {total_grade: .2f}, you need to have {required_grade: .2f} in Midterms, or {dean_grade: .2f} to become a dean's lister."
        elif required_grade >= 100 and dean_grade > 100:
            result = f"It is not possible to pass and become a dean's lister with a required grade of {required_grade: .2f} in Midterms and {dean_grade: .2f} for dean's lister"
        #Pass but not a dean's lister
        elif required_grade < 70 and dean_grade > 100:
            result = f"In order to reach the passing grade {total_grade: .2f}, you need to have {required_grade: .2f} in Midterms, but it is not possible to become a dean lister with a required grade of {dean_grade: .2f}"
        #Study hard to pass and to become or not become a dean's lister
        elif required_grade >= 70 and dean_grade <= 100:
            result = f"In order to reach the passing grade {total_grade: .2f}, you will need to study hard to achieve a grade of {required_grade: .2f} in Midterms, or {dean_grade: .2f} to become a dean's lister."
        elif required_grade >= 70 and dean_grade > 100:
            result = f"You will need to study hard to achieve a grade of {required_grade: .2f} in Midterms to reach the passing grade 75. It is not possible to become dean's lister as you need a required grade of {dean_grade: .2f}."
    
    else:
        return render_template('index.html', f"Please put valid inputs")

    #Returns result to display in front of the student
    return result

if __name__ == '__main__':
    app.run(debug=True)



#Hello, I mostly used ChatGPT to help me creating this simple grade calculator, mostly in knowing how python flask work GET and POST, how to retrieve inputs from html, how to use else, if, elseif, return function, or in general, mostly everything.
#I also used ChatGPT for debugging codes because 