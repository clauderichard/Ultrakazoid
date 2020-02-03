from ukz import *

ukztestresults = []
def inittests():
  ukztestresults = []
def testresult(b,s):
  print(s)
  ukztestresults.append((b,s))
def testresults():
  g = 0
  f = 0
  for (b,s) in ukztestresults:
    if b:
      g += 1
    else:
      f += 1
  print(f"#Successes: {g}. Failures: {f}")

def pmel(m):
  s = f"{m.t}:{m.d}:"
  for n in m.notes:
    s += f"({n.t},{n.d}:{n.p},{n.l})"
  s += "Gs:"
  i = 0
  for gs in m.gradients:
    s += f"Typ{i}:"
    for g in gs:
      s += f"{g.t},{g.d}"
    i += 1
  return s

def equk(f,a,b):
  m = f(a)
  n = f(b)
  if m != n:
    testresult(False,f"FAIL: {a} == {b}\n {pmel(m)}\n {pmel(n)}")
  else:
    testresult(True,f"Good: {a} == {b}")
def equkz(a,b):
  equk(ukz,a,b)
def equkd(a,b):
  equk(ukd,a,b)
    
def nequk(f,a,b):
  m = f(a)
  n = f(b)
  if m == n:
    testresult(False,f"FAIL: {a} != {b}\n {pmel(m)}\n {pmel(n)}")
  else:
    testresult(True,f"Good: {a} != {b}")
def nequkz(a,b):
  nequk(ukz,a,b)
def nequkd(a,b):
  nequk(ukd,a,b)
    
    
def chkuk(f,s,t,d,ns):
  m = f(s)
  ns1 = sorted(list(map(lambda n: \
   (n.t,n.d,n.p,n.l), m.notes)))
  if ns1 != ns or t!=m.t or d!=m.d:
    testresult(False,f"FAIL: {s}, ({t},{d}):{ns}\n ({m.t},{m.d}):{ns1}")
  else:
    testresult(True,f"Good: {s}, {ns}")
def chkukz(s,t,d,ns):
  chkuk(ukz,s,t,d,ns)
def chkukd(s,t,d,ns):
  chkuk(ukd,s,t,d,ns)
