import importlib, importlib.util, sys
mods = ['altair','streamlit','plotly','pycountry','pandas']
print('Python', sys.version)
for m in mods:
    try:
        spec = importlib.util.find_spec(m)
        if spec is None:
            print(m + ': NOT INSTALLED')
        else:
            mod = importlib.import_module(m)
            print(m + ': ' + getattr(mod, '__version__', 'unknown'))
    except Exception as e:
        print(m + ': ERROR - ' + str(e))
