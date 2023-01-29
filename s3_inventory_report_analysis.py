import argparse
import os
import json
import logging

from aws_credentials import AwsCredentials
from s3_inventory_report import s3_inventory_report_base
class s3_inventory_report_size(s3_inventory_report_base):

    def processing(self, data_raw):
        pass

    def publish(self,**kwargs):
        pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='[%(levelname)s] %(asctime)s |%(name)s| %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger('S3 inventory analyser')
    parser = argparse.ArgumentParser(description="S3 inventory analyser and report generator",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-m", help="Path to manifest file (can be local or s3:// path )", type=str, required=True)
    parser.add_argument("--d", help="Depth of analysis", type=int, default=1)
    parser.add_argument("--key", help="aws access key id ", type=str, default="")
    parser.add_argument("--secret", help="aws access secret key ", type=str, default="")
    parser.add_argument("--credentials_from_env_variables", help="Try use credentials from env variables ",
                        default=False, action='store_true')
    parser.add_argument("--log_level", help='Logging level',choices=['debug', 'info', 'error'])
    args = parser.parse_args()
    logger.setLevel(str.upper(args.log_level))
    logger.info(f"Start. Inventory manifest:{args.m}. Depth of analysis:{args.d} ")
    ac = AwsCredentials(aws_key=args.key,aws_secret=args.secret)
    manifest_json_str = ""
    if args.m.startswith('s3://'):
        pass # download manifest from s3
    else:
        if not os.path.exists(args.m):
            logger.error(f" Can't find manifest file by the following local path: {args.m}")
            exit(-1)
        with open(args.m, 'r') as mfid:
            manifest_json_str = mfid.read()
    try:
        json.loads(manifest_json_str)
    except ValueError as err:
        logger.error(f" Incorrect json: {args.m}. Error: {str(err)}")
        exit(-1)

    report = s3_inventory_report_size(manifest_json=manifest_json_str,depth=args.d)
    #download inventory manifest
