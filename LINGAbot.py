import sys
from time import sleep
from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.common.by import By

#ネットワーク読み込み待機時間
sleepTime = 1
# chromeDriverオプション設定(エラーメッセージ削除)
options = webdriver.ChromeOptions() 
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#Chromeを起動
driver = webdriver.Chrome(options=options)


def main():   
    #ログイン
    login()
    #開始、終了する問題番号の取得
    unit,targetScore = getTargetScore()

    while(True):
        #mode:(0)単語の意味/(1)空欄補充
        for mode in range(2):
            moveUnit()
            if getScore() >= targetScore:
                return
            print("現在のユニット:", str(unit) + "-" + str(unit+24) + ("(単語の意味)" if mode ==0 else "(空欄補充)"))
            print("====================================")
            selectUnit(mode,unit)
            Answer(mode)
            print("1ユニットを終了しました。")
        unit += 25


def login():
    # リンガポルタを開く
    driver.get("https://w5.linguaporta.jp/user/seibido/index.php")
    driver.set_window_size(720, 1280)

    for i in range(0, 3):
        try:
            """
            print("IDを入力")
            uid = input()
            print("パスワードを入力")
            uPassword = input()
            """

            uid = str('i32101')
            uPassword = ('ringo120')


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

def getTargetScore():
    # 目標点数取得
    while(True):
        print("目標の点数を入力してください。(25の倍数)")
        targetScore = int(input())
        if targetScore % 25 == 0:
            break
        else:
            print("無効な番号です。入力しなおして下さい。")

    # 解答をスタートする番号の取得
    while(True):
        print("解答を開始する問題番号を入力してください(1-25の場合は1、226-250の場合は226)")
        start = int(input())
        if start % 25 == 1:
            break
        else:
            print("無効な番号です。入力しなおして下さい。")
    return start,targetScore

# ユニット選択
def moveUnit():
    try:
        for i in range(5):
            try:

                driver.execute_script("document.Study.submit()") # 本の選択画面へ移行
                
                driver.execute_script("select_reference('70')") # cocet2600を選択
                return
            except:
                sleep(sleepTime)#ネットワーク待機時間
    except:
        driver.quit()
        sys.exit()

# 点数の取得、終了の判定
def getScore():
    score = driver.find_element(By.XPATH,'//*[@id="point_table_reference"]/tbody/tr/td[1]').text
    score = score.replace("点\n（10400点満点）","")
    print("現在の総得点:" + score)
    return int(score)

#解答ユニット選択
def selectUnit(mode,unit_start):
    unit_start = (unit_start-1)/25
    script = "select_unit('drill', '" + str(1813 + mode + (unit_start)*4) + "', '');"
    try:
        driver.execute_script(script)
    except:
        driver.quit()
        sys.exit()


# Answer-単語の意味
def meaning(history,question):
            # 選択肢の取得
        answersPath = []
        answersText = []

        for i in range(5):
            answersPath.append(driver.find_element(By.XPATH, '//*[@id="answer_0_' + str(i) + '"]'))

        for i in range(5):
            answersText.append(answersPath[i].get_attribute('value'))
    
        print("選択肢: {}, {}, {}, {}, {}".format(answersText[0],answersText[1],answersText[2],answersText[3],answersText[4]))

        
        # 解答の取得
        choice = 0
        try:# 今までに出てきた問題
            for i in answersText:
                if history[question] == i:
                    break
                else:
                    choice = choice + 1
            print("解答:", choice,answersText[choice])
        except:# はじめての問題
            print("解答:未登録の問題です。")
            history[question] = "a"
            choice = 0
            
            
        # 選択肢クリック
        for i in range(50):
            try: 
                answersPath[choice].click()
                break
            except:
                print("can't click")
                sleep(sleepTime)

        # "解答する"ボタンのクリック
        driver.find_element(By.XPATH,'//*[@id="ans_submit"]').submit()

        return history


# Answer-空欄補充
def blanc(history,question):
            # 解答の取得
        try:
            print("解答:", history[question])
        except:
            print("解答: 未登録の問題です。")
            history[question] = "a"

        # 解答の入力
        driver.find_element(By.XPATH,'//*[@id="tabindex1"]').send_keys(history[question])

        # "解答する"ボタンのクリック
        driver.find_element(By.XPATH,'//*[@id="ans_submit"]').submit()
        return history

def Answer(mode):
    history = {}
    while(True):
        print("------------------------------------")
        
        # 問題の取得
        try:
            question = driver.find_element(By.XPATH,'//*[@id="qu02"]').text
        except:
            print("このユニットは既に完了しています。")
            break

        print("問題:", question)

        # 解答
        if mode == 0 :
            history = meaning(history,question)
        elif mode == 1:
            history = blanc(history,question)

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
                    # 答えの登録
                    if mode == 0:
                        answer = driver.find_element(By.XPATH,'//*[@id="drill_form"]')
                        answer = answer.text.replace("正解：","")
                        
                    elif mode == 1:
                        answer = driver.find_element(By.XPATH,'//*[@id="question_area"]/div[3]/input')
                        answer = answer.get_attribute("value").strip()
                    
                    print("answer:" + answer)
                    history[question] = answer
                   
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
    
    print("指定された点数を超えました。プログラムを終了します。")
    driver.quit()  # ブラウザーを終了する。
    sys.exit()
