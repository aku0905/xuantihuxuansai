class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/database_name'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭 SQLAlchemy 的事件系统
    SQLALCHEMY_ECHO = True  # 启用详细日志