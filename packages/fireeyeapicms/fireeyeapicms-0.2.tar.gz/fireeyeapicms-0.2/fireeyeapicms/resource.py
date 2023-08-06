import fireeyeapicms.client as cli
import urllib
import json
import time


class Timeout(Exception):
    def __init__(self,message):
        super(Timeout,self).__init__(message)
        self.message=message

class ResourceRequestError(Exception):
    def __init__(self,message):
        super(ResourceRequestError,self).__init__(message)
        self.message=message

class SearchError(Exception):
    def __init__(self,message):
        super(SearchError,self).__init__(message)
        self.message=message

class METHODS(object):
    GET="GET"
    POST="POST"

class Resource(object):
    def __init__(self,client):
        self.client=client
        self._method=METHODS.GET
        self.url = self.client.server+"/cms/{}"
        self.data ={}
        self.status_codes={}
        self.paged=False
        self.params={}

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self,x):
        if not hasattr(METHODS,x):
            raise RuntimeError("invalid method " + x)
        else:
            self._method=x

    def __iter__(self):
        return self

    def next(self):
        return self.request()

    def request(self):
        """override for paging"""
        response = self.client.req(self.method,self.url,self.data,self.status_codes[self.method],self.params)
        status = response.status_code
        data = json.loads(response.content)
        if response.status_code in self.status_codes[self.method]:
            status="Success"
        return {
            "data":data,
            "response":response,
            "status":status
        }


class SearchEmail(Resource):
    NO_TOTAL=-1
    NO_COUNT = -1
    def __init__(self,client):
        super(SearchEmail,self).__init__(client)
        self.status_codes = {
            "POST":[200,201],
            "GET":[200,201]
        }
        #paging columns
        self.page_count=SearchEmail.NO_COUNT
        self.page_processed=0
        self.list_key="list"
        self.total = SearchEmail.NO_TOTAL
        self.params={}
        self.total_key="total"
        self.job_status_key="job_status"
        self.offset_key="offset"

    def request(self):
        if self.paged==False:
            return super(SearchEmail,self).request()
        if self.total != SearchEmail.NO_TOTAL and (self.page_processed==self.total):
            raise StopIteration
        else:
            result = super(SearchEmail,self).request()
            if result["status"]!="Success":
                raise ResourceRequestError("Request failed: " + str(result["statis"]) + str(result["response"].content))
            #do we wait for the job to finish? check if the job_status_col variable is set to tell us to do that.
            if self.job_status_key is not None:
                if result["data"][self.job_status_key]!="completed":
                    return result
            result_json=result["data"]
            if self.total_key in result_json.keys():
                self.total=int(result_json[self.total_key])
                if self.page_processed < self.total:
                    #increment processed
                    num_rec = len(result_json[self.list_key])
                    count_rec = num_rec if num_rec < self.page_count else self.page_count
                    self.page_processed +=count_rec
                    #increment offset
                    self.params[self.offset_key]=self.page_count+1
                return result
            else:
                #no total column
                return result


    @staticmethod
    def get_default(default,param,kwargs):
        return default if param not in kwargs else kwargs[param]

    def get_search(self,kwargs):
        terms=[
               "search[sender]",
               "search[recipient]",
               "search[subject_line]",
                "search[start_date]",
                "search[end_date]",
                "search[message_tracker_id]",
                "search[chosen_label]",
               ]
        url_pre_encode={}
        for term in terms:
            if term in kwargs.keys():
                url_pre_encode[term]=kwargs[term]

        return url_pre_encode

    def _set_kwargs(self,kwargs):
        """
        :param kwargs: Dict
            num:
            sort:
            sort_by:
            offset:
            group_filter:
            applianaces:
            ---------------
            at least one of:
               "search[sender]",
               "search[recipient]",
               "search[subject_line]",
                "search[message_tracker_id]",
            ---------------
            optional:
                "search[start_date]",
                "search[end_date]",
                "search[chosen_label]",
        :return:
        """

        num=SearchEmail.get_default('25',"num",kwargs)
        sort= SearchEmail.get_default('',"sort",kwargs)
        sort_by= SearchEmail.get_default('',"sort_by",kwargs)
        offset = SearchEmail.get_default(0,"offset",kwargs)
        group_filter = SearchEmail.get_default("All","group_filter",kwargs)
        appliances= SearchEmail.get_default("All","appliances",kwargs)
        job_id = SearchEmail.get_default('',"job_id",kwargs)
        args = {}
        args["num"]=str(num)
        args["sort"]=str(sort)
        args["sort_by"]=str(sort_by)
        args["offset"]=str(offset)
        args["group_filter"]=str(group_filter)
        args["appliances"]=str(appliances)
        args["job_id"]=str(job_id)
        args["search[chosenLabel]"]="Custom"
        return args

    def _set_search(self,kwargs):
        """
        :param kwargs: Dict
            num:
            sort:
            sort_by:
            offset:
            group_filter:
            applianaces:
            ---------------
            at least one of:
               "search[sender]",
               "search[recipient]",
               "search[subject_line]",
                "search[message_tracker_id]",
            ---------------
            optional:
                "search[start_date]",
                "search[end_date]",
                "search[chosen_label]",
        :return:
        """
        args = self._set_kwargs(kwargs)
        search_params = self.get_search(kwargs)
        args.update(search_params)
        self.params=args.copy()

    def search_url(self,kwargs):
        """
        first set search url and wait for complete status
        :param kwargs: Dict
            num:
            sort:
            sort_by:
            offset:
            group_filter:
            applianaces:
            ---------------
            at least one of:
               "search[sender]",
               "search[recipient]",
               "search[subject_line]",
                "search[message_tracker_id]",
            ---------------
            optional:
                "search[start_date]",
                "search[end_date]",
                "search[chosen_label]",
        :return:
        """
        self._set_search(kwargs)

    def search_results(self,kwargs,job_id):
        self.paged=True
        """
        then set job_id and page through results if need be.
        :param kwargs: Dict
            num:
            sort:
            sort_by:
            offset:
            group_filter:
            applianaces:
            job_id
            ---------------
            at least one of:
               "search[sender]",
               "search[recipient]",
               "search[subject_line]",
                "search[message_tracker_id]",
            ---------------
            optional:
                "search[start_date]",
                "search[end_date]",
                "search[chosen_label]",
        :return:
        """
        kwargs["job_id"]=job_id
        args = self._set_kwargs(kwargs)
        params = self._set_search(args)
        self.page_count=int(args["num"])
        self.url=self.url.format(params)
        #todo(aj) do i need to handle paging?
        #if so then save kwargs as member variable for future replacement and paging.
        #override self.request, first call parent, then set count,total_done,total_records,offset member variables

class SearchProcessed(SearchEmail):
    def __init__(self,client):
        super(SearchProcessed,self).__init__(client)
        self.url = self.url.format("message_tracking/messages")


class SearchQueued(SearchEmail):
    def __init__(self,client):
        super(SearchQueued,self).__init__(client)
        self.url = self.url.format("message_queued/messages")
