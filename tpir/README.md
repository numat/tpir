TPIR
=====

A simple server for reading the ATMI TPIR.

On connection, this device vomits out one-way data (most of this is
undocumented and ultimately discarded). A serial upgrader needs to stay on top
of the buffer stream and present a clean request-response server.

HTTP API
========

`GET /` Returns an object of the form `[0, 0, 0, 0]`, corresponding to the
four IR channels.
