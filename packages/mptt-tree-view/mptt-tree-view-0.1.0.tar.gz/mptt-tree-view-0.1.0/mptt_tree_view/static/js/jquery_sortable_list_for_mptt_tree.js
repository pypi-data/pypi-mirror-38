$.widget( "mptt_tree_view.mpttTreeView", {

    options: {
        restUrl: "/checklist/checklist_list/",
    },

    _create: function() {
        var sortableListsOption = {
            complete: function(currEl){
                console.log(currEl);
                var parentPk = null;
                var curLi = currEl;//parseInt($(currEl.parents("li")[0])

                //if("") is a false condition.
                if($(curLi.parents("ul")[0]).attr("pk")==""||$(curLi.parents("ul")[0]).attr("pk")){
                    parentPk = $(curLi.parents("ul")[0]).attr("pk");
                }
                else{
                    parentPk = $(curLi.parents("li")[0]).attr("pk");
                }

                if(parentPk!=curLi.attr("parent")){
                    $(".tree-root-ul", this.element).mpttAjax('updateParent', currEl.attr("pk"), parentPk,
                    function(){
                        currEl.attr("parent", parentPk);
                    });
                }
            },
            // All elements with class clickable will be clickable
            ignoreClass: 'no-drag',
            placeholderClass: 'placeholderClass',
            // or like a jQuery css object
            placeholderCss: {'background-color':'yellow'},
            hintClass: 'hintClass',
            // or like a jQuery css object
            hintCss: {'background-color':'green', 'border':'1px dashed white'}
        }
        this.element.sortableLists( sortableListsOption );
        $(".tree-root-ul", this.element).mpttAjax( {restUrl: this.options.restUrl} );
    }
});
