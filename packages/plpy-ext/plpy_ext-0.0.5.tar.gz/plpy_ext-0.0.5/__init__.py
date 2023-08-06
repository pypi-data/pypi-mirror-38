import time
import plpy


def print(*args):
    plpy.info(*args)


def execute(query, args):
    """ Usage:
    query = 'SELECT * FROM tab WHERE uid = $1 created_at <= $2'
    args = (
        (uid, 'varchar'),
        (created_at, 'timestamp')
    )
    execute(query, args)
    """
    types = [t for _, t in args]
    values = [v for v, _ in args]
    plan = plpy.prepare(query, types)
    return plan.execute(values)


def fetch(query, size=1000000, verbose=False):
    """
    Decorator what fetch queried rows by parts ad apply decorated function as callback to each row.
    To break fetching, decorated function must return False.
    :param query: string - SQL query.
    :param size: int - number of rows for fetch by one part.
    :param verbose: bool - if True, prints some info in fetching process.
    """
    start_time = time.time()

    def log(*args):
        if verbose:
            print(*[a.replace('%TIME_SPENT%', get_spent_time()) for a in args])

    def get_spent_time():
        return time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time))

    log('start fetching rows by parts. part size = %s' % size)

    def decorator(func):
        cursor = plpy.cursor(query)
        while True:
            log('fetch rows...   (%TIME_SPENT%)')
            res = cursor.fetch(size)
            if not res.nrows():
                break

            log('process rows... (%TIME_SPENT%)')
            for row in res:
                if func(row) is False:
                    return

        log('total time spent: %TIME_SPENT%')
    return decorator
