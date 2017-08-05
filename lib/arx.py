import arxiv_lib as arxiv
import subprocess

chunk = 100
DEFSEARCH = "DEF_CATEGORY="

def count_results(q, st, suf):
    c = 0
    x = 1
    while (x != 0):
        x = len(arxiv.query(search_query = q + " " + suf, start = c + st, max_results = chunk))
        c = c + x
    return c

def parse_id(link):
    if '.' in link.split('/')[-1]:
        return link.split('/')[-1]
    else:
        return link.split('/')[-2] + '/' + link.split('/')[-1]

def collect_all(q, st, suf):
    x = arxiv.query(search_query = q + " " + suf, start = st, max_results = chunk)
    c = x
    while (len(x) != 0):
        x = arxiv.query(search_query = q + " " + suf, start = st + len(c), max_results = chunk)
        c = c + x
    return sorted(c, key = lambda x: x.published)

def write_new_log(ls, log):
    log_file = open(log, "w")
    fls = set(ls[0]).union(set(ls[1]))
    for s in fls:
        log_file.write(s)
        log_file.write("\n")
    return 0

def get_new_log(user_ls):
    backup_name = "."+user_ls+".old"
    try:
        user_ls_file = open(user_ls, "r")
    except:
        print "Please create your personal list file."
        return 0
    try:
        user_old_file = open(backup_name, "r")
    except:
        command = "touch " + backup_name 
        subprocess.call([command], shell=True)
        user_old_file = open(backup_name, "r")

    current_list = user_ls_file.readlines()
    current_list = [x.strip() for x in current_list if x[0] != '#']
    old_list = user_old_file.readlines()
    old_list = [x.strip() for x in old_list if x[0] != '#']
    user_old_file.close()
    user_ls_file.close()
    command = "cp " + user_ls + " " + backup_name 
    subprocess.call([command], shell=True)


    suff = ""
    log = [[],[]]

    for st in current_list:
        if st.strip().startswith(DEFSEARCH):
            suff = "AND (" + st[len(DEFSEARCH):].strip() + ")"
        else:
            results = collect_all(st.strip(), 0, suff)
            results = [parse_id(x.id) for x in results]
            for x in results:
                if st.strip() in old_list:
                    log[0].append(x)
                else:
                    log[1].append(x)
    return [set(log[0]),set(log[1])]


def check_for_new(log, user_ls, output):
    try: 
        log_file = open(log, "r")
    except:
        ls = get_new_log(user_ls)
        write_new_log(ls, log)
        return 0

    ids_old = log_file.readlines()
    ids_old = [x.strip() for x in ids_old]
    log_file.close()
    ids_new = get_new_log(user_ls)
    diff = [x.strip() for x in ids_new[0] if not(x in ids_old)]
    plist = set(arxiv.query(id_list = diff))
    plist = [x for x in plist if not(parse_id(x.id) in ids_old)]
    new_file = open(output, "a")
    for p in plist:
        new_file.write((', '.join(p.authors) + "\n" + p.title + "\n\n" +p.arxiv_comment + "\n\n" + p.summary + "\n" + p.pdf_url + "\n$\n").encode("utf-8"))
    new_file.close()
    write_new_log(ids_new, log)

def is_int(s):
     try:
             int(s)
             return True
     except ValueError:
             return False


