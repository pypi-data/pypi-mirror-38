def event_to_mapper(event, mapper):
    fields = mapper["fields"]
    mapped_event = dict()
    for field in event:
        mapped_event[
            mapper[field]
        ] = event[field]
    mapped_event.update(mapper["additional_fields"])
    return mapped_event