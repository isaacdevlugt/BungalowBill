Circuit serializer for PennyLane

TODO: 

- regular `save` method to be called after a QNode is defined
- regular `load` method
- if calling a circuit many times, say, for an optimization routine, have a built-in check-pointing system
- demos are a good source of different (usable!) circuits
- check for file existence before dumping and loading

Foreseeable issues:

- if using a decorator, every time the circuit is called the `save` method gets called (not good! only want to save once typically)
- `@save` method that can be compound decorated with @qml.qnode may cause bugs elsewhere in PennyLane
- currently we can't take gradients of a qnode that has been loaded in 
- qml.BaisState() saves the np array of binary states with required_grad = True?? aghh
