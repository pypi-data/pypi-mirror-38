# DSInterface
A tiny python port of WPILib's driverstation class

## Installation
DSInterface can be installed from pip using the command:
```
python3 -m pip install DSInterface
```

Next, import it in your project:
```python
import DSInterface as DSI
```

## Usage
In order to acces any data from FMS or the DriverStation, the `DriverStation` class must be initalized.
```python
ds = DSI.DriverStation()
```

### Pulling data from FMS
These are the avalible methods for `DriverStation`:

| Method | What it Does |
| ------ | ------------ |
| `getAlliance()` | Returns a `DSI.alliances` enum to represent the alliance |
| `getStation()` | Returns an int from 1 to 3 that matches with your assigned station for the following match |
| `getMatchType()` | Returns an int that represents the match type |
| `getFMSControlData()` | Returns the raw FMS control data |
| `getReplayNumber()` | Returns the replay number |
| `getMatchNumber()` | Returns the match number |
| `getEventName()` | Returns the event name as a string |
| `getGSM()` | Returns the game specific message as an uppercase string |
