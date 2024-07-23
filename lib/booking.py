class Booking():
  #Set object attributes
  def __init__(self, id, space_id, date_booked, userid_booker, userid_approver, approved, display_message_icon = False, paid = False):
    self.id = id 
    self.space_id = space_id
    self.date_booked = date_booked
    self.userid_booker = userid_booker
    self.userid_approver = userid_approver
    self.approved = approved
    self.display_message_icon = display_message_icon
    self.paid = paid

  # Equality method
  def __eq__(self, other):
    return self.__dict__ == other.__dict__
  
  # Formatting
  def __repr__(self):
    return f"Booking({self.id}, {self.space_id}, {self.date_booked}, {self.userid_booker}, {self.userid_approver}, {self.approved}, {self.display_message_icon}, {self.paid})" 
  
  # # Update approval attribute of a booking
  # def mark_approved(self):
  #   self.approved = True
  #   self.display_message_icon = True


  



    






















    