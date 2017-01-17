# The sieve/rotator algorithm
# Take a fine-grained PRMT schedule and
# turn it into a DRMT schedule for num_procs processors

class SlotOccupancy:
  def __init__(self):
    self.match_slot = False
    self.action_slot = False
  def __str__(self):
    return "\nmatch: " + str(self.match_slot) + "\n" + "action: " + str(self.action_slot)
  def __repr__(self):
    return "\nmatch: " + str(self.match_slot) + "\n" + "action: " + str(self.action_slot)

def sieve_rotator(pipe_schedule, num_procs, dM, dA):
  # For each processor is the match, action slot taken already?
  proc_occupied = [SlotOccupancy() for i in range(num_procs)]

  # Current time (starting from 0) after scheduling a certain number of nodes
  current_time = 0

  # Construct drmt schedule as a dictionary
  drmt_schedule = dict()

  # Transform pipe_schedule into a form that gives all the match operations or all the action operations in each time slot
  print pipe_schedule
  max_time=max(pipe_schedule)
  print max_time
  assert((max_time + 1) <= (2 * num_procs)) # otherwise reject it outright
  for t in range(max_time + 1):
    # schedule match column in table
    if (t%2 == 0):
      while (proc_occupied[current_time%num_procs].match_slot):
        current_time += 1
        print "NOP current_time incremented to ", current_time
      print "scheduled a match column at", current_time
      for v in pipe_schedule[t]: drmt_schedule[v] = current_time
      proc_occupied[current_time%num_procs].match_slot = True
      current_time += dM

    # schedule action column in table
    else:
      while (proc_occupied[current_time%num_procs].action_slot):
        current_time += 1
        print "NOP current_time incremented to ", current_time
      print "scheduled an action at", current_time
      for v in pipe_schedule[t]: drmt_schedule[v] = current_time
      proc_occupied[current_time%num_procs].action_slot = True
      current_time += dA

  return drmt_schedule