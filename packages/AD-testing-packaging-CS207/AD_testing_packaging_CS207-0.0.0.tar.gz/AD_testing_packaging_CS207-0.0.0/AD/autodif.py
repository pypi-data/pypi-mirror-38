def linear_roots(a=1.0, b=0.0):
  """Returns the roots of a linear equation: ax+ b = 0.

  INPUTS
  =======
  a: float, optional, default value is 1
     Coefficient of linear term
  b: float, optional, default value is 0
     Coefficient of constant term

  RETURNS
  ========
  roots: 1-tuple of real floats
     Has the form (root) unless a = 0 
     in which case a ValueError exception is raised

  EXAMPLES
  =========
  """
  if a == 0:
      raise ValueError("The linear coefficient is zero.  This is not a linear equation.")
  else:
    return ((-b / a)) 
