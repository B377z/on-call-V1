from datetime import datetime

schedule_list = []

def get_last_id():
    if schedule_list:
        return schedule_list[-1]['id']
    return 0

class Schedule:
    def __init__(self, id, staffId, start_date, end_date, status='scheduled', description='', is_published=False):
        self.id = id
        self.staffId = staffId
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.description = description
        self.is_published = is_published
        self.createdAt = datetime.utcnow()
        self.updatedAt = datetime.utcnow()
        
    def __repr__(self):
        return (f"<Schedule id={self.id}, staffId={self.staffId}, start_date={self.start_date}, "
                f"end_date={self.end_date}, status={self.status}, description={self.description}, "
                f"is_published={self.is_published}, createdAt={self.createdAt}, updatedAt={self.updatedAt}>")
