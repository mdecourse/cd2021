from src.env import VrepEnvironment
import settings, argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test',      action='store_true', help='Test in an environment with moving objects')
    args = parser.parse_args()  

    if args.test:
        environment = VrepEnvironment(settings.SCENES + '/room_dynamic.ttt')
    else:
        environment = VrepEnvironment(settings.SCENES + '/room_static.ttt')
    environment.start_vrep()