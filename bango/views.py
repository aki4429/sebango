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

    def get_queryset(self):
        #コード検索
        cq_word = self.request.GET.get('cquery')
        #背番号検索
        seq_word = self.request.GET.get('sequery')
        #仕入先コード検索
        scq_word = self.request.GET.get('scquery')
        #仕入先名検索
        snq_word = self.request.GET.get('snquery')

        if cq_word or seq_word or scq_word or snq_word:
            bango_list = Bango.objects.filter(
                Q(hcode__icontains=cq_word), 
                Q(se__icontains=seq_word), 
                Q(shiire__scode__icontains=scq_word), 
                Q(shiire__sname__icontains=snq_word)).order_by('se') 
        else:
            #object_list = Bango.objects.all()
            bango_list = ''

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
        data.append([bango.hcode, bango.se, bango.shiire.scode, bango.shiire.sname])

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


