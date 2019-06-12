
This is the app for practicing 100 list technique used to memoize large number. 
It uses Python and Kivy.   

## Build

- Install buildozer
- Install requirements from `requirements.txt` and only then `requirements-kivy.txt`
- Run `make run` to run locally with Python on your machine
- Run `make build-android` to make Android build

The app is not tested on ios, sorry. 

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

- Option 2 breaks the app on android.
- Type annotations also break the app.
