from django.shortcuts import render, get_object_or_404, redirect
from .models import Bango, Shiire, Label
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
import csv
from django.http import HttpResponse

 
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
                Q(shiire__sname__icontains=snq_word)) 
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
            writer.writerow([data.sebango.hcode, data.sebango.se, '*'+data.sebango.se+'*', data.sebango.shiire.scode, data.sebango.shiire.sname])
    return response
