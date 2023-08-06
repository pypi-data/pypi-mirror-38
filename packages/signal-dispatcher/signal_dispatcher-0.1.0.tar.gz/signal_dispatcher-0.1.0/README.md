# Introduction
This package contains simple PyQt 5 signal dispatcher. It solves one of the problems that I often face - easy connecting signals with handlers. The approach used is very similar to the basic functionality of the Symfony's event dispatcher. 
Signals are added in dictionary using aliases. Then handlers are added in another dictionary also using aliases. After running the ```SignalDispatcher::dispatch()``` method, all the signals are connected with their proper handlers based on aliases. The dispatch method must be called before the application enters main loop.

# Installation
Use: ```pip3 install signal-dispatcher```.

# Usage
```python
import PyQt5
import signal_dispatcher 

# Register event
signal = PyQt5.QtCore.pyqtSignal().emit()
signal_dispatcher.SignalDispatcher.register_signal('my_signal', signal)

# Register handler
def my_handler():
    print('signal handled')
    
signal_dispatcher.SignalDispatcher.register_handler('my_signal', my_handler())

# Dispatch and handle
signal_dispatcher.SignalDispatcher.dispatch()

``` 

# Methods reference

## SignalDispatcher

### Methods

###### SignalDispatcher.register_signal(*string* alias, *pyqtSignal* signal) -> void
Used to register signal at the dispatcher. Note that you can not use alias that already exists.

###### SignalDispatcher.register_handler(*string* alias, *callable* handler)
Used to register handler at the dispatcher.

###### SignalDispatcher.dispatch()
This methods runs the wheel. It is used to connect signal with their handlers, based on the aliases.

###### SignalDispatcher.signal_aliases()
Returns all available signal aliases.

###### SignalDispatcher.handler_aliases()
Gets all available handler aliases.

###### SignalDispatcher.signal_alias_exists(*string* alias)
Checks if signal alias exists.

###### SignalDispatcher.handler_alias_exists(*stirng* alias)
Checks if handler alisa exists.

## SignalDispatcherError

### Methods

###### ___init___(self, *string* message)