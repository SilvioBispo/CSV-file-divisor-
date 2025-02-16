from flask import Flask, request
import csv
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS

UPLOAD_FOLDER = 'csv'
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
file_name = list()


@app.get('/')
def get_registered():
    file_name.clear()
    with open("csv/list_file.csv", mode='r') as read_file:
        fileread_csv = csv.reader(read_file)
        for line in fileread_csv:
            file_name.append(line)
    return file_name


@app.post('/')
def post_registered():
    file_request = request.files['file']
    file_request.save(file_request.filename)
    with open("file_name.csv",newline='', mode='w') as append_csv:
        file_append = csv.writer(append_csv)
        file_append.writerow([file_request.filename])
    append_csv.close()
    return file_request.filename


@app.put('/')
def put_registered():
    new_file = request.files['file']
    with open("csv/list_file.csv", mode='r') as read_file:
        list_read = csv.reader(read_file)
        for line in list_read:
            if line == new_file.filename:
                file_name.append(new_file.filename)
            file_name.append(line)
    read_file.close()
    file = "csv/" + new_file.filename
    os.remove(file)
    new_file.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(new_file.filename)))
    with open("csv/list_file.csv", newline='', mode='w') as write_file:
        list_write = csv.writer(write_file)
        for line in file_name:
            list_write.writerow(line)
    write_file.close()
    return new_file.filename


@app.delete('/')
def delete_registered():
    file_name.clear()
    delete_file = {"file": request.json['file']}

    with open('csv/list_file.csv', mode='r') as read_file:
        list_read = csv.reader(read_file)
        for line in list_read:
            file_name.append(line)
    read_file.close()
    file = delete_file['file']
    if [file] in file_name:
        file_name.remove([file])
        file = "csv/" + file
        os.remove(file)
    with open('csv/list_file.csv', newline='', mode='w') as write_file:
        list_write = csv.writer(write_file)
        for line in file_name:
            list_write.writerow(line)
    write_file.close()
    return delete_file


@app.delete('/delete_all')
def delete_all():
    with open("csv/list_file.csv", mode='r') as read_file:
        list_read = csv.reader(read_file)
        for line in list_read:
            file = str(line)
            file = file.removeprefix("['")
            file = file.removesuffix("']")
            file = "csv/" + file
            os.remove(file)
    read_file.close()
    file_name.clear()
    with open("csv/list_file.csv",mode='w') as write_file:
        list_write = csv.writer(write_file)
        list_write.writerows(file_name)
    write_file.close()
    return "delete all"


@app.get('/tables')
def create_tables():
    file_name.clear()
    new_tables = {}
    with open('file_name.csv', mode='r') as read_csv:
        read_file = csv.reader(read_csv)
        for line in read_file:
            file = line
    read_csv.close()
    file = str(file[0])
    with open(file, mode='r') as read_csv:
        read_file = csv.DictReader(read_csv)
        filed_name = read_file.fieldnames
        for line in read_file:
            id = line['nome']
            if id not in new_tables:
                new_tables[id] = []
            new_tables[id].append(line)
    read_csv.close()
    for line in new_tables:
        line_name = str(line) + ".csv"
        i = str(line)
        file_name.append(line_name)
        line_path = "csv/" + str(line_name)
        with open(line_path, mode='w') as write_csv:
            file_write = csv.writer(write_csv)
            file_write.writerow(filed_name)
            for lines in new_tables[i]:
                row = dict(lines)
                file_write.writerow(row.values())
        write_csv.close()
    with open('csv/list_file.csv',newline='', mode='w') as write_csv:
        list_write = csv.writer(write_csv)
        for line in file_name:
            list_write.writerow([line])
    write_csv.close()
    return file_name


app.run()
