import fireeyeapicms.client as cli
import fireeyeapicms.resource as res
import time
import datetime

class MissingArg(Exception):
    def __init__(self,message):
        super(MissingArg,self).__init__(message)
        self.message=message

class SearchUtil(object):
    DATE_FORMAT="%m/%d/%Y"
    def __init__(self,
                 client,
                 subject=None,
                 start_date=None,
                 end_date=None,
                 sender_address=None,
                 num=25
                 ):
        """
        :param subject: str
        :param start_date: mm/dd/yyyy
        :param end_date: mm/dd/yyyy
        :param sender_address: str
        :param num:  int
        :param client : fireeyeapi.client
        """
        self.client=client
        if not subject and not sender_address:
            raise MissingArg("need a subject or a sender")
        start_date=self._check_date(start_date)
        end_date = self._check_date(end_date)

        self.kwargs={}
        self.set_kwargs(subject,"search[subject_line]")
        self.set_kwargs(start_date,"search[start_date]")
        self.set_kwargs(end_date,"search[end_date]")
        self.set_kwargs(sender_address,"search[sender]")
        self.set_kwargs(num,"num")
        pass

    def set_kwargs(self,var,name):
        """
        :param var: value
        :param name: str
        :return:
        """
        if var is not None:
            self.kwargs[name]=var

    def search(self,total_time=15,wait_inc=1):
        """
        :param total_time: int; total seconds wait time
        :param wait_inc: int; seconds to wait per iteration
        :return:
        """
        resource = res.SearchProcessed(self.client)
        resource.search_url(self.kwargs)
        all_data=[]
        result = resource.request()
        result_json = result["data"]
        if result_json["job_status"]!="progress":
            raise RuntimeError("error:" + result["response"].status_code)
        result_resource = res.SearchProcessed(self.client)
        total_wait_accumulated=0
        result_resource.search_results(self.kwargs,result_json["job_id"])
        for result in result_resource:
            if total_wait_accumulated >=total_time:
                raise RuntimeError("waited max time")
            if result["status"]=="Success":
                if result["data"]["job_status"]=="completed":
                    all_data.extend(result["data"]["list"])
                else:
                    time.sleep(wait_inc)
                    total_wait_accumulated+=wait_inc
            else:
                raise RuntimeError("error: " + result["response"].status_code)
        return all_data

    def _check_date(self,date):
        if date is None:
            cur = datetime.datetime.now()
            start_date=cur.strftime(SearchUtil.DATE_FORMAT)
        else:
            try:
                datetime.datetime.strptime(date,SearchUtil.DATE_FORMAT)
            except ValueError as e:
                raise e
        return date
