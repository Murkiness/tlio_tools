
res_text = ''

def update_line(line: str, ancor: str) -> str:
    beginning_part = "\"{% static '"
    ending_part = "' %}\""

    i = 0
    st = 0
    while True:
        print(i)
        try:
            i = line.index(ancor, st)
            slice_start = i + len(ancor)
            close_index = find_close_index(line, i)
            if not 'http' in line[slice_start:close_index]:
                line = line[:slice_start] + beginning_part + line[slice_start:close_index] + ending_part + line[close_index:]

            st = close_index


        except ValueError:
            break

    line = line.replace('/favicon.ico', '\"data:,\"', 1)

    return line


def find_close_index(line, start_pos):
    js_ind = None
    css_ind = None

    try:
        js_ind = line.index('.js', start_pos)
        js_ind += 3
    except:
        pass

    try:
        css_ind = line.index('.css', start_pos)
        css_ind += 4
    except:
        pass

    arr = [js_ind, css_ind]
    arr = [x for x in arr if x is not None]

    return min(arr)




with open('index.html', 'r') as f:
    line = f.readline()

    l = update_line(line, 'href=')
    l = update_line(l, 'src=')

    print(l)


    res_text = '{% load static %}' + l


with open('index.html', 'w') as f:
    f.write(res_text)
