from django.core.context_processors import csrf
from django.views.generic import TemplateView

from djangoautoconf.django_utils import retrieve_param
from djangoautoconf.model_utils.url_for_models import get_rest_api_url, get_tastypie_api_url


class DynamicJsTreeView(TemplateView):
    item_class = None
    default_level = 2
    template_name = "mptt_tree_view/dynamic_jstree_list.html"
    app_name = "checklist"

    def __init__(self, **kwargs):
        super(DynamicJsTreeView, self).__init__(**kwargs)
        self.tree_items = None
        self.root_pk = "None"

    def get_context_data(self, **kwargs):
        # context = super(AddTagTemplateView, self).get_context_data(**kwargs)
        context = {}
        c = {"user": self.request.user,
             "root_pk": self.root_pk,
             "is_root_node_needed": False,
             "dynamic_js_tree_url": self.get_base_tree_load_url(),
             }
        c.update(csrf(self.request))
        context.update(c)
        # log = logging.getLogger(__name__)
        # log.error(context)
        return context

    def get_base_tree_load_url(self):
        return "%s?format=json" % (
            get_tastypie_api_url(self.item_class))

