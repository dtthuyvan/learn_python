
import sys
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from my_database import TouristSpot, TourGuide
def init_data_first_time(mycol):
   mylist = [
      {
      "name": "Ha Long Bay",
      "sub_title": "Di Sản Thiên Nhiên Thế Giới",
      "description": """Vịnh Hạ Long, nằm ở tỉnh Quảng Ninh, là một trong những kỳ quan thiên nhiên hàng đầu của Việt Nam và thế giới. Được UNESCO nhiều lần công nhận là Di sản Thiên nhiên Thế giới, vịnh nổi bật với hàng nghìn hòn đảo đá vôi và đảo phiến thạch với hình dạng đa dạng, độc đáo, nổi lên từ mặt nước xanh ngọc bích.
Hệ thống đảo đá và hang động kỳ vĩ tạo nên một bức tranh thủy mặc sống động. Các hoạt động phổ biến tại đây bao gồm du thuyền trên vịnh, chèo thuyền kayak để khám phá các hang động ẩn sâu, tắm biển tại các bãi tắm hoang sơ, và thăm các làng chài nổi để tìm hiểu về cuộc sống của người dân địa phương.""",
      "image": "https://media.istockphoto.com/id/1216347894/vi/anh/dau-go-island-halong-bay-sunset-cruise-vietnam.jpg?s=612x612&w=0&k=20&c=hMG1ATJkSMetnoFADF-1FwRgkmnhtEjQlJhgxU-e4Jg=",
      "price_tour":"$100"
      },
      {
      "name": "Sapa",
      "sub_title": "Địa điểm du lịch nổi tiếng Việt Nam",
      "description": """Sa Pa là một điểm du lịch cách trung tâm thành phố Lào Cai khoảng hơn 30 km. Nằm ở độ cao trung bình 1500 – 1800 m so với mặt nước biển, Thị Trấn Sapa luôn chìm trong làn mây bồng bềnh, tạo nên một bức tranh huyền ảo đẹp đến kỳ lạ. Nơi đây, có thứ tài nguyên vô giá đó là khí hậu quanh năm trong lành mát mẻ, với nhiệt độ trung bình 15-18°C.
Khách du lịch đến đây không chỉ để tận hưởng không khí trong lành, sự yên bình giản dị của một vùng đất phía Tây Bắc, mà Sapa còn là điểm đến để bạn chiêm ngưỡng những vẻ đẹp hoang sơ của những ruộng bậc thang, thác nước, những ngọn vúi hùng vĩ, khám phá những phong tục tập quán, nét đẹp văn hóa của các dân tộc trên núi như : H’Mong đen, Dzao đỏ, Tày, Dzáy…""",
      "image": "https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcQKpiwndn5_H4SJ2F1CB_pgT7O3wvMY0eteAFtMjTa7qmqXIc-OaPS76Wk7Fzgwqinxj02DCuhIZJW5O9417slVAbB6kMSKNQxqmo61vg",
      "price_tour":"$100"
      },
      {
      "name": "Hội An",
      "sub_title": "Di sản văn hoá thế giới",
      "description": """Hội An là một thành phố cũ thuộc tỉnh Quảng Nam cũ tại Việt Nam. Phố cổ Hội An từng là một thương cảng quốc tế sầm uất, gồm những di sản kiến trúc đã có từ hàng trăm năm trước, được UNESCO công nhận là di sản văn hóa thế giới từ năm 1999.""",
      "image": "https://i1-dulich.vnecdn.net/2022/04/14/HoiAn2-1649913055-1163-1649913061.jpg?w=0&h=0&q=100&dpr=2&fit=crop&s=17mImAUV2r5rtYvGR9p5lg",
      "price_tour":"$80"
      },
      {
      "name": "Sơn Đoòng",
      "sub_title": "Hang động tự nhiên lớn nhất thế giới",
      "description": """Sơn Đoòng là hang động lớn nhất hành tinh và cũng là hang động hùng vĩ nhất tại Việt Nam. Hang Sơn Đoòng được ông Hồ Khanh - một thợ rừng người Phong Nha, Quảng Bình phát hiện ra cửa hang vào năm 1990 và đến năm 2009 thì được nhóm thám hiểm hang động Anh-Việt (The British Vietnam Caving Expedition Team) do ông Howard Limbert dẫn đầu vào thám hiểm, khảo sát và đo vẽ. Hang Sơn Đoòng được nhóm thám hiểm cùng với tạp chí National Geographic công bố là hang động đá vôi tự nhiên lớn nhất thế giới năm 2009. Năm 2013, Hang Sơn Đoòng được tổ chức kỷ lục thế giới Guinness ghi nhận là hang động tự nhiên lớn nhất thế giới""",
      "image": "https://oxalisadventure.com/uploads/2022/12/sondoongcavebanner800__638073075744874957.jpg",
      "price_tour":"$200"
      },
      {
      "name": "Đảo Phú Quốc",
      "sub_title": "Hòn đảo lớn nhất Việt Nam",
      "description": """Phú Quốc là một đặc khu trực thuộc tỉnh An Giang, Việt Nam. Trước đây, đảo Phú Quốc cùng các đảo nhỏ lân cận và quần đảo Thổ Chu hợp lại tạo thành thành phố Phú Quốc trực thuộc tỉnh Kiên Giang ở vịnh Thái Lan, đây là thành phố đảo đầu tiên và duy nhất được thành lập của Việt Nam""",
      "image": "https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcRFkfF2exUGoU772WhhD7Y6xnJRrSXt0v32pgtAH-JT_zyZBfPfql-Ms1eIqdArr266_d2aHudDjQtAjWMFibTkEvo1FNgChTd7Z9xrIw",
      "price_tour":"$150"
      },
   ]

   x = mycol.insert_many(mylist)
   print(x.inserted_ids) # print list of the _id values of the inserted documents

def init_tour_guide(mycol):
  mylist = [
    {"name": "Tun", "id": 1},
    {"name": "Tin", "id": 2},
    {"name": "Jack", "id": 3},
    {"name": "Pepsi", "id": 4},
    {"name": "Bap", "id": 5}
  ]
  x = mycol.insert_many(mylist)

def get_database():
  load_dotenv()
  connection = os.getenv("MONGO_CONNECTION_STRING")

  if not connection:
    raise ValueError("Please setup database connection string!")

  myclient = MongoClient(connection)
  mydb = myclient["tourist"] #In MongoDB, a database is not created until it gets content!
  mycol = mydb["tourist_spot"] #In MongoDB, a collection is not created until it gets content!
  collist = mydb.list_collection_names()
  if "tourist_spot" not in collist:
    init_data_first_time(mycol)
  
  mycol2 = mydb["tour_guide"] #In MongoDB, a collection is not created until it gets content!
  collist = mydb.list_collection_names()
  if "tour_guide" not in collist:
    init_tour_guide(mycol2)

  return mydb

def get_tourist_spot(mydb):
  mycol = mydb["tourist_spot"]
  return mycol.find()

def get_tour_guid(mydb):
  mycol = mydb["tour_guide"]
  return mycol.find()

if __name__ == "__main__":
  db = get_database()
  place = get_tourist_spot(db)
  for x in place:
    print(x)
  people = get_tour_guid(db)
  for x in people:
    print(x)
