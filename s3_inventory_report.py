from abc import ABC, abstractmethod
from typing import List,Iterator

class s3_inventory_report_base(ABC):
    """
    Common abstract class for all reports based on S3 inventory files
    abstract method 'processing' should be overloaded in inherited classes
    """

    def __init__(self, manifest_json: str, depth: int = 1):
        """
        :param manifest_json: String containing Inventory manifest json data
        :param depth: Depth of analysis
        """
        self.__depth = depth  # how many levels of prefixes should be analysed
        self.__manifest_json = manifest_json  # s3 inventory manifest json string
        self.__report = {} # dictionary in format key:prefix - value:aggregated metric

    def add_data(self,data:List[List]):
        """
        processing portion of inventory data
        :param data: List of List contains inventory data
        :return: None
        """
        pass

    def list_of_inventory_files(self)->Iterator[str]:
        """
        :return: Iterator[str] - new file
        """
        pass

    def reset_report(self):
        """
        Remove all results of data aggregation
        :return: None
        """
        self.__report = {}

    @abstractmethod
    def processing(self, data_raw:List)->bool:
        """
        Should contain code of processing of one line of inventory data
        Should story results of processing in self.__report dictionary
        :param data_raw:
        :return: bool . True on Success and False otherwise
        """

        pass

    @abstractmethod
    def publish(self,**kwargs):
        """
        Create any kind of report based on currently aggregated data self.__report
        """
        pass