from Module.data_process import *
from datetime import date
today=date.today()

class Time_Object():
    def __init__(self, year, data):
        self.year=year
        self.total=0
        self.max_detail1=0
        self.max_detail2=0
        self.min_detail1=0
        self.min_detail2=0

        self.detailer=''
        self.min_detailer=[0,0]
        self.max_detailer=[0,0]

        self.frame=None
        self.frame1=None

        self.value=0
        self.value1=0
        self.data=data
        self.detail=''
        self.print=['' for i in range(1,6)]
        
    def update(self):
        
        self.print[0]='The most {:s}: {:d} with {:d} new players'.format(self.detail, self.max_detail1, self.max_detail2)
        self.print[1]='The least {:s}: {:d} with {:d} new players'.format(self.detail, self.min_detail1, self.min_detail2)
        self.print[2]='Total new player in {:s}: {:d} is {:d}'.format(self.detail, int(self.value), self.value1)
        self.print[3]='The most {:s}: {:d} with {:d} new players'.format(self.detailer, self.max_detailer[0], self.max_detailer[1])
        self.print[4]='The least {:s}: {:d} with {:d} new players'.format(self.detailer, self.min_detailer[0], self.min_detailer[1])
    
    def get_statistics(self):
        self.max_detail1=self.frame[1][0]
        self.max_detail2=self.frame[1][1]

        self.min_detail1=self.frame[2][0]
        self.min_detail2=self.frame[2][1]
        self.update()

    def get_detail(self):

        self.value1=self.frame[0][int(self.value)]
        print(self.frame)
        print(self.value)
        print(self.value1)
        print(self.frame1)
        self.max_detailer=self.frame1[1]
        self.min_detailer=self.frame1[2]
        self.update()
    
    def check_value(self):
        pass
        

class Month(Time_Object):
    def __init__(self, year, data):
        super().__init__(year, data)
        self.detail='Month'
        self.detailer='Day'

    def get_statistics(self):
        """Lấy thông tin số người theo từng tháng của năm, để vẽ biểu đồ, vs lại lấy tháng nhiều nhất, ít nhất"""
        self.frame=self.data.get_statistics(1, self.year)
        super().get_statistics()
        self.check_value()
        
    def get_detail(self):
        """Nếu value !=0, tức người dùng chỉ định rõ tháng, Ghi ra tổng số người/tháng, Ngày nhiều/ít nhất/ tháng"""
        self.frame1=self.data.get_statistics(3, [self.value, self.year])
        super().get_detail()
        self.check_value()

    def check_value(self):
        if (self.year==str(today.year)):
            cur_month=today.month
            if self.max_detail1>cur_month:
                self.print[0]=''
            if self.min_detail1>cur_month:
                self.print[1]=''
            if self.max_detailer[0]>cur_month:
                self.print[3]=''
            if self.min_detailer[0]>cur_month:
                self.print[4]=''


class Quarter(Time_Object):
    def __init__(self, year, data):
        super().__init__(year, data)
        self.detail='Quarter'
        self.detailer='Month'

    def get_statistics(self):
        """Lấy thông tin số người theo từng quý của năm, để vẽ biểu đồ, vs lại lấy quí nhiều nhất, ít nhất"""
        self.frame=self.data.get_statistics(2, self.year)
        super().get_statistics()
        self.check_value()
       
    def get_detail(self):
        """Nếu value !=0, tức người dùng chỉ định rõ quí, Ghi ra tổng số người/quí đó, tháng nhiều/ít ngwuoif nhất"""
        self.frame1=self.data.get_statistics(4, [self.value,self.year])
        super().get_detail()
        self.check_value()

    def check_value(self):
        if (self.year==str(today.year)):
            cur_quarter=(today.month-1)/3+1
            if self.max_detail1>cur_quarter:
                self.print[0]=''
            if self.min_detail1>cur_quarter:
                self.print[1]=''
            if self.max_detailer[0]>cur_quarter:
                self.print[3]=''
            if self.min_detailer[0]>cur_quarter:
                self.print[4]=''

class Year():
    def __init__(self, value):
        self.value=value
        self.user=User_Data()
        self.detail=Time_Object(self.value, self.user)
        self.total=0

    def get_detail(self, type, value=None):
        if type==1:
            self.detail=Quarter(self.value, self.user)
        else:
            self.detail=Month(self.value, self.user)

        dict=self.user.get_statistics(0)
        self.total=dict[self.value]
        self.print='Total no_player in {:s}: {:d}'.format(self.value,self.total)
        self.detail.get_statistics()

        if value!=None:
            self.detail.value=value
            self.detail.get_detail()
        
    def get_graph(self):
        if self.detail.value==None or self.detail.value==0:
            return self.detail.frame[0]
        else:
            return self.detail.frame1[0]


# year=Year('2019')
# year.get_detail(1, '4')

# for i in range (5):
#     print(year.detail.print[i])

    