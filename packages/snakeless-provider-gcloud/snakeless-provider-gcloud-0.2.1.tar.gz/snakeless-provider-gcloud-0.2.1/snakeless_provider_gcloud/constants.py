EVENTS_MAPPING = {
    "http": {
        "id": "httpsTrigger",
        "fields": {
            "path": "url"
        },
        "additional_fields": {}
    },
    "pubsub": {
        "id": "eventTrigger",
        "fields": {
            "topic": "resource"
        },
        "additional_fields": {
            "eventType": "providers/cloud.pubsub/eventTypes/topic.publish",
        }
    }
}