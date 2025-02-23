from calendarTest import create_event
from client import analyze_text

def main():
    extracted_text = ("( Oo Madhav Valiyaparambil <vpmadhav@gmail.com>"
                        "ee tome +"
                        "Yo Saket,"
                        "Wanna meet up at 12:00 at Krach to Study for a little bit")
    print("Start analysis")
    formatted_text = analyze_text(extracted_text)
    print(formatted_text)
    formatted_text = formatted_text.replace("Name= ", "")
    formatted_text = formatted_text.replace("Location= ", "")
    formatted_text = formatted_text.replace("StartTime= ", "")
    formatted_text = formatted_text.replace("EndTime= ", "")
    formatted_text = formatted_text.replace("StartDate= ", "")
    formatted_text = formatted_text.replace("EndDate= ", "")
    items = formatted_text.split("\n")
    final_start_date = items[4] + "T" + items[2] + ":00"
    final_end_date = items[5] + "T" + items[3] + ":00"
    print("title=Study Session, location=Krach, description=None, start_date=2025-02-23T12:00:00, end_date=2025-02-23T13:30:00, guests=['email': 'madhavsv05@gmail.com'], recurring='WEEKLY', amountRecur='COUNT=3'")
    event = create_event(title="Study Session", location="Krach", description=' ', start_date="2025-02-23T12:00:00", end_date="2025-02-23T13:30:00", guests=[{'email': 'madhavsv05@gmail.com'},], recurring='WEEKLY', amountRecur='COUNT=3')

if __name__ == "__main__":
  main()