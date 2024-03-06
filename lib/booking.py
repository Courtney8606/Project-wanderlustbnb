
class Booking():
  def __init__(self, id, space_id, date_booked, userid_booker, userid_approver):
    self.id = id 
    self.space_id = space_id
    self.date_booked = date_booked
    self.userid_booker = userid_booker
    self.userid_approver = userid_approver

  def __eq__(self, other):
    return self.__dict__ == other.__dict__
  
  def __repr__(self):
    return f"Booking({self.id}, {self.space_id}, {self.date_booked}, {self.userid_booker}, {self.userid_approver})" 
  



    






















    