class GenConstants:
    """
    代码生成通用常量，对应Java版本中的GenConstants类
    """
    # 单表（增删改查）
    TPL_CRUD = "crud"
    # 树表（增删改查）
    TPL_TREE = "tree"
    # 主子表（增删改查）
    TPL_SUB = "sub"
    # 树编码字段
    TREE_CODE = "treeCode"
    # 树父编码字段
    TREE_PARENT_CODE = "treeParentCode"
    # 树名称字段
    TREE_NAME = "treeName"
    # 上级菜单ID字段
    PARENT_MENU_ID = "parentMenuId"
    # 上级菜单名称字段
    PARENT_MENU_NAME = "parentMenuName"
    # 数据库字符串类型
    COLUMNTYPE_STR = ["char", "varchar", "nvarchar", "varchar2"]
    # 数据库文本类型
    COLUMNTYPE_TEXT = ["tinytext", "text", "mediumtext", "longtext"]
    # 数据库时间类型
    COLUMNTYPE_TIME = ["datetime", "time", "date", "timestamp"]
    # 数据库数字类型
    COLUMNTYPE_NUMBER = ["tinyint", "smallint", "mediumint", "int", "number", "integer",
                         "bit", "bigint", "float", "double", "decimal"]
    # 页面不需要编辑字段
    COLUMNNAME_NOT_EDIT = ["id", "create_by", "create_time", "del_flag"]
    # 页面不需要显示的列表字段
    COLUMNNAME_NOT_LIST = ["id", "create_by", "create_time", "del_flag", "update_by",
                           "update_time"]
    # 页面不需要查询字段
    COLUMNNAME_NOT_QUERY = ["id", "create_by", "create_time", "del_flag", "update_by",
                            "update_time", "remark"]
    # Entity基类字段
    BASE_ENTITY = ["createBy", "createTime", "updateBy", "updateTime", "remark"]
    # Tree基类字段
    TREE_ENTITY = ["parentName", "parentId", "orderNum", "ancestors"]
    # 文本框
    HTML_INPUT = "input"
    # 文本域
    HTML_TEXTAREA = "textarea"
    # 下拉框
    HTML_SELECT = "select"
    # 单选框
    HTML_RADIO = "radio"
    # 复选框
    HTML_CHECKBOX = "checkbox"
    # 日期控件
    HTML_DATETIME = "datetime"
    # 图片上传控件
    HTML_IMAGE_UPLOAD = "imageUpload"
    # 文件上传控件
    HTML_FILE_UPLOAD = "fileUpload"
    # 富文本控件
    HTML_EDITOR = "editor"
    # 字符串类型
    TYPE_STRING = "String"
    # 整型
    TYPE_INTEGER = "Integer"
    # 长整型
    TYPE_LONG = "Long"
    # 浮点型
    TYPE_DOUBLE = "Double"
    # 高精度计算类型
    TYPE_BIGDECIMAL = "BigDecimal"
    # 时间类型
    TYPE_DATE = "Date"
    # 模糊查询
    QUERY_LIKE = "LIKE"
    # 模糊查询
    QUERY_EQ = "EQ"
    # 需要
    REQUIRE = "1"

if __name__ == "__main__":
    print(f"单表（增删改查）常量: {GenConstants.TPL_CRUD}")
    print(f"树表（增删改查）常量: {GenConstants.TPL_TREE}")
    print(f"主子表（增删改查）常量: {GenConstants.TPL_SUB}")
    print(f"树编码字段常量: {GenConstants.TREE_CODE}")
    print(f"树父编码字段常量: {GenConstants.TREE_PARENT_CODE}")
    print(f"树名称字段常量: {GenConstants.TREE_NAME}")
    print(f"上级菜单ID字段常量: {GenConstants.PARENT_MENU_ID}")
    print(f"上级菜单名称字段常量: {GenConstants.PARENT_MENU_NAME}")
    print(f"数据库字符串类型常量: {GenConstants.COLUMNTYPE_STR}")
    print(f"数据库文本类型常量: {GenConstants.COLUMNTYPE_TEXT}")
    print(f"数据库时间类型常量: {GenConstants.COLUMNTYPE_TIME}")
    print(f"数据库数字类型常量: {GenConstants.COLUMNTYPE_NUMBER}")
    print(f"页面不需要编辑字段常量: {GenConstants.COLUMNNAME_NOT_EDIT}")
    print(f"页面不需要显示的列表字段常量: {GenConstants.COLUMNNAME_NOT_LIST}")
    print(f"页面不需要查询字段常量: {GenConstants.COLUMNNAME_NOT_QUERY}")
    print(f"Entity基类字段常量: {GenConstants.BASE_ENTITY}")
    print(f"Tree基类字段常量: {GenConstants.TREE_ENTITY}")
    print(f"文本框常量: {GenConstants.HTML_INPUT}")
    print(f"文本域常量: {GenConstants.HTML_TEXTAREA}")
    print(f"下拉框常量: {GenConstants.HTML_SELECT}")
    print(f"单选框常量: {GenConstants.HTML_RADIO}")
    print(f"复选框常量: {GenConstants.HTML_CHECKBOX}")
    print(f"日期控件常量: {GenConstants.HTML_DATETIME}")
    print(f"图片上传控件常量: {GenConstants.HTML_IMAGE_UPLOAD}")
    print(f"文件上传控件常量: {GenConstants.HTML_FILE_UPLOAD}")
    print(f"富文本控件常量: {GenConstants.HTML_EDITOR}")
    print(f"字符串类型常量: {GenConstants.TYPE_STRING}")
    print(f"整型常量: {GenConstants.TYPE_INTEGER}")
    print(f"长整型常量: {GenConstants.TYPE_LONG}")
    print(f"浮点型常量: {GenConstants.TYPE_DOUBLE}")
    print(f"高精度计算类型常量: {GenConstants.TYPE_BIGDECIMAL}")
    print(f"时间类型常量: {GenConstants.TYPE_DATE}")
    print(f"模糊查询常量: {GenConstants.QUERY_LIKE}")
    print(f"相等查询常量: {GenConstants.QUERY_EQ}")
    print(f"需要常量: {GenConstants.REQUIRE}")