import os
import sys
import shutil

APP_NAME = 'henry'

def main():
    deploy_path = os.environ['DEPLOYMENT_ROOT']
    deploy_path = os.path.join(deploy_path, APP_NAME)

    if not os.path.exists(deploy_path):
        print 'FIRST time deployment!!'
        print 'make sure correct configs on server is made'
    else:
        print 'no es primera vez'
        old_path = deploy_path + '-old'
        if os.path.exists(old_path):
            shutil.rmtree(old_path)
        print 'backup at', old_path
        shutil.copytree(deploy_path, old_path)
        shutil.rmtree(deploy_path)
    current_path = os.path.realpath(__file__)
    print 'copiando desde', current_path,'hasta', deploy_path
    shutil.copytree(os.path.dirname(current_path), deploy_path)
    return 0


if __name__ == '__main__':
    sys.exit(main())

