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


def fetch(query, size=1000000, verbose=False, limit=None):
    """
    Decorator what fetch queried rows by parts ad apply decorated function as callback to each row.
    To break fetching, decorated function must return False.
    :param query: string - SQL query.
    :param size: int - number of rows for fetch by one part.
    :param verbose: bool - if True, prints some info in fetching process.
    :param limit: int - count of rows to process.
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
        part_num = 0
        row_num = 0
        while True:
            part_num += 1

            log('part %s - fetch rows...   (%TIME_SPENT%)' % part_num)
            res = cursor.fetch(size)
            if not res.nrows():
                break

            log('part %s - process rows... (%TIME_SPENT%)' % part_num)
            for row in res:
                row_num += 1

                result = func(row, row_num) if func.__code__.co_argcount == 2 else func(row)

                if result is False:
                    return

                if limit and row_num >= limit:
                    log('limit reached (%s). stop.' % limit)
                    return

        log('total time spent: %TIME_SPENT%')
    return decorator
