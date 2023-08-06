Install with:
```
pip install vtigerpy
```

Authentication:
```
vtiger = Vtiger(endpoint='http://localhost',username='<username>',accessKey='<access_key>')
```

Webservice:
```
import json
res = vtiger.post(operation='listTypes')
res.json()
```