from schema import And, Use, Optional


SUPPORTED_RUNTIMES = ["python37"]
SUPPORTED_MEMORY_SIZES = [128, 256, 512, 1024, 2048]

GCLOUD_SCHEMA = {
    "project": {
        "creds": str,
        "runtime": And(
            Use(str),
            lambda runtime: runtime in SUPPORTED_RUNTIMES,
            error="Unsupported runtime",
        ),
        "region": str,
        Optional("api_prefix"): str,
        Optional("memory_size", default=128): And(
            Use(int),
            lambda memory_size: memory_size in SUPPORTED_MEMORY_SIZES,
            error="Invalid memory size",
        ),
        Optional("timeout", default=60): And(
            Use(int), lambda timeout: timeout > 0
        ),
        # Optional("deployment_bucket"): str,
        Optional("env_file_path", default=".env"): str,
    },
    # Optional("package"): {
    #     Optional("include"): [str],
    #     Optional("exclude"): [str],
    #     Optional("exclude_dev_dependencies", default=True): bool,
    #     Optional("individually", default=False): bool,
    # },
    "functions": {
        str: {
            "handler": str,
            "handler_path": str,
            "events": [
                {
                    Optional("http"): {
                        "path": str
                    }
                },
                {
                    Optional("pubsub"): {
                        "topic": str
                    }
                }
            ],
            Optional("name"): str,
            Optional("description"): str,
            Optional("memory_size", default=128): And(
                Use(int),
                lambda memory_size: memory_size in SUPPORTED_MEMORY_SIZES,
                error="Invalid memory size",
            ),
            Optional("runtime"): And(
                Use(str),
                lambda runtime: runtime in SUPPORTED_RUNTIMES,
                error="Unsupported runtime",
            ),
            Optional("timeout", default=60): And(
                Use(int), lambda timeout: timeout > 0
            ),
            Optional("env_file_path", default=""): str,
            Optional("merge_env", default=False): bool,
            Optional("tags"): {str: str},
            # Optional("package"): {
            #     Optional("include"): [str],
            #     Optional("exclude"): [str],
            #     Optional("individually", default=False): bool,
            # },
        }
    },
}
