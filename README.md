
## Notes

Use 
```python
class YourWidget(Widget):
    def __init__(self, your_args, **kwargs):
        super(YourWidget, self).__init__(**kwargs)
```
instead of 
```python
class YourWidget(Widget):
    def __init__(self, your_args, **kwargs):
        super().__init__(**kwargs)
```

Option 2 breaks the app on android.

Type annotations also break the app.
