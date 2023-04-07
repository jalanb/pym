try:
    pass
except:
    pass

try:
    pass
except Exception:
    pass

try:
    pass
except Exception as e:
    print(str(e))

try:
    pass
except (Exception, SyntaxError) as e:
    print(str(e))
