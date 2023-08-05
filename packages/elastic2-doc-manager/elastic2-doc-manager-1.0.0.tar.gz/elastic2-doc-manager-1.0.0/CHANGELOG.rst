Changelog
=========

Version 1.0.0
-------------

- Drop support for Python 3.3 and earlier, including Python 2.

Version 0.4.0
-------------

- Remove reliance on ``mongo_connector.compat``.

Version 0.3.0
-------------

- Support for Elasticsearch 5.x.
- Significant performance improvements because operations are buffered.
- BulkIndexErrors are now caught and reraised as OperationFailed.

Version 0.2.0
-------------

- Bug fix for namespace information saved in the mongo-connector metadata index.
- Support AWS Elasticsearch Service Request Signing.

Version 0.1.0
-------------

This was the first release of elastic-doc-manager.
