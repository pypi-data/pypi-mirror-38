# 颜色日志

## 使用说明

```python
from color_log import Logger

log = Logger()
log.info(msg)
log.error(msg)
```

linux系统使用 `tail -F -s5 logs/log` 实时监控日志变化