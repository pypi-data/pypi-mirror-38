
guiLocalSettings.setIfNotExists('page_update_interval', 15000)

var gui_base_object = {

    getTemplateName : function (type, default_name)
    {
        var tpl = this.api.bulk_name + '_'+type
        if (!spajs.just.isTplExists(tpl))
        {
            if(default_name)
            {
                return default_name;
            }
            return 'entity_'+type
        }

        return tpl;
    },

    getTitle : function()
    {
        return this.api.name
    },

    stopUpdates : function()
    {
        this.update_stoped = true
        clearTimeout(this.update_timoutid)
    },

    startUpdates : function()
    {
        if(this.update_timoutid)
        {
            return;
        }

        if(this.update_stoped === true)
        {
            return;
        }

        this.update_timoutid = setTimeout(() =>
        {
            this.update_timoutid = undefined
            if(!this.model.filters)
            {
                console.warn("startUpdates [no filters]")
                this.startUpdates()
                return;
            }

            $.when(this.updateFromServer()).always(() => {
                console.log("startUpdates [updated]")
                this.startUpdates()
            })
        }, guiLocalSettings.get('page_update_interval'))
    },

    updateFromServer : function ()
    {
        return false;
    },

    /*
     * Function inits field in model.
     */
    initField: function(field)
    {
        if(!this.model.guiFields[field.name])
        {
            if (!this.model.guiFields[field.name])
            {
                let type = getFieldType(field, this.model)

                var field_value = undefined
                if (this.model.data) {
                    field_value = this.model.data[field.name]
                }
                this.model.guiFields[field.name] = new window.guiElements[type](field, field_value, this)
            }
        }
    },

    renderAllFields : function(opt)
    {
        let html = []
        for(let i in opt.fields)
        {
            html.push(this.renderField(opt.fields[i], opt))
        }

        let id =  getNewId();
        return JUST.onInsert('<div class="fields-block" id="'+id+'" >'+html.join("")+'</div>', () => {

            let fields = $('#'+id+" .gui-not-required")
            if(!this.api.hide_non_required || this.api.hide_non_required >= fields.length)
            {
                return;
            }

            //fields.hide()
            fields.addClass("hide")
            $('#'+id).appendTpl(spajs.just.render('show_not_required_fields', {fields:fields, opt:opt}))
        })
    },

    /**
     * Draw a field when drawing an object.
     * @param {object} field
     * @returns {html}
     * @todo Наверно можно перенести эту функцию guiElements.js
     */
    renderField : function(field, render_options)
    {
        // Add link to dependent fields
        let parent_field_name = undefined
        if(field.additionalProperties && field.additionalProperties.field)
        {
            parent_field_name = field.additionalProperties.field
        }
        if(field.parent_field)
        {
            parent_field_name = field.parent_field
        }
        if (!Array.isArray(parent_field_name))
        {
            parent_field_name = [parent_field_name]
        }
        let thisField = this.model.guiFields[field.name];

        for (let i in parent_field_name)
        {
            let parentField = this.model.guiFields[parent_field_name[i]];

            if(parentField && parentField.addOnChangeCallBack)
            {
                parentField.addOnChangeCallBack(function() {
                    thisField.updateOptions.apply(thisField, arguments);
                })
            }
        }

        return this.model.guiFields[field.name].render($.extend({}, render_options))
    },

    /**
     * Gets the values of all fields from this.model.guiFields
     * @returns {basePageView.getValue.obj}
     */
    getValue : function (hideReadOnly)
    {
        var obj = {}
        let count = 0;
        for(let i in this.model.guiFields)
        {
            if(this.model.guiFields[i].opt.readOnly && hideReadOnly)
            {
                continue;
            }

            let val = this.model.guiFields[i].getValidValue(hideReadOnly);
            if(val !== undefined && val !== null && !(typeof val == "number" && isNaN(val)) )
            {
                obj[i] = val;
            }

            count++;
        }

        if(count == 1 && this.model.guiFields[0] )
        {
            obj = obj[0]
        }

        return obj;
    },

    /**
     * It returns only the correct value, if it is not correct then it should throw an exception
     */
    getValidValue : function (hideReadOnly)
    {
        if(hideReadOnly)
        {
            return undefined
        }
        return this.getValue.call(arguments);
    },

    base_init : function (api_object,  url_vars= {}, object_data = undefined)
    {
        this.url_vars = $.extend(true, {}, spajs.urlInfo.data.reg, url_vars)
        this.model.title = this.api.bulk_name
    },
    init : function ()
    {
        this.base_init.apply(this, arguments)
    },

    apiQuery : function ()
    {
        return api.query.apply(api, arguments)
    },

    getDataFromForm : function (method)
    {
        let data = this.getValue(true)
        if (this['onBefore'+method])
        {
            data = this['onBefore'+method].apply(this, [data]);
        }

        return data
    },

    sendToApi : function (method, callback, error_callback, data)
    {
        var def = new $.Deferred();

        try{
            if(!data)
            {
                data = this.getDataFromForm(method)
            }

            if (data == undefined || data == false)
            {
                def.reject()
                if(error_callback)
                {
                    if(error_callback(data) === false)
                    {
                        return;
                    }
                }

                return def.promise();
            }

            if (data == true)
            {
                if(callback)
                {
                    if(callback(data) === false)
                    {
                        return;
                    }
                }

                def.resolve()
                return def.promise();
            }


            if(!this.api.schema[this.api.method[method]] || !this.api.schema[this.api.method[method]].operationId)
            {
                debugger;
                throw "!this.schema[this.api.method[method]].operationId"
            }

            let operationId = this.api.schema[this.api.method[method]].operationId.replace(/(set)_([A-z0-9]+)/g, "$1-$2")

            var operations = []
            operations = operationId.split("_");
            for(let i in operations)
            {
                operations[i] = operations[i].replace("-", "_")
            }

            var query = []
            var url = this.api.path
            if(this.url_vars)
            {
                for(let i in this.url_vars)
                {
                    if(/^api_/.test(i))
                    {
                        url = url.replace("{"+i.replace("api_", "")+"}", this.url_vars[i])
                    }
                }

                // Modification to that if we have a multi-operation
                for(let i in this.url_vars)
                {
                    if(/^api_/.test(i))
                    {
                        if(typeof this.url_vars[i] != "string")
                        {
                            this.url_vars[i] = this.url_vars[i]+""
                        }

                        if(this.url_vars[i].indexOf(",") != -1)
                        {
                            let ids = this.url_vars[i].split(",")
                            for(let j in ids)
                            {
                                query.push(url.replace(this.url_vars[i], ids[j]))
                            }

                            continue;
                        }
                    }
                }
            }

            if(query.length == 0)
            {
                // Modification to that if we have not a multi-operation
                query = [url]
            }

            query.forEach(qurl => {

                qurl = qurl.replace(/^\/|\/$/g, "").split(/\//g)
                let q = {
                    //type:'mod',
                    data_type:qurl,
                    data:data,
                    method:method
                }

                $.when(this.apiQuery(q)).done(data =>
                {
                    if(callback)
                    {
                        if(callback(data) === false)
                        {
                            return;
                        }
                    }

                    if(data.not_found > 0)
                    {
                        guiPopUp.error("Item not found");
                        def.reject({text:"Item not found", status:404})
                        return;
                    }

                    def.resolve(data)
                }).fail(e => {
                    if(callback)
                    {
                        if(error_callback(e) === false)
                        {
                            return;
                        }
                    }

                    this.showErrors(e, q.method)
                    def.reject(e)
                })
            })

        }catch (e) {
            webGui.showErrors(e)

            def.reject()
            if(e.error != 'validation')
            {
                throw e
            }
        }

        return def.promise();
    },

    showErrors : function(error, method){

        tabSignal.emit('guiItemFactory.showErrors', {thisObj: this, api_response: error, query_method: method})

        if (!error)
        {
            return
        }

        debugger;
        if(!error.status || error.status < 400)
        {
            return webGui.showErrors(error)
        }

        let text = ""
        if(error.data.detail)
        {
            text = error.data.detail +". "
        }



        if(this.api.schema[this.api.method[method]]
            && this.api.schema[this.api.method[method]].responses
            && this.api.schema[this.api.method[method]].responses[error.status]
            && this.api.schema[this.api.method[method]].responses[error.status].description)
        {
            text += this.api.schema[this.api.method[method]].responses[error.status].description
        }
        else if(this.api.schema[method]
            && this.api.schema[method].responses
            && this.api.schema[method].responses[error.status]
            && this.api.schema[method].responses[error.status].description)
        {
            text += this.api.schema[method].responses[error.status].description
        }

        return guiPopUp.error(text)
    }
}

/**
 * Based on the description of the api path, forms the page object.
 * @param {type} api_object
 * @returns {guiObjectFactory.res}
 */
function guiObjectFactory(api_object)
{
    if(typeof api_object == "string")
    {
        api_object = window.guiSchema.path[api_object]
    }

    if (api_object == undefined)
    {
        console.error('Path \`{path}\` doesn\'t exist'.format({path: api_object}))
    }

    /**
     * Used in page template
     */
    this.model = {
        selectedItems : {},
        guiFields:{}
    }

    let arr = [this, window.gui_base_object]
    if(window["gui_"+api_object.type+"_object"])
    {
        arr.push(window["gui_"+api_object.type+"_object"])
    }

    if(api_object.extension_class_name)
    {
        for(let i in api_object.extension_class_name)
        {
            if(api_object.extension_class_name[i] && window[api_object.extension_class_name[i]])
            {
                arr.push(window[api_object.extension_class_name[i]])
            }
        }
    }

    arr.push({api:api_object})

    $.extend.apply($, arr)
    this.init.apply(this, arguments)

}

































function emptyAction(action_info, guiObj, dataLine = undefined)
{
    let url_vars = $.extend(true, {}, guiObj.url_vars)
    if(dataLine)
    {
        let keys = action_info.path.match(/{([^\}]+)}/g)
        for(let i in keys)
        {
            let key = keys[i].slice(1, keys[i].length - 1)
            if(url_vars['api_'+key] === undefined)
            {
                url_vars['api_'+key] = dataLine.url_key
            }
        }
    }

    var pageItem = new guiObjectFactory(action_info, url_vars)
    return function(){
        return pageItem.exec()
    }
}

/**
 * Goes to the search results page.
 * Url builds on the basis of which page is open.
 *
 * @param {string} query
 * @returns {$.Deferred}
 */
function goToSearch(obj, query)
{
    if (obj.isEmptySearchQuery(query))
    {
        return vstGO(spajs.urlInfo.data.reg.page);
    }

    return vstGO(spajs.urlInfo.data.reg.searchURL(obj.searchObjectToString(trim(query))));
}

function deleteAndGoUp(obj)
{
    var def = obj.delete();
    $.when(def).done(function(){
        var upper_url = spajs.urlInfo.data.reg.baseURL().replace(/\/\d+$/g, '');
        vstGO(upper_url);
    })

    return def;
}

function goToMultiAction(ids, action, selection_tag)
{
    if(action && action.isEmptyAction)
    {
        let pageItem = new guiObjectFactory(action, {api_pk: ids.join(",")});
        pageItem.exec();

        window.guiListSelections.unSelectAll(selection_tag);
        return false;
    }

    return vstGO([spajs.urlInfo.data.reg.page_and_parents, ids.join(","), action.name]);
}

function goToMultiActionFromElements(elements, action, selection_tag)
{
    let ids = window.guiListSelections.getSelectionFromCurrentPage(elements);

    return goToMultiAction(ids, action, selection_tag)
}

function addToParentsAndGoUp(item_ids, selection_tag)
{
    return $.when(changeSubItemsInParent('POST', item_ids)).done(function (data)
    {
        window.guiListSelections.setSelection(selection_tag, item_ids, false);
        vstGO(spajs.urlInfo.data.reg.baseURL());
    }).fail(function (e)
    {
        webGui.showErrors(e)
    }).promise();
}

/**
 * To add and remove items in the list
 * @param {array} item_ids
 * @returns {promise}
 */
function changeSubItemsInParent(action, item_ids)
{
    var def = new $.Deferred();
    if(!item_ids || item_ids.length == 0)
    {
        def.resolve()
        return def.promise();
    }

    let parent_id = spajs.urlInfo.data.reg.parent_id
    let parent_type = spajs.urlInfo.data.reg.parent_type
    let item_type = spajs.urlInfo.data.reg.page_type

    if(!parent_id)
    {
        console.error("Error parent_id not found")
        debugger;
        def.resolve()
        return def.promise();
    }

    let query = []
    for(let i in item_ids) {

        if (action == "DELETE") {
            let data_type = [parent_type, parent_id / 1, item_type, item_ids[i] / 1];
            query.push({
                type: "mod",
                data_type: data_type,
                method: action,
            })
        }
        else {
            let data = {
                id: item_ids[i] / 1,
            };
            query.push({
                type: "mod",
                data_type: item_type,
                item: parent_type,
                data: data,
                pk: parent_id,
                method: action,
            })
        }
    }

    return api.query(query)
}


function getUrlBasePath()
{
    return window.location.hash.replace(/^#/, "").replace(/\/+$/, "")
}

function renderErrorAsPage(error)
{
    return spajs.just.render('error_as_page', {error:error, opt: {}});
}

function isEmptyObject(obj)
{
    if(!obj)
    {
        return true;
    }

    return Object.keys(obj).length == 0
}

function questionForAllSelectedOrNot(selection_tag, path){
    var answer;
    var action = guiSchema.path[path];
    if(action)
    {
        var question = "Apply action <b>'"+ action.name + "'</b> for elements only from this page or for all selected elements?";
        var answer_buttons = ["For this page's selected", "For all selected"];
        $.when(guiPopUp.question(question, answer_buttons)).done(function(data){
            answer = data;
            if($.inArray(answer, answer_buttons) != -1)
            {
                if(answer == answer_buttons[0])
                {
                    goToMultiActionFromElements($('.multiple-select .item-row.selected'), action, selection_tag);
                }
                else
                {
                    goToMultiAction(window.guiListSelections.getSelection(selection_tag), action, selection_tag);
                }
            }
        });
    }

    return false;
}

function questionDeleteAllSelectedOrNot(thisObj) {
    var answer;
    var question = "Apply action <b> 'delete' </b> for elements only from this page or for all selected elements?";
    var answer_buttons = ["For this page's selected", "For all selected"];

    $.when(guiPopUp.question(question, answer_buttons)).done(function(data){
        answer = data;
        if($.inArray(answer, answer_buttons) != -1)
        {
            let ids;
            let tag = thisObj.api.selectionTag;
            if(answer == answer_buttons[0])
            {
                ids = window.guiListSelections.getSelectionFromCurrentPage($('.multiple-select .item-row.selected'));
                deleteSelectedElements(thisObj, ids, tag);
            }
            else
            {
                ids = window.guiListSelections.getSelection(tag);
                deleteSelectedElements(thisObj, ids, tag);
            }
        }
    });

    return false;
}

function questionDeleteOrRemove(thisObj)
{
    var answer;
    var question = "<b> Delete </b> selected elements at all or just <b> remove </b> them from this list?";
    var answer_buttons = ["Delete this page's selected", "Delete all selected", "Remove this page's selected", "Remove all selected"];

    $.when(guiPopUp.question(question, answer_buttons)).done(function(data){
        answer = data;
        if($.inArray(answer, answer_buttons) != -1)
        {
            let ids;
            let tag = thisObj.api.selectionTag;
            switch(answer)
            {
                case answer_buttons[0]:
                    ids = window.guiListSelections.getSelectionFromCurrentPage($('.multiple-select .item-row.selected'));
                    deleteSelectedElements(thisObj, ids, tag);
                    break;
                case answer_buttons[1]:
                    ids = window.guiListSelections.getSelection(tag);
                    deleteSelectedElements(thisObj, ids, tag);
                    break;
                case answer_buttons[2]:
                    ids = window.guiListSelections.getSelectionFromCurrentPage($('.multiple-select .item-row.selected'));
                    removeSelectedElements(ids, tag);
                    break;
                case answer_buttons[3]:
                    ids = window.guiListSelections.getSelection(tag);
                    removeSelectedElements(ids, tag);
                    break;
            }
        }
    });

    return false;
}

/**
 * The function deletes elements whose id are listed in the ids array
 * (can be either all selected items or just items from the current page).
 */
function deleteSelectedElements(thisObj, ids, tag)
{
    $.when(thisObj.deleteArray(ids)).done(function(d)
    {
        window.guiListSelections.unSelectAll(tag);

        for(let i in ids)
        {
            $(".item-row.item-"+ids[i]).remove()
        }
    })

    return false;
}


/**
 * The function removes from the list (but does not delete at all) the elements whose id are listed in the ids array
 * (can be either all selected items or just items from the current page).
 */
function removeSelectedElements(ids, tag)
{
    $.when(changeSubItemsInParent('DELETE', ids)).done(function()
    {
        window.guiListSelections.unSelectAll(tag);
        for(let i in ids)
        {
            $(".item-row.item-"+ids[i]).remove();
        }
        guiPopUp.success("Selected elements were successfully removed from parent's list.");

    }).fail(function (e)
    {
        webGui.showErrors(e)
        debugger;
    })

    return false;
}