oarpy: OAR job management in python
===================================

Getting started
---------------

Submit
~~~~~~

Run an OAR job that prints "Hello world":

.. code-block:: python

    from oarpy.oarjob import submit

    job = submit(command='echo "Hello word"', name='helloword',
                 project='oarpy', core=1, gpu=False, walltime={'hours':2})
    print(job)
    job.wait()

    if job.exit_code:
        print('Failed:\n{}'.format(job.stderr))
    elif job.exit_code is None:
        print('Interrupted:\n{}'.format(job.stdout))
    else:
        print('Succes:\n{}'.format(job.stdout))

    job.remove_logs()

Only "command" is required, all other arguments are optional. See documentation for more fine-grained control with the JobFactory and Resource classes.

Search
~~~~~~

Find a job in case you know the job ID:

.. code-block:: python

    from oarpy.oarjob import Job
    job = Job(1130922)
    print(job)

Find a job in case you do not know the job ID (not all arguments are necessary):

.. code-block:: python

    from oarpy.oarjob import search
    from oarpy import timeutils
    import os

    owner = os.getlogin()
    start = timeutils.add(timeutils.now(),minutes=-10)
    jobs = search(owner=owner, start=start, name='quickstart',
                  project='oarpy', state='Terminated')
    print(jobs)