import datetime


def get_current_datetime_str() -> str:
    now = \
        datetime.datetime.now(
            tz = datetime.timezone(
                offset = datetime.timedelta(
                    hours = 0
                )
            )
        )
    ye = now.year
    mo = now.month
    da = now.day
    ho = now.hour
    mi = now.minute
    se = now.second
    mo = f'0{mo}'[-2:]
    da = f'0{da}'[-2:]
    ho = f'0{ho}'[-2:]
    mi = f'0{mi}'[-2:]
    se = f'0{se}'[-2:]

    current_datetime_str = f'{ye}-{mo}-{da}T{ho}:{mi}:{se}+00:00'

    return current_datetime_str





