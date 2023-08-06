from django.core.context_processors import csrf
from django.views.generic import TemplateView

from djangoautoconf.django_utils import retrieve_param


class TreeView(TemplateView):
    item_class = None
    default_level = 2
    template_name = "mptt_tree_view/jquery_sortable_list.html"

    def __init__(self, **kwargs):
        super(TreeView, self).__init__(**kwargs)
        self.tree_items = None
        self.root_pk = ""

    def get_context_data(self, **kwargs):
        # context = super(AddTagTemplateView, self).get_context_data(**kwargs)
        context = super(TreeView, self).get_context_data(**kwargs)
        self.init_tree_items()
        self.get_final_query_set()
        c = {"user": self.request.user, "nodes": self.tree_items, "root_pk": self.root_pk,
             "is_root_node_needed": False}
        c.update(csrf(self.request))
        context.update(c)
        # log = logging.getLogger(__name__)
        # log.error(context)
        return context

    def get_final_query_set(self):
        pass

    def init_tree_items(self):
        data = retrieve_param(self.request)
        if "root" in data:
            self.root_pk = data["root"]
            self.tree_items = self.get_children(self.root_pk)
        else:
            self.tree_items = self.item_class.objects.filter(level__lt=self.get_level())

    def get_level(self):
        data = retrieve_param(self.request)
        if "level" in data:
            try:
                return int(data["level"])
            except:
                pass
        return self.default_level

    def get_children(self, root_pk):
        root = self.item_class.objects.filter(pk=root_pk)
        tree_items = self.item_class.objects.get_queryset_descendants(root, include_self=True).filter(
                level__lt=root[0].level + self.get_level() + 1)
        return tree_items


class JsTreeView(TreeView):
    item_class = None
    default_level = 2
    template_name = "mptt_tree_view/jstree_list.html"
