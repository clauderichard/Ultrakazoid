from .test_uk_base import TestUkBase

class TestUkPipes(TestUkBase):

################
# Tests

  def test_pipe_seq_start(self):
    self.equkz("|c","c")
    self.equkz("c|","c<¬")
    self.equkz("[ce|]","[ce]<¬")
    
  def test_pipe_seq_end(self):
    self.equkz("[c||d]e","c(de)")
    self.equkz("[c*2_3||d]e","c*2_3(de)")
    
  def test_pipe_par_start(self):
    self.equkz("(ce|)","(ce)<¬")
    self.equkz("(ce*2|)","[e_2c]<¬")
    
  def test_pipe_par_end(self):
    self.equkz("(c*2||de*3)f","(c_2de_3).f")
    
  def test_pipe_reverseorder(self):
    self.failukz("[c||d|e]")
    self.failukz("(c||d|e)")
    
  def test_pipe_par_duplicate_start(self):
    self.failukz("(c|d|e)")
  def test_pipe_seq_duplicate_start(self):
    self.failukz("[c|d|e]")
  def test_pipe_par_duplicate_end(self):
    self.failukz("(c||d||e)")
  def test_pipe_seq_duplicate_end(self):
    self.failukz("[c||d||e]")


################################
