# Тестирование

В репозитории нет существующих тестов. Рекомендуется добавить модульные тесты с `pytest` для ключевой логики:

- Парсинг файлов в `sorted/parse.py`.
- Операции чтения/записи CSV и обновления записей.

Установка pytest:

```bash
pip install pytest
```

Запуск всех тестов:

```bash
pytest -q
```

Пример простого теста (создайте `tests/test_csv.py`):

```python
import pandas as pd

def test_create_df_temp(tmp_path):
    p = tmp_path / "data.csv"
    df = pd.DataFrame([{"id": 1, "name": "test"}])
    df.to_csv(p, index=False)
    df2 = pd.read_csv(p)
    assert df2.loc[0, 'id'] == 1
```
