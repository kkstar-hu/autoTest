import yaml
from Base.basepage import BasePage


def read_yaml(name):
    with open(name, encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.FullLoader)
        return data


def generate_yaml(driver,name,index=1):
    """
    前提：需打开窗口后调用此函数
    name：生成的yaml名称
    功能：自动在运行处生成yaml，获取窗口所有的lable名，自动写到yaml的健值
    """
    page=BasePage(driver)
    labelelement=page.get_elements("xpath",f"(//form[starts-with(@class,'el-form')])[{index}]//label")
    label= {}
    for x in labelelement:
       label[x.text]=" "
    with open("./"+name+".yaml", "w",encoding='utf-8') as f:  # 写文件
        yaml.safe_dump(data=label, stream=f,allow_unicode=True)


def generate_yaml_gtos(driver,name,index=1):
    page=BasePage(driver)
    labelelement=page.get_elements("xpath",f"(//form[starts-with(@class,'el-form')])[{index}]//label")
    label= {}
    for x in labelelement:
       label[x.get_attribute("textContent")]=" "
    with open("./"+name+".yaml", "a",encoding='utf-8') as f:  # 写文件
        yaml.safe_dump(data=label, stream=f,allow_unicode=True)



