from calendarTest import create_event

def main():
    create_event(title='Function Test',location='walc',description=' ', start_date='2025-02-20T09:00:00', end_date='2025-02-20T11:00:00',guests=[{'email': 'madhavsv05@gmail.com'},], recurring='WEEKLY', amountRecur='COUNT=3')

if __name__ == "__main__":
  main()