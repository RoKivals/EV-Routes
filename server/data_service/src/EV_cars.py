from bs4 import BeautifulSoup
from database.schemas import CarCreate
import requests

def parse_ev_cars() -> list:
    result = []

    for page_idx in range(0, 20):
        url_page = f"https://ev-database.org/#group=vehicle-group&rs-pr=10000_100000&rs-er=0_1000&rs-ld=0_1000&rs-ac=2_23&rs-dcfc=0_300&rs-ub=10_200&rs-tw=0_2500&rs-ef=100_350&rs-sa=-1_5&rs-w=1000_3500&rs-c=0_5000&rs-y=2010_2030&s=1&p={page_idx}-50"

        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            response = requests.get(url_page, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            cars_list = soup.find_all('div', {'class': 'list-item', 'data-jplist-item': ''})

            for idx, car in enumerate(cars_list):
                title_link = car.find('a', class_='title')
                if title_link:
                    spans = title_link.find_all('span')
                    full_name = ' '.join(span.text.strip() for span in spans)
                else:
                    print(f'Отсуствует название для {idx + 1} машины')
                
                specs = car.find('div', class_='specs')
                
                consumpting = specs.find('div', {'data-tooltip': "Efficiency under standardized conditions"}).find('span', class_='efficiency').text.strip()
                battery_capacity = specs.find('div', {'data-tooltip': "Useable battery capacity."}).find('span', class_='battery_p').text.strip()
                hidden_info = car.find('div', class_='hidden')
                type_charger = hidden_info.find('span', attrs={'title': lambda x: x and 'plug' in x}).text.strip()

                result.append(CarCreate(name=full_name, 
                                        battery_capacity=battery_capacity, 
                                        consumpting=consumpting, 
                                        type_charger=type_charger))
        except Exception as e:
                print(f"Ошибка на странице {page_idx}: {e}")
                
        print(f"Была собрана информация о {len(cars_list)} автомобилях")
        return result

if __name__ == "__main__":
    print(parse_ev_cars())