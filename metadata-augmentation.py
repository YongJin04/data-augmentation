import json
import time
import csv

def read_metadata_from_csv(file_path):
    metadata_list = []
    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row = {key.lower(): value for key, value in row.items()}
            metadata = {
                'folder_name': row['folder_name'],
                'sender_email': row['sender_email'],
                'sender_name': row['sender_name'],
                'receiver_emails': row['receiver_emails'],
                'cc_emails': row['cc_emails'],
                'bcc_emails': row['bcc_emails'],
                'delivery_time_unixtime': row['delivery_time_unixtime'],
                'subject': row['subject'],
                'attachments': row['attachments']
            }
            metadata_list.append(metadata)
    return metadata_list

def create_dataset(metadata):
    datasets = []

    folder_name_dict = {
        "해당 메일의 메일함을 알려줘": f"해당 메일은 '{metadata['folder_name']}'함에 있습니다.",
        "이 메일이 어느 폴더에 있는지 알려주세요.": f"이 메일은 '{metadata['folder_name']}' 폴더에 있습니다.",
        "메일이 저장된 폴더 이름을 알고 싶어요.": f"메일이 저장된 폴더는 '{metadata['folder_name']}'입니다.",
        "메일 폴더의 이름을 확인해줄 수 있나요?": f"메일 폴더의 이름은 '{metadata['folder_name']}'입니다.",
        "이 메일의 저장 폴더를 알려줘.": f"이 메일의 저장 폴더는 '{metadata['folder_name']}'입니다.",
        "메일이 위치한 폴더를 알려줄래?": f"메일이 위치한 폴더는 '{metadata['folder_name']}'입니다.",
        "메일이 어떤 폴더에 있는지 알려주세요.": f"메일은 '{metadata['folder_name']}' 폴더에 있습니다.",
        "이 메일이 속한 폴더의 이름을 알려줘.": f"이 메일이 속한 폴더의 이름은 '{metadata['folder_name']}'입니다.",
        "메일 폴더명을 알려주세요.": f"메일 폴더명은 '{metadata['folder_name']}'입니다.",
        "이 메일이 어느 폴더에 속해있는지 확인해줄 수 있어?": f"이 메일은 '{metadata['folder_name']}' 폴더에 속해 있습니다."
    }

    for instruction, output in folder_name_dict.items():
        datasets.append({
            "context": "",
            "instruction": instruction,
            "output": output,
            "label": "메일함",
            "metadata": [metadata]
        })
    
    sender_receiver_dict = {
        "해당 메일의 송수신자 이메일을 알려줘": f"해당 메일의 송신자 이메일은 '{metadata['sender_email']}'이고, 수신자 이메일은 '{metadata['receiver_emails']}'입니다.",
        "이 메일에서 송수신자의 이메일 주소를 찾아줄 수 있나요?": f"이 메일의 송신자는 '{metadata['sender_email']}'이며, 수신자는 '{metadata['receiver_emails']}'입니다.",
        "이 이메일의 송수신 정보를 제공해줄래?": f"이 이메일의 송신자는 '{metadata['sender_email']}'입니다. 수신자들은 '{metadata['receiver_emails']}'입니다.",
        "메일의 발신자와 수신자 이메일을 알고 싶어요.": f"메일의 발신자 이메일은 '{metadata['sender_email']}'이고, 수신자 이메일은 '{metadata['receiver_emails']}'입니다.",
        "이 이메일의 발신자와 수신자를 확인해주세요.": f"이 이메일의 발신자는 '{metadata['sender_email']}'이며, 수신자는 '{metadata['receiver_emails']}'입니다.",
        "메일 송수신자 이메일을 알려주세요.": f"메일 송신자 이메일은 '{metadata['sender_email']}'이고, 수신자 이메일은 '{metadata['receiver_emails']}'입니다.",
        "이 메일의 송수신자 정보를 나에게 제공해 줄 수 있나요?": f"송신자 이메일은 '{metadata['sender_email']}'이고, 수신자 이메일은 '{metadata['receiver_emails']}'입니다.",
        "메일의 송신자와 수신자 이메일 주소를 알려줘.": f"메일의 송신자 이메일은 '{metadata['sender_email']}'이며, 수신자 이메일은 '{metadata['receiver_emails']}'입니다.",
        "이 이메일의 송수신자 이메일 정보를 제공해줘.": f"송신자의 이메일은 '{metadata['sender_email']}'이고, 수신자의 이메일은 '{metadata['receiver_emails']}'입니다.",
        "메일 송수신 이메일 주소를 확인해줄 수 있어?": f"이 메일의 송신자 이메일은 '{metadata['sender_email']}'이고, 수신자 이메일은 '{metadata['receiver_emails']}'입니다."
    }

    for instruction, output in sender_receiver_dict.items():
        datasets.append({
            "context": "",
            "instruction": instruction,
            "output": output,
            "label": "송수신",
            "metadata": [metadata]
        })
    
    sender_dict = {
        "해당 메일의 송신자 이메일을 알려줘": f"해당 메일의 송신자 이메일은 '{metadata['sender_email']}'입니다.",
        "이 메일에서 발신자의 이메일 주소를 알려줘.": f"이 메일의 발신자 이메일은 '{metadata['sender_email']}'입니다.",
        "이 이메일의 발신자를 알려주세요.": f"이 이메일의 발신자는 '{metadata['sender_email']}'입니다.",
        "메일의 송신자 이메일을 알려줄 수 있나요?": f"메일의 송신자 이메일은 '{metadata['sender_email']}'입니다.",
        "이 메일의 송신자 이메일 정보를 제공해줘.": f"송신자 이메일은 '{metadata['sender_email']}'입니다.",
        "메일의 발신자 이메일을 알고 싶어요.": f"메일의 발신자 이메일은 '{metadata['sender_email']}'입니다.",
        "이 메일의 송신자를 확인해주세요.": f"이 메일의 송신자는 '{metadata['sender_email']}'입니다.",
        "이 이메일의 발신자 이메일을 알려줘.": f"이 이메일의 발신자 이메일은 '{metadata['sender_email']}'입니다.",
        "메일의 발신자 정보를 제공해주세요.": f"메일의 발신자는 '{metadata['sender_email']}'입니다.",
        "메일 송신자 이메일을 알려주세요.": f"메일 송신자 이메일은 '{metadata['sender_email']}'입니다."
    }

    for instruction, output in sender_dict.items():
        datasets.append({
            "context": "",
            "instruction": instruction,
            "output": output,
            "label": "송수신",
            "metadata": [metadata]
        })
    
    sender_name_dict = {
        "해당 메일의 송신자 이름을 알려줘": f"해당 메일의 송신자 이름은 '{metadata['sender_name']}'입니다.",
        "이 메일의 발신자 이름을 알려주세요.": f"이 메일의 발신자 이름은 '{metadata['sender_name']}'입니다.",
        "메일의 송신자 이름을 알고 싶어요.": f"메일의 송신자 이름은 '{metadata['sender_name']}'입니다.",
        "송신자의 이름을 알려줄 수 있나요?": f"송신자의 이름은 '{metadata['sender_name']}'입니다.",
        "이 메일에서 발신자의 이름을 확인해줘.": f"이 메일의 발신자는 '{metadata['sender_name']}'입니다.",
        "메일의 발신자 이름을 제공해줄래?": f"메일의 발신자 이름은 '{metadata['sender_name']}'입니다.",
        "이 메일의 송신자를 확인해주세요.": f"이 메일의 송신자는 '{metadata['sender_name']}'입니다.",
        "메일에서 발신자의 이름을 알려줘.": f"메일에서 발신자의 이름은 '{metadata['sender_name']}'입니다.",
        "메일 송신자의 이름을 알려주세요.": f"메일 송신자의 이름은 '{metadata['sender_name']}'입니다.",
        "이 이메일의 발신자 이름을 알려줄 수 있어?": f"이 이메일의 발신자 이름은 '{metadata['sender_name']}'입니다."
    }

    for instruction, output in sender_name_dict.items():
        datasets.append({
            "context": "",
            "instruction": instruction,
            "output": output,
            "label": "송수신",
            "metadata": [metadata]
        })
    
    receiver_dict = {
        "해당 메일의 수신자 이메일을 알려줘": f"해당 메일의 수신자 이메일은 '{metadata['receiver_emails']}'입니다.",
        "이 메일의 수신자 이메일 주소를 알려줘.": f"이 메일의 수신자 이메일은 '{metadata['receiver_emails']}'입니다.",
        "메일의 수신자 이메일을 알고 싶어요.": f"메일의 수신자 이메일은 '{metadata['receiver_emails']}'입니다.",
        "수신자의 이메일 주소를 알려주세요.": f"수신자의 이메일은 '{metadata['receiver_emails']}'입니다.",
        "이 이메일의 수신자를 알려줄 수 있나요?": f"이 이메일의 수신자는 '{metadata['receiver_emails']}'입니다.",
        "메일의 수신자 정보를 제공해줄래?": f"메일의 수신자 이메일은 '{metadata['receiver_emails']}'입니다.",
        "이 메일에서 수신자 이메일을 찾아줄 수 있어?": f"이 메일의 수신자 이메일은 '{metadata['receiver_emails']}'입니다.",
        "수신자 이메일을 확인해줄 수 있나요?": f"수신자 이메일은 '{metadata['receiver_emails']}'입니다.",
        "메일에서 수신자 이메일을 알려주세요.": f"메일에서 수신자 이메일은 '{metadata['receiver_emails']}'입니다.",
        "이 메일의 수신자 이메일 정보를 제공해줘.": f"이 메일의 수신자 이메일은 '{metadata['receiver_emails']}'입니다."
    }

    for instruction, output in receiver_dict.items():
        datasets.append({
            "context": "",
            "instruction": instruction,
            "output": output,
            "label": "송수신",
            "metadata": [metadata]
        })
    
    cc_emails_dict = {
        "해당 메일의 참조자를 알려줘": f"해당 메일의 참조자는 존재하지 않습니다." if metadata['cc_emails'] == "" else f"해당 메일의 참조자는 '{metadata['cc_emails']}'입니다.",
        "이 메일의 참조자 목록을 알려주세요.": f"참조자 목록이 없습니다." if metadata['cc_emails'] == "" else f"참조자는 '{metadata['cc_emails']}'입니다.",
        "메일의 참조자를 알고 싶어요.": f"참조자가 없습니다." if metadata['cc_emails'] == "" else f"메일의 참조자는 '{metadata['cc_emails']}'입니다.",
        "참조된 이메일 주소를 알려줄 수 있나요?": f"참조된 이메일 주소가 없습니다." if metadata['cc_emails'] == "" else f"참조된 이메일 주소는 '{metadata['cc_emails']}'입니다.",
        "이 메일에서 참조자를 확인해주세요.": f"이 메일에는 참조자가 없습니다." if metadata['cc_emails'] == "" else f"이 메일의 참조자는 '{metadata['cc_emails']}'입니다.",
        "메일에서 참조된 사람들을 알려줘.": f"참조된 사람들이 없습니다." if metadata['cc_emails'] == "" else f"참조된 사람들은 '{metadata['cc_emails']}'입니다.",
        "참조자 목록을 제공해줄래?": f"참조자 목록이 존재하지 않습니다." if metadata['cc_emails'] == "" else f"참조자 목록은 '{metadata['cc_emails']}'입니다.",
        "메일의 참조자 이메일을 알려주세요.": f"참조자 이메일이 없습니다." if metadata['cc_emails'] == "" else f"참조자 이메일은 '{metadata['cc_emails']}'입니다.",
        "이 메일의 참조자 목록을 확인해줄 수 있어?": f"참조자가 없습니다." if metadata['cc_emails'] == "" else f"참조자는 '{metadata['cc_emails']}'입니다.",
        "메일에서 참조자의 정보를 제공해줘.": f"참조자 정보가 없습니다." if metadata['cc_emails'] == "" else f"참조자 정보는 '{metadata['cc_emails']}'입니다."
    }

    for instruction, output in cc_emails_dict.items():
        datasets.append({
            "context": "",
            "instruction": instruction,
            "output": output,
            "label": "참조자",
            "metadata": [metadata]
        })
    
    bcc_emails_dict = {
        "해당 메일의 숨은 참조자를 알려줘": f"해당 메일의 숨은 참조자는 존재하지 않습니다." if metadata['bcc_emails'] == "" else f"해당 메일의 숨은 참조자는 '{metadata['bcc_emails']}'입니다.",
        "이 메일의 숨은 참조자 목록을 알려주세요.": f"숨은 참조자가 없습니다." if metadata['bcc_emails'] == "" else f"숨은 참조자는 '{metadata['bcc_emails']}'입니다.",
        "메일에서 숨은 참조자를 알고 싶어요.": f"숨은 참조자가 존재하지 않습니다." if metadata['bcc_emails'] == "" else f"메일의 숨은 참조자는 '{metadata['bcc_emails']}'입니다.",
        "숨은 참조된 이메일 주소를 알려줄 수 있나요?": f"숨은 참조된 이메일 주소가 없습니다." if metadata['bcc_emails'] == "" else f"숨은 참조된 이메일 주소는 '{metadata['bcc_emails']}'입니다.",
        "이 메일에서 숨은 참조자를 확인해주세요.": f"이 메일에는 숨은 참조자가 없습니다." if metadata['bcc_emails'] == "" else f"이 메일의 숨은 참조자는 '{metadata['bcc_emails']}'입니다.",
        "메일에서 숨은 참조된 사람들을 알려줘.": f"숨은 참조된 사람들이 없습니다." if metadata['bcc_emails'] == "" else f"숨은 참조된 사람들은 '{metadata['bcc_emails']}'입니다.",
        "숨은 참조자 목록을 제공해줄래?": f"숨은 참조자 목록이 존재하지 않습니다." if metadata['bcc_emails'] == "" else f"숨은 참조자 목록은 '{metadata['bcc_emails']}'입니다.",
        "메일의 숨은 참조자 이메일을 알려주세요.": f"숨은 참조자 이메일이 없습니다." if metadata['bcc_emails'] == "" else f"숨은 참조자 이메일은 '{metadata['bcc_emails']}'입니다.",
        "이 메일의 숨은 참조자 목록을 확인해줄 수 있어?": f"숨은 참조자가 없습니다." if metadata['bcc_emails'] == "" else f"숨은 참조자는 '{metadata['bcc_emails']}'입니다.",
        "메일에서 숨은 참조자의 정보를 제공해줘.": f"숨은 참조자 정보가 없습니다." if metadata['bcc_emails'] == "" else f"숨은 참조자 정보는 '{metadata['bcc_emails']}'입니다."
    }

    for instruction, output in bcc_emails_dict.items():
        datasets.append({
            "context": "",
            "instruction": instruction,
            "output": output,
            "label": "참조자",
            "metadata": [metadata]
        })

    delivery_time_dict = {
        "해당 메일의 전송 시간을 알려줘": f"해당 메일의 전송 시간은 '{format_unix_time(metadata['delivery_time_unixtime'])}'입니다.",
        "이 메일의 발송 시간을 알려주세요.": f"이 메일의 발송 시간은 '{format_unix_time(metadata['delivery_time_unixtime'])}'입니다.",
        "메일이 언제 전송되었는지 알고 싶어요.": f"메일의 전송 시간은 '{format_unix_time(metadata['delivery_time_unixtime'])}'입니다.",
        "메일의 전송 시간을 확인해줄 수 있나요?": f"메일의 전송 시간은 '{format_unix_time(metadata['delivery_time_unixtime'])}'입니다.",
        "이 메일이 전송된 시간을 알려줘.": f"이 메일이 전송된 시간은 '{format_unix_time(metadata['delivery_time_unixtime'])}'입니다.",
        "메일 전송 시간을 제공해줄래?": f"메일 전송 시간은 '{format_unix_time(metadata['delivery_time_unixtime'])}'입니다.",
        "메일이 언제 발송되었는지 알려주세요.": f"메일이 발송된 시간은 '{format_unix_time(metadata['delivery_time_unixtime'])}'입니다.",
        "이 메일의 전송된 시각을 알려줘.": f"이 메일의 전송된 시각은 '{format_unix_time(metadata['delivery_time_unixtime'])}'입니다.",
        "메일 발송 시간을 알려주세요.": f"메일 발송 시간은 '{format_unix_time(metadata['delivery_time_unixtime'])}'입니다.",
        "이 메일의 전송 시간 정보를 제공해줘.": f"이 메일의 전송 시간 정보는 '{format_unix_time(metadata['delivery_time_unixtime'])}'입니다."
    }

    for instruction, output in delivery_time_dict.items():
        datasets.append({
            "context": "",
            "instruction": instruction,
            "output": output,
            "label": "전송 시간",
            "metadata": [metadata]
        })
    
    subject_dict = {
        "해당 메일의 제목을 알려줘": f"해당 메일의 제목은 존재하지 않습니다." if metadata['subject'] == "" else f"해당 메일의 제목은 '{metadata['subject']}'입니다.",
        "이 메일의 제목을 알려주세요.": f"제목이 없습니다." if metadata['subject'] == "" else f"이 메일의 제목은 '{metadata['subject']}'입니다.",
        "메일의 제목을 알고 싶어요.": f"메일 제목이 존재하지 않습니다." if metadata['subject'] == "" else f"메일의 제목은 '{metadata['subject']}'입니다.",
        "메일 제목을 확인해줄 수 있나요?": f"제목이 없습니다." if metadata['subject'] == "" else f"메일 제목은 '{metadata['subject']}'입니다.",
        "이 메일의 제목을 확인해줘.": f"이 메일에는 제목이 없습니다." if metadata['subject'] == "" else f"이 메일의 제목은 '{metadata['subject']}'입니다.",
        "메일 제목을 알려줄래?": f"메일 제목이 없습니다." if metadata['subject'] == "" else f"메일 제목은 '{metadata['subject']}'입니다.",
        "메일의 제목을 제공해주세요.": f"제목이 없습니다." if metadata['subject'] == "" else f"메일의 제목은 '{metadata['subject']}'입니다.",
        "이 메일 제목을 알려줘.": f"이 메일은 제목이 없습니다." if metadata['subject'] == "" else f"이 메일의 제목은 '{metadata['subject']}'입니다.",
        "메일의 주제를 알려주세요.": f"주제가 없습니다." if metadata['subject'] == "" else f"메일의 주제는 '{metadata['subject']}'입니다.",
        "이 메일에 제목이 무엇인지 확인해줄 수 있어?": f"이 메일에는 제목이 없습니다." if metadata['subject'] == "" else f"이 메일의 제목은 '{metadata['subject']}'입니다."
    }

    for instruction, output in subject_dict.items():
        datasets.append({
            "context": "",
            "instruction": instruction,
            "output": output,
            "label": "제목",
            "metadata": [metadata]
        })

    attachment_dict = {
        "해당 메일의 첨부 파일 이름을 알려줘": f"해당 메일의 첨부 파일은 존재하지 않습니다." if metadata['attachments'] == "" else f"해당 메일의 첨부 파일은 '{metadata['attachments']}'입니다.",
        "이 메일의 첨부 파일을 알려주세요.": f"첨부 파일이 없습니다." if metadata['attachments'] == "" else f"이 메일의 첨부 파일은 '{metadata['attachments']}'입니다.",
        "메일에 첨부된 파일 이름을 알고 싶어요.": f"첨부 파일이 존재하지 않습니다." if metadata['attachments'] == "" else f"메일에 첨부된 파일 이름은 '{metadata['attachments']}'입니다.",
        "메일의 첨부 파일 명을 확인해줄 수 있나요?": f"첨부 파일이 없습니다." if metadata['attachments'] == "" else f"메일의 첨부 파일 명은 '{metadata['attachments']}'입니다.",
        "이 메일에서 첨부 파일을 찾아줘.": f"이 메일에는 첨부 파일이 없습니다." if metadata['attachments'] == "" else f"이 메일의 첨부 파일은 '{metadata['attachments']}'입니다.",
        "메일에 포함된 첨부 파일을 알려줘.": f"첨부 파일이 없습니다." if metadata['attachments'] == "" else f"메일에 포함된 첨부 파일은 '{metadata['attachments']}'입니다.",
        "메일에서 첨부 파일의 이름을 제공해주세요.": f"첨부 파일이 없습니다." if metadata['attachments'] == "" else f"메일에서 첨부 파일의 이름은 '{metadata['attachments']}'입니다.",
        "이 메일에 포함된 첨부 파일 목록을 알려줘.": f"첨부 파일이 없습니다." if metadata['attachments'] == "" else f"이 메일에 포함된 첨부 파일 목록은 '{metadata['attachments']}'입니다.",
        "메일 첨부 파일의 이름을 알려주세요.": f"첨부 파일이 존재하지 않습니다." if metadata['attachments'] == "" else f"메일 첨부 파일의 이름은 '{metadata['attachments']}'입니다.",
        "이 메일에 있는 첨부 파일 이름을 확인해줄 수 있어?": f"이 메일에는 첨부 파일이 없습니다." if metadata['attachments'] == "" else f"이 메일에 있는 첨부 파일 이름은 '{metadata['attachments']}'입니다."
    }

    for instruction, output in attachment_dict.items():
        datasets.append({
            "context": "",
            "instruction": instruction,
            "output": output,
            "label": "첨부 파일",
            "metadata": [metadata]
        })

    return datasets

def convert_and_save_to_jsonl(datasets, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for data in datasets:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')

def format_unix_time(unix_time):
    weekday_dict = {
        'Monday': '월요일',
        'Tuesday': '화요일',
        'Wednesday': '수요일',
        'Thursday': '목요일',
        'Friday': '금요일',
        'Saturday': '토요일',
        'Sunday': '일요일'
    }
    return time.strftime(f'%Y년 %m월 %d일 %H시 %M분 %S초 ({weekday_dict[time.strftime("%A", time.gmtime(int(unix_time)))]})', time.gmtime(int(unix_time)))

if __name__ == "__main__":
    csv_file_path = './extract.csv'
    output_jsonl_file = './output.jsonl'

    metadata_list = read_metadata_from_csv(csv_file_path)

    all_datasets = []
    for metadata in metadata_list:
        datasets = create_dataset(metadata)
        all_datasets.extend(datasets)

    convert_and_save_to_jsonl(all_datasets, output_jsonl_file)

    print(f"JSONL 파일이 '{output_jsonl_file}'에 저장되었습니다.")
