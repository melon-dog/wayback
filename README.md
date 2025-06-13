# wayback_utils.py

This module provides a Python interface to interact with the Wayback Machine web page archiving service (web.archive.org). It allows you to save URLs, check the status of archiving jobs, and verify if a URL has already been indexed.

Based on [SPN2 Public API Docs](https://archive.org/details/spn-2-public-api-page-docs-2023-01-22)

## Main classes:

- WayBackStatus: Represents the status of an archiving job.
- WayBackSave: Represents the response when requesting to archive a URL.
- WayBack: Main class to interact with the Wayback Machine API.

# Installation
```pip install wayback_utils```
- You need valid access keys (`ACCESS_KEY` and `SECRET_KEY`) to use the archiving API.
- You can provide an on_confirmation callback function to save() to receive the final archiving status asynchronously.
- The module uses requests and threading.

## Basic usage:

> [!NOTE]  
> You can obtain your `ACCESS_KEY` and `SECRET_KEY` from [archive.org](https://archive.org/account/s3.php).
1. Initialize the WayBack class with your access keys:
```python
    from wayback_utils import WayBack, WayBackStatus, WayBackSave
    
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

> [!WARNING]  
> URLs archived with the Wayback Machine may take up to 12 hours to become fully indexed and discoverable.

## save() parameters:

The `save( )` method accepts several optional parameters to customize the capture process:

- `url`: The URL to be archived.
- `timeout`: Maximum time (in seconds) to wait for the archiving operation to complete.
- `capture_all`: Capture a web page with errors (HTTP status=4xx or 5xx). By default SPN2 captures only status=200 URLs.
- `capture_outlinks`: Capture web page outlinks automatically. This also applies to PDF, JSON, RSS and MRSS feeds.
- `capture_screenshot`: Capture full page screenshot in PNG format. This is also stored in the Wayback Machine as a different capture.
- `delay_wb_availability`: The capture becomes available in the Wayback Machine after ~12 hours instead of immediately. This option helps reduce the load on our systems. All API responses remain exactly the same when using this option.
- `force_get`: Force the use of a simple HTTP GET request to capture the target URL. By default SPN2 does a HTTP HEAD on the target URL to decide whether to use a headless browser or a simple HTTP GET request. force_get overrides this behavior.
- `skip_first_archive`: Skip checking if a capture is a first if you don’t need this information. This will make captures run faster.
- `if_not_archived_within`: Capture web page only if the latest existing capture at the Archive is older than the limit in seconds, e.g. “120”. If there is a capture within the defined timedelta, SPN2 returns that as a recent capture. The default system is 45 min.
- `outlinks_availability`: Return the timestamp of the last capture for all outlinks.
- `email_result`: Send an email report of the captured URLs to the user’s email.
- `js_behavior_timeout`: Run JS code for <N> seconds after page load to trigger target page functionality like image loading on mouse over, scroll down to load more content, etc. The default system <N> is 5 sec. WARNING: The max <N> value that applies is 30 sec. NOTE: If the target page doesn’t have any JS you need to run, you can use js_behavior_timeout=0 to speed up the capture.
- `on_confirmation`: Optional callback called when archiving finishes.

Returns a `WayBackSave` object with details about the save progress or result.
- `url`: The URL to be archived.
- `job_id`: The unique identifier of the archiving job to check.
- `message`: Any important message about the processs.
- `status_code`: The save request status code.

## status() parameters:

The `status( )` method checks the status of an archiving job.

- `job_id`: The unique identifier of the archiving job to check.
- `timeout`: Maximum time in seconds to wait for the status response.

Returns a `WayBackStatus` object with details about the job's progress or result.
- `status`: Archiving job status, "pending", "success", "error".
- `job_id`: The unique identifier of the archiving job to check.
- `original_url`: The URL to be archived.
- `screenshot`: Screenshot of the website, if requested (capture_screenshot=1).
- `timestamp`: Snapshot timestamp.
- `duration_sec`: Duration of the archiving process.
- `status_ext`: Error code
- `exception`: Error 
- `message`: Additional information about the process.
- `outlinks`: List of processed outlinks (outlinks_availability=1).
- `resources`: All files downloaded from the web.
- `archive_url`: Full link to the website via the Wayback Machine

## indexed() parameters:

The `indexed( )` method checks if a given URL has already been archived and indexed by the Wayback Machine.

- `url`: The URL to check for existing archives.
- `timeout`: Maximum time in seconds to wait for the response.

Returns `True` if the URL has at least one valid (HTTP 2xx or 3xx) archived snapshot, otherwise `False`.

# License:
[MIT license](https://github.com/melon-dog/wayback_utils?tab=MIT-1-ov-file).
