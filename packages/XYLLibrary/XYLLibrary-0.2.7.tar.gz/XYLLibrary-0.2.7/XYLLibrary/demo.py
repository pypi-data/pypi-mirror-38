import uiautomator2 as ut2
import selenium
def main():
    u = ut2.connect('192.168.2.4:7912')
    print(u.info)
    u.app_start('com.android.launcher3')
    u(text='私人FM').click()
    u(description='转到上一层级').click()
    u(text='每日推荐').click()
    u(description='转到上一层级').click()
    u(text='歌单').click()
    u(description='转到上一层级').click()
    u(text='排行榜').click()
    u(description='转到上一层级').click()

if __name__ == '__main__':
    main()