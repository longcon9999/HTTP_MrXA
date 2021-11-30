from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)


def time_vector(p, c, m):
    result = {}
    connection = {}
    try:
        for i in range(len(p)):
            result[i + 1] = [[int(tmp.strip()) for tmp in p[i].split(",")]]
        print(result)
        for i in c:
            tmp = i.split("-")
            connection[",".join([x.strip() for x in tmp[1].split(",")])] = ",".join(
                [x.strip() for x in tmp[0].split(",")])
        print(connection)
        for i in range(1, m + 1):
            for j in range(1, len(p) + 1):
                tmp = result.get(j)
                if tmp is None:
                    tmp = [[0, 0, 0]]
                pre_tmp = tmp[i - 1]
                after_tmp = []
                for _i in range(len(pre_tmp)):
                    if _i == j - 1:
                        after_tmp.append(pre_tmp[_i] + 1)
                    else:
                        after_tmp.append(pre_tmp[_i])
                if connection.get(f"{j},{i}") is not None:
                    compare_item = str(connection.get(f"{j},{i}"))
                    compare_vector = result.get(int(compare_item.split(",")[0]))[int(compare_item.split(",")[1])]
                    for _i in range(len(after_tmp)):
                        if after_tmp[_i] < compare_vector[_i]:
                            after_tmp[_i] = compare_vector[_i]
                tmp.append(after_tmp)
                result[j] = tmp
        return result, True
    except Exception as e:
        return e, False


def phys_time_sys(client_send, server_received, server_send, client_received):
    try:
        client_send_time = datetime.strptime(client_send, "%Y-%m-%d %H:%M:%S.%f")
        server_received_time = datetime.strptime(server_received, "%Y-%m-%d %H:%M:%S.%f")
        server_send_time = datetime.strptime(server_send, "%Y-%m-%d %H:%M:%S.%f")
        client_received_time = datetime.strptime(client_received, "%Y-%m-%d %H:%M:%S.%f")
        result = ((server_received_time - client_send_time) + (server_send_time - client_received_time)) / 2
        return str(client_received_time + result)[:-3], True
    except Exception as e:
        return f"{e}", False


def berkeley_gt(server, client_1, client_2):
    try:
        server_time = datetime.strptime(server, "%Y-%m-%d %H:%M:%S.%f")
        client_1_time = datetime.strptime(client_1, "%Y-%m-%d %H:%M:%S.%f")
        client_2_time = datetime.strptime(client_2, "%Y-%m-%d %H:%M:%S.%f")
        offset = ((client_1_time - server_time) + (client_2_time - server_time)) / 3
        client_1_offset = offset - (client_1_time - server_time)
        client_2_offset = offset - (client_2_time - server_time)
        server_update = str(server_time + offset)
        client_1_update = str(client_1_time + client_1_offset)
        client_2_update = str(client_2_time + client_2_offset)
        if server_update == client_2_update and client_2_update == client_1_update:
            ms = str(round(float(server_update[server_update.rfind(":") + 1:]), 3))
            ms = ms[ms.rfind("."):]
            if len(ms) == 3:
                ms += "0"
            elif len(ms) == 2:
                ms += "00"
            elif len(ms) == 1:
                ms += "000"
            server_update = f"{server_update[:server_update.rfind('.')]}{ms}"
            return int(round(offset.total_seconds() * 1000, 0)), \
                   int(round(client_1_offset.total_seconds() * 1000, 0)), \
                   int(round(client_2_offset.total_seconds() * 1000, 0)), server_update, True
        else:
            return "Lỗi tính toán", None, None, None, False
    except Exception as e:
        return e, None, None, None, False


def lamport_time(process, message):
    try:
        result = {}
        connection = {}
        steps = {}
        for i in range(len(process)):
            tmp = process[i].split(",")
            step = int(tmp[1].strip())
            num_events = int(tmp[2].strip())
            items = [int(tmp[0].strip())]
            for j in range(1, num_events):
                items.append(items[j-1]+step)
            result[i] = items
            steps[i] = step
        print(result)
        print(steps)
        for i in message:
            tmp = i.split("-")
            connection[",".join([x.strip() for x in tmp[1].split(",")])] = ",".join(
                [x.strip() for x in tmp[0].split(",")])
        print(connection)
        while True:
            f = True
            for key in connection.keys():
                tmp = [x.strip() for x in connection.get(key).split(",")]
                compare_tmp = [x.strip() for x in key.split(",")]
                val = result.get(int(tmp[0]) - 1)[int(tmp[1])] + 1
                compare_val = result.get(int(compare_tmp[0]) - 1)[int(compare_tmp[1])]
                if val > compare_val:
                    f = False
                    list_value = result.get(int(compare_tmp[0]) - 1)
                    list_value[int(compare_tmp[1])] = val
                    for j in range(int(compare_tmp[1]) + 1, len(list_value)):
                        list_value[j] = list_value[j-1] + steps.get(int(compare_tmp[0]) - 1)
                    result[(int(compare_tmp[0]) - 1)] = list_value
            if f:
                break
        print(result)
        return result, True
    except Exception as e:
        return f"{e}", False


def voted_wireless_net(voted_values, conn, message):
    try:
        dict_result = {}
        input = voted_values.split(";")
        conn = conn.split(";")
        mes = message.split(";")
        list_index = {}
        cost_index = {}
        _max = None
        for i in range(1, len(input) + 1):
            cost_index[i] = int(input[i - 1])
            if _max is not None:
                if cost_index.get(_max) < cost_index.get(i):
                    _max = i
            else:
                _max = i
        result = f"P{_max},{cost_index.get(_max)}"
        while True:
            f = True
            for i in range(1, len(conn) + 1):
                tmp = list_index.get(i)
                if tmp is None:
                    f = False
                    tmp = [i]
                    if conn[i - 1] != "_":
                        tmp = [i]
                        tmp.extend((int(x.strip()) for x in conn[i - 1].split(",")))
                    list_index[i] = tmp
                else:
                    new_tmp = []
                    for j in tmp:
                        new_tmp.extend(list_index.get(j))
                    new_tmp = list(sorted(set(new_tmp)))
                    if len(new_tmp) != len(tmp):
                        f = False
                    list_index[i] = new_tmp
            if f:
                break
        print(list_index)
        for m in mes:
            tmp = m.split("-")
            src = int(tmp[0].strip())
            des = int(tmp[1].strip())
            tmp = list_index.get(src)
            _max = None
            for i in tmp:
                if _max is not None:
                    if cost_index.get(_max) < cost_index.get(i):
                        _max = i
                else:
                    _max = i
            if list_index.get(des) < list_index.get(_max):
                dict_result[f"P{src} gửi P{des}"] = f"P{_max},{cost_index.get(_max)}"
            else:
                dict_result[f"P{src} gửi P{des}"] = f"P{des},{cost_index.get(des)}"
        return dict_result, result, True
    except Exception as e:
        return f"{e}", None, False


@app.route('/', methods=["GET"])
def index():
    return render_template("homepage.html")


@app.route('/vector_time', methods=["POST", "GET"])
def vector_time():
    if request.method == "POST":
        try:
            num_process = int(request.form.get("num_process"))
            num_message = int(request.form.get("num_message"))
            num_event = int(request.form.get("num_events"))
            p = []
            m = []
            for i in range(num_process):
                p.append(request.form.get(f"process{i}"))
            for i in range(num_message):
                m.append(request.form.get(f"mess{i}"))
            result, ok = time_vector(p, m, num_event)
            if ok:
                return render_template("result_page.html", result=result)
            else:
                return render_template("vector_time.html", Error=result)
        except Exception as e:
            print(e)
            return render_template("vector_time.html", Error=e)
    return render_template("vector_time.html")


@app.route("/sys_physic_time", methods=["POST", "GET"])
def sys_physic_time():
    if request.method == "POST":
        try:
            time_send_client = request.form.get("time_send_client").strip()
            time_received_client = request.form.get("time_received_client").strip()
            time_send_server = request.form.get("time_send_server").strip()
            time_received_server = request.form.get("time_received_server").strip()
            result, ok = phys_time_sys(time_send_client, time_received_server, time_send_server, time_received_client)
            if ok:
                return render_template("sys_physic_time.html", result=result)
            else:
                return render_template("sys_physic_time.html", Error=result)
        except Exception as e:
            print(e)
            return render_template("sys_physic_time.html", Error=e)
    return render_template("sys_physic_time.html")


@app.route("/berkeley", methods=["POST", "GET"])
def berkeley():
    if request.method == "POST":
        try:
            server_time = request.form.get("time_server").strip()
            client_1_time = request.form.get("client_1").strip()
            client_2_time = request.form.get("client_2").strip()
            offset, offset_client_1, offset_client_2, time_update, mes = \
                berkeley_gt(server_time, client_1_time, client_2_time)
            result = [["Điều phối", server_time, offset], ["Thành viên", client_1_time, offset_client_1],
                      ["Thành viên", client_2_time, offset_client_2], time_update]
            if mes:
                return render_template("berkeley.html", result=result)
            else:
                return render_template("berkeley.html", Error=offset)
        except Exception as e:
            print(e)
            return render_template("berkeley.html", Error=e)
    return render_template("berkeley.html")


@app.route("/lamport", methods=["POST", "GET"])
def lamport():
    if request.method == "POST":
        try:
            num_process = int(request.form.get("num_process"))
            num_message = int(request.form.get("num_message"))
            process = []
            message = []
            for i in range(num_process):
                process.append(request.form.get(f"process{i}"))
            for i in range(num_message):
                message.append(request.form.get(f"mess{i}"))
            result, ok = lamport_time(process=process, message=message)
            if ok:
                return render_template("result_page.html", result=result)
            else:
                return render_template("lamport.html", Error=result)
        except Exception as e:
            print(e)
            return render_template("lamport.html", Error=e)
    return render_template("lamport.html")


@app.route("/voted_wireless", methods=["POST", "GET"])
def voted_wireless():
    if request.method == "POST":
        try:
            voted_values = request.form.get("voted_values")
            conn = request.form.get("conn")
            message = request.form.get("message")
            # print(voted_wireless_net(voted_values, conn, message))
            dict_result, result, ok = voted_wireless_net(voted_values, conn, message)
            results = {"data": dict_result, "final": result}
            if ok:
                return render_template("voted_wireless_net.html", results=results)
            else:
                return render_template("voted_wireless_net.html", Error=dict_result)
        except Exception as e:
            return render_template("voted_wireless_net.html", Error=e)
    return render_template("voted_wireless_net.html")


if __name__ == "__main__":
    app.run(debug=True)
