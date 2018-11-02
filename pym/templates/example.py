Example(
    'Standard python types, no html',
    [1, 2, 3
     , 4.0
     , 'a', u'b'
     , ('c', ('d', 'e')
        , set(['f', 'f'])) # nested
     , (i*2 for i in xrange(10))
     ])
# output = '1234.0abcdef024681012141618'

Example(
    'Standard python types, no html *or* html escaping',
    [1, '<', 2, '<', 3],
    visitor_map=default_visitors_map)
# output = '1<2<3'

