import os
import sys
import shutil

APP_NAME = 'henry'
STATIC = 'static'

def main():
    deploy_path = os.environ['DEPLOYMENT_ROOT']
    deploy_path = os.path.join(deploy_path, APP_NAME)
    static_path = os.environ['STATIC_ROOT']
    static_path = os.path.join(static_path, APP_NAME)

    from_dp_path = os.path.realpath(__file__)
    from_static_path = os.path.join(from_dp_path, STATIC)

    backup_dir(from_dp_path, deploy_path)
    backup_dir(from_static_path, static_path)

    return 0


def backup_dir(from_dir, to_dir, backup=True):
    if not os.path.exists(to_dir):
        print 'FIRST time deployment!!'
        print 'make sure correct configs on server is made'
    else:
        print 'no es primera vez'
        old_path = to_dir + '-old'
        if backup:
            if os.path.exists(old_path):
                shutil.rmtree(old_path)
            print 'backup at', old_path
            shutil.copytree(to_dir, old_path)
        shutil.rmtree(to_dir)

    print 'copiando desde', from_dir,'hasta', to_dir
    shutil.copytree(from_dir, to_dir)
    print 'exitoso!'

if __name__ == '__main__':
    sys.exit(main())

