# Open Driver Waypoint Coordinator

## Installation
This is a python3 library, so make sure to use pip for python3
```sh
python3 -m pip install ODWC
```

In your python project, include the library as follows:
```python3
import ODWC as odwc
```

## Usage
First, create a `Coordinator` (aka. router):
```python3
router = odwc.Coordinator(students, drivers)
```
The `Coordinator` constructor takes a list of students and a list of drivers. These are described in the **Data Types** section below.

Next, calculate the scheduals.
```python3
scheduals = router.calculate()
```
THis will return a dictionary with the names of the drivers as keys and their scheduals as a list for the value.

A key with the name `failed` will also be returned. This may contain a list of `Student` objects (described below). These are the students that could not be automatically schedualed and require manual schedualing.

## Data Types
These are the various types and formats that are used.

### Student
`Student` is a class that contains info about each student. These are only returned. **DO NOT** pass them in to the `Coordinator`. They contain the following values:
```python3
pickup: str
dropoff: str
time: float
```

To convert the time to a human-readable time, use the `floatToTime()` function and pass in the time.

### Student list
When passing in a list of students, use the following structure:
```python3
[
	{
	"pickup":"<address>",
	"dropoff":"<address>",
	"time":"<24 hour time>"
	},
	...
]
```

Here is an example:
```python3
[
	{
	"pickup":"525 Dundas St, London, ON N6B 1W5",
	"dropoff":"450 Dundas St, London, ON N6B 3K3",
	"time":"15:00"
	}
]
```

### Driver list
Passing in a list of drivers works in a similar way.
```python3
[
	{
	"name":"<Unique name>",
	"location":"<Starting location of the car>"
	},
	...
]
```

Here is an example:
```python3
[
	{
	"name":"driver 1",
	"location":"600 Oxford St E, London, ON N5Y 3J1"
	}
]