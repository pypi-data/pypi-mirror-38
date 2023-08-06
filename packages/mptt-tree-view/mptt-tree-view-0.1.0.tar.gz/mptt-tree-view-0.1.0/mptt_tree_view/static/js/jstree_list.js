$(function () {
    $('.tree-list').jstree({
      "core" : {
        "check_callback" : true
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
       ]
    });
    $('.tree-list').on("select_node.jstree", function (e, data) {
//      var url = "{{request.path}}"+"?root="+$("#"+data.selected[0]).attr("pk");
//      window.location.href = url;
    });
    $('.tree-list').jstree("open_all");
});
