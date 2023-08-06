# 颜色日志

## 使用说明

```python
from py_smtp.smtp_send import send

send('smtp服务器:端口', ['测试员', 'wujh@ebfcn.com.cn'], '密码', ['收件人1','收件人2'], ['抄送人1','抄送人2'], '标题', '内容', ['附件1','附件2'])
```

linux系统使用 `tail -F -s5 logs/log` 实时监控日志变化