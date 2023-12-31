from flask_app import *
from flask import request, session
import controller
import random
import copy

table_data = controller.table_data

@app.route('/<token>')
def index(token):
    table_no = controller.get_table_no_by_token(token)
    if type(table_no) == int:
        session['token'] = token
        session['table_info'] = controller.get_table(controller.get_table_no_by_token(token))

        return app.send_static_file('index.html')

### 토큰 검증
# curl -X POST -H 'Content-type:application/json' http://127.0.0.1:5000/check-token -d '{"token":"0b79fdd4-8cf8-4a5f-8506-904d1207e9fb"}'
@app.route('/check-token', methods=['POST'])
def check_token():
    output = dict()

    data = request.get_json()  
    token = data.get('token')

    table_no = controller.get_table_no_by_token(token)

    if type(table_no) == int or table_no == 'admin':
        output['result'] = "ok"
        output['table_no'] = table_no
        output['active'] = controller.get_table(table_no).get('active')
        return output
    else:
        output['result'] = "fail"
        return output


### 입력값 저장
### client ###
# curl -X POST -H 'Content-type:application/json' http://127.0.0.1:5000/set-table -d '{"token":"0b79fdd4-8cf8-4a5f-8506-904d1207e9fb", "gender":"male", "nums":3, "note":"남자 셋", "photo":false, "referrer":"이유빈"}' 

### admin ### param --> admin token, table_no / + 바꾸려는 값들
# curl -X POST -H 'Content-type:application/json' http://127.0.0.1:5000/set-table -d '{"token":"5ea91197-09ef-42e9-9bd9-d1d183b6db70", "table_no":1, "active":true}' 
@app.route('/set-table', methods=["POST"])
def set_table():
    output = dict()
    data = request.get_json()
    token = data.get('token')
    table_no = controller.get_table_no_by_token(token)

    if type(table_no) == int:
        gender = data.get('gender')
        nums = data.get('nums')
        note = data.get('note')
        photo = data.get('photo')
        referrer = data.get('referrer')
        random_code = 0
        random_code = str(random.randint(0000, 9999)).zfill(4)
        
        result = controller.set_table(table_no, nums, gender, photo, note, referrer, random_code)
            
        output['result'] = result
        return output

    if table_no == 'admin':
        result = controller.set_table_admin(data)
        output['result'] = result
        return output
                
    else:
        output['result'] = "fail"
        return output



### 전체 테이블 조회
### 플라스크를 통한 호출이 아닌 직접 호출 시 매개변수 체크 필수
# curl -X POST -H 'Content-type:application/json' http://127.0.0.1:5000/get-all -d '{"token":"0b79fdd4-8cf8-4a5f-8506-904d1207e9fb", "code":470066}'
# curl -X POST -H 'Content-type:application/json' http://127.0.0.1:5000/get-all -d '{"token":"{admin token}"}'
@app.route('/get-all', methods=['POST'])
def get_all():
    output = dict()
    data = request.get_json()
    token = data.get('token')
    code = data.get('code')

    table_no = controller.get_table_no_by_token(token)

    if type(table_no) == int and table_data[table_no-1]['code'] == code:
        exclude_code = copy.deepcopy(table_data)
        for data in exclude_code:
            del data['code']
        output['result'] = exclude_code
        return output
    elif table_no == 'admin':
        output['result'] = table_data
        output['admin_record'] = controller.admin['record']
        return output
    else:
        output['result'] = "fail"
        return output


### 테이블 정보 조회
### client ###
# curl -X POST -H 'Content-type:application/json' http://127.0.0.1:5000/get-table -d '{"token":"0b79fdd4-8cf8-4a5f-8506-904d1207e9fb", "code":470066}'

### admin ### param --> +) admin_token
# curl -X POST -H 'Content-type:application/json' http://127.0.0.1:5000/get-table -d '{"admin_token":"5ea91197-09ef-42e9-9bd9-d1d183b6db70", "token":"0b79fdd4-8cf8-4a5f-8506-904d1207e9fb"}'
@app.route('/get-table', methods=['POST'])
def get_table():
    output = dict()

    data = request.get_json()  
    token = data.get('token')
    admin_token = data.get('admin_token')
    code = data.get('code')
    
    table_info = controller.get_table(controller.get_table_no_by_token(token))

    if table_info and (controller.get_table_no_by_token(admin_token) == 'admin' \
           or table_info['active'] and table_info['code'] == code) :
            output['result'] = table_info
            return output
    elif table_info and table_info['code'] != code :
        output['result'] = "code_unmatch"
        return output

    output['result'] = "fail"
    return output



### 테이블 정보 수정
# curl -X POST -H 'Content-type:application/json' http://127.0.0.1:5000/update-info -d '{"token":"0b79fdd4-8cf8-4a5f-8506-904d1207e9fb", "code":470066,"m_count":3,"f_count":4,"note":"ccc"}'
@app.route('/update-info', methods=["POST"])
def update_info():
    output = dict()
    data = request.get_json()
    token = data.get('token')
    code = data.get('code')
    table_no = controller.get_table_no_by_token(token)

    if type(table_no) == int and table_data[table_no-1]['code'] == code:
        m_count = data.get('m_count')
        f_count = data.get('f_count')
        note = data.get('note')

        output['result'] = controller.update_info(table_no, m_count, f_count, note)        
        return output
    else:
        output['result'] = "fail"
        return output




### 하트 보내기
# curl -X POST -H 'Content-type:application/json' http://127.0.0.1:5000/send-like -d '{"token":"0b79fdd4-8cf8-4a5f-8506-904d1207e9fb", "code":470066, "received_table":2}'
@app.route('/send-like', methods=["POST"])
def send_like():
    output = dict()
    data = request.get_json()
    token = data.get('token')
    code = data.get('code')
    my_table = controller.get_table_no_by_token(token)
    received_table = data.get('received_table')

    try :
        received_table = int(received_table)
    except :
        pass

    if type(my_table) == int and table_data[my_table-1]['code'] == code:
        output['result'] = controller.send_like(my_table, received_table)
        return output
    else:
        output['result'] = "fail"
        return output





### 하트 거절
# curl -X POST -H 'Content-type:application/json' http://127.0.0.1:5000/reject -d '{"token":"0b79fdd4-8cf8-4a5f-8506-904d1207e9fb", "code":470066, "reject":2}'
@app.route('/reject', methods=["POST"])
def reject():
    output = dict()
    data = request.get_json()
    token = data.get('token')
    code = data.get('code')
    table_no = controller.get_table_no_by_token(token)
    rejected_table = data.get('received_table')

    try :
        rejected_table = int(rejected_table)
    except :
        pass

    if type(table_no) == int and table_data[table_no-1]['code'] == code:
        output['result'] = controller.reject(table_no, rejected_table)
        return output
    else:
        output['result'] = "fail"
        return output





### 직원 호출  ( 일단 시간 추가 요청, 하트 충전 요청 없음 )
# curl -X POST -H 'Content-type:application/json' http://127.0.0.1:5000/call -d '{"token":"0b79fdd4-8cf8-4a5f-8506-904d1207e9fb", "code":470066}'
# curl -X POST -H 'Content-type:application/json' http://127.0.0.1:5000/call -d '{"token":"0b79fdd4-8cf8-4a5f-8506-904d1207e9fb", "code":470066}'
@app.route('/call', methods=["POST"])
def call():
    output = dict()
    data = request.get_json()
    token = data.get('token')
    code = data.get('code')

    table_no = controller.get_table_no_by_token(token)

    if type(table_no) == int and table_data[table_no-1]['code'] == code:
        output['result'] = controller.call(table_no)
        return output
    else:
        output['result'] = "fail"
        return output

@app.route('/del-record', methods=['POST'])
def del_record() :
    output = dict()
    data = request.get_json()

    token = data.get('token')
    code = data.get('code')

    table_no = controller.get_table_no_by_token(token)

    if type(table_no) != int or table_data[table_no-1]['code'] != code :
        output['result'] = "fail"
        return output

    record_id = data.get('record_id')
    output['result'] = controller.delete_record(table_no, record_id)

    return output


@app.route('/record', methods=['GET'])
def record():
    output = dict()
    controller.write_table_data()
    print('log saved')
    output['result'] = 'ok'
    return output
