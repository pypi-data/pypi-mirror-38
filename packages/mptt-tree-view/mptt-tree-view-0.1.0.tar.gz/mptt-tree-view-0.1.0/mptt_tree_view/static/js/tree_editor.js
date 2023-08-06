$.widget( "tree_editor.treeEditor", {
    /*
    <ul class="" pk="{{node.pk}}">
        <li pk="{{ node.pk }}" item-order="{{ node.get_order }}"
            parent="{{ node.parent.pk }}">
                <div class="dd3-handle">"Drag"</div>
                <div class="item-box no-drag">
                    {% block item_box %}
                    {{node}}
                    {% endblock %}
                </div>
        </li>
    </ul>
    */
    options: {
        liHtml: '<li pk="-1" item-order="-1" parent="-1">'+
                    '<div class="dd3-handle handle-box">"Drag"</div>' +
                    '<div class="item-box no-drag">'+
                    '</div>'+
                '</li>',
        title: ""
    },

    getContentElem: function(liElem){
        return $(".item-content", liElem);
    },

    appendChild: function(parentUl, callback){
        var child = $(this.options.liHtml);
        parentUl.append(child);
        if(callback) callback(child);
    },

    insertChildBefore: function(li, callback){
        var child = $(this.options.liHtml);
        li.before(child);
        if(callback) callback(child);
    },

    getLi: function(elemInLi){
        return $(elemInLi.parents("li")[0]);
    },

    _create: function() {
    }
});
