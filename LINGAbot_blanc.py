import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By

#ネットワーク読み込み待機時間
sleepTime = 1
#ChromeDriverのパスを設定
CHROMEDRIVER = "!!!ここにchromedriver.exeのパスを入力!!!"
#ChromeDriverのstartとstopを制御するServiceオブジェクトを介してパスを渡す
chrome_service = service.Service(executable_path=CHROMEDRIVER)
#Chromeを起動
driver = webdriver.Chrome(service=chrome_service)

def main():
    #ログイン
    login()
    #開始、終了する問題番号の取得
    start,end = getQuestionNumber()

    while(start <= end):
        selectCocet()
        print('現在のユニット:', str(start)+'-'+str(start+24))
        selectUnit(start)
        Answer()
        start += 25
        print("1ユニットを終了しました。")


def login():
    # リンガポルタを開く
    driver.get('https://w5.linguaporta.jp/user/seibido/index.php')
    driver.set_window_size(720, 1280)

    for i in range(0, 3):
        try:
            print('IDを入力')
            uid = input()
            print('パスワードを入力')
            uPassword = input()
            
            id = driver.find_element(By.XPATH, '//*[@id="content-login"]/form/table/tbody/tr[1]/td/input')
            password = driver.find_element(By.XPATH, '//*[@id="content-login"]/form/table/tbody/tr[2]/td/input')
            submit = driver.find_element(By.XPATH, '//*[@id="btn-login"]')

            id.clear()
            id.send_keys(uid)
            password.send_keys(uPassword)
            submit.submit()

            return
        except:
                print("ログインに失敗しました。再度入力して下さい。")
    print("失敗回数の上限に達しました。プログラムを終了します。")
    driver.quit()
    sys.exit()

def getQuestionNumber():
    while(True):
        print('開始する番号を入力して下さい。(1-25の場合は1, 126-150の場合は126)')
        start = int(input())
        if start % 25 == 1:
            break
        else:
            print("無効な番号です。入力しなおして下さい。")

    while(True):
            print('終了する番号を入力して下さい。(1-25の場合は25, 126-150の場合は150)')
            end = int(input())
            if end % 25 == 0:
                break
            else:
                print("無効な番号です。入力しなおして下さい。")
    return start,end

def selectCocet():
    try:
        for i in range(5):
            try:#解答終了時に開く
                driver.execute_script("document.Study.submit()") # 本の選択画面へ移行
                driver.execute_script("select_reference('70')") # cocet2600を選択
                return
            except:
                sleep(sleepTime)#ネットワーク待機時間
    except:
        driver.quit()
        sys.exit()

#解答ユニット選択
def selectUnit(unit_start):
    unit_start = (unit_start-1)/25
    script = "select_unit('drill', '" + str(1814 + (unit_start)*4) + "', '');"
    try:
        driver.execute_script(script)
    except:
        driver.quit()
        sys.exit()


def Answer():
    history = {}
    while(True):
        print("=================================================")

        # 問題の取得
        try:
            question = driver.find_element(By.XPATH,'//*[@id="qu02"]').text
        except:
            print("このユニットは既に完了しています。")
            break
        print("問題:", question)

        # 解答の取得
        try:
            print("解答:", history[question])
        except:
            print("解答: 未登録の問題です。")
            history[question] = "a"

        #解答の入力
        driver.find_element(By.XPATH,'//*[@id="tabindex1"]').send_keys(history[question])

        # "解答する"ボタンのクリック
        driver.find_element(By.XPATH,'//*[@id="ans_submit"]').submit()
                

        # 正解と不正解の判定
        for i in range(50):
            sleep(sleepTime)
            try:
                driver.find_element(By.XPATH,'//*[@id="true_msg"]')
                print('結果: 正解')
                break
            except:
                try:
                    driver.find_element(By.XPATH,'//*[@id="false_msg"]')
                    print("結果: 不正解")
                    # 解答を見るボタンを押す
                    driver.find_element(By.XPATH,'//*[@id="under_area"]/form[1]/input[2]').submit()
                    # 答えを登録
                    answer = driver.find_element(By.XPATH,'//*[@id="question_area"]/div[3]/input')
                    answer = answer.get_attribute("value")
                    print("answer:" + answer)
                    
                    history[question] = answer.strip(" ")
                   
                    break
                except:
                    print("correcting...")

        # 次へすすめる場合は進む、なければユニット終了
        try:
            driver.find_element(By.XPATH,'//*[@id="under_area"]/form/input[1]').submit()
            sleep(sleepTime)
        except:
            return

if __name__ == '__main__':
    main()

    print("指定されたすべてのユニットの解答を完了しました。プログラムを終了します。")
    driver.quit()  # ブラウザーを終了する。
    sys.exit()