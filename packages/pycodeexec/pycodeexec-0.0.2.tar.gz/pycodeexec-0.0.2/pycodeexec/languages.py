LANGUAGES = {
    "python": {
        "aliases": [

        ],
        "versions": {
            "default": {
                "image": "python",
                "tag": "alpine",
                "command": 'python -c "{}"'
            },
            "3.6": {
                "tag": "3.6-alpine"
            },
            "2": {
                "tag": "2.7-alpine"
            }
        }
    },
    "javascript": {
        "aliases": [
            "js",
            "node",
            "nodejs"
        ],
        "versions": {
            "default": {
                "image": "node",
                "tag": "alpine",
                "command": 'node -e "{}"'
            },
        }
    },
    "ruby": {
        "aliases": [
            "rb"
        ],
        "versions": {
            "default": {
                "image": "ruby",
                "tag": "alpine",
                "command": 'ruby -e "{}"'
            }
        }
    },
    "c": {
        "aliases":[],
        "versions": {
            "default":{
                "image": "frolvlad/alpine-gxx",
                "tag":"latest",
                "command":'sh -c \'echo "{}"|gcc -w -xc -o p - >/dev/null && chmod 700 p && ./p\''
            }
        }
    }
}
