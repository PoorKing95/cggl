def check_comm(authors):
    try:
        order = [author.get('commOrder', '0') for author in authors if author.get('isComm', False)]
        order.sort()

        flag = True
        for i, val in enumerate(order):
            if int(val) != (i + 1):
                flag = False

        return flag
    except Exception as e:
        return False
