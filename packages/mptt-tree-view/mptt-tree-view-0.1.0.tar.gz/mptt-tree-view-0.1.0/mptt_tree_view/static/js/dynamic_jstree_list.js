$(function () {
    $('.tree-list').jstree({
      "core" : {
        "check_callback" : true,
        'data' : /*{

          'url': dynamicJsTreeUrl,
          'data': function (node) {
            return { 'parent' : "None" };
          },
          'callback': */
          function(obj, callback){
            var parent = rootPk;
            if(obj.id!="#"){
                parent=obj.id;
            }
            console.log(obj);
//            console.log(callback);
            $.get(dynamicJsTreeUrl, {"parent": parent, "limit":9999}, function(data){
                var tree_nodes = [];
                $.each(data.objects, function(key, value){
                    tree_nodes.push({"id":value.id, "text": get_node_text(value),
                    'state' : { 'opened' : false}, "children": true});
                });
                callback.call(this, tree_nodes);
            });
          }
        //}
      },
      "checkbox": {
        //three_state : false, // to avoid that fact that checking a node also check others
        whole_node : false,  // to avoid checking the box just clicking the node
        tie_selection : false // for checking without selecting and selecting without checking
      },
      "plugins" : [
        "checkbox",
        //, "table"
        "dnd"
       ],
    });
    $('.tree-list').on("select_node.jstree", function (e, data) {
//      var url = "{{request.path}}"+"?root="+$("#"+data.selected[0]).attr("pk");
//      window.location.href = url;
    });
//    $('.tree-list').jstree("open_all");
});
