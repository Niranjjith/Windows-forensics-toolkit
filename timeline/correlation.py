from collections import defaultdict


def group_events_by_date(events):

    grouped = defaultdict(list)

    for event in events:

        date_key = (
            event["timestamp"]
            .date()
        )

        grouped[date_key].append(
            event
        )

    return dict(grouped)