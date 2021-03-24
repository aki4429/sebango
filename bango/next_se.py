#upload list = [規格, 仕入先コード] を受けて、
#そのコード分類の次の背番号を返す。

#その分類の最後の背番号の次を返す
def se_last(sebango, Bango):
    moji = sebango.split('-')[0]
    bunruis = Bango.objects.filter(se__contains=moji).order_by('se')
    suji = bunruis.last().se.split('-')[1]
    next_suji = str(int(suji) + 1).zfill(4)
    next_sebango = moji + "-" + next_suji
    return next_sebango

#次の背番号を作成 
def se_next(sebango):
    moji = sebango.split('-')[0]
    suji = sebango.split('-')[1]
    next_suji = str(int(suji) + 1).zfill(4)
    next_sebango = moji + "-" + next_suji
    return next_sebango

#登録済みか
def already(row, Bango):
    b=Bango.objects.filter(hcode__exact = row[0])
    if len(b) > 0 and b[0].shiire.scode == row[1] :
        return True
    else:
        return False

def set_next_se(up_list, Bango):
    #背番号付きリスト
    new_list = []
    #分類をキーにして最後の背番号を格納する辞書
    last_se = {}
    for up in up_list:
        #strip
        up[0] = up[0].strip()
        up[1] = up[1].strip()

        #登録済みの場合スキップ
        if not already(up, Bango):
            #コードの最初３文字を分類文字列として格納
            bunrui =  up[0][:3]
            #最初３文字が数字なら資材/分類数字毎に背番号管理
            if bunrui.isdigit():
            #分類キーが辞書になければ、Bnagoから最後の背番号取得して作成
                if bunrui not in last_se:
                    last_se[bunrui] = Bango.objects.filter(hcode__startswith = bunrui).order_by('se').last().se
                    next_se = se_next(last_se[bunrui])
                    new_list.append([up[0], next_se, up[1]])
                    last_se[bunrui] = next_se
                else:
                    next_se = se_next(last_se[bunrui])
                    new_list.append([up[0], next_se, up[1]])
                    last_se[bunrui] = next_se

            #最初３文字が数字以外はすべてT-背番号=T分類
            else:
                bunrui = "T"
                if bunrui not in last_se:
                    last_se[bunrui] = Bango.objects.filter(se__startswith = bunrui).order_by('se').last().se
                    next_se = se_next(last_se[bunrui])
                    new_list.append([up[0], next_se, up[1]])
                    last_se[bunrui] = next_se
                else:
                    next_se = se_next(last_se[bunrui])
                    new_list.append([up[0], next_se, up[1]])
                    last_se[bunrui] = next_se

    return new_list










