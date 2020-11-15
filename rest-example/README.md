# REST API

## Run

```python
  python api.py
```

## Endpoints

- [GET /](http://localhost:5000)
- [GET /recipes](http://localhost:5000/recipes)
- [GET /recipe/:id](http://localhost:5000/recipe/1)
- POST /recipe
  - sample request body
  ```json
  {
    "title": "popcorn",
    "ingredients": "corn kernels",
    "directions": "cook over open flame until cooked"
  }
  ```
