from django.shortcuts import render, get_object_or_404, redirect
from .models import Bango, Shiire, Label
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import HttpResponse
from .forms import UploadFileForm, BangoForm
import os, io, csv
from .next_se import set_next_se, se_last
from .make_space_one import s_one

UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/files/'
 
class BangoList(LoginRequiredMixin, ListView):
    template_name='bango/bango_list.html'
    context_object_name = 'bango_list'
    model = Bango 

    def post(self, request):
        labels = request.POST.getlist('label')  # <input type="checkbox" name="delete"のnameに対応
    #POSTされたorderの配列をセッションに保存
        request.session['labels'] = labels
        label_list =[]
        for label in labels:
            l = Label(sebango = Bango.objects.get(pk=label), qty=0)
            label_list.append(l)

        Label.objects.bulk_create(label_list)

        return redirect('label_list')  # 一覧ページにリダイレクト

    #検索語とフィールド名を指定して、その言葉がフィールドに
    #含まれるクエリーセットを返す関数。
    #検索語はスペースで区切って、リストでANDでつなげる
    def make_q(self,query, q_word, f_word):
        #(2)キーワードをリスト化させる(複数指定の場合に対応させるため)
        search      = self.request.GET[q_word].replace("　"," ")
        search_list = search.split(" ")
        filter = f_word + '__' + 'contains' #name__containsを作る
        #(例)info=members.filter(**{ filter: search_string })
        #(3)クエリを作る
        for word in search_list:
        #TIPS:AND検索の場合は&を、OR検索の場合は|を使用する。
            query &= Q(**{ filter: word })
            #(4)作ったクエリを返す
        return query


    def get_queryset(self):
        query = Q()
        flag = 0 #一つも検索語がなければ、flag==0

        #コード検索
        if 'cquery' in self.request.GET:
            query = self.make_q(query, 'cquery', 'hcode')
            flag += 1

        #背番号検索
        if 'sequery' in self.request.GET:
            query = self.make_q(query, 'sequery', 'se')
            flag += 1

        #仕入先CD名検索
        if 'scquery' in self.request.GET:
            scq_word = self.request.GET.get('scquery')
            query &= Q(shiire__scode__icontains=scq_word)
            flag += 1

        #仕入先名検索
        if 'snquery' in self.request.GET:
            snq_word = self.request.GET.get('snquery')
            query &= Q(shiire__sname__icontains=snq_word)
            flag += 1

        #規格検索
        if 'kquery' in self.request.GET:
            query = self.make_q(query, 'kquery', 'kikaku')
            flag += 1

        #備考検索
        if 'bquery' in self.request.GET:
            query = self.make_q(query, 'bquery', 'biko')
            flag += 1

        if flag == 0:
            bango_list = ""
        else:
            bango_list = Bango.objects.filter(query).order_by('se')

        return bango_list


class LabelList(LoginRequiredMixin, ListView):
    template_name='bango/label_list.html'
    context_object_name = 'label_list'
    model =  Label
    label_list = Label.objects.all()

    #return label_list

@login_required
def label_delete_all(request):
    Label.objects.all().delete()
    return redirect('bango_list')

class LabelUpdate(LoginRequiredMixin, UpdateView):
    template_name='bango/label_update.html'
    context_object_name = 'label_list'
    model =  Label
    label_list = Label.objects.all()
    fields = ['qty']

    def get_success_url(self):
        return reverse('label_list')

@login_required
# データのダウンロード
def make_label(request):
    # レスポンスの設定
    response = HttpResponse(content_type='text/csv; charset=CP932')
    filename = 'labels.csv'  # ダウンロードするcsvファイル名
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    writer = csv.writer(response)
    # データ出力
    label_data = Label.objects.all()  # 対象ラベルデータを取得
    for data in label_data:
        for i in range(int(data.qty)):
            writer.writerow([s_one(data.sebango.hcode), data.sebango.se, '*'+data.sebango.se+'*', data.sebango.shiire.scode, data.sebango.shiire.sname])
    return response

@login_required
def upload(request):
    if request.method == 'POST':
        # POST
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved. by binary
            f = request.FILES['file']
            path = os.path.join(UPLOAD_DIR, f.name)
            with open(path, 'wb') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

            # open csv
            with open(path, 'r', encoding='CP932') as destination:
                # read csv
                reader = csv.reader(destination)
                #listを取得
                upload_list =[]
                for row in reader:
                    upload_list.append(row)

                list_with_se = set_next_se(upload_list, Bango)

                # bulk insert 
                bango_list = []
                for row in list_with_se:
                    l = Bango(hcode = row[0], se = row[1], 
                            shiire=Shiire.objects.filter(scode__iexact=row[2])[0])
                    bango_list.append(l)

                Bango.objects.bulk_create(bango_list)
                os.remove(path)

            return redirect('bango_list')
    else:
        # GET
        form = UploadFileForm()
        return render(request, 'bango/upload.html', {'form':form})

#背番号リストをダウンロード
@login_required
def down_sebango(request):
    response = HttpResponse(content_type='text/csv; charset=Shift-JIS')
    response['Content-Disposition'] = 'attachment; filename="sebango_list.csv"'
    bangos = Bango.objects.order_by('se')
    data = []
    for bango in bangos:
        data.append([bango.se, bango.hcode, bango.kikaku])

    sio = io.StringIO()
    writer = csv.writer(sio)
    writer.writerows(data)
    response.write(sio.getvalue().encode('cp932'))

    return response

class BangoDetail(LoginRequiredMixin, DetailView):
    model = Bango

class BangoUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'bango/bango_update_form.html'
    model = Bango
    form_class = BangoForm
 
    def get_success_url(self):
        return reverse('bango_detail', kwargs={'pk': self.object.pk})

class BangoCopy(LoginRequiredMixin, UpdateView):
    template_name = 'bango/bango_copy.html'
    model = Bango
    form_class = BangoForm

    def get_success_url(self):
        return reverse('bango_detail', kwargs={'pk': self.object.pk})

    #ここでコピーするためにget_objectをオーバーライドします。
    def get_object(self, queryset=None):
        #self.request.GETは使えないので、self.kwargsを使うところがミソ
        bango = Bango.objects.get(pk=self.kwargs.get('pk'))
        #プライマリーキーを最新に。これがしたいためのオーバーライド
        bango.pk = Bango.objects.last().pk + 1
        #背番号をその分類の最後の次の背番号に変更
        bango.se = se_last(bango.se, Bango)
        return bango

class BangoDelete(LoginRequiredMixin, DeleteView):
    template_name = 'bango/bango_delete.html'
    model = Bango

    def get_success_url(self):
        return reverse('bango_list')


