import pandas

class Observables:
  def __init__(self, path):
    self.dataframe = pandas.read_table(path)
    mysillyobject.name = name
    mysillyobject.age = age

  def BRNP(self, A, B):
    self.BRNP = self.dataframe[f'b_H3_{A}{B}']
