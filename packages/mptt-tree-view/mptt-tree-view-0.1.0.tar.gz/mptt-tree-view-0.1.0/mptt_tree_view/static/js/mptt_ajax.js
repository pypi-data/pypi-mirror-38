$.widget( "mptt.mpttAjax", {
    options: {
        restUrl: "/checklist/rest_api/checklist_tree_item/",
        errorHandling: function (){
            alert("mpttAjax data update error");
        }
    },
    createItemOnServer: function(parentPk, text, itemOrder, callback) {
        $.post(this.options.restUrl, {parent:parentPk, content:text, item_order: itemOrder}, function(result){
            if(callback)callback(result);});
    },

    ajaxReq: function(type, pk, data){
        $.ajax({
          url : this.options.restUrl+pk+"/",
          data : JSON.stringify(data),
          type : type,
          contentType : 'application/json',
          processData: false,
          dataType: 'json',
          error: this.options.errorHandling
        });
    },

    getItemUpdateUrl: function(itemPk){
        return this.options.restUrl+itemPk+"/";
    },

    updateItem: function(itemPk, data, callback){
        $.ajax({
          url : this.getItemUpdateUrl(itemPk),
          data : JSON.stringify(data),
          type : 'PATCH',
          contentType : 'application/json',
          processData: false,
          dataType: 'json',
          error: this.options.errorHandling
        }).done(function(result){if(callback) callback(result);});
    },

    updateParent: function(itemPk, parentPk, callback){
        this.updateItem(itemPk, {"parent": parentPk}, callback);
    },
    setParentAsNull: function(itemPk, callback){
        this.updateParent(itemPk, null, callback);
    },
});
