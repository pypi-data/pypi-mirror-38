
# ==================================================================================================

def convert(**kwargs):
  r'''
Convert a pair of elastic constants into other pairs of elastic constants. The
input arguments are any of the pairs of constants.

:options:

  **E, nu, K, G, lambda, mu** (``<float>``)
    Any combination of two elastic constants. (To deal with the name "lambda" a dictionary can be
    used, or the abbreviated keyword "lam" may be used.)

:returns:

  **parameters** (``<dict>``)
    Dictionary with all combinations of elastic constants filled.

.. note::

  See: https://en.m.wikipedia.org/wiki/Elastic_modulus
  '''

  if 'mu'  in kwargs: kwargs['G'     ] = kwargs.pop('mu' )
  if 'lam' in kwargs: kwargs['lambda'] = kwargs.pop('lam')

  if len(kwargs) != 2: raise IOError('Exactly two elastic constants must be given as input')

  K   = kwargs.get('K'     , None)
  E   = kwargs.get('E'     , None)
  lam = kwargs.get('lambda', None)
  G   = kwargs.get('G'     , None)
  nu  = kwargs.get('nu'    , None)

  if K is not None and E is not None:
    kwargs['lambda'] = 3.*K * (3.*K-E)/(9.*K-E)
    kwargs['G'     ] = 3.*K*E         /(9.*K-E)
    kwargs['nu'    ] =        (3.*K-E)/(6.*K  )

  if K is not None and lam is not None:
    kwargs['E'     ] = 9.*K*(K-lam)/(3.*K-lam)
    kwargs['G'     ] = 3.  *(K-lam)/ 2.
    kwargs['nu'    ] =         lam /(3.*K-lam)

  if K is not None and G is not None:
    kwargs['E'     ] = (9.*K*G)/(3.*K+G)
    kwargs['lambda'] = K-2.*G/3.
    kwargs['nu'    ] = (3.*K-2.*G)/(2.*(3.*K+G))

  if K is not None and nu is not None:
    kwargs['E'     ] = 3.*K*(1.-2.*nu)
    kwargs['lambda'] = 3.*K*nu/(1.+nu)
    kwargs['G'     ] = 3.*K*(1.-2.*nu)/(2.*(1.+nu))

  if E is not None and lam is not None:
    R = (E**2.+9.*lam**2.+2.*E*lam)**.5
    kwargs['K'     ] = (E+3.*lam+R)/6.
    kwargs['G'     ] = (E-3.*lam+R)/4.
    kwargs['nu'    ] = 2.*lam/(E+lam+R)

  if E is not None and G is not None:
    kwargs['K'     ] = E*G/(3.*(3.*G-E))
    kwargs['lambda'] = G*(E-2.*G)/(3.*G-E)
    kwargs['nu'    ] = E/(2.*G)-1.

  if E is not None and nu is not None:
    kwargs['K'     ] = E/(3.*(1.-2.*nu))
    kwargs['G'     ] = E/(2.*(1.+   nu))
    kwargs['lambda'] = E*nu/((1+nu)*(1-2.*nu))

  if lam is not None and G is not None:
    kwargs['K'     ] = lam+2./3.*G
    kwargs['E'     ] = G*(3.*lam+2.*G)/(lam+G)
    kwargs['nu'    ] = lam/(2.*(lam+G))

  if lam is not None and nu is not None:
    kwargs['K'     ] = lam*(1.+nu)/(3.*nu)
    kwargs['E'     ] = lam*(1.+nu)*(1.-2.*nu)/nu
    kwargs['G'     ] = lam*(1.-2.*nu)/(2.*nu)

  if G is not None and nu is not None:
    kwargs['K'     ] = 2.*G*(1.+nu)/(3.*(1-2.*nu))
    kwargs['E'     ] = 2.*G*(1.+nu)
    kwargs['lambda'] = 2.*G*nu/(1-2.*nu)

  kwargs['mu'] = kwargs['G']

  return kwargs

# ==================================================================================================

if __name__ == '__main__':

  def verify(A, B):
    for key in A:
      if abs(A[key]-B[key]) > 1.e-12:
        print(key, A[key], B[key])
        raise IOError('Parameters inconsistent')

  param = convert(E=1., nu=.3)

  verify(param, convert(K   = param['K'     ], E   = param['E'     ]))
  verify(param, convert(K   = param['K'     ], lam = param['lambda']))
  verify(param, convert(K   = param['K'     ], G   = param['G'     ]))
  verify(param, convert(K   = param['K'     ], nu  = param['nu'    ]))
  verify(param, convert(E   = param['E'     ], lam = param['lambda']))
  verify(param, convert(E   = param['E'     ], G   = param['G'     ]))
  verify(param, convert(E   = param['E'     ], nu  = param['nu'    ]))
  verify(param, convert(lam = param['lambda'], G   = param['G'     ]))
  verify(param, convert(lam = param['lambda'], nu  = param['nu'    ]))
  verify(param, convert(G   = param['G'     ], nu  = param['nu'    ]))



