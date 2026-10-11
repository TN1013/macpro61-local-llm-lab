MacPro6,1 Local LLM Lab
Kernel pp512 regression-boundary study

Research date:
2026-10-11

Kernel series:
Linux 6.12.108-labtest
Linux 6.12.109-labtest
Linux 6.12.110-labtest
Linux 6.12.111-labtest
Linux 6.12.112-labtest

Raw evidence snapshot:
final-v131-boundary-20261011-223425

Raw evidence outer-manifest SHA256:
e0f4c6a29ef7f4621d6aa7dc98b7563374c056f4c291bc925ad3fa79b40d372c

Derived-analysis manifest SHA256:
e6b281d1a18bfdbce45e028e5d58c5ae4b88352d8ed4d6ee8f34dcc696685d66

Result:
Under the controlled cold-test conditions used in this campaign,
the pp512 performance regression boundary is localized between
Linux 6.12.110 and Linux 6.12.111.

Performance remains on the regressed side in Linux 6.12.112.

Cause:
Not yet identified. The responsible kernel commit or subsystem
has not yet been isolated.
