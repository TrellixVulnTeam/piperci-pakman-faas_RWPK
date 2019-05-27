import yaml
import io
import sys

# Read YAML file
def main(argv):

    with open(argv[0]) as stream:
        try:
            data_loaded = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return 1
    # print the read file
    print(data_loaded)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))