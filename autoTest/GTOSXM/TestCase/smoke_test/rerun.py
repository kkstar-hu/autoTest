import os

a = 1
for i in range(100):
    if a >=5 :
        break
    else:
        print(f'运行{a}次')
        os.system(r'python D:\ATA\autoTest\GTOSXM\TestCase\SmokeTest\run.py')
        a += i