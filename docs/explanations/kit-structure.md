# Understanding a kit file structure

## Kit file layout

```python
class KitWindow(MainWindow):
	def __init__():
		...

	def get_measures():
		...					# Define here how to retrieve sensors measures

	def checkGPIOstate():
		...					# Define here how to check IN/OUT pins current state

def deviceConnection():
	...						# Define here how to verify device connection state
```

## What is the `KitWindow` class ?

The `KitWindow` is the class that will be used by VMCGUI core application to build the interactive interface.
In other words, when you will select a kit from the start window, VMCGUI will use the imported `KitWindow` class to construct a 'window' object, according to `KitWindow` attributes.
