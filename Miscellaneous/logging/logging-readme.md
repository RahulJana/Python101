# Different Levels of `logging`

1. level: `DEBUG`: Detailed information, typically of interest only when diagnosing problems.

2. level: `INFO`: Confirmation that things are working as expected.

3. level: `WARNING`: An indication that something unexpected happened, or indicative of some problem in the near future (e.g., disk space low). The software is still working as expected.

4. level: `ERROR`: Due to a more serious problem, the software has not been able to perform some function.

5. level: `CRITICAL`: A very serious error, indicating that the program itself may be unable to continue running.

- These levels are stored as `int` values.

```text
DEBUG:  10
INFO:  20
WARNING:  30
ERROR:  40
CRITICAL:  50
```

# LogRecord Attributes

| Attribute       | Description                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| `args`          | Variable data to be merged into the `msg` string.                           |
| `asctime`       | Human-readable time when the `LogRecord` was created.                       |
| `created`       | Time when the `LogRecord` was created (as returned by `time.time()`).       |
| `exc_info`      | Exception tuple (if provided).                                              |
| `filename`      | Filename portion of pathname.                                               |
| `funcName`      | Name of function containing the logging call.                               |
| `levelname`     | Text logging level for the message (`'DEBUG'`, `'INFO'`, `'WARNING'`, etc.).|
| `levelno`       | Numeric logging level for the message (`10`, `20`, `30`, etc.).             |
| `lineno`        | Source line number where the logging call was issued.                       |
| `message`       | The logged message, computed as `msg % args`.                               |
| `module`        | Module (name portion of filename).                                          |
| `msecs`         | Millisecond portion of the time when the `LogRecord` was created.           |
| `msg`           | The format string passed in the original logging call.                      |
| `name`          | Name of the logger used to log the call.                                    |
| `pathname`      | Full pathname of the source file where the logging call was issued.         |
| `process`       | Process ID (if available).                                                  |
| `processName`   | Process name (if available).                                                |
| `relativeCreated`| Time in milliseconds when the `LogRecord` was created, relative to the start of the program. |
| `stack_info`    | Stack frame information (if available).                                     |
| `thread`        | Thread ID (if available).                                                   |
| `threadName`    | Thread name (if available).                                                 |

For more details, refer to the [LogRecord Attributes documentation](https://docs.python.org/3/library/logging.html#logrecord-attributes).


# Different `logger` selection


```log
2025-03-21 21:45:03,123:root:INFO:Created Employee: John Doe - john.doe@company.com 
```
