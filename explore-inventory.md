---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.0
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

```python
from init import *
```

```python
# Setup new project
initProject('Parameterized_model_OWF_Original')
```

```python
EF='EF v3.0 no LT'
climate = (EF, 'climate change no LT', 'global warming potential (GWP100) no LT')
```

```python
EI_DB = 'ecoinvent'
USER_DB='lif-owi'

eidb = Database(EI_DB)
userdb = Database(USER_DB)

loadParams()

print('Ecoinvent %d acts' % len(eidb))
print('User db %d acts' % len(userdb))
```

```python
explore_impacts(USER_DB, EI_DB, climate)
```
