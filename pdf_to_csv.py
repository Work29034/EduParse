import pdfplumber
import csv
import re
from grade_mappings import grade_points_map, subject_credits

def process_pdf(file_path):
    output_csv = file_path.replace('.pdf', '.csv')
    rows = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split('\n')
            for line in lines:
                student_data = {
                    'Roll Number': '', 'Student Name': '', 'Class': '', 'Section': '',
                    'Department': '', 'Year': '', 'Semester': '',
                    'Subject Code': '', 'Subject Name': '', 'Grade': '',
                    'Grade Points': '', 'Credits': ''
                }

                roll_match = re.search(r'\b[0-9]{2}[A-Z]{3}[0-9]{4}\b', line)
                if roll_match:
                    student_data['Roll Number'] = roll_match.group(0)

                if 'Name:' in line:
                    student_data['Student Name'] = line.split('Name:')[-1].strip()
                if 'Class:' in line:
                    student_data['Class'] = line.split('Class:')[-1].strip()
                if 'Sec:' in line:
                    student_data['Section'] = line.split('Sec:')[-1].strip()
                if 'Dept:' in line:
                    student_data['Department'] = line.split('Dept:')[-1].strip()
                if 'Year:' in line:
                    student_data['Year'] = line.split('Year:')[-1].strip()
                if 'Sem:' in line:
                    student_data['Semester'] = line.split('Sem:')[-1].strip()
                if 'SubCode:' in line:
                    student_data['Subject Code'] = line.split('SubCode:')[-1].strip()
                if 'SubName:' in line:
                    student_data['Subject Name'] = line.split('SubName:')[-1].strip()
                if 'Grade:' in line:
                    student_data['Grade'] = line.split('Grade:')[-1].strip()

                if student_data['Grade']:
                    student_data['Grade Points'] = grade_points_map.get(student_data['Grade'], 'N/A')
                if student_data['Subject Code']:
                    student_data['Credits'] = subject_credits.get(student_data['Subject Code'], 'N/A')

                if student_data['Roll Number'] and student_data['Subject Code']:
                    rows.append([
                        student_data['Roll Number'], student_data['Student Name'], student_data['Class'],
                        student_data['Section'], student_data['Department'], student_data['Year'],
                        student_data['Semester'], student_data['Subject Code'], student_data['Subject Name'],
                        student_data['Grade'], student_data['Grade Points'], student_data['Credits']
                    ])

    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Roll Number', 'Student Name', 'Class', 'Section', 'Department', 'Year', 'Semester', 'Subject Code', 'Subject Name', 'Grade', 'Grade Points', 'Credits'])
        writer.writerows(rows)

    return output_csv
