wayback_utils.py

This module provides a Python interface to interact with the Wayback Machine web page archiving service (web.archive.org). It allows you to save URLs, check the status of archiving jobs, and verify if a URL has already been indexed.

Main classes:
-------------

- WayBackStatus: Represents the status of an archiving job.
- WayBackSave: Represents the response when requesting to archive a URL.
- WayBack: Main class to interact with the Wayback Machine API.

Basic usage:
------------
> **Note:**  
> You can obtain your `ACCESS_KEY` and `SECRET_KEY` from [https://archive.org/account/s3.php](https://archive.org/account/s3.php).
1. Initialize the WayBack class with your access keys:
```python
    wb = WayBack(ACCESS_KEY="your_access_key", SECRET_KEY="your_secret_key")
```
2. Save a URL:
```python
    result = wb.save("https://example.com")
```
3. Check the status of a job:
```python
    status = wb.status(result.job_id)
```
4. Verify if a URL is already indexed:
```python
    is_indexed = wb.indexed("https://example.com")
```

You can also pass a callback function to `save()` using the `on_confirmation` parameter. This callback will be called asynchronously with the final result of the archiving operation:

```python
def my_callback(result):
    print("Archiving finished:", result.status)

result = wb.save("https://example.com", on_confirmation=my_callback)
```

> **Warning:**  
> URLs archived with the Wayback Machine may take up to 12 hours to become fully indexed and discoverable.
Notes:
------

- You need valid access keys (ACCESS_KEY and SECRET_KEY) to use the archiving API.
- You can provide an on_confirmation callback function to save() to receive the final archiving status asynchronously.
- The module uses requests and threading.

License:
--------
MIT license.
