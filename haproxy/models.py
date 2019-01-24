from django.db import models

class Instance(models.Model):
    name = models.CharField(max_length=255,null=False,blank=False,verbose_name="实例名称")
    ip = models.CharField(max_length=255,null=False,blank=False,verbose_name="IP地址")
    ha_version = models.CharField(max_length=255,null=False,blank=False,verbose_name="haproxy版本")
    cluster = models.CharField(max_length=255,null=False,blank=False,verbose_name="所属集群")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "haproxy实例"
        verbose_name_plural = verbose_name

class Frontend(models.Model):
    name = models.CharField(max_length=255,null=False,blank=False,verbose_name="frontend名称")
    ip = models.CharField(max_length=255,null=False,blank=False,verbose_name="监听地址")
    port = models.CharField(max_length=255,null=False,blank=False,verbose_name="端口")
    mode = models.CharField(max_length=255,null=False,blank=False,verbose_name="模式")
    monitor_uri = models.CharField(max_length=255,null=False,blank=False,verbose_name="监测地址")
    instance = models.ManyToManyField(Instance,db_constraint=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "frontend全局配置"
        verbose_name_plural = verbose_name

class Backend(models.Model):
    name = models.CharField(max_length=255,null=False,blank=False,verbose_name="backend名称")
    balance = models.CharField(max_length=255,null=True,blank=True,verbose_name="balance规则")
    instance = models.ManyToManyField(Instance,db_constraint=False)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Backend"
        verbose_name_plural = verbose_name

class UseBackend(models.Model):
    backend = models.ForeignKey(Backend,db_constraint=False)
    frontend = models.ForeignKey(Frontend,db_constraint=False,null=True)
    acl = models.CharField(max_length=255,null=True,blank=True,verbose_name="Acl规则")

    class Meta:
        verbose_name = "UseBackend"
        verbose_name_plural = verbose_name

class Option(models.Model):
    item = models.CharField(max_length=255,null=False,blank=False,verbose_name="option选项")
    param = models.CharField(max_length=255,null=True,blank=True,verbose_name="option参数")
    frontend = models.ForeignKey(Frontend,db_constraint=False,null=True)
    backend = models.ForeignKey(Backend,db_constraint=False,null=True)


    def __str__(self):
        return self.item

    class Meta:
        verbose_name = 'option'
        verbose_name_plural = verbose_name

class Server(models.Model):
    name = models.CharField(max_length=255,null=False,blank=False,verbose_name="server名称")
    ip = models.CharField(max_length=255,null=False,blank=False,verbose_name="server ip")
    port = models.CharField(max_length=255,null=False,blank=False, verbose_name="server端口")
    check_interval = models.CharField(max_length=255,null=False,blank=False,verbose_name="检测间隔")
    rise = models.CharField(max_length=255,null=False,blank=False,verbose_name="正常检测次数")
    fall = models.CharField(max_length=255,null=False,blank=False,verbose_name="失败检测次数")
    cookie = models.CharField(max_length=255,null=True,blank=True,verbose_name="Cookie值")
    weight = models.CharField(max_length=255,null=True,blank=True,verbose_name='权重')
    backend = models.ForeignKey(Backend,db_constraint=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "server信息"
        verbose_name_plural = verbose_name

class Acl(models.Model):
    name = models.CharField(max_length=255,null=False,blank=False,verbose_name="Acl名称")
    criterion = models.CharField(max_length=255,null=False,blank=False,verbose_name="acl规则")
    criterion_args = models.CharField(max_length=255,null=True,blank=True,verbose_name="acl规则参数")
    flags = models.CharField(max_length=255,null=True,blank=True,verbose_name="acl flags")
    value = models.CharField(max_length=255,null=False,blank=False,verbose_name="acl value")
    frontend = models.ForeignKey(Frontend,db_constraint=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "acl配置"
        verbose_name_plural = verbose_name



