EVENTS_MAPPING = {
    "http": {
        "trigger_id": "httpsTrigger",
        "fields": {
            "path": "url"
        },
        "additional_fields": {}
    },
    "pubsub": {
        "trigger_id": "eventTrigger",
        "fields": {
            "topic": "resource"
        },
        "additional_fields": {
            "eventType": "providers/cloud.pubsub/eventTypes/topic.publish",
        }
    }
}