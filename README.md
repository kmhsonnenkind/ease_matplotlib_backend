
# matplotlib backend for rendering in Eclipse


## Overview

This is a simple proof of concept that it is possilbe to render to Eclipse views using **matplotlib** and **EASE**.

It is not meant to be used productively but rather as a starting point for anyone interested in actually implementing a full backend.


## Installation

Simply run `python setup.py install` to have install the package and have it available in matplotlib.


## Usage

To use the renderer you need to tell **matplotlib** to use the module by calling:
```python
matplotlib.use('module://matplotlib_backend_ease')
```

This will only work if running in an **EASE py4j** script engine as the displaying of data is done using Java functionality called from Python.


## Example

This quick example shows how to use the renderer and draw something simple.

```python
import matplotlib

# Must be called before importing pyplot!
matplotlib.use('module://matplotlib_backend_ease')

import matplotlib.pyplot as plt

# Just draw something simple
plt.figure()
plt.plot([1, 2, 3], [1, 2, 3])
plt.show()

```


## Known issues

As this is just a proof of concept there are several issues (some of which could be resolved fairly easily though):

#### The created files are not deleted automatically
**Fix:** Just clean up manually or add a simple `org.eclipse.ui.IPartListener2` that deletes the file in its `partClosed()` method. This needs to be done in Java though as asynchronous callbacks from other threads are not working (reliably) in py4j.

#### `pyplot.show()` does not wait for the view to be closed
**Fix:** Once again just create an `IPartListener2` that sets the `EventTimedShow.show_stopper` event. Bit more tricky because you need to get back to Python this time but still manageable because you have more control over Java threads in Java (duh).

#### The backend only renders static images so no zoom, hover, etc.
**Fix:** This can be a bit tricky. We would either need to implement a full backend or try to hijack some of the HTML renderers available.