from django.shortcuts import redirect
from django.shortcuts import render
from block.models import Block
from article.models import Article
from article.forms import ArticleForm
from django.views.generic import View,DetailView
from django.core.paginator import Paginator



def article_list(request,block_id):
    block_id = int(block_id)
    block = Block.objects.get(id=block_id)
    all_articles = Article.objects.filter(block=block,status=0).order_by("-id")
    ARTICLE_CNT_1PAGE = 1
    page_no = int(request.GET.get("page_no","1"))
    p = Paginator(all_articles,ARTICLE_CNT_1PAGE)
    page = p.page(page_no)
    articles_objs = page.object_list
    if page_no > p.num_pages:
        page_no = p.num_pages
    if page_no <= 0:
        page_no = 1
    page_cnt = p.num_pages
    page_links = [i for i in range(page_no - 3,page_no + 4)
                  if i > 0 and i <= p.num_pages]
    previous_link = page_links[0]-1
    next_link = page_links[-1]+1
    has_previous = previous_link > 0
    has_next = next_link <= page_cnt
    return render(request,"article_list.html",{"articles":articles_objs,"b":block,"page_cnt":page_cnt,
                                               "current_no":page_no,"page_links":page_links,
                                               "previous_link":previous_link,"next_link":next_link,
                                               "previous":has_previous,"next":has_next,"current":page_no})



class ArticleCreateView(View):

    template_name = "article_create.html"

    def init_data(self,block_id):
        self.block_id = block_id
        self.block = Block.objects.get(id=block_id)

    def get(self,request,block_id):
        self.init_data(block_id)
        return render(request,self.template_name,{"b":self.block})

    def post(self,request,block_id):
        self.init_data(block_id)
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.block = self.block
            article.status = 0
            article.save()
            return redirect("/article/list/%s" % self.block_id)
        else:
            return render(request,self.template_name,{"b":self.block,"form":form})


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = "a"

