# -*- coding: utf-8 -*-
# 语言
LANGUAGE = 'chinese'

# log 日志信息记录等级: debug<info<warn<error<critical
LOG_LEVEL = 'info'

# 允许系统警告在控制台输出: True/False
ALLOW_CONSOLE_SYSTEM_WARN = True

# 是否进行参数检查
ALLOW_ARG_CHECK = True

# 显示精度控制(小数点个数)
PRECISION_LEVEL = 3


# 日志设置
LOGGER_CONFIG = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "%(asctime)s FuctionName::%(funcName)s - %(lineno)s - %(name)s :: %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console_handler": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        "sys_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "maxBytes": 10485760,
            "backupCount": 10
        },
        "usr_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "maxBytes": 5242880,
            "backupCount": 10
        }
    },
    "loggers": {
        "atrader": {
            "level": "DEBUG",
            "handlers": [
                "sys_handler"
            ],
            "propagate": 0
        },
        "userlog": {
            "level": "DEBUG",
            "handlers": [
                "usr_handler"
            ],
            "propagate": 0
        }
    }
}
